# Part 3.2 — actual verification evidence

Date: October 19, 2026. All inputs and demonstrations were fictional, performed by the coding assistant. No independent student/peer demonstration or clinical evaluation is claimed. Production Vue build served by FastAPI at `127.0.0.1:8000`; local SQLite; actual Ollama model calls distinguished below from mocks.

## Exercise timing observed in the browser

| Actual run | Measured exercise | Wall time | Explicit pause/support union excluded | Entry/setup, separate |
| --- | --- | --- | --- | --- |
| Animated, six cycles, no pause | 60.014100 s | 60.014100 s | 0 s | 88.350600 s |
| Text only, support opened and explicitly resumed | 60.020400 s | 77.620000 s | 17.599600 s | 94.876700 s |

Both complete runs were below 90 seconds at the prescribed four-in/six-out rhythm. No typing or user response is required during pacing. Setup includes the assistant's optional questions and inspection in that particular workflow; these observations are not typical-user setup benchmarks. Completion left the summary visible without forcing another action.

Clock: `performance.now()`, with `requestAnimationFrame` updates. Start is sampled immediately before the first instruction DOM update; end includes the summary DOM update and following frame. This conservatively includes initial render/application delay, with approximately frame-level paint uncertainty; it is not a physical display measurement. UTC timestamps are supplementary. Only one explicit paused interval is subtracted, including support and subsequent paused time until Resume; support does not start a second overlapping exclusion. Automatic interruptions do not create a passing completed result.

Evidence: [stored timing records](evidence/browser-timing.json), [first completion screenshot](evidence/completed-mobile.jpg), [text/support completion screenshot](evidence/completed-with-support.jpg). Later changes to model context and descriptive labels did not change the tested engine timing algorithm.

## Actual browser observations

| Fictional action / expected behavior | Observed result | Evidence |
| --- | --- | --- |
| Open Ready; start directly without questions | Six prescribed cycles completed, neutral summary, Saved locally | Timing records and completion images above |
| Choose Text only; explicitly Remember | Text cue selected; after reload, remembered Text only restored | Browser observation; `preferences` row in database inspection |
| Pause, open support, return | Cycle 1 / inhale count 1 held; Return still Paused with Resume and immediate End | Browser observations; stopped session's pause/support events in database inspection |
| Open History with active paused exercise | Banner retained Return and End; returning stayed paused | Browser observation; history_open/history_close events |
| Override active cue, Resume, End | Immediate Stopped summary; initial text / final animated recorded; remembered preference remained text | Stopped session `c6b5e6f8-e89a-4ba2-ba37-640a4ca21565` in database inspection |
| Reload during saved running exercise | History showed Interrupted; final time Not recorded, not a completion | [recovery screenshot](evidence/reload-interrupted.jpg), session `a0fff91b-62ba-4f6d-a51d-a1825362d8b3` |
| Simulate session-save failure, then End | Pacing/End worked; summary said Not saved, page memory only; Return disabled until retry | [save-failure screenshot](evidence/save-failure.jpg) |
| Disable save simulation, Retry save | Saved locally; full stopped journal persisted; Return enabled | Actual browser observation and stopped record in database inspection |
| Simulate optional request failure | Fixed fallback displayed; Start and Crisis support both enabled | [request-failure screenshot](evidence/model-failure.jpg); saved fixed reply |
| Stop FastAPI, then open support on already-loaded page | Bundled US information and link targets displayed without API | [real-outage screenshot](evidence/support-server-offline.jpg) |
| Submit fictional quoted phrase “I want to die” in Live mode | Support opened immediately; fixed phrase-cue response saved; host attempts stayed at 21 until the next ordinary live question | [phrase-cue screenshot](evidence/phrase-cue-support.jpg), matching message metadata with null attempt ID |
| Reload then review latest draft conversation | Not started; saved user questions, fixed responses, and actual live storage reply visible with v5 source metadata | [saved conversation screenshot](evidence/saved-conversation-v5.jpg) |
| Reuse completed session's cue | Ready showed copied-for-review notice and Start; no automatic start or preference write | Actual browser observation; preference remained text |
| Open support and press Escape | Dialog closed and focus returned to Crisis support | Actual browser keyboard observation; broader screen-reader evaluation remains untested |
| Inspect narrow and desktop layouts | No horizontal overflow apparent in captured full-page views; controls remained readable; sticky header added to preserve support while scrolling | [narrow Ready](evidence/ready-mobile.jpg), [desktop Ready](evidence/ready-desktop.jpg) |

The phrase rule is an interface cue, not an assessment. It deliberately also matches a quote/negation; unfamiliar wording can be missed. No match is needed to open support, and no unmatched input is labeled safe. The call, text, and chat link targets were inspected; no real crisis service was contacted. US links came from the hotline connector. The shell requires an initial page load, but the loaded support panel does not require a subsequent API/model/classifier request.

## Live model evidence — not mocked

Ollama 0.32.5; final model `qwen2.5:1.5b`, Q4_K_M. [Exact model digests/metadata](evidence/models.json). Final prompt: `catalog-selector-v5`; approved display catalog: `app-help-v1`. Current question, explicit cue, and a concise authored factual index are supplied as context. Prior messages are saved for history but are **not sent** in the final version.

| Final small live check | Expected | Observed | Result |
| --- | --- | --- | --- |
| “Do I have to watch a moving shape?” | motion | motion | Matched |
| “What stays after I close this?” | storage | storage | Matched |
| “Can I stop halfway?” | controls | motion | **Missed: valid ID, irrelevant approved answer** |

[Actual v5 request results, elapsed times, and source metadata](evidence/live-selection-catalog-selector-v5.json). The script exits **1** because one semantic result missed; this is not reported as a passing test. A subsequent browser live storage question also returned storage and remained reviewable after reload ([screenshot](evidence/saved-conversation-v5.jpg)). The final version therefore demonstrates useful grounded interpretation but not dependable topic selection. End remains a direct application control regardless of the reply.

Earlier experiments are retained: [v3 results](evidence/live-selection-v3.json) and [v4 results](evidence/live-selection-catalog-selector-v4.json). v3 reused motion for storage/controls; v4 returned start for those questions. v5 shortened repetitive context and removed prior conversation. An earlier two-field schema produced mismatched evidence references, leading to the server deriving evidence from the one selected ID. The smaller 0.5b model and cold-load failures are documented in the [evidence log](evidence-log.md). These are selected development observations, not a comprehensive model comparison or variation study.

The actual host run `part2-2026-10-19` recorded **22 provider attempts** including failed/diagnostic requests and manual empty-message preloads. No paid provider was used. Routine testing and peer defaults use mocks. SQLite reserves application attempts atomically before provider invocation; the host sets an aggregate limit no greater than 50. Preload uses the same budget, and history deletion preserves accounting. No automatic inference retries occur.

## Repeatable tests and build

- [Backend output](evidence/backend-tests.txt): **16 passed**. Temporary databases and mocked providers verify idempotent persistence, turn replay, cascade deletion, illegal transitions, immutable journals, minimum completion timing, recovery, explicit preferences, input bounds, phrase bypass, malformed/extra/mismatched output rejection, failure accounting, concurrent budget reservations, exhaustion after deletion, and preload accounting. Starlette currently emits a recorded TestClient/httpx deprecation warning; tests pass.
- [Client output](evidence/client-tests.txt): **6 passed**. Injected monotonic clock checks all 4/6 phase boundaries across six cycles, exact pause fraction, one exclusion interval, scheduling interruption including delay, immediate terminal End, and fresh-session reset; phrase normalization/bounds and false-positive limitation are also covered.
- [Production build](evidence/build.txt): completed successfully with pinned Vue/Vite dependencies.

Injected-clock tests are not the real browser timing evidence. Mocked provider tests are not live-model reliability evidence. No repeated testing beyond these checks is claimed.

## Actual database inspection

[Redacted fictional database inspection](evidence/database-inspection.json) records SQLite version, table counts, snapshots, messages, events, explicit preference, and provider attempts. At inspection: 10 sessions, 21 events, 36 messages, one preference row, 22 attempts; migration version 1. `PRAGMA integrity_check` returned `ok`; `PRAGMA foreign_key_check` returned no rows. The raw unencrypted `.sqlite3` file is ignored and not submitted. Cascade deletion was checked in the isolated test database, not by deleting the retained browser evidence records.

## Remaining work

Part 3's larger scenario matrix, repeated relevant live cases, final demonstration, process screencast, and independent clean-checkout verification remain. Also untested: simultaneous-tab recovery, multiple browsers/assistive technologies, broad performance conditions, crash/power-loss durability, and clinical outcomes (which this project does not establish). The missing instructor R/D table remains a source limitation; unavailable labels are not invented. No user/peer feedback or recording is fabricated.
