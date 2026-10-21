# IST 402 — Assignment 3, Part 2 (3.2)

## Submitted version

**Project:** Pause, a localhost coursework skills prototype. **Date:** October 21, 2026. **Milestone:** Working Application and Safety.

- Repository: [abn54/Health-App](https://github.com/abn54/Health-App).
- Working branch: [codex/part2-prototype](https://github.com/abn54/Health-App/tree/codex/part2-prototype).
- Submitted implementation/evidence commit: [`9e20276b6678ae8337cc2e64a0e9940396bb798b`](https://github.com/abn54/Health-App/commit/9e20276b6678ae8337cc2e64a0e9940396bb798b). The implementation was frozen before finalizing these links; a subsequent report-only commit does not change that snapshot.
- [Run instructions](https://github.com/abn54/Health-App/blob/9e20276b6678ae8337cc2e64a0e9940396bb798b/README.md), [design and flow](https://github.com/abn54/Health-App/blob/9e20276b6678ae8337cc2e64a0e9940396bb798b/docs/design.md), [architecture and revisions](https://github.com/abn54/Health-App/blob/9e20276b6678ae8337cc2e64a0e9940396bb798b/docs/architecture.md), [complete research mapping](https://github.com/abn54/Health-App/blob/9e20276b6678ae8337cc2e64a0e9940396bb798b/docs/research-findings.md).
- [Verification and screenshots](https://github.com/abn54/Health-App/blob/9e20276b6678ae8337cc2e64a0e9940396bb798b/docs/part2-verification.md), [current SQLite inspection](https://github.com/abn54/Health-App/blob/9e20276b6678ae8337cc2e64a0e9940396bb798b/docs/evidence/database-inspection-oct21.json), [requirements audit](https://github.com/abn54/Health-App/blob/9e20276b6678ae8337cc2e64a0e9940396bb798b/docs/requirements-audit.md).
- [AI-use disclosure](https://github.com/abn54/Health-App/blob/9e20276b6678ae8337cc2e64a0e9940396bb798b/AI-USE.md), [curated process evidence](https://github.com/abn54/Health-App/blob/9e20276b6678ae8337cc2e64a0e9940396bb798b/docs/evidence-log.md), [agent instructions](https://github.com/abn54/Health-App/blob/9e20276b6678ae8337cc2e64a0e9940396bb798b/AGENTS.md).

Upload **this one `report.md`** for Part 3.2. Supporting code and evidence are linked above. The supplied overview assigns the finished demonstration and process screencast to **Part 3.3**; no recording is claimed for this milestone.

## Working experience and scope

Vue presents one prescribed skill: **inhale four counts, exhale six counts, six cycles at one second per count**. FastAPI serves the production UI/API on `127.0.0.1:8000`; SQLite stores fictional conversations, session records, events and an optional explicit cue preference. No extra skill or speech feature is required for this coherent version. It is fictional coursework only: no diagnosis, therapy, promised improvement, human monitoring, real distressed participants or service deployment.

Ready offers direct Start without a question or model response. Animated circle expands for four counts and contracts for six; Text only retains the instruction/count without the moving shape. Pause preserves the phase and fractional count; Resume is explicit; End immediately stops pacing and produces a neutral partial-session summary. Completion leaves the summary visible as long as desired. Opening Crisis support, History or the sidebar AI assistant pauses an active exercise; Return does not automatically resume. New questions are disabled while an exercise is active.

The sidebar assistant answers optional questions about this app's pacing, controls, settings, storage and boundaries. It shares the Practice question panel and saved conversation. It is bounded application help, not a therapeutic conversation. History shows Completed, Stopped, Interrupted or Not started, the available timing, initial/last cue, recorded events and saved questions/replies with source labels. Draft conversations can continue; copying a historical cue returns to Ready for review and requires a fresh Start.

Remember saves a deliberate cue choice; Reset restores the system default. A session override does not silently overwrite the remembered setting. System reduced-motion chooses text by default. The app knows explicit selections and interaction records; it does not infer distress, diagnoses, treatment needs, whether someone followed the rhythm or whether it helped. No streak, rating, improvement score or reward pressures completion.

## Research grounding and tradeoffs

The complete instructor table was supplied October 21. Earlier Part 1 copies omitted it; the archived design report is not retroactively presented as having that source. The study involved 15 patients, 13 clinicians, 15 prototype sessions and 150 coded participant–task combinations. Counts below are **mentions, not effectiveness measures**.

| Finding | Implemented decision and compromise |
| --- | --- |
| **R1:** attention falls beyond 90–100 seconds; ~60 comfortable (38) | Six 10-second cycles, no response/model/save wait during pacing; measured app/render delay included below. |
| **R2:** frictionless crisis access (30) | Sticky shell button directly opens bundled information, independent of any question, API or classifier. |
| **R3:** permission to stop/leave (39) | Immediate End, neutral partial outcomes and explicit Leave without saving after a failed write; unsaved loss is explained. |
| **R4:** user controls the journey (68) | Optional questions, reversible cue choice, explicit Resume and fresh Start after history reuse; model cannot navigate. |
| **D1:** progressive contraction, without an established distress detector (54) | Starting replaces Ready's cards/settings with the simple exercise view. This uses chosen activity, not inferred emotional state; exit/support/navigation remain. |
| **D2:** one atomic skill/action (100) | One current inhale/exhale instruction in the main exercise view. Retaining shell navigation is an explicit compromise with R4 and safety. |
| **D3:** minimize disclosure/performance cost (148) | No required story, rating, typing, chat, diagnosis or outcome proof. Less subjective data means no usefulness inference. |
| **D4:** persistently visible safety (31) | Crisis support remains inside the exercise and during loading/errors; actual loaded-page outage checks support this claim. |
| **D5:** personalization without configuration burden (49) | One skill, optional remembered cue and history reuse reduce repeated decisions. One explicit Remember action sacrifices some automatic adaptation to preserve R4. |
| **D6:** restrained, non-judgmental presentation (97) | Muted colors, neutral language, text-only option and reduced-motion default. Optional motion serves pacing and remains reversible. |

The supplied [Kaggle conversational resource](https://www.kaggle.com/datasets/elvis23/mental-health-conversational-data) informed the intent/pattern/response organization and authored app-question variations. Its metadata and first greeting preview were inspected earlier; no whole-file/provenance/clinical audit, dataset training or copied reply catalog is claimed. [Dataset design notes](https://github.com/abn54/Health-App/blob/9e20276b6678ae8337cc2e64a0e9940396bb798b/docs/dataset-design-notes.md) distinguish that limited use from the instructor research table. No earlier coursework source code was supplied or reused.

## Model contribution and limits

Actual local inference uses **Ollama 0.32.5, `qwen2.5:3b` Q4_K_M**, prompt **`catalog-selector-v7`**, approved display catalog **`app-help-v1`**. [Exact digest/metadata](https://github.com/abn54/Health-App/blob/9e20276b6678ae8337cc2e64a0e9940396bb798b/docs/evidence/models-oct21.json). FastAPI supplies the current fictional question, seven concise authored app facts, topic definitions and three authored classification examples. Earlier conversation and selected cue are not sent. Saved conversation supports review, rather than expanding model authority.

The model interprets paraphrases and selects one allowlisted `reply_id`. FastAPI validates the schema, derives the catalog reference, and displays authored text as text. The model cannot write preferences, change skill/timing, prescribe advice, navigate or control storage. Invalid output, timeout or provider failure gives a fixed fallback. Schema validity does not establish semantic relevance.

The current actual three-question regression run matched **motion, storage and controls**, including the previously wrong “Can I stop halfway?” question. [Exact expected/observed results and elapsed times](https://github.com/abn54/Health-App/blob/9e20276b6678ae8337cc2e64a0e9940396bb798b/docs/evidence/live-selection-catalog-selector-v7.json). One additional authored paraphrase, “Am I allowed to quit before the last cycle?”, also selected controls ([result](https://github.com/abn54/Health-App/blob/9e20276b6678ae8337cc2e64a0e9940396bb798b/docs/evidence/live-novel-v7.json)). The browser's Live controls reply persisted and remained visible after reload ([screenshot](https://github.com/abn54/Health-App/blob/9e20276b6678ae8337cc2e64a0e9940396bb798b/docs/evidence/part32-history-reloaded-oct21.jpg)). These selected development cases informed the prompt; they are not independent accuracy estimates or a repeated variation study.

Earlier v5 selected motion for the stop question. The subsequent v6 runs with [1.5b](https://github.com/abn54/Health-App/blob/9e20276b6678ae8337cc2e64a0e9940396bb798b/docs/evidence/live-selection-catalog-selector-v6-1_5b.json) and [3b](https://github.com/abn54/Health-App/blob/9e20276b6678ae8337cc2e64a0e9940396bb798b/docs/evidence/live-selection-catalog-selector-v6-3b.json) each matched only two of three cases, including storage misses. This evidence led to balanced authored examples in v7. Failures remain recorded; changing model size alone did not establish relevance. Direct End and support do not depend on the answer.

Mocks are the UI/peer-test default. Live mode requires explicit host configuration and UI selection. SQLite atomically reserves attempts before calls; failures, explicit retries and host preloads count toward the host-controlled session limit of **at most 50**. Exhaustion returns labeled mocks, and deleting history preserves accounting. No automatic inference retry occurs. The isolated October 21 verification host recorded **13 attempts**, including two preloads and unsuccessful selections. No paid provider was used.

## Timing and persistence evidence

| Actual browser run | Exercise duration | Wall time | Explicit pause/support union excluded | Entry/setup, separately |
| --- | --- | --- | --- | --- |
| October 21 animated, six cycles | **60.013500 s** | 60.013500 s | 0 s | 0.255100 s |
| October 19 text only, support opened and resumed | **60.020400 s** | 77.620000 s | 17.599600 s | 94.876700 s |

Both are below the 90-second exercise limit. October 21 setup was an automated direct-entry action; October 19 setup included optional questions/inspection. Neither is a typical-user benchmark. No user response is required during pacing. [Current stored timing](https://github.com/abn54/Health-App/blob/9e20276b6678ae8337cc2e64a0e9940396bb798b/docs/evidence/browser-timing-oct21.json), [earlier timing](https://github.com/abn54/Health-App/blob/9e20276b6678ae8337cc2e64a0e9940396bb798b/docs/evidence/browser-timing.json), [fresh completion screenshot](https://github.com/abn54/Health-App/blob/9e20276b6678ae8337cc2e64a0e9940396bb798b/docs/evidence/part32-completed-oct21.jpg).

`performance.now()` provides one monotonic source. The first marker is immediately before the instruction DOM update; the final marker follows summary rendering and the next animation frame. Application delays are included, with approximately frame-level paint uncertainty; physical display measurement is not claimed. One paused interval avoids double subtraction when support overlaps Pause. Hidden-page/reload or scheduling interruption is not excluded as a voluntary pause and does not produce a passing completion.

SQLite migration 1 stores session snapshots/revisions, ordered events, user/assistant turns and reply provenance, one explicit cue preference, and provider-attempt accounting. Parameterized queries and foreign keys are used. Save states distinguish Saving, Saved locally and Not saved; local storage is unencrypted and restricted to fictional use. Deleting a session cascades its messages/events; deleting all additionally resets preferences, preserving the attempt budget.

The new isolated read-only inspection found **7 sessions, 4 events, 22 messages and 13 attempts**, integrity `ok` and no foreign-key violations. Reloaded History showed the completed session and actual v7 conversation. The original workspace database was not newly exported; raw SQLite files and local logs are ignored. Earlier preference/reload/override observations and mock deletion tests are linked in verification.

## Safety, leaving and failures

Crisis support is a clearly labeled sticky shell control on Ready, assistant, exercise, summary and History. Bundled region-labeled information opens without model/API/classifier permission. Actual checks stopped FastAPI, submitted an optional question, observed an unavailable/unconfirmed-save error, then opened support ([outage evidence](https://github.com/abn54/Health-App/blob/9e20276b6678ae8337cc2e64a0e9940396bb798b/docs/evidence/part32-api-offline-support-oct21.jpg)). This establishes independence after initial page load, not server-free installation or external service availability. Resource targets were inspected; no real service was contacted.

Client/server phrase matching has four bounded, normalized phrases. A match opens the same support route and bypasses inference with a fixed boundary reply. It can miss paraphrases/languages and flag quotations or negations; it is a fallible interface cue, not clinical assessment or proof of safety. No alert or human monitoring is implied. Manual support requires no match.

Actual simulated optional-model failure produced a fixed fallback while Start/support stayed available. A simulated session-save failure still allowed End, truthfully showed Not saved, and offered Retry or **Leave without saving** ([screenshot](https://github.com/abn54/Health-App/blob/9e20276b6678ae8337cc2e64a0e9940396bb798b/docs/evidence/part32-unsaved-exit-oct21.jpg)). Leave returned to Ready; a new session saved after simulation was disabled. Unsaved changes may be lost; already saved History remains. Reload recovery marks persisted running/paused records Interrupted with unknown final timing; it does not invent completion or promise unload persistence.

## Verification, generated code and remaining work

Current checks: [16 backend tests passed](https://github.com/abn54/Health-App/blob/9e20276b6678ae8337cc2e64a0e9940396bb798b/docs/evidence/backend-tests-oct21.txt), [6 client tests passed](https://github.com/abn54/Health-App/blob/9e20276b6678ae8337cc2e64a0e9940396bb798b/docs/evidence/client-tests-oct21.txt), [production build succeeded](https://github.com/abn54/Health-App/blob/9e20276b6678ae8337cc2e64a0e9940396bb798b/docs/evidence/build-oct21.txt). Backend tests use temporary SQLite and mocked providers for persistence, transitions, schema failures, phrase bypass and budget concurrency/exhaustion/deletion. Client tests use an injected clock for phase boundaries, pauses, interruptions, immediate End and fresh-session reset. A TestClient dependency warning is retained. These tests are distinct from real browser timing and live semantic results.

The generated exercise engine derives the active count from monotonic elapsed time rather than accumulating one-second timer callbacks. Modulo ten seconds selects inhale versus exhale; dividing by ten selects the cycle. Pause freezes active progress, and Resume records one excluded interval. Long scheduling gaps interrupt. This keeps application pacing independent of model latency and explains why interrupted sessions cannot be reported as completed timed runs. The new save-loop identity guard also prevents an older discarded write failure from overwriting a newer session's save state.

Part 3.2 has a working end-to-end skill, bounded actual model contribution, SQLite/history, measured duration, independent support and demonstrated failure/exit behavior. **Part 3.3 remains:** complete the fifteen-scenario evaluation and three cross-case checks; repeat relevant live cases to examine variation; verify an independent clean checkout; refine integration; provide the finished demo and failure/process screencast with the student's code explanation. Broader assistive-technology/browser testing, simultaneous-tab reconciliation and crash durability remain untested. Clinical effectiveness is not established. AI generated much of the code, tests and documentation; actual tool/model roles and failed approaches are disclosed. No student/peer understanding, feedback, recording or Canvas submission is fabricated.
