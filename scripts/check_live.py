"""Explicit, small fictional live check. Routine tests never invoke this script."""
import argparse
import json
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

parser = argparse.ArgumentParser()
parser.add_argument('--live', action='store_true', required=True, help='Explicitly allow three live local-model requests')
parser.add_argument('--base', default='http://127.0.0.1:8000')
args = parser.parse_args()


def api(path, method='GET', data=None):
    request = Request(args.base + '/api' + path, method=method, headers={'Content-Type':'application/json'},data=json.dumps(data).encode() if data is not None else None)
    with urlopen(request, timeout=15) as response:
        return json.load(response)


health = api('/health')
if not health['live_enabled'] or health['limit'] - health['attempts'] < 3:
    raise SystemExit('Enable live on the host with at least three remaining attempts first.')
sid = str(uuid.uuid4())
api('/sessions/' + sid, 'PUT', {'revision':1,'status':'draft','created_at':datetime.now(timezone.utc).isoformat(),'events':[]})
cases = [('Do I have to watch a moving shape?','motion'),('What stays after I close this?','storage'),('Can I stop halfway?','controls')]
observations = []
for question, expected in cases:
    started = time.perf_counter()
    result = api('/sessions/' + sid + '/messages','POST', {'turn_id':str(uuid.uuid4()),'question':question,'cue':'text','mode':'live'})
    observations.append({'question':question,'expected_reply_id':expected,'observed':result,'elapsed_ms':round((time.perf_counter()-started)*1000,2),'matched':result['source']=='live' and result['reply_id']==expected})
    print(question, 'expected=', expected, 'observed=', result['reply_id'], 'source=',result['source'])
record = {'date':datetime.now(timezone.utc).isoformat(),'method':'Actual local Ollama requests through running FastAPI; three sequential questions in one persisted session; provider context documented by prompt version; one run per case, not a variation study','before':health,'after':api('/health'),'session_id':sid,'cases':observations}
Path('docs/evidence/live-selection-' + health['prompt_version'] + '.json').write_text(json.dumps(record,indent=2)+'\n')
raise SystemExit(0 if all(r['matched'] for r in observations) else 1)
