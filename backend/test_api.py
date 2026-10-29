import asyncio
import json
import uuid
from datetime import datetime, timezone

import httpx
import pytest
from fastapi.testclient import TestClient

from backend import main as m


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(m, "DB_PATH", tmp_path / "test.sqlite3")
    monkeypatch.setattr(m, "LIVE", False)
    monkeypatch.setattr(m, "REVIEW", True)
    monkeypatch.setattr(m, "RUN_ID", "test")
    m.migrate()
    with TestClient(m.app) as client:
        yield client


def draft():
    return {"revision": 1, "status": "draft", "created_at": datetime.now(timezone.utc).isoformat(), "events": []}


def create(client):
    sid = str(uuid.uuid4()); data = draft()
    assert client.put('/api/sessions/' + sid, json=data).status_code == 200
    return sid, data


def ask(client, sid, question, **kwargs):
    return client.post(f'/api/sessions/{sid}/messages', json={"turn_id": str(uuid.uuid4()), "question": question, "cue": "text", **kwargs})


def started(data):
    data = {**data, "revision": 2, "status": "running", "cue_initial": "text", "cue_final": "text", "first_instruction_at": datetime.now(timezone.utc).isoformat(), "events": [{"id":str(uuid.uuid4()),"sequence":1,"type":"start","elapsed_ms":0,"details":{}}]}
    return data


def test_persistence_idempotency_and_cascade(client):
    sid, data = create(client)
    assert client.put('/api/sessions/' + sid, json=data).status_code == 200
    assert ask(client, sid, 'Can I stop halfway?').json()['reply_id'] == 'controls'
    detail = client.get('/api/sessions/' + sid).json()
    assert detail['status'] == 'draft' and len(detail['messages']) == 2
    assert client.delete('/api/sessions/' + sid).status_code == 200
    with m.db() as c:
        assert c.execute('SELECT count(*) FROM messages').fetchone()[0] == 0
        assert c.execute('PRAGMA foreign_key_check').fetchall() == []


def test_replay_turn_never_calls_twice(client):
    sid, _ = create(client)
    payload = {"turn_id":str(uuid.uuid4()),"question":"What gets saved?","cue":"text"}
    a = client.post(f'/api/sessions/{sid}/messages',json=payload).json()
    b = client.post(f'/api/sessions/{sid}/messages',json=payload).json()
    assert a == b
    assert len(client.get('/api/sessions/' + sid).json()['messages']) == 2
    payload['question'] = 'a different question'
    assert client.post(f'/api/sessions/{sid}/messages',json=payload).status_code == 409


def test_rendered_completion_and_illegal_state(client):
    sid, data = create(client); data = started(data)
    assert client.put('/api/sessions/' + sid,json=data).status_code == 200
    data.update(revision=3,status='completed',wall_ms=59999,excluded_ms=0,assignment_duration_ms=59999,final_step_at=datetime.now(timezone.utc).isoformat())
    data['events'].append({"id":str(uuid.uuid4()),"sequence":2,"type":"completed","elapsed_ms":59999,"details":{}})
    assert client.put('/api/sessions/' + sid,json=data).status_code == 422
    data.update(wall_ms=60017,assignment_duration_ms=60017)
    assert client.put('/api/sessions/' + sid,json=data).status_code == 200
    data.update(revision=4,status='running')
    assert client.put('/api/sessions/' + sid,json=data).status_code in (409,422)


def test_journal_cannot_be_rewritten(client):
    sid, data = create(client); data = started(data)
    assert client.put('/api/sessions/' + sid,json=data).status_code == 200
    data['events'][0]['details'] = {'reason':'changed'}; data['revision'] += 1
    assert client.put('/api/sessions/' + sid,json=data).status_code == 409


def test_recovery_keeps_drafts_and_marks_only_active_unknown(client):
    draft_sid, _ = create(client); sid, data = create(client)
    assert client.put('/api/sessions/' + sid,json=started(data)).status_code == 200
    assert client.post('/api/recover').json()['recovered'] == 1
    recovered = client.get('/api/sessions/' + sid).json()
    assert recovered['status'] == 'interrupted' and recovered['wall_ms'] is None
    assert client.get('/api/sessions/' + draft_sid).json()['status'] == 'draft'


@pytest.mark.parametrize('text', ['I want to die', 'I do not want to die', 'I WANT   TO DIE'])
def test_direct_api_phrase_bypasses_provider(client, monkeypatch, text):
    monkeypatch.setattr(m,'LIVE',True)
    async def forbidden(*args): raise AssertionError('must not call provider')
    monkeypatch.setattr(m,'provider',forbidden)
    sid, _ = create(client)
    response = ask(client,sid,text,mode='live').json()
    assert response['rule_id'] == 'phrase-cue-v1'
    assert client.get('/api/health').json()['attempts'] == 0


@pytest.mark.parametrize('raw', ['not json','{"reply_id":"motion","evidence_ids":["catalog:storage"]}','{"reply_id":"motion","evidence_ids":["catalog:motion"],"advice":"bad"}'])
def test_invalid_model_output_is_fixed_and_counted(client,monkeypatch,raw):
    monkeypatch.setattr(m,'LIVE',True)
    async def provider(*args): return raw
    monkeypatch.setattr(m,'provider',provider)
    sid, _ = create(client)
    result = ask(client,sid,'moving circle',mode='live').json()
    assert result['source'] == 'fixed' and result['text'] == m.FALLBACK
    assert client.get('/api/health').json()['attempts'] == 1


def test_provider_failure_counts_and_budget_survives_deletion(client,monkeypatch):
    monkeypatch.setattr(m,'LIVE',True); monkeypatch.setattr(m,'LIMIT',1)
    async def broken(*args): raise httpx.ReadTimeout('mock timeout')
    monkeypatch.setattr(m,'provider',broken)
    sid, _ = create(client)
    assert ask(client,sid,'moving circle',mode='live').json()['source'] == 'fixed'
    client.delete('/api/local-data')
    sid, _ = create(client)
    answer = ask(client,sid,'moving circle',mode='live').json()
    assert answer['source'] == 'mock'
    assert client.get('/api/health').json()['attempts'] == 1


def test_atomic_budget_with_concurrent_requests(client,monkeypatch):
    monkeypatch.setattr(m,'LIVE',True); monkeypatch.setattr(m,'LIMIT',2)
    async def provider(*args):
        await asyncio.sleep(.05)
        return json.dumps({'reply_id':'motion'})
    monkeypatch.setattr(m,'provider',provider)
    sid,_ = create(client)
    async def run():
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=m.app),base_url='http://test') as c:
            return await asyncio.gather(*(c.post(f'/api/sessions/{sid}/messages',json={'turn_id':str(uuid.uuid4()),'question':'moving circle','cue':'text','mode':'live'}) for _ in range(6)))
    results = asyncio.run(run())
    assert sum(r.json()['source']=='live' for r in results) == 2
    assert sum(r.json()['source']=='mock' for r in results) == 4
    assert client.get('/api/health').json()['attempts'] == 2


def test_preference_is_explicit_and_resettable(client):
    assert client.get('/api/preferences').json() == {'cue':None}
    client.put('/api/preferences',json={'cue':'text'})
    sid,_ = create(client); ask(client,sid,'change my preference')
    assert client.get('/api/preferences').json() == {'cue':'text'}
    client.put('/api/preferences',json={'cue':None})
    assert client.get('/api/preferences').json() == {'cue':None}


def test_input_bounds_and_review_failure(client):
    sid,_=create(client)
    assert ask(client,sid,'x'*501).status_code == 422
    assert ask(client,sid,'   ').status_code == 422
    response=ask(client,sid,'Can I pause?',simulate_failure=True).json()
    assert response['source']=='fixed'
    assert client.get('/api/health').json()['attempts']==0


def test_host_preload_uses_same_budget_and_skips_at_cap(client,monkeypatch):
    from backend.warm_model import warm
    monkeypatch.setattr(m,'LIVE',True); monkeypatch.setattr(m,'LIMIT',1)
    calls=[]
    class FakeClient:
        def __init__(self,**kwargs): pass
        async def __aenter__(self): return self
        async def __aexit__(self,*args): pass
        async def post(self,*args,**kwargs):
            calls.append(kwargs)
            return httpx.Response(200,request=httpx.Request('POST','http://local-test'),json={'done':True})
    monkeypatch.setattr(httpx,'AsyncClient',FakeClient)
    asyncio.run(warm()); asyncio.run(warm())
    assert len(calls)==1
    assert client.get('/api/health').json()['attempts']==1
    with m.db() as c:
        assert c.execute('SELECT outcome FROM model_attempts').fetchone()[0]=='preload-complete'


@pytest.mark.parametrize('question,topic', [
    ('Can you be my therapist?', 'scope'),
    ('What is stress?', 'stress'),
    ('Does this app infer stress from clicks?', 'checkin'),
    ('Can it remember my usual cue?', 'preferences'),
    ('Which handbook sources are loaded?', 'resources'),
])
def test_expanded_help_is_catalog_text_without_preference_or_session_control(client, question, topic):
    sid, _ = create(client)
    result = ask(client, sid, question).json()
    assert result['source'] == 'mock' and result['reply_id'] == topic
    assert result['text'] == m.CATALOG[topic]
    assert result['catalog_version'] == 'app-help-v5'
    detail = client.get('/api/sessions/' + sid).json()
    assert detail['status'] == 'draft' and detail['events'] == []
    assert detail['messages'][-1]['content'] == result['text']
    assert client.get('/api/preferences').json() == {'cue': None}
    assert client.get('/api/health').json()['attempts'] == 0


def test_history_last_chat_uses_saved_user_messages_and_reorders_old_conversations(client):
    old, _ = create(client)
    newer, _ = create(client)
    empty, _ = create(client)
    assert client.get('/api/sessions/' + empty).json()['last_chat_at'] is None
    assert ask(client, old, 'How long is the exercise?').status_code == 200
    assert ask(client, newer, 'What gets saved?').status_code == 200
    with m.db() as c:
        c.execute("UPDATE messages SET created_at=? WHERE session_id=? AND role='user'", ('2026-10-26T15:00:00+00:00', newer))
        c.execute("UPDATE messages SET created_at=? WHERE session_id=? AND role='user'", ('2026-10-27T15:00:00+00:00', old))
        # A later assistant response or exercise-save time is not a user chat date.
        c.execute("UPDATE messages SET created_at=? WHERE role='assistant'", ('2026-10-28T15:00:00+00:00',))
        c.execute("UPDATE sessions SET created_at=?", ('2026-10-20T15:00:00+00:00',))
    rows = client.get('/api/sessions').json()
    assert [r['id'] for r in rows] == [old, newer, empty]
    assert rows[0]['last_chat_at'] == '2026-10-27T15:00:00+00:00'
    assert rows[2]['last_chat_at'] is None
    detail = client.get('/api/sessions/' + old).json()
    assert detail['last_chat_at'] == rows[0]['last_chat_at']
    assert all(m['created_at'] for m in detail['messages'])
    assert ask(client, old, 'Can I stop halfway?').status_code == 200
    assert client.delete('/api/sessions/' + old).status_code == 200
    assert all(r['id'] != old for r in client.get('/api/sessions').json())


def stopped_practice(client, cue='text'):
    sid, data = create(client)
    data = started(data)
    data.update(cue_initial=cue, cue_final=cue)
    assert client.put('/api/sessions/' + sid, json=data).status_code == 200
    data.update(revision=3, status='stopped', wall_ms=1500, assignment_duration_ms=1500)
    data['events'].append({'id':str(uuid.uuid4()),'sequence':2,'type':'stopped','elapsed_ms':1500,'details':{}})
    assert client.put('/api/sessions/' + sid, json=data).status_code == 200
    return sid


def test_profile_migration_persistence_validation_and_independent_cue(client):
    original = client.get('/api/profile').json()
    assert original['reply_detail'] == 'standard' and original['use_history'] is False
    assert original['latest_practice'] is None and original['updated_at'] is None
    client.put('/api/preferences', json={'cue':'text'})
    saved = client.put('/api/profile', json={'reply_detail':'brief','use_history':True}).json()
    assert saved['updated_at'] and saved['remembered_cue'] == 'text'
    m.migrate()  # Existing profile/cue survive idempotent migration/restart.
    assert client.get('/api/profile').json() == saved
    assert client.put('/api/profile',json={'reply_detail':'clinical','use_history':True}).status_code == 422
    assert client.put('/api/profile',json={'reply_detail':'brief','use_history':True,'diagnosis':'invented'}).status_code == 422
    reset = client.put('/api/profile',json={'reply_detail':'standard','use_history':False}).json()
    assert reset['use_history'] is False and reset['remembered_cue'] == 'text'
    with m.db() as c:
        assert {r[0] for r in c.execute('SELECT version FROM migrations')} == {1,2}


def test_reply_length_uses_reviewed_variants_without_inferred_persona(client):
    sid, _ = create(client)
    regular = ask(client,sid,'How long is the exercise?').json()
    assert regular['text'] == m.CATALOG['pacing']
    client.put('/api/profile',json={'reply_detail':'brief','use_history':False})
    brief = ask(client,sid,'How long is the exercise?').json()
    assert brief['text'] == m.compose_reply('pacing',{'reply_detail':'brief','use_history':False},'text')[0]
    assert len(brief['text']) < len(regular['text'])
    assert brief['personalization_context'] == {'reply_detail':'brief','history_used':False}
    assert client.get('/api/sessions/' + sid).json()['events'] == []
    assert client.get('/api/preferences').json()['cue'] is None


def test_opt_in_tailors_from_real_saved_history_and_opt_out_removes_context(client):
    practice = stopped_practice(client, 'animated')
    sid, _ = create(client)
    assert client.get('/api/profile').json()['latest_practice'] is None
    before = ask(client,sid,'Can I stop halfway?').json()
    assert 'latest saved practice' not in before['text']
    client.put('/api/preferences',json={'cue':'animated'})
    client.put('/api/profile',json={'reply_detail':'brief','use_history':True})
    after = ask(client,sid,'Can I stop halfway?').json()
    assert 'current cue is Text only' in after['text']
    assert 'remembered cue is Animated circle' in after['text']
    assert 'latest saved practice was stopped' in after['text']
    assert 'finishing is not required' in after['text']
    assert 'last recorded Animated circle' in after['text']
    context = after['personalization_context']
    assert context['history_used'] and context['latest_practice']['status'] == 'stopped'
    assert client.get('/api/sessions/' + sid).json()['messages'][-1]['metadata']['personalization_context'] == context
    client.put('/api/profile',json={'reply_detail':'brief','use_history':False})
    assert ask(client,sid,'Can I stop halfway?').json()['personalization_context']['history_used'] is False
    client.put('/api/profile',json={'reply_detail':'brief','use_history':True})
    client.delete('/api/sessions/' + practice)
    empty = ask(client,sid,'How long is the exercise?').json()
    assert 'no saved finished' in empty['text'] and 'latest saved practice was stopped' not in empty['text']


def test_live_selector_receives_no_profile_or_raw_history_but_display_is_tailored(client,monkeypatch):
    stopped_practice(client)
    sid, _ = create(client)
    client.put('/api/profile',json={'reply_detail':'brief','use_history':True})
    monkeypatch.setattr(m,'LIVE',True)
    calls=[]
    async def provider(question,cue):
        calls.append((question,cue))
        return '{"reply_id":"motion"}'
    monkeypatch.setattr(m,'provider',provider)
    result = ask(client,sid,'Can I turn off the moving circle?',mode='live').json()
    assert calls == [('Can I turn off the moving circle?','text')]
    assert result['source'] == 'live' and result['personalization_context']['history_used'] is True
    assert 'latest saved practice was stopped' in result['text']
    assert client.get('/api/health').json()['attempts'] == 1
    assert client.get('/api/profile').json()['reply_detail'] == 'brief'


def test_profile_does_not_tailor_boundary_or_unrelated_topics_and_delete_all_resets(client):
    stopped_practice(client)
    sid, _ = create(client)
    client.put('/api/profile',json={'reply_detail':'brief','use_history':True})
    boundary = ask(client,sid,'I want to die').json()
    assert boundary['text'] == m.BOUNDARY and 'personalization_context' not in boundary
    scope = ask(client,sid,'Can you be my therapist?').json()
    assert scope['personalization_context']['history_used'] is False
    assert 'not a therapist' in scope['text'] and 'latest saved practice' not in scope['text']
    failure = ask(client,sid,'How long is the exercise?',simulate_failure=True).json()
    assert failure['text'] == m.FALLBACK and 'personalization_context' not in failure
    client.delete('/api/local-data')
    reset = client.get('/api/profile').json()
    assert reset['reply_detail']=='standard' and reset['use_history'] is False and reset['latest_practice'] is None
    assert reset['remembered_cue'] is None and reset['updated_at'] is None


def test_all_topics_have_plain_reviewed_brief_variants(client):
    from backend.catalog import CONTENT
    client.put('/api/profile',json={'reply_detail':'brief','use_history':False})
    for topic in CONTENT['topics']:
        answer, context = m.compose_reply(topic,{'reply_detail':'brief','use_history':False},'text')
        assert answer == CONTENT['topics'][topic]['brief'] and context['history_used'] is False
        assert '<script' not in answer


def test_replayed_turn_keeps_original_profile_snapshot_after_reset(client):
    stopped_practice(client)
    sid, _ = create(client)
    client.put('/api/profile',json={'reply_detail':'brief','use_history':True})
    turn={'turn_id':str(uuid.uuid4()),'question':'Can I stop halfway?','cue':'text','mode':'mock'}
    original=client.post(f'/api/sessions/{sid}/messages',json=turn).json()
    client.put('/api/profile',json={'reply_detail':'standard','use_history':False})
    replay=client.post(f'/api/sessions/{sid}/messages',json=turn).json()
    assert replay==original
    next_reply=ask(client,sid,'Can I stop halfway?').json()
    assert next_reply['reply_detail']=='standard' and next_reply['personalization_context']['history_used'] is False


def test_latest_practice_uses_exercise_start_not_old_draft_creation(client):
    older=stopped_practice(client,'animated')
    latest=stopped_practice(client,'text')
    with m.db() as c:
        # Fix both timestamps: this must remain independent of the machine's date.
        # The newer practice began from a much older draft conversation.
        for sid, created, exercise_start in [
            (older, '2020-01-01T00:00:00+00:00', '2020-02-01T00:00:00+00:00'),
            (latest, '2019-01-01T00:00:00+00:00', '2021-01-01T00:00:00+00:00'),
        ]:
            row=c.execute('SELECT snapshot FROM sessions WHERE id=?',(sid,)).fetchone()
            snapshot=json.loads(row['snapshot'])
            snapshot.update(created_at=created,first_instruction_at=exercise_start)
            c.execute('UPDATE sessions SET created_at=?,snapshot=? WHERE id=?',(created,json.dumps(snapshot),sid))
    client.put('/api/profile',json={'reply_detail':'standard','use_history':True})
    summary=client.get('/api/profile').json()['latest_practice']
    assert summary['cue']=='text' and summary['started_at']=='2021-01-01T00:00:00+00:00'


@pytest.mark.parametrize('text',['what is mello',"what's mello",'tell me about mello','what is the purpose of this app','what is this app for','What can mello help me with?'])
def test_app_purpose_explains_features_without_repeated_role_warning(client,text):
    sid,_=create(client)
    result=ask(client,sid,text).json()
    assert result['reply_id']=='about' and 'mello' in result['text']
    assert result['text']==m.CATALOG['about']
    assert 'not a therapist' not in result['text']
    assert 'fictional' not in result['text']


@pytest.mark.parametrize('text',['Can you be my therapist?','Can you diagnose me?','Is this app for therapy?'])
def test_role_questions_still_receive_explicit_honest_limits(client,text):
    sid,_=create(client)
    result=ask(client,sid,text).json()
    assert result['reply_id']=='scope'
    assert 'not a therapist' in result['text']
    assert result['source']=='mock'
