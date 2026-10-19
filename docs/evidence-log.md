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
