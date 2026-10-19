# Pause — Part 3.2 coursework prototype

Vue, FastAPI, and SQLite application running on **localhost only**. Complete six cycles of four one-second counts in and six out. Review saved sessions and fictional conversations, choose a reversible pacing cue, and open bundled Crisis support from every view.

**Fictional coursework use only.** This is not therapy, diagnosis, or a monitored service. Do not deploy or recommend it as mental health support.

Repository: [abn54/Health-App](https://github.com/abn54/Health-App). Submission: [report.md](report.md). The original design report is retained in [submissions/part1/report.md](submissions/part1/report.md).

## Run a clean checkout

Requirements: Python 3.11 or newer; Node 22.12 or newer with npm. This version was developed with Python 3.14.7, Node 26.7.0, npm 11.19.0, Vue 3.5.44, and Vite 8.3.4. Dependencies are pinned in `requirements.txt` and `frontend/package-lock.json`.

```sh
git clone --branch codex/part2-prototype https://github.com/abn54/Health-App.git
cd Health-App
sh scripts/run.sh
```

Open **http://127.0.0.1:8000**. The script creates a project virtual environment, installs pinned dependencies, performs `npm ci`, builds Vue, and serves the build and API from FastAPI on loopback. Stop with Ctrl+C. Internet is needed for dependency installation; the built app uses no external fonts or assets. Exercise and support have no API prerequisite after the page loads. Initially loading the page still requires the server.

Replies are **mocked by default**. Ollama and API keys are unnecessary for exercise, history, preferences, support, or routine tests. SQLite is created automatically at `data/pause.sqlite3` and ignored by Git. It is local unencrypted storage: enter fictional inputs only.

## Optional real local model

Install [Ollama](https://ollama.com/download) from its official source. In a separate terminal:

```sh
OLLAMA_HOST=127.0.0.1:11434 OLLAMA_NO_CLOUD=1 ollama serve
```

If an Ollama server already runs on that port, use it rather than starting a duplicate. Pull the tested model, then launch the app with explicit live permission:

```sh
ollama pull qwen2.5:1.5b
ALLOW_LIVE_MODEL=1 OLLAMA_MODEL=qwen2.5:1.5b MODEL_TEST_RUN_ID=peer-review-01 MODEL_ATTEMPT_LIMIT=50 sh scripts/run.sh
```

The startup script explicitly preloads the local model (up to 60 seconds, outside the exercise) and counts that provider attempt. Cold startup exceeded the eight-second question timeout during development. If preload fails, the app still starts. The UI still defaults to Mock. Expand **Questions about the prototype?**, select **Live local model**, and ask a fictional app question such as “What stays after I close this?” FastAPI sends the catalog, selected cue, current question, and approved app facts (earlier messages are saved for review but not sent) to local Ollama. Only validated catalog text can appear. Missing Ollama, an eight-second timeout, malformed selection, or wrong evidence returns a fixed fallback; Start and Crisis support remain available.

`MODEL_TEST_RUN_ID` identifies the host's peer-test session. Reuse it across restarts of that session: attempted, failed, and retried provider calls count toward an aggregate SQLite budget capped at 50. History deletion does not reset accounting. At the limit replies use visibly labeled mocks. Start a new ID only for a genuinely new host-controlled test session. Do not run multiple differently configured hosts against the same database. Model files are not committed.

## Review and verify

```sh
.venv/bin/python -m pytest backend/test_api.py -q
cd frontend
npm test
npm run build
```

Backend tests use temporary databases and mocked provider outputs. Client tests use an injected clock. Actual browser duration and live-model observations are separate in [Part 2 evidence](docs/part2-verification.md). A dependency deprecation warning from Starlette's current TestClient is recorded rather than hidden.

For development, run `.venv/bin/python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000`, and `npm run dev` inside `frontend` in a second terminal. Vite binds loopback and proxies `/api`. Production-build checks use port 8000. Rebuild and restart FastAPI when switching from an unbuilt frontend to the static build.

For deliberate fictional failures, launch with `REVIEW_TOOLS=1`. Expand **Coursework review tools** to simulate a model failure or session-save failure. These controls are absent by default. Stopping the API also demonstrates a real outage: the already-loaded exercise/support continue; history and persistence report failure. Do not contact real crisis services during testing.

## Prototype behavior

1. Choose Animated circle or Text only. Remember is explicit; Reset removes the saved preference. Changing the active cue never changes the remembered preference or pace.
2. Start without questions. Pause preserves the phase/count fraction; Resume is explicit. End is immediate. Completion leaves the summary on screen.
3. Open Crisis support during an exercise: it pauses. Return leaves it paused. History behaves the same way and retains Return and End controls.
4. Review History: status, initial/final cue, timing, events, and conversation source labels. Draft questions are “Not started.” Reuse copies a recorded cue into Ready without starting or remembering it.
5. Deleting a session removes its conversation/events. Delete all additionally resets the preference after confirmation. Provider-attempt accounting remains. Unsaved records stay only in page memory with Retry; closing may lose them.

One active page/tab is assumed. Hiding the page or a scheduling gap over two seconds interrupts; there is no automatic resume. Reload recovers persisted running/paused sessions as interrupted with unknown final timing, while drafts stay Not started. Multi-tab reconciliation, broader model evaluation, screen-reader certification, and Part 3 recordings remain outside this milestone.

## Project map

| File | Purpose |
| --- | --- |
| `frontend/src/App.vue` | UI, explicit choices, persistence journal, bundled support |
| `frontend/src/engine.js` | Deterministic state and monotonic pacing |
| `backend/main.py` | Validated API, migration, SQLite, Ollama adapter, atomic budget |
| `backend/catalog.py` | Authored approved responses, mocks, fallible phrase cues |
| `docs/design.md`, `docs/architecture.md` | Original design and implementation notes |
| `docs/dataset-design-notes.md` | Actual use and inspection limits of supplied Kaggle resource |
| `docs/part2-verification.md`, `docs/evidence/` | Actual observations and redacted evidence |
| `AI-USE.md`, `docs/evidence-log.md` | AI disclosure, selected decisions and failures |

The R1–R4 / D1–D6 table was absent from the supplied briefs. Only R1's attention finding and D1's stated limitation are mapped by label; other labels are not invented. The Kaggle source informed intent/pattern/catalog design; no training, clinical audit, or effectiveness claim is made. No earlier coursework source code was supplied or reused.
