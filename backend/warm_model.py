"""Explicit host-only preload; reserves the same persistent provider-attempt budget."""
import asyncio
import uuid

import httpx

from . import main as m


async def warm():
    if not m.LIVE:
        return
    attempt = str(uuid.uuid4())
    with m.db() as c:
        c.execute('BEGIN IMMEDIATE')
        used = c.execute('SELECT count(*) FROM model_attempts WHERE test_run_id=?', (m.RUN_ID,)).fetchone()[0]
        if used >= m.LIMIT:
            print('Model budget exhausted; preload skipped, mocks remain available.')
            return
        c.execute('INSERT INTO model_attempts VALUES(?,?,?,?,?,?)', (attempt,m.RUN_ID,None,m.MODEL,m.now(),'preload-reserved'))
    try:
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post('http://127.0.0.1:11434/api/chat',json={'model':m.MODEL,'messages':[],'stream':False,'keep_alive':'30m'})
            response.raise_for_status()
        outcome = 'preload-complete'
        print('Local model preloaded. The UI still defaults to mocked replies.')
    except Exception:
        outcome = 'preload-failed'
        print('Model preload failed. The app will still run; live questions may use a fixed fallback.')
    with m.db() as c:
        c.execute('UPDATE model_attempts SET outcome=? WHERE id=?',(outcome,attempt))


if __name__ == '__main__':
    asyncio.run(warm())
