# Curated evidence log — Part 3.1

Work dates: October 8 and October 13, 2026. E01–E07 record the October 8 work; E08 onward record the October 13 audit, submission clarification, report consolidation, and repository preparation. This log records design work, not software behavior. Prompts are paraphrased to keep the log focused; no credentials, private third-party content, personal health data, or research-participant records are included.

## E01 — Scope and repository inspection

- Input: the student supplied the complete available Assignment 3 brief, then selected “Part 3.1: design, flow, and project documentation.”
- Observation: the project directory contained an initialized Git repository with no commits, no remote, and no application files. No applicable parent `AGENTS.md` was found in the inspected ancestor paths.
- Decision: prepare a design package, not a working-application claim. Use the course's Vue/FastAPI/SQLite stack as the planned architecture.
- Result: the local requirements checklist, [README](../README.md), and [agent instructions](../AGENTS.md).

## E02 — Missing source and supplied dataset

- Input: when asked about the absent R1–R4 / D1–D6 table, the student supplied the Kaggle conversation-dataset URL.
- Observation: the brief lists that dataset as optional conversation material, separately from the research table. Opening the URL returned the titled dataset page but no readable dataset body.
- Decision: retain explicit R1/D1 references available in the brief; mark the remaining mapping pending. Do not invent dataset findings or treat the dataset as the instructor's table.
- Result: [source record](sources.md) and [research reasoning](design.md#research-connections-and-tradeoffs).

## E03 — Revised design approach

- Design alternative considered: a conversation-first entry that asks the person to explain their situation and waits for a model response before guiding the exercise.
- Evidence used in review: the brief requires low interaction effort, a measured sequence under 90 seconds, deliberately controlled skill steps, and crisis access despite model failure. A model-dependent start introduces an unnecessary input/wait requirement; a model-paced exercise would also make step timing variable.
- Revision: make Start directly available; use deterministic client pacing and optional, bounded application questions outside the guided sequence.
- Tradeoff: this is less conversational and supports fewer questions, but gives a clear independent path through the prescribed skill.
- Result: [main flow](design.md#main-experience) and [model contract](architecture.md#model-contract).
- Limit: this is a revised design approach, not an observed runtime failure. A genuine implementation failure and diagnostic screencast remain work for later milestones.

## E04 — Timing calculation

- Inputs: four counts in, six counts out, six cycles, one second per count.
- Calculation: `(4 + 6) × 6 = 60 seconds` of planned exercise time.
- Decision: no required response, model wait, or save wait inside the sequence; keep setup timing separate.
- Limit: this establishes the intended schedule only. Browser rendering, interruptions, and actual completion timing are unmeasured. See the [timing contract](architecture.md#exercise-state-and-transition-contract).

## E05 — Support-reference review

- Observation: the official 988 site lists call, text, and chat access. Find A Helpline provides country-based lookup. Their pages were opened on October 8, 2026; no service was contacted.
- Decision: specify a static panel with clearly labeled regional information, independent of the model and API. Do not infer user location or assert service availability beyond the referenced information.
- Result: [resource references and copy](sources.md#proposed-support-panel-references).

## E06 — Document verification

Ran a local document-consistency check with Python 3.14.7. Results:

```text
Markdown files checked: 10
Local links and anchors checked: 33
Planned scenarios: 19; all marked Not run
Explicit behavior checks: 3
Intended timing arithmetic: (4 + 6) x 6 = 60 seconds; not measured
Document errors: 0
```

The check resolved repository-relative links and heading anchors, checked fenced-code balance and trailing whitespace, counted the planned cases/checks, and verified the schedule arithmetic. It did not render the Mermaid diagram, run the application, inspect a database, measure exercise timing, or evaluate the model. A final editorial review retained the missing-table and missing-submission-metadata notices.

## E07 — Dataset browser inspection and source correction

- Input: the student supplied the same Kaggle link again after receiving the design draft.
- Method: after text-only retrieval again failed to expose the relevant content, opened the exact public page in the in-app browser and expanded the first intent's fields, input examples, and replies.
- Observation: the data card, file preview, and displayed license label were accessible. The reviewed sample uses an intent with grouped input patterns and replies. Inspection was limited to that sample; no dataset download or whole-file audit occurred.
- Decision: correct the earlier source-access limitation in the current source notes and AI disclosure. Use the structure as an interaction-design comparison, retain optional questions, and keep the approved application catalog independent of dataset replies. A read-only review subagent checked this fit against the existing design.
- Result: updated source notes, model-role discussion, AI disclosure, and report. The missing research-table mapping and all unexecuted application checks remain explicitly pending.

## E08 — Requirements audit and design corrections, October 13

- Input: the student supplied the assignment brief again and asked to ensure all requirements were fulfilled. The previously selected milestone was Part 3.1; the audit separately lists unfinished requirements for Parts 3.2 and 3.3.
- Source comparison: a line-by-line comparison found the assignment body unchanged; the new paste only omits the earlier opening navigation link. Both pastes lack the referenced R/D table.
- Source-access attempt: opening the supplied Canvas course link reached school device authentication, which could not be completed here. Course content was not obtained. No authentication details are retained in this log.
- Independent review: two subagents checked requirement coverage and design consistency. Git inspection found no commits or remote. Review identified missing support-view End behavior, inconsistent during-exercise cue controls, ambiguous draft recovery, an implicit timing/state contract, and overly certain save wording.
- Corrections: specified conditional support return/End, explicit monotonic timing and fractional pause progress, History navigation pause, cue-change records, preserved never-started drafts, and a catalog reply that directs users to actual save status. Updated the flow and sketches and added planned scenarios S20–S24.
- Results: the local requirements audit, revised design/architecture, evaluation plan, report, source notes, README, and AI disclosure. The audit identifies missing source/submission details rather than claiming all requirements pass.
- Verification: Python 3.14.7 checked 11 Markdown files and 72 local links/anchors, balanced code fences, trailing whitespace, the 24 unique scenarios all marked Not run, three behavior checks, and the matching report count. Zero document errors were found. External hosted access and Mermaid rendering were not verified by this check.
- Limits: this is document-based evidence. All 24 fictional application scenarios and three behavior checks remain unexecuted; no database, application, live-model result, recording, or clinical effect is claimed.

## E09 — Part 1 submission clarification, October 13

- Input: the student supplied the Part 1 submission instructions, requiring one `report.md` and referring to overview Section 8, plus the visible 100-point fulfillment rubric.
- Observation: this confirms the design milestone. The rubric's longer description was not supplied. The exact overview URL was not accessible through text-only browsing; the supplied overview remains the content source for this audit.
- Revision: explicitly identify the report as the Part 1 upload, explain the role of hosted supporting links, and use future tense for proposed application behavior. Include the actual document-verification result while keeping measured/runtime evidence unclaimed.
- Remaining requirements: the research table, repository URL, submitted commit, and access-verified hosted document links. Later implementation and recordings remain later-milestone work, not additional Part 1 prerequisites.

## E10 — Single-file report consolidation, October 13

- Input: the student asked to merge the report and design because Part 1 allows one uploaded file.
- Change: consolidated the full design, flow diagram, screen sketches, relevant architecture/data specifications, selected process evidence, and AI disclosure into `report.md`. Replaced its local-file references with internal section links so the core design can be reviewed from the uploaded Markdown file.
- Result: `report.md` is the single upload artifact. Original design files remain repository working notes. No application implementation or recording was added; existing research-source and repository/version gaps remain visible.
- Verification: the first standalone-file check found one remaining link to `design.md`; it was changed to the included flow's internal anchor. The repeat check passed: 430 report lines, 10 internal links, zero relative file dependencies, expected design/data/disclosure sections present, balanced code fences, and zero document errors. These are document checks, not runtime evidence.

## E11 — Part 1 scope cleanup and supplied repository, October 13

- Input: the student asked whether the missing information belonged to later milestones, requested only Part 1 requirements, and supplied `https://github.com/abn54/Health-App` as the intended repository.
- Observation: the repository is accessible through the GitHub connection and initially contains only a one-line README. Its existing main-branch history can be preserved while adding the design documents.
- Revision: reduced the upload report from 6,472 words to approximately 2,530 words, retaining the required design, flow/sketches, model role, data/personalization, research reasoning, selected process evidence, and AI disclosure. Removed the detailed later-milestone behavior-check table, repeated pending notices, full response catalog, and implementation-level state table from the upload; detailed working notes remain in the repository.
- Submission decision: retain the required repository/version information, use the supplied repository, and finalize immutable supporting-document links after the document snapshot commit exists. The full research table remains an explicit source limitation in the research discussion rather than an invented mapping.
- Publication scope: coursework design documents only; no application deployment, course upload, runtime evidence, or recording is claimed.

## E12 — Repository publication boundary, October 13

- Observation: the supplied repository's main branch initially contains only `README.md`, at commit `9e7a37e0a65044eb7fbac254aedbfa03c51342b5`. This commit does not contain the coursework design and must not be cited as its submitted version.
- Attempt: prepared a document tree preserving existing history and requested its creation through the GitHub connector.
- Result: automatic approval review rejected the public upload because it exceeded the student's latest request to provide only one Markdown file. No tree, document commit, or branch update was created by the agent. No workaround or alternate publication route was attempted.
- Revision: retained the verified repository URL, removed links to unpublished documents, and kept the required design-commit field explicit in the single report. The shortened report contains the necessary Part 1 design components; publication requires further authorization.

## E13 — Repository completion authorized and dataset use made explicit, October 13

- Input: after being told the repository should contain the design documents, the student affirmed that all Part 3.1 design, flow, and project documentation must be there, and reiterated the supplied Kaggle link.
- Authorization: this follows the earlier publication rejection and supplies authorization to complete the Part 1 documentation in Health-App. Only the core design/documents are selected for publication; local audit and later evaluation-plan files are excluded.
- Source check: revisited the exact Kaggle page. The preview still shows the same intent structure and greeting-entry counts. Added authored application-question variations that demonstrate how the structure informs the model's approved-answer design.
- Resulting artifacts: report, README, AGENTS.md, AI disclosure, design, architecture, dataset design notes, source notes, and this curated log. No application implementation, clinical training, course upload, or recording is claimed.
- Version plan: publish the supporting-document snapshot first, then finalize the report's design-commit field and immutable document links. The uploaded report identifies that actual snapshot; its own metadata update can be a subsequent repository commit.

## E14 — Authorized browser publication, October 13

- The renewed GitHub connector write passed approval review but returned `403 Resource not accessible by integration`. This is a connector permission limitation, separate from the earlier approval rejection.
- The student's signed-in GitHub browser showed ownership and the normal Add file / Upload files controls. Used that existing access to publish the authorized document package, without changing integration permissions.
- The root-document upload completed at commit `ee3641bef0851d2886c2eaa51db6db428f4aba7a`, preserving the initial README commit as its parent. Design-folder files and final report metadata follow in subsequent document commits.
- File selection and content checks are limited to the Part 1 package. No application deployment or Canvas submission occurs in this workflow.

## Evidence still required in later milestones

- Running-interface observations and screenshots, actual database records, and measured exercise/setup durations.
- Completed expected/observed scenario results, with mocked and live checks labeled separately.
- Model/provider identifiers and repeated live-case observations.
- A real failure investigation, a surprising finding, a generated-code explanation, and demonstration/process recordings.
- Clean-checkout startup verification, exact submission commit, hosted links, and reviewer-access checks.

## Part 3.2 — actual implementation and verification, October 19, 2026

Student prompt: “can u do part 2”, with the assignment overview supplied again. This explicitly expanded the earlier Part 1-only scope. The original report is archived in `submissions/part1/report.md`; the current `report.md` describes the implementation.

Selected changes and evidence:

| Prompt/check | Observation | Decision/change |
| --- | --- | --- |
| Build the Part 2 prototype using the approved design | Initially only design documents existed | Added Vue UI, monotonic exercise engine, FastAPI routes, SQLite migration/history/preferences, approved catalog, and local Ollama adapter |
| First actual browser startup | `GET /api/recover` returned 404; UI truthfully reported the server unavailable even though `/api/health` worked | Corrected the client to POST; reloaded and observed normal preferences/config loading |
| Inspect repeated-session timing state | Engine Start initially retained previous elapsed/pause fields | Reset those fields; added the new-session regression test; subsequent browser session started at cycle 1/count 1 |
| Initial actual Qwen2.5:0.5b selection | Debug output selected pacing with evidence `["1"]`; app rejected invalid evidence | Kept fixed fallback; tried the larger local 1.5b model and tighter schema |
| Actual 1.5b cold startup | Eight-second live-question timeout canceled loading | Added explicit host preload outside the exercise, counted in the persistent attempt budget; retained the short question timeout |
| Original two-field selection contract | A preloaded debug output selected motion with `catalog:storage` | Removed redundant model-selected evidence; server now derives the reference from the allowlisted ID |
| Context revisions v2–v4 | Valid JSON still selected irrelevant topics; the three-case v3/v4 files retain those failures | Removed prior messages from model context and shortened approved factual context; final prompt is v5 |
| Final v5 actual live run | Motion and storage correct; controls question incorrectly selected motion | Documented the remaining semantic limitation. Did not count schema acceptance as task success or claim 3/3 |
| First real browser exercise | 60,014.100 ms exercise; 88,350.600 ms setup; no excluded pause | Meets the supplied 90-second exercise requirement for this run; retain actual SQLite record and screenshot |
| Text-only browser exercise with support access | 77,620.000 ms wall − 17,599.600 ms explicit pause/support union = 60,020.400 ms; setup 94,876.700 ms | Preserve exact pause/count; Return stays paused; no double exclusion |
| Stop / reload / failure workflows | Immediate stopped summary; reload recovery interrupted with unknown final time; simulated save never claimed success; retry saved full journal | Keep explicit outcome/save states and in-page retry; do not promise unload persistence |
| FastAPI stopped in a real outage | Loaded client still opened bundled region-labeled support and its links | Confirms support does not require API/model/classifier after initial page load; no service was contacted |
| SQLite inspection | Integrity check `ok`, empty foreign-key check; sessions/events/messages persisted; 22 host provider attempts including manual diagnostic/preload calls | Commit redacted fictional inspection output, never the raw SQLite file |

Mocked/injected-clock tests and build output are retained separately from actual browser/live evidence in `docs/evidence/`. Current counts are 16 passing backend tests and 6 passing client tests. The backend emits a recorded Starlette/httpx TestClient deprecation warning. The live-check command intentionally exits 1 when a semantic case misses; its result is not an automated-test pass.

No recording, peer feedback, physical display measurement, clinical result, complete 15-scenario Part 3 evaluation, or clean-checkout exercise was fabricated. Actual browser screenshots, JSON observations, and database inspection support Part 2. Official implementation references checked: [Ollama chat API](https://docs.ollama.com/api/chat), [structured outputs](https://docs.ollama.com/capabilities/structured-outputs), [FastAPI first steps](https://fastapi.tiangolo.com/tutorial/first-steps/), and [Vite guide](https://vite.dev/guide/). Earlier missing-table/source limitations remain unchanged.

## October 20, 2026 — AI assistant in the left sidebar

Student request: “it should be added in the dropdowns on the left side.” Added a selected AI assistant navigation entry and dedicated view that automatically expands/focuses the existing question panel. It shares the current conversation, reply selector, and persistence rather than creating a second chat implementation. Preserved Practice access and the paused-exercise Return/End/support controls; new questions still require Ready. Limited history_close events to actual History exits, including switching from History to the assistant. Adjusted narrow navigation to fit three entries.

Verification: production build succeeded from `frontend`; actual browser opened the assistant from Practice and History, received correct labeled mock replies for authored motion/storage questions, paused an active exercise at inhale count 1, returned still paused, opened support, and ended the session. The 390-pixel layout reported scrollWidth = clientWidth = 390. Screenshots are linked in the verification document. No live model call, new full-duration timing run, or rerun of the historical backend/client suite is claimed for this navigation change. README, design/architecture, report, and AI disclosure were aligned.


## October 21, 2026 — new research source, model revision and unsaved exit

Student prompt: “develop 3.2,” with the complete overview. Unlike earlier copies, Section 3 now includes all ten R/D findings. Mapped the actual table in `research-findings.md`; the Kaggle preview remains a separate, limited structural inspiration. Research mention counts are not outcome measures. No private dashboard/account text is published.

| Check or revision | Actual observation | Resulting decision |
| --- | --- | --- |
| Compare new overview with current documentation | Old design-only audit still said not implemented; table was finally present | Update current requirements/audit and add complete research mapping; preserve dated historical observations |
| Inspect End after failed save against R3 | End stopped pacing, but the old summary required saving before Return | Add explicit Leave without saving and a clear data-loss notice; retain Retry and saved History |
| Actual browser save failure / End / Leave | Not saved shown; Leave returned to Ready without a server save; new session saved after disabling simulation | Keep explicit discard, session-identity guard and queue isolation; no successful save invented for abandoned record |
| v6 with 1.5b, then 3b | Each matched 2/3 regression questions; storage still received an irrelevant selection | Retain both failed result files; do not report either as semantic success |
| v7 / 3b with balanced authored examples | Motion, storage and formerly wrong “Can I stop halfway?” all matched in one run | Use v7/3b for the bounded selector; examples and tested cases are development material, not independent validation |
| Extra authored question “Am I allowed to quit before the last cycle?” | Correct controls reply, live source, 389.57 ms | Evidence of this one paraphrase only, not a variation or accuracy estimate |
| Actual browser Live stop question | Correct controls reply persisted with v7 metadata and remained visible after reload | Link screenshot plus matching SQL messages; do not count UI and API regression observations as independent samples |
| Fresh six-cycle browser run | 60,013.500 ms exercise, 255.100 ms automated setup, no excluded interval | Below 90 seconds for this run; no response needed during pacing; retain exact SQL timing and screenshot |
| Stop isolated FastAPI, submit optional question, open support | Request reported unavailable/unconfirmed save; bundled support opened without API | Preserve independent shell route; no real service contacted; failed turn absent from saved History after reload |
| Read-only isolated SQLite inspection | 7 sessions, 4 events, 22 messages, 13 attempts; integrity ok; no FK violations | Publish only fictional curated inspection, not raw SQLite or original workspace data |
| Current repeatable checks | 16 backend tests and 6 client tests passed; production build succeeded | Preserve output, including the existing TestClient deprecation warning; separate from live relevance and real timing |

The isolated host uses run ID `part2-2026-10-21` and its own ignored verification database. Its 13 attempts include failures and two preloads. The original port-8000 app was restarted with the new model/prompt while keeping its original database and host run ledger (23 attempts at restart); no budget was reset. Both hosts remain loopback and enforce their host-session cap of 50. The temporary verification host is stopped after checks.

The prior section “Evidence still required in later milestones” describes the historical Part 1 state; working-interface, SQL and model evidence now exist. Part 3's complete 15-scenario evaluation, three cross-case checks, repeated live variation, independent clean-checkout verification, final demo, process screencast and student explanation remain outstanding. No recording, independent student feedback or clinical benefit is fabricated.


## October 27, 2026 — requested colors, assistant popup and FAQs

User request: phase color coding, an assistant popup, more visuals/questions/FAQs, handbook references, and connection to the pasted ideation discussion. The assignment and project prohibit therapy/diagnosis claims, so the assistant role remains educational; the linked pages' access and evidence limits are explicit. No book file has been supplied.

| Evidence | Decision/result |
| --- | --- |
| Public-page review found a resource page, a publisher listing and a diagnostic-reference overview | Add source-typed optional reading cards; do not treat these as therapy handbooks or import diagnostic criteria. Add a short sourced NIMH general definition only. |
| Student discussion notes concern privacy/questionnaire effort/click inference | Preserve direct entry, reversible cue preferences, no click-based stress inference; explain these choices in FAQs. Original cited papers remain unverified. |
| First visual version added vertical content before Start | Move Start above decorative preview; observed visible at desktop 1280×720. |
| First colored exercise put End below the desktop viewport | Reduce decorative circle/space size; final End bounds y=615.5–659.5 within 720px. Engine unchanged. |
| Initial popup scrolled its whole surface | Keep header/Close/support fixed; scroll the question area separately, collapse suggestions after a message. Mobile document width matched 390px; support/Close stayed in bounds. |
| Actual popup/support/keyboard workflow | Opening during practice paused at inhale count 1; questions disabled; support returned to popup; close stayed paused; explicit Resume and End saved partial session. Shift+Tab wrapped; Escape restored launcher focus. |
| Actual API shutdown while popup loaded | Question error reported unconfirmed save; bundled support opened; saved earlier reply remained after restart/reload and failed turn was absent. |
| Fresh browser six-cycle run | 60,016.600 ms exercise/wall, 0 excluded, setup 18,153.200 ms; exact SQL and screenshots retained. Later CSS spacing changes do not alter timing code. |
| v8 actual local-model checks | Original motion/storage/controls plus five new topic questions matched once each; eight questions and one preload counted in isolated host ledger. Not a repeated variation or held-out accuracy study. |
| Current verification | 21 backend and 6 client tests passed; build succeeded; separate fictional SQL integrity ok/no FK violations. |

[Detailed expected/observed results and links](ui-refinement-oct27.md). No real distressed person, crisis service contact, clinical benefit, handbook audit, independent student test or Part 3.3 recording is claimed. Earlier failed/revised approaches remain in their dated sections.


## October 27 — new UI, layout and colors

User requested a visual redesign after discussing possible names. Kept Pause as the unconfirmed working name. Replaced the dark sidebar with sticky top navigation, moved existing independent support into it, used ivory/terracotta/lavender, changed system typography, and authored static SVG flower/landscape artwork. Active pacing/controller/model/storage behavior remains unchanged.

First browser review found excessive empty space from narrow side-by-side cards and a small navigation overflow in the intermediate pane. Stacked the medium-width layout and reduced top-nav spacing. Actual phone width was 390/390; tested active End/support positions and popup pause/support/return/End with saved Stopped status. Existing six client tests/build passed. An attempted isolated full-duration run lost its browser tab; retained the Running/no-final-time observation and recovery to Interrupted as a failure to obtain completion evidence. Earlier timed results are not relabeled as new. No model call, clinical evaluation or recording occurred. [Detailed observations and screenshots](visual-redesign.md).

## October 27 — optional voice and sound

Requested assistant speech plus inhale/exhale voice/sounds. Implemented on-device English speech with explicit defaults/controls, optional half-second soft phase tones, independent timer, stale-playback cancellation and page-memory settings. Initial native Preview failed because timer functions were assigned as controller methods; browser inspection exposed `Illegal invocation`, resolved with wrapper functions. Fake tests had passed, so they were not treated as browser evidence. Preview labels were subsequently clarified to distinguish them from assistant reading. A selected-field SQL read first assumed columns that this snapshot-based schema does not have; corrected extraction reads the JSON snapshot and exports only the new fictional timing record.

Observed: corrected preview start/finish; confirmed mock assistant auto/manual read; Stop and support cancel; a complete spoken sequence with six Inhale and six Exhale starts and 60.016200 s measured duration, 0 excluded and 0.500500 s setup; soft-tone Inhale/Exhale, Pause/Resume/End; phone-width controls with no horizontal overflow; audio off after reload. 17 client tests, 21 backend tests/build passed. No new provider call, audio recording, participant feedback or clinical effect is claimed. [Exact results, evidence links and limits](voice-output.md).

## October 27 — mello and conversation dates

Implemented the selected mello name, Started/Last chatted history dates, per-message local timestamps and recent-conversation sorting. Dates come from saved user-message timestamps; no-chat sessions stay explicit, and save/reply activity does not fabricate a chat date. Review caught the read-only `last_chat_at` needing exclusion from a reopened draft's PUT snapshot; the actual saved-draft continuation then worked. First small fixed circle still overlapped a phone value, so the final 46/44 px control moved into the sticky header. Actual 390/667 px browser checks and isolated fictional conversation evidence are in [mello-history-update.md](mello-history-update.md). 22 backend tests passed; original 17 client tests/build passed. Historical evidence remains historical, with no new live inference/timing/recording claim.

## October 28 — presentation readiness

The four-part rubric exposed a real gap: remembered cues/history existed, but chatbot replies did not use them. Added explicit standard/brief reply detail and opt-in factual saved-practice context, separate cue/profile reset, visible history-based cue reuse and reviewed local rendering. No clinical/emotional persona is inferred. Review caught latest-practice ordering needing exercise-start time rather than old draft creation, plus asynchronous profile-load guards; both were revised before finalization.

Actual isolated browser checks covered profile save/reload, per-session cue override, support-return paused, partial stop, mock tailored answer/reset comparison, phone controls and a 60.008600-second completed run. Profile-save outage remained truthful and support available. 33 backend tests, 17 original client tests/build passed. Live v9 selected the less direct unsupported topic for a therapist request; v10's added example did not correct it. The final v4 catalog makes both role/limits answers explicitly say not a therapist; topic relevance remains limited. Seven host-counted attempts (one preload, six selections) stayed under 50 across restarts. [Exact evidence and limits](presentation-readiness-oct28.md). The walkthrough is prepared; no presentation/recording/upload or full Part 3.3 evaluation is claimed.

## Later October 28 — accessibility and chatbot-only voice

Removed all app-generated breathing audio and its controls. Added chatbot-only labeled blue/red playback controls, curated local voices/speed, skip/navigation/focus improvements, explicit assistive announcement text, higher contrast/larger text and narrow stacking. Initial axe scans found real contrast, landmark and invalid decorative-ARIA problems; they were fixed and initial JSON retained. A narrow larger-text layout still overlapped labels despite zero detected violations, so manual inspection led to stacking. The first large dev audit panel covered a test input; the harness was reduced and production did not contain it. An interruption stopped local servers; they were restored without inventing observations.

Eight recorded final-state scans have zero detected violations but retain incomplete/manual checks. Selected text contrast was also calculated. Actual keyboard actions, 320/390 px checks, chatbot speech/Stop and duplicate-announcement suppression were observed; no acoustic or real screen-reader/blind-user certification is claimed. The final silent production run measured 60.015400 s, zero excluded and 0.340300 s setup. 17 client + 33 backend tests/build passed. [Evidence and explicit limits](accessibility-update-oct28.md). No new live inference, recording, paid provider or clinical result was involved.


## October 28 — localhost connection recovery

The student reported the frontend did not work. Actual initial HTTP request failed with connection refused; no process listened on 8000 or 11434. The browser's existing tab also showed connection refused. The prior process termination's cause is unknown; no frontend code defect was inferred. Restarted the existing built app and optional Ollama service as detached localhost processes, retaining the existing database, host test-run ID and budget (1/50). No inference/preload requested. Root HTML, both referenced built JS/CSS assets and health endpoint returned HTTP 200. A fresh browser tab rendered mello, Accessibility options expanded/collapsed, and the browser error log returned no entries. The existing error tab could not be bound through browser tooling because its generated data URL was blocked, so a fresh localhost tab was used. [Actual restored page](evidence/localhost-restored-oct28.jpg). Runtime logs remain ignored locally; no original history/conversations exported. README now explains restarting an already-built app and keeping the server running. This was runtime recovery, with no new exercise timing, model evaluation or unit-test result claimed.


## Later October 28 — bottom-right assistant composer

Moved the launcher to a reserved bottom-right rail and added the requested rounded composer with optional reply voice. Initial popup details markup generated an unwanted summary and hid the composer; a popup div/flex container corrected it. The first CSS append used the wrong working directory and was corrected before final build. Axe found a real character-help contrast issue (3.61:1 from older CSS specificity), corrected with a more specific rule. Four selected final scans detected zero violations with incomplete checks retained. Actual mocked Enter/Shift+Enter/Send, auto-read/Stop, keyboard wrapping/Escape, phone large-text geometry, support and partial exercise End were checked. 17 existing client tests and build passed. No new backend test, full-duration run, inference, recording or screen-reader certification is claimed. A later phone screenshot resize was inconsistent and discarded; earlier measured phone reflow is retained. [Evidence](composer-update-oct28.md).


## Late October 28 — simpler, accurate chat wording

The student requested removing repeated fictional/therapist wording and making the experience seem real even when it is not. Reduced repeated labels and technical clutter, retained a short truthful coursework/demo notice, prepared/live source explanation and explicit scope answers for direct clinical-role questions. Added the approved about topic. Actual isolated browser purpose and therapist turns matched their reviewed topics, with zero provider attempts. Initial backend run: 38 passed/one existing date-dependent ordering test failed; fixed both test timestamps rather than product ordering, then all 39 backend tests passed. 17 client tests/build passed. No new live relevance/timing/recording/accessibility claim. [Details](chat-copy-oct28.md).


## October 30 — Part 3.3 final evaluation and refinements

- Request: “3.3 now,” with the complete supplied overview. Read current project/research/dataset notes and retained Part 3.2 report in submissions/part2/latest-report.md. No agents or real distressed participants were used.
- Repeatable actual checks: 39 backend + 17 client tests, production build, 22 new in-process HTTP scenarios with zero real provider calls. Expected/observed JSON distinguishes synthetic timing and stub-backed “live” source fields from real inference.
- Browser: six full runs, 3 per cue (60.0082–60.0254 seconds, setup separate); seventh final recorded run 60.0136 seconds. Pause/support/history/End/reload and actual API outage retained honest partial/unknown/Not saved states; explicit retry confirmed save after restart.
- Failed approach U11: stopping reply speech removed its focus target; BODY focus meant popup-local Escape missed the event. An attempted profile reset behind the still-inert popup never reached SQLite. The fix uses nextTick focus restoration and capture Escape; actual retest closed to launcher. The process recording reproduces the before/fix and explains generated code.
- Revised approach U15: History read could beat pause save, producing an In progress list row beside Paused banner. Navigation stays immediate; list GET awaits the active journal. Actual retest showed Paused; failed saves still permit older records and support.
- Live variation: qwen2.5:3b / Ollama 0.32.5, selector-v11/catalog-v5, 5 fictional questions × 3 = 15 selections. No within-group topic variation; scope question consistently unsupported (0/3 relevance), other expectations 12/12. Valid schema/consistency are not semantic verification. No prompt revision hides the failure. One preload and one recorded demo selection bring the same ledger to 17/50.
- Clean checkout: baseline49ea522 preceded UI fixes; final GitHub clone83ddf65 installed/built/ran from README, page/assets200, 39+17 tests and22 scenarios passed, clean Git status. One evaluation harness invocation first omitted --output; corrected without product change. Same Mac/agent, not independent human/cross-OS review.
- Recording: native capture attempt yielded no verified output, so actual task-tab screenshots were captured at about2fps and encoded with original timing, disclosed idle cuts outside exercise, soft captions and transcripts. Full decode verification/sample inspection passed. No third-party private browser content or raw database was exported. Silent, AI-operated videos do not assert student delivery/understanding.
- [Full actual evaluation](part3-evaluation.md), [revisions](part3-revisions.md), [recordings](recordings/README.md). No clinical effectiveness, blind-user validation, Canvas upload or deployment is claimed.
