# IST 402 — Assignment 3, Part 2 (3.2)

## Submitted version and evidence

**Project:** Pause, a localhost coursework skills prototype. **Milestone:** working implementation. **Date:** October 20, 2026 (sidebar update; original verification October 19).

- Repository: [abn54/Health-App](https://github.com/abn54/Health-App).
- Part 2 branch: [codex/part2-prototype](https://github.com/abn54/Health-App/tree/codex/part2-prototype).
- Submitted implementation and verification commit: [`7196b192591b18f8212c247b20d3e52826b648f5`](https://github.com/abn54/Health-App/commit/7196b192591b18f8212c247b20d3e52826b648f5). This report was finalized after freezing that code/evidence snapshot; the subsequent report-only commit does not change the implementation.
- [Run instructions](https://github.com/abn54/Health-App/blob/7196b192591b18f8212c247b20d3e52826b648f5/README.md), [design](https://github.com/abn54/Health-App/blob/7196b192591b18f8212c247b20d3e52826b648f5/docs/design.md), [architecture and implementation revisions](https://github.com/abn54/Health-App/blob/7196b192591b18f8212c247b20d3e52826b648f5/docs/architecture.md).
- [Actual verification results and screenshots](https://github.com/abn54/Health-App/blob/7196b192591b18f8212c247b20d3e52826b648f5/docs/part2-verification.md), [database inspection](https://github.com/abn54/Health-App/blob/7196b192591b18f8212c247b20d3e52826b648f5/docs/evidence/database-inspection.json), [curated development evidence](https://github.com/abn54/Health-App/blob/7196b192591b18f8212c247b20d3e52826b648f5/docs/evidence-log.md).
- [AI-use disclosure](https://github.com/abn54/Health-App/blob/7196b192591b18f8212c247b20d3e52826b648f5/AI-USE.md), [coding-agent instructions](https://github.com/abn54/Health-App/blob/7196b192591b18f8212c247b20d3e52826b648f5/AGENTS.md).

Upload **this one `report.md`** for Part 2. The supporting code, documentation, and evidence are linked in the repository. The supplied brief places the finished demonstration and process screencast in Part 3; no recording is claimed for this milestone.

## What is implemented

Vue presents one prescribed skill: **six cycles of inhale four counts and exhale six counts, at one second per count**. FastAPI serves the production UI and API on `127.0.0.1:8000`; SQLite stores fictional conversations, session outcomes/events, timing, and an explicit optional cue preference. No other skill, speech input, or therapeutic chatbot is included.

The left sidebar includes **AI assistant**, which opens the existing question panel directly with the current conversation and reply-mode selector. The Practice disclosure remains available. Opening the assistant during an exercise pauses it, retains Return/End and Crisis support, and leaves new questions disabled until the exercise ends. Ready offers a direct Start action and a choice of Animated circle or Text only. During the exercise, the circle expands over four seconds and contracts over six; the words/count remain the pacing cue. Pause preserves the phase and fractional count, Resume is explicit, and End immediately produces a partial-session summary. Completion leaves the summary visible without forcing another action. Opening History or Crisis support pauses; returning does not resume automatically. Hiding/leaving the page or a scheduling gap over two seconds interrupts rather than falsely completing the sequence.

History shows Completed, Stopped, Interrupted, or Not started; initial/final or last recorded cue; available timing; events; and saved conversation with Mock, Live local model, or Fixed response metadata. Draft questions can be reopened. Reusing a recorded cue copies it into Ready without starting or remembering it. Per-session deletion cascades to messages/events; Delete all additionally resets the preference after confirmation. Save failures remain visibly unsaved in page memory, with Retry; closing may lose them.

The prototype consistently identifies itself as fictional coursework. It does not diagnose, provide therapy, promise symptom improvement, or imply human monitoring. It is not deployed or offered as a mental health support service.

## Model contribution and relevant context

Actual local Ollama 0.32.5 calls use **`qwen2.5:1.5b`**, with exact digest in the [model metadata](https://github.com/abn54/Health-App/blob/7196b192591b18f8212c247b20d3e52826b648f5/docs/evidence/models.json). Mock remains the default. Live mode requires explicit host configuration and then an explicit UI choice; no paid key is needed.

The final prompt, `catalog-selector-v5`, supplies the current question (at most 500 characters), chosen cue, and seven concise approved app facts. The model interprets natural language and returns one allowlisted `reply_id`. FastAPI validates the exact schema, derives the matching catalog reference, and displays only the authored `app-help-v1` response as text. The model cannot change timing, steps, navigation, preferences, or database state. Unsupported or invalid output and provider failure produce fixed responses. A late response cannot overlay an active exercise.

The [actual three-case live check](https://github.com/abn54/Health-App/blob/7196b192591b18f8212c247b20d3e52826b648f5/docs/evidence/live-selection-catalog-selector-v5.json) selected motion for “Do I have to watch a moving shape?” and storage for “What stays after I close this?” correctly. It incorrectly selected motion for “Can I stop halfway?” The latter was valid schema but irrelevant content. The check therefore exits 1 and is **not reported as a pass**. A subsequent browser storage question returned the correct approved reply, which remained visible in History after reload. This establishes a concrete model contribution, with a known relevance limitation; it does not establish reliable interpretation or clinical safety.

Earlier attempts asked the model for both a reply ID and an evidence ID; a real response paired motion with the storage reference. The server now derives that redundant reference. Including recent messages also led to irrelevant repeated topics. The final version retains conversations for review but omits them from the model context and uses a shorter factual index. That reduces context/confusion and data sent, at the cost of weaker ambiguous follow-up handling. Earlier failed results remain in the evidence.

The host recorded **22 provider attempts**, including failures, diagnostic calls, and empty-message preloads. Application/preload reservations use the same persistent, server-owned SQLite budget, capped at 50 per host peer-test session. Retries/failures count; there are no automatic inference retries; exhaustion switches to labeled mocks. History deletion does not reset accounting. A cold-load failure led to a separate counted host preload outside exercise timing.

## Measured timing and persistence

These are actual production-build browser observations, distinct from injected-clock tests:

| Completed run | Exercise duration | Raw wall time | Explicit pause/support excluded once | Entry/setup separately |
| --- | --- | --- | --- | --- |
| Animated, uninterrupted | **60.014100 s** | 60.014100 s | 0 s | 88.350600 s |
| Text only, support access and explicit Resume | **60.020400 s** | 77.620000 s | 17.599600 s | 94.876700 s |

[Timing records](https://github.com/abn54/Health-App/blob/7196b192591b18f8212c247b20d3e52826b648f5/docs/evidence/browser-timing.json) and [completion screenshot](https://github.com/abn54/Health-App/blob/7196b192591b18f8212c247b20d3e52826b648f5/docs/evidence/completed-with-support.jpg) support these results. Both exercises were below 90 seconds. No typing/response is needed during pacing. Setup includes optional questions and the assistant's inspection in those workflows, so it is not a typical-user benchmark.

The timer samples `performance.now()` immediately before the first instruction DOM update and includes the final summary DOM update/following animation frame. This conservatively includes render/application delay, with frame-level paint uncertainty. UTC timestamps are supplementary. Only explicit paused time, including support, is excluded once; interrupted sessions are not completion evidence.

Actual SQL inspection found 10 sessions, 21 events, 36 messages, one preference row, and 22 attempts. Integrity check returned `ok`; foreign-key check returned no rows. Parameterized queries, migration version 1, idempotent revisions/turns, validated transitions, and append-only event prefixes support consistency. The raw SQLite file is ignored; only fictional redacted inspection output is committed. Cascade deletion and concurrency are verified in isolated test databases.

## Crisis access, failures, and leaving

A clearly labeled sticky **Crisis support** control opens bundled, region-labeled information from every view. It has no API/model/classifier prerequisite after the initial page load. During a real FastAPI outage, the loaded page still opened the information and its verified link targets. No service was contacted. The support dialog retains immediate End for an active exercise and restores focus when closed.

A small Unicode/case/whitespace-normalized bounded phrase list is checked in the client and again by FastAPI. A fictional quoted phrase opened support immediately and bypassed the model. Quotes/negations may also match; unfamiliar language may be missed. This is a fallible interface cue, not a clinical assessment, and unmatched text is never called safe. Manual access is always available.

Browser evidence shows a fixed fallback after a simulated optional-request failure, with Start and support still enabled. Simulated save failure displayed Not saved; disabling the simulation and retrying persisted the retained stopped-session journal. End worked immediately. Reload during a saved running exercise produced Interrupted with unknown final timing in History, rather than inventing a completed session or an unload save.

## Verification, design reasoning, and limits

[Repeatable backend checks](https://github.com/abn54/Health-App/blob/7196b192591b18f8212c247b20d3e52826b648f5/docs/evidence/backend-tests.txt): **16 passed**, using temporary databases/mocked providers. [Client checks](https://github.com/abn54/Health-App/blob/7196b192591b18f8212c247b20d3e52826b648f5/docs/evidence/client-tests.txt): **6 passed**, using an injected clock. [Production build](https://github.com/abn54/Health-App/blob/7196b192591b18f8212c247b20d3e52826b648f5/docs/evidence/build.txt): successful. A Starlette TestClient/httpx deprecation warning is recorded. Mocked tests establish deterministic application behavior; they do not establish live-model relevance. Browser screenshots cover narrow and desktop layouts; comprehensive assistive-technology testing is not claimed. The October 20 sidebar update was checked with a fresh production build and browser navigation/mock-answer checks, including the 390-pixel layout; the October 19 timing/unit results remain historical evidence for the unchanged timer/backend.

R1's attention finding supports a 60-second, no-typing sequence, with setup reported separately and no model wait inside the exercise. The brief's personalization/control/effort discussion supports separate Remember and Reset actions: an explicit preference saves repetition, while avoiding automatic adaptation preserves choice at the cost of an extra deliberate action. A text cue reduces motion without altering the prescribed skill. D1's stated limitation supports keeping crisis access independent of detection. The full R1–R4 / D1–D6 table was missing from the supplied briefs; unavailable label meanings are not invented.

The supplied [Kaggle Mental Health Conversational Data resource](https://www.kaggle.com/datasets/elvis23/mental-health-conversational-data) was used as an interaction-design reference. Its inspected intent/pattern/response structure informed authored motion/storage/controls variations, the mock groups, and the model's approved-catalog selection. [Dataset notes](https://github.com/abn54/Health-App/blob/7196b192591b18f8212c247b20d3e52826b648f5/docs/dataset-design-notes.md) distinguish the limited preview inspection from any whole-file, provenance, training, or clinical audit. It does not replace the instructor's research table. No earlier travel/hotel application source code was supplied or reused.

One generated-code decision is the monotonic timer: elapsed time is accumulated active time plus `now - anchor`, rather than incrementing a counter on each callback. Pause retains that exact accumulated fraction; Resume creates a new anchor. A fresh Start resets timing fields. This prevents callback drift and cross-session carryover. A gap over two seconds interrupts rather than skipping unseen steps. Separately, an atomic `BEGIN IMMEDIATE` reservation serializes provider-budget claims before concurrent requests can call the model. These choices and the observed recovery-method, retained-timer, cold-load, and model-context failures are explained in the evidence log.

Part 2's working prototype and evidence are complete within this scope. Remaining work includes improving model topic relevance, Part 3's broader evaluation/repeated live cases, independent clean-checkout verification, final demonstration/process screencast, multi-tab reconciliation, and broader browser/accessibility testing. No peer feedback, recording, clinical outcome, or unperformed test is claimed. The AI disclosure identifies the assistant's implementation/testing/documentation role and model identifiers; independent student review and understanding have not yet been recorded.
