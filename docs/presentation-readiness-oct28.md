# Presentation readiness and profile verification — October 28, 2026

The student supplied four 25-point presentation criteria and explicitly requested both application gap fixes and a walkthrough. [presentation-walkthrough.md](../presentation-walkthrough.md) is the demonstration sequence and speaking script. This document records implementation and actual observations, not a grade or a completed presentation/recording.

## Gap addressed

Before this revision, the remembered cue and reusable history personalized the UI, but assistant responses did not actually use a saved profile or practice history. The new optional local profile persists **standard/brief reply detail** and **use saved practice context**, off by default. It is one local-host profile, shared by anyone using that server, not an authenticated identity or a clinical persona. No name, mood rating, diagnosis, biography or required check-in is collected. The fictional presenter persona Alex is a design example, not participant data.

The app uses explicit cue choices, the system reduced-motion default, chosen activity, and opted-in factual saved records. Start simplifies the main interface; a remembered cue restores; a session override does not remember itself. With context on, a latest-practice card can copy its recorded cue for review without starting or resuming. The assistant chooses reviewed standard/brief copy and can append fixed current/remembered cue and latest terminal status/cue sentences for relevant practice topics. Profile reset returns to standard/context-off independently of cue/history. Individual record deletion removes it from future summaries; Delete all resets profile/cue/history while retaining provider accounting. Old replies preserve their actual context snapshot.

Model interpretation and personalization are separate: Mock uses authored matching; Live uses local Ollama to select a catalog ID. The server applies reviewed local tailoring after selection. Raw profile/history are not sent to the model; no model output changes the skill, timing, preferences or navigation. Fixed phrase-boundary/failure responses do not acquire personalized practice claims. General-information, scope and unsupported topics do not append practice history. The UI identifies reply detail/context used.

## Expected and observed

All browser inputs below were fictional, on an isolated SQLite database separate from workspace history.

| Check | Expected | Actual observation |
| --- | --- | --- |
| Profile and cue save/reload | Explicit choices persist, saving reported truthfully | Remembered Text only; saved Brief reminders/context on; reload restored all three. No account/name/story was needed. |
| Session override and support | Override preserves the sequence, support pauses, stop stays partial | Changed active Text only to Animated circle, opened support, returned paused, then ended. Stopped record: **9.953900 s adjusted**, **10.612500 s wall**, **0.658600 s explicit support/pause**, **0.450000 s setup**. Remembered cue remained Text only. No service was contacted. |
| New factual context | Profile UI updates from real saved record; relevant reply reflects it | Most recent saved practice showed Stopped/Animated circle. Mock “Can I stop halfway?” used the brief variant plus current Animated circle, remembered Text only and stopped-practice wording. The reply said finishing was not required. |
| Reset/opt out | New answers stop using practice history; old saved replies stay unchanged | Reset profile; same fictional question returned the standard controls answer without practice context. Prior tailored reply remained a historical message. |
| Therapist boundary | Honest educational role and limits | Mock role reply stated coursework prototype, not therapist, no diagnosis/treatment/monitoring. Live relevance limitation and final boundary-copy change are below. |
| Full skill with profile enabled | Six 4-in/6-out cycles, no timing authority delegated to profile/model | Completed Text only run: **60.008600 s exercise/wall**, **0 s excluded**, **62.499700 s setup** (optional fictional question/control exploration before Start). Profile then displayed Completed/Text only. Timing includes app/render delay; setup is reported separately, not hidden. |
| Phone controls | Profile form and header remain usable | 390 × 844 viewport, document width and scroll width both 390. Save/reset, named form controls and the small header assistant remained available. No comprehensive accessibility certification is claimed. |
| History cue reuse | Copy a factual prior cue without saving/starting | Final build’s **Use last practice cue for this visit** copied Text only and explicitly reported not remembered/Start remains a choice. A reload still restored the separately remembered Text only choice. |
| API outage | Profile failure cannot claim save or disable support | Stopped isolated API; changing profile and saving reported **not confirmed saved** and offered Reload. Bundled support opened with API stopped. After restart/reload, prior saved Brief/context-on remained intact. |
| Repeatable verification | Storage, consent, context, replay, boundaries and original invariants remain checked | **33 backend tests passed**, **17 existing client tests passed**, production build succeeded, `git diff --check` clean. Existing Starlette TestClient deprecation warning remains. No new client unit tests were added for the profile UI; that behavior was checked in the browser. |

The timing/browser snapshot is [profile-browser-oct28.json](evidence/profile-browser-oct28.json). It predates the final copy/name-classification revision and records initial `catalog-selector-v8` / `app-help-v3` mock results honestly. The later copy/prompt and asynchronous-load guard refinements do not alter `engine.js`; final profile reload/reuse and live display were checked separately. No new full run after those text/load-guard refinements is claimed.

Screenshots: [saved profile](evidence/profile-saved-oct28.jpg), [phone profile](evidence/profile-phone-oct28.jpg), [initial tailored mock reply](evidence/profile-tailored-reply-oct28.jpg), [completed run](evidence/profile-completed-oct28.jpg), [failed profile save](evidence/profile-save-failure-oct28.jpg), [final tailored live reply](evidence/profile-live-final-oct28.jpg). Some screenshots show a scrolled portion of a panel; the full actual reply and metadata are in the JSON evidence.

## Actual live checks, revision and remaining relevance limit

Local **Ollama 0.32.5 / qwen2.5:3b Q4_K_M**, model digest recorded in [final live evidence](evidence/live-profile-final-oct28.json). Final prompt **catalog-selector-v10**, catalog **app-help-v4**, personalization **profile-copy-v1**. The isolated host run `presentation-2026-10-28` retained **7/50 attempts** across restarts: one counted successful preload and six validated selections. Schema success is not semantic relevance.

- Three initial v9/v3 authored questions selected scope for “What is mello?”, controls for “Can I stop halfway?”, and **unsupported** for the therapist request rather than the expected scope. The unsupported answer stayed within approved limits but was less direct. [Actual v9 evidence](evidence/live-profile-v9-oct28.json).
- Added explicit scope few-shot examples in v10. The therapist request still selected unsupported: this attempt did **not** fix classification. [Retained v10 development result](evidence/live-profile-v10-development-oct28.json).
- Revised the shared unsupported copy in **catalog v4** so both possible role/limits answers explicitly say “not a therapist” and no monitoring, diagnosis or treatment. The final live therapist request again selected unsupported; it now displayed the explicit boundary. A final controls question selected controls and displayed actual Completed/Text only context via local rules. [Exact final results/ledger](evidence/live-profile-final-oct28.json).

This is a finite development check, not independent accuracy, clinical validation or the planned repeated variation study. The correct topic is still not guaranteed. The walkthrough defaults to Mock for repeatability and explicitly explains the live selector and its limitation. Source labels never call a mock a live inference. The original host’s budget was preserved separately; workspace history was not exported. No paid provider, model training, microphone use or recording was involved.

## Decisions and limits to explain

The latest-practice lookup originally used session creation; review identified that a conversation can remain a draft for days before an exercise begins. It now orders by first exercise instruction time with a legacy creation fallback, with a regression test. Older loads cannot overwrite a newer profile save or touched draft choices. These are software correctness decisions, not clinical findings.

The authenticated overview could not be opened through the web tool. This revision uses the student’s actual pasted presentation rubric and the previously supplied full instructor R/D table in [research-findings.md](research-findings.md); it does not infer additional course rules. The selected Kaggle resource remains the limited preview/intent-organization use described in [dataset notes](dataset-design-notes.md).

The presentation script addresses all four criteria with actions and explanations. Student delivery, recording/upload, the full Part 3.3 fifteen-scenario/three-behavior evaluation, independent checkout, multi-user authentication, screen-reader certification and clinical outcomes are not claimed complete. The four presentation criteria alone do not state recording requirements.
