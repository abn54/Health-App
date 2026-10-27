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
    assert result['catalog_version'] == 'app-help-v2'
    detail = client.get('/api/sessions/' + sid).json()
    assert detail['status'] == 'draft' and detail['events'] == []
    assert detail['messages'][-1]['content'] == result['text']
    assert client.get('/api/preferences').json() == {'cue': None}
    assert client.get('/api/health').json()['attempts'] == 0
