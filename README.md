# mello — Part 3.3 coursework prototype

Vue, FastAPI, and SQLite application running on **localhost only**. Choose paced breathing, 5–4–3–2–1 grounding or STOP. Breathing retains six cycles of four one-second counts in and six out. Review saved sessions and fictional conversations, choose a reversible pacing cue, and open bundled Crisis support from every view.

**Fictional coursework use only.** This is not therapy, diagnosis, or a monitored service. Do not deploy or recommend it as mental health support.

Repository: [abn54/Health-App](https://github.com/abn54/Health-App). Submission: [report.md](report.md). The original design report is retained in [submissions/part1/report.md](submissions/part1/report.md). Earlier Part 2 reports remain in [submissions/part2/](submissions/part2/), including the last submitted [Part 2 report](submissions/part2/latest-report.md).

Part 3.3: [evaluation and actual results](docs/part3-evaluation.md), [design revisions](docs/part3-revisions.md), [finished-app and process recordings with transcripts](docs/recordings/README.md), and [final clean-checkout evidence](docs/evidence/part3-final-clean-checkout-oct30.json). The October 30 implementation is `83ddf65c92e62f3207c8113eb1d77e87942b58b8`. The October 31 coastal revision adds two exercises; its dated evidence is separate from the earlier recordings and evaluation.

Presentation preparation: [rubric-aligned walkthrough and speaking notes](presentation-walkthrough.md), [profile changes and actual checks](docs/presentation-readiness-oct28.md). Expand **Your local profile** on Practice for **Standard explanations / Brief reminders** and an opt-in switch to use cue/saved practice context in replies. **Save profile** persists these choices; **Reset profile** restores standard replies and context off while keeping cue/history. One profile is shared by anyone using this localhost server; no account, name, diagnosis or mood rating is needed.

Accessibility: **Accessibility options** offers Higher contrast, Larger text and configurable screen-reader breathing updates. Skip to main content, named controls, keyboard focus, phase/count text, and independent support remain available. These options apply to the current visit. Breathing has **no app-generated speech or tones**; a user's screen reader may read accessible instructions in its own voice. [Actual accessibility checks and limits](docs/accessibility-update-oct28.md).

Optional **Chatbot voice** exists only in the assistant: blue **Preview voice / Read reply aloud**, red **Stop voice**, a speed selector and an opt-in automatic-reading checkbox. Enhanced voice-name options rank first when installed; known novelty voices are hidden. Available quality depends on the device, and no acoustic-quality guarantee is made. Voice choices reset on reload, with no microphone, recording or remote TTS. Keep auto-read off if a screen reader is already reading replies.

Current interface (October 31): **mello — the quiet coast**. The top bar has Practice, Session history and Crisis support. The assistant exists **only** in the bottom-right popup; no duplicate top navigation entry or inline chat. A locally bundled original coastal image, muted green palette and three direct Start cards form the new layout. [Changes, actual checks, asset prompt and limits](docs/coastal-update-oct31.md).

New guides: **5–4–3–2–1 grounding** uses five 12-second prompts; **STOP** uses four 15-second prompts. Both have an intended one-minute sequence, Pause for more time, immediate End, interruption recovery and skill-labeled local history. The model cannot edit their steps or timing. All practice audio remains off. Profile/history response tailoring deliberately remains specific to breathing records and is labeled accordingly.

The assistant popup keeps a rounded message composer visible while the conversation scrolls. Enter sends; Shift+Enter adds a line. Read replies enables optional spoken replies; Reply & voice options expands voice/speed and prepared/live controls. Existing storage names remain compatible.

Earlier functional refinements: color-coded inhale/exhale, an optional assistant popup, eleven FAQs, six editable suggested questions, an SVG rhythm guide and a source-labeled reading shelf. [October 27 changes and actual verification](docs/ui-refinement-oct27.md).

## Run a clean checkout

Requirements: Python 3.11 or newer; Node 22.12 or newer with npm. This version was developed with Python 3.14.7, Node 26.7.0, npm 11.19.0, Vue 3.5.44, and Vite 8.3.4. Dependencies are pinned in `requirements.txt` and `frontend/package-lock.json`.

```sh
git clone --branch codex/part2-prototype https://github.com/abn54/Health-App.git
cd Health-App
sh scripts/run.sh
```

Open **http://127.0.0.1:8000**. The script creates a project virtual environment, installs pinned dependencies, performs `npm ci`, builds Vue, and serves the build and API from FastAPI on loopback. Stop with Ctrl+C. Internet is needed for dependency installation; the built app uses no external fonts or assets. Exercise and support have no API prerequisite after the page loads. Initially loading the page still requires the server.

If the browser reports **connection refused**, check that the localhost server is still running. After dependencies and the build already exist, restart it from the repository directory with `.venv/bin/python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000` and keep that terminal open. This serves both the built Vue frontend and API; a separate Vite server is unnecessary for port 8000. Use the explicit live-mode configuration above/below only when intended. The server does not automatically start after reboot.

Replies are **mocked by default**. Ollama and API keys are unnecessary for exercise, history, preferences, support, or routine tests. SQLite is created automatically at `data/pause.sqlite3` and ignored by Git. It is local unencrypted storage: enter fictional inputs only.

## Optional real local model

Install [Ollama](https://ollama.com/download) from its official source. In a separate terminal:

```sh
OLLAMA_HOST=127.0.0.1:11434 OLLAMA_NO_CLOUD=1 ollama serve
```

If an Ollama server already runs on that port, use it rather than starting a duplicate. Pull the tested model, then launch the app with explicit live permission:

```sh
ollama pull qwen2.5:3b
ALLOW_LIVE_MODEL=1 OLLAMA_MODEL=qwen2.5:3b MODEL_TEST_RUN_ID=peer-review-01 MODEL_ATTEMPT_LIMIT=50 sh scripts/run.sh
```

The startup script explicitly preloads the local model (up to 60 seconds, outside the exercise) and counts that provider attempt. Cold startup exceeded the eight-second question timeout during development. If preload fails, the app still starts. The UI still defaults to Mock. Choose the bottom-right **Ask the assistant** button, expand **Reply & voice options**, then select **Live local model**, and ask a fictional app question such as “What stays after I close this?” FastAPI sends the current question and approved app facts with authored classification examples (earlier messages and the selected cue are not sent) to local Ollama. Only reviewed catalog text can appear after validation. The saved reply-length choice and opted-in factual practice context are applied by reviewed local rules; the model does not receive the profile or raw history. The assistant is educational, not a therapist; it cannot diagnose or provide treatment. General stress answers link their NIMH source; handbook listings are not treated as full-text evidence. The tested model is listed on the [official model page](https://ollama.com/library/qwen2.5:3b), including its license; the model files are not redistributed in this repository. Missing Ollama, an eight-second timeout, malformed or disallowed selection returns a fixed fallback; Start and Crisis support remain available.

`MODEL_TEST_RUN_ID` identifies the host's peer-test session. Reuse it across restarts of that session: attempted, failed, and retried provider calls count toward an aggregate SQLite budget capped at 50. History deletion does not reset accounting. At the limit replies use visibly labeled mocks. Start a new ID only for a genuinely new host-controlled test session. Do not run multiple differently configured hosts against the same database. Model files are not committed.

## Review and verify

```sh
.venv/bin/python -m pytest backend/test_api.py -q
cd frontend
npm test
npm run build
```

Backend tests use temporary databases and mocked provider outputs. Client tests use injected exercise clocks and fake speech APIs and announcement-text cases to check cancellation, late playback, voice ordering, unavailable output and assistive text. The exercise-clock cases remain separate. Actual browser duration and live-model observations are separate in [Part 2 evidence](docs/part2-verification.md). A dependency deprecation warning from Starlette's current TestClient is recorded rather than hidden.

For development, run `.venv/bin/python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000`, and `npm run dev` inside `frontend` in a second terminal. Vite binds loopback and proxies `/api`. Production-build checks use port 8000. Rebuild and restart FastAPI when switching from an unbuilt frontend to the static build.

For deliberate fictional failures, launch with `REVIEW_TOOLS=1`. Expand **Coursework review tools** to simulate a model failure or session-save failure. These controls are absent by default. Stopping the API also demonstrates a real outage: the already-loaded exercise/support continue; history and persistence report failure. Do not contact real crisis services during testing.

## Prototype behavior

1. Choose Animated circle or Text only. Remember is explicit; Reset removes the saved preference. Changing the active cue never changes the remembered preference or pace.
2. Start without questions. Pause preserves the phase/count fraction; Resume is explicit. End is immediate. Completion leaves the summary on screen.
3. Opening the assistant popup during practice pauses it and disables new questions. Close returns to the paused exercise; Resume is explicit. Crisis support remains inside the popup header. Open Crisis support during an exercise: it pauses. Return leaves it paused. History behaves the same way and retains Return and End controls.
4. Review History: Started and Last chatted dates/times, per-message timestamps in the device’s time zone, status, initial/final cue, timing, events, and conversation source labels. Draft questions are “Not started.” Reuse copies a recorded cue into Ready without starting or remembering it.
5. Deleting a session removes its conversation/events. Delete all additionally resets cue and profile choices after confirmation. Provider-attempt accounting remains. Unsaved records stay only in page memory with Retry; the summary also offers Leave without saving, so a failed write cannot trap someone after End. Unsaved changes may be lost; already saved records remain in History.

The current catalog is `app-help-v6`, prompt template `catalog-selector-v12`, and personalization copy `profile-copy-v1`. The model remains `qwen2.5:3b`.

To use a different loopback port for an isolated review, set `MELLO_PORT=8002 sh scripts/run.sh`; the default remains 8000.

One active page/tab is assumed. Hiding the page or a scheduling gap over two seconds interrupts; there is no automatic resume. Reload recovers persisted running/paused sessions as interrupted with unknown final timing, while drafts stay Not started. Multi-tab reconciliation, broad model evaluation and real screen-reader/blind-user validation remain unresolved. Part 3.3 includes a small repeated live selection and actual demonstration/process recordings; these do not establish clinical effectiveness.

## Project map

| File | Purpose |
| --- | --- |
| `frontend/src/App.vue` | UI, explicit choices, persistence journal, bundled support |
| `frontend/src/engine.js` | Deterministic state and monotonic pacing |
| `frontend/src/audio.js` | Chatbot-only on-device speech, curated voice ordering and cancellation |
| `frontend/src/accessibility.js` | Screen-reader announcement text; no speech synthesis |
| `backend/main.py` | Validated API, migration, SQLite, Ollama adapter, atomic budget |
| `backend/catalog.py`, `shared/help-content.json` | Shared reviewed FAQ/model copy, sources, mocks and fallible phrase cues |
| `frontend/src/components/` | Shared assistant panel, FAQ/reading shelf and original SVG rhythm guide |
| `docs/design.md`, `docs/architecture.md`, `docs/research-findings.md` | Design, implementation revisions and full R/D mapping |
| `docs/dataset-design-notes.md` | Actual use and inspection limits of supplied Kaggle resource |
| `docs/part2-verification.md`, `docs/evidence/` | Actual observations and redacted evidence |
| `AI-USE.md`, `docs/evidence-log.md` | AI disclosure, selected decisions and failures |

The complete R1–R4 / D1–D6 table arrived in the student's October 21 overview. [Research mapping](docs/research-findings.md) connects all ten findings to implemented decisions, evidence, and explicit tradeoffs. Earlier missing-table notices describe the historical Part 1 source limitation. The Kaggle source informed intent/pattern/catalog design; no training, clinical audit, or effectiveness claim is made. No earlier coursework source code was supplied or reused.


For development accessibility scans, run the normal backend (or a separate fictional database), then `MELLO_REVIEW_API=http://127.0.0.1:8001 npm run dev -- --port 5173` in `frontend` if using a separate API on 8001. Without that optional variable Vite proxies the normal 8000 API. Open `http://127.0.0.1:5173/?a11y-review` and use **Run accessibility audit** after manually reaching each state. The dev-only harness uses pinned `axe-core` 4.14.0; it is absent from the production build. Automated scans report only detectable issues and include items needing manual review; they are not WCAG certification or a substitute for blind-user/screen-reader testing.


Current chat wording: **Your question / You** replaces repeated fictional-question labels. **Prepared reply** is the display name for the mock path, with its reviewed-text meaning explained in Reply & voice options. Live mode still only selects reviewed text. Ordinary purpose questions explain the app features; direct therapist/diagnosis questions retain explicit limits. One short visible coursework/demo notice remains. Saved earlier messages keep their original text and metadata. [Actual checks](docs/chat-copy-oct28.md).


## Part 3.3 repeatable evaluation

After the normal setup, run `.venv/bin/python scripts/evaluate_part3.py --output /tmp/mello-mocked.json` for 22 fictional in-process HTTP scenarios. It uses disposable SQLite/stubbed providers, not real model calls. The existing test commands above remain. The October 30 final clean checkout ran 39 backend tests, 17 client tests and these 22 scenarios successfully; page/assets returned 200 with live mode and review tools off. A Starlette TestClient deprecation warning remains.

`scripts/evaluate_part3_live.py --live --base http://127.0.0.1:8001 --output /tmp/mello-live.json` is only for an explicitly configured isolated live review host with its own `PAUSE_DB`, stable `MODEL_TEST_RUN_ID`, `ALLOW_LIVE_MODEL=1` and cap at most 50. It makes 15 real selections; do not use for routine tests. The actual October 30 run plus preload and one recorded demonstration used 17/50 attempts. Repeated role-question misclassification remains documented.

Final keyboard refinement restores popup focus after a speech control disappears and captures Escape while a dialog is open. History navigation waits for the active save journal before fetching the list so the saved row reflects Paused. The [failure, evidence and retests](docs/part3-evaluation.md) explain these changes.


October 31 revision checks: 44 backend tests, 21 client tests, build and 22 mocked scenarios passed. Separate selected live evaluation used nine actual selections plus one counted preload (10/50). Single actual Grounding/STOP browser completions are recorded separately from synthetic tests. Earlier recordings and clean-checkout evidence identify their older pinned version; they do not claim to show the coastal layout.
