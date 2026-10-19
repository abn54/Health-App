# Requirements audit — Assignment 3

Audited October 13, 2026 against the student's newly supplied assignment text and the current project files.

**Verdict: the Part 3.1 design is documented.** The full research-source table still needs verification. The student has since supplied [Health-App](https://github.com/abn54/Health-App), and its URL is recorded in the report. A design commit and hosted supporting documents remain required: automatic approval review rejected publication because the latest request asked for one Markdown file. Parts 3.2 and 3.3 have plans only; their implementation and observed evidence do not exist in this checkout.

The Part 1 submission instructions subsequently supplied by the student confirm the selected milestone and require one uploaded `report.md`, following Section 8 of the overview. The pasted rubric rates fulfillment of the stated sub-problem; its longer description was not included. “Documented” below means a design requirement has an identifiable artifact; it does not mean the proposed behavior has been implemented or tested. No grade, clinical validity, or student understanding is inferred from these checks.

## Part 3.1 and shared requirements

| ID | Requirement | Status | Evidence or remaining action |
| --- | --- | --- | --- |
| P01 | Select one or more prescribed skills and preserve the steps. | Documented | [Design](design.md#purpose-and-scope): four counts in, six out, six cycles; alternatives and scope explained. |
| P02 | Show the main experience with a sketch or flow diagram. | Documented | [Flow and screen sketches](design.md#main-experience), including pause, completion, interruption, and support routes. |
| P03 | Explain reading, typing, and decision effort. | Documented | [Personalization and control](design.md#personalization-and-user-control): direct Start, optional questions, no required personal-context entry. |
| P04 | Connect important decisions and tradeoffs to the R/D research findings. | **Incomplete: source needed** | [Available mapping](design.md#research-connections-and-tradeoffs) uses the supplied R1 finding, D1 caveat, and narrative. Obtain the actual table, check the design against it, and map the relevant findings. The assignment does not say that every label must become a feature. |
| P05 | Explain what information the application has, its assumptions, and user correction. | Documented | [Personalization and control](design.md#personalization-and-user-control): explicit preferences and records; no inferred distress, diagnosis, or benefit. |
| P06 | Define a useful model contribution, relevant context, and limits. | Documented | [Model contract](architecture.md#model-contract): natural-language selection over approved application explanations; bounded recent context; validation and fallback limits. |
| P07 | Deliberately control the skill sequence, saved state, exits, and support access in application code. | Documented | [Architecture](architecture.md): component responsibilities and explicit transition/timing contract. |
| P08 | Propose Vue, FastAPI, and SQLite on localhost with persistent conversation/session history. | Documented | [Responsibilities](architecture.md#responsibilities), [SQLite records](architecture.md#proposed-sqlite-records), and [API surface](architecture.md#proposed-api-surface). Implementation is due later. |
| P09 | Explain saved data, visible history, personalization, and user control. | Documented | [Schema](architecture.md#proposed-sqlite-records) and [failure/deletion policy](architecture.md#persistence-failures-and-deletion); visible explicit cue choices, override, reset, and history reuse. |
| P10 | Use interaction/motion when it serves the chosen skill. | Documented | [Screen sketches](design.md#screen-sketches): animated pacing and equivalent text-only mode; accessible controls and phase announcements planned. |
| P11 | Design an intended guided sequence of no more than 90 seconds, including app delays; state response assumptions and separate setup. | Documented, unmeasured | [Timing](design.md#timing-and-interruption): calculated 60 seconds, no required responses or network waits; setup estimate labeled unmeasured; actual measurement is a later requirement. |
| P12 | Exclude only user-chosen pauses/support time from the measure and avoid forced exit. | Documented | [Timing](design.md#timing-and-interruption) distinguishes voluntary pause from automatic interruption and leaves completion open. |
| P13 | Keep clearly identified crisis-support information available independently of models/classifiers, including failures. | Documented, untested | [Support design](design.md#crisis-access-and-crisis-related-input) and [B1](evaluation-plan.md#explicit-behavior-checks); static client route, including error views. |
| P14 | Make a deliberate crisis-input decision and explain any detection limits. | Documented | [Input branch](architecture.md#crisis-related-input-branch): narrow phrase cue, false positives/misses, no risk classification, permanent manual access. |
| P15 | Record unresolved design questions. | Documented | [Open decisions](design.md#decisions-still-to-resolve): missing source, actual browser behavior, model choice, interruption timing, reuse, and submission details. |
| P16 | Maintain useful README, AGENTS.md, and design notes. | Present | [README](../README.md), [AGENTS.md](../AGENTS.md), [design](design.md), and [architecture](architecture.md). Review needs no runtime installation. |
| P17 | Describe the project accurately as coursework; no diagnosis, therapy, or implied monitoring. | Documented | Project boundary and UI copy in [README](../README.md) and [design](design.md). No application is deployed. |
| P18 | Use fictional testing only; do not offer the app as a support tool. | Documented | [Agent instructions](../AGENTS.md) and [evaluation plan](evaluation-plan.md). All application scenarios are planned, not executed. |
| P19 | Identify reuse from earlier assignments. | Documented within available evidence | [README](../README.md): architecture patterns identified; no earlier code supplied and no code reuse claimed. Inspect and name reused files if any are added later. |
| P20 | Disclose AI tools/models and their roles, identifiers where available. | Present; student review pending | [AI-USE.md](../AI-USE.md), including the requirements audit and design-review agents. Unknown exact serving-model identifiers are explicitly marked unknown. |
| P21 | Keep a curated, redacted evidence log with at least one failed or revised approach. | Present | [Evidence log](evidence-log.md): E03 revised entry design; E07 source-access correction; E08 audit corrections. No fabricated runtime failure is claimed. |
| P22 | Provide a milestone report explaining completion, evidence, and unresolved work. | Draft present | [report.md](../report.md); its content distinguishes plans from observations. |
| P23 | Include repository URL and exact submitted commit. | Repository URL filled; commit still required | The student supplied Health-App; the design has not been committed or published there. Do not use the existing README commit as if it identified this design. |
| P24 | Provide accessible links to the milestone's design and evidence. | Core content included; hosted documents still required | The report embeds the design and selected evidence. Hosted repository links cannot be supplied until the supporting documents are published. |

## Later milestone requirements

These are required by the full assignment and remain unfinished. They are not prerequisites for the design milestone, whose brief explicitly says a working application is not expected.

| Milestone | Requirement group | Current evidence and status |
| --- | --- | --- |
| 3.2 | Complete at least one skill through the running interface. | Not implemented; design only. |
| 3.2 | Demonstrate model contribution and SQLite conversation/session persistence. | Not implemented; proposed contract/schema only. |
| 3.2 | Measure exercise duration and report setup separately. | Not run; arithmetic is not browser measurement. |
| 3.2 | Demonstrate independent crisis access, failed requests, and leaving an exercise. | Not run; behavior specified and cases planned. |
| 3.2 | Use browser/database evidence across the application; explain unfinished scope. | No runtime browser/database evidence. |
| 3.2 | Submit its own report.md with repository, commit, and accessible evidence. | Not created; the root report is for Part 3.1 only. |
| 3.3 | Complete history/personalization and explain implementation-driven changes from 3.1. | Not implemented; no implementation comparison yet. |
| 3.3 | Verify clean-checkout startup using the README. | Not run; no application or startup commands yet. |
| 3.3 | Evaluate at least 15 fictional scenarios and three explicit behavior checks; record expected/observed results. | [Evaluation plan](evaluation-plan.md) exceeds the planned scenario minimum and defines three checks. All observed results remain Not run. |
| 3.3 | Use repeatable mocked checks and a repeated small selection of live cases; distinguish results. | Mock strategy and nine live attempts proposed; neither executed. |
| 3.3 | Report an observed surprise and an untested limitation. | Candidate limitations named; no observed surprise claimed. |
| 3.3 | Demonstrate the finished app and record a failure investigation, decision, and generated-code explanation. | No recordings or implementation failure evidence yet. |
| 3.3 | Default peer testing to mocks; cap live calls at no more than 50 per host session and then return to mocks. | Budget behavior designed; enforcement unimplemented. |
| 3.3 | Update documentation, AI disclosure, curated evidence, and a final milestone report with accessible links. | Design-stage documents exist; final application evidence/report remain future work. |

## Optional items correctly excluded from the required scope

- All four skills: the brief permits selecting one or more.
- Speech: optional; if added later, browser verification and a usable alternative become necessary.
- External datasets, independent clinical research, and an existing-app comparison: optional. Dataset inspection does not supply the missing instructor table.
- Character.AI registration: not required.
- A Part 3.1 working application, paid live calls, or a screencast: not required by this supplied milestone brief.

## Submission closure

1. Obtain the research table from the course material and revise the relevant mapping. The October 13 paste has the same assignment body as the earlier paste and still omits the table. Opening the course page reached school device authentication, so the table could not be retrieved in this audit.
2. Publish the design to the student-provided Health-App repository with explicit authorization, then record its actual document-snapshot commit; do not invent version identifiers.
3. Replace repository-relative links in the upload copy with absolute links at that commit. Check the instructor can open the design and evidence, including any required repository sharing.
4. Have the student review the design and disclosure and be able to explain the model/code boundary, timing calculation, personalization tradeoff, and evidence limitations. No student review or understanding is claimed by this audit.
5. Upload the finalized Part 3.1 report. No course submission has been made by the agent.

## Audit method and limits

Compared both supplied briefs, inspected the project and Git status, and used two independent document reviews to check coverage and design consistency. Corrected design inconsistencies rather than treating planned tests as results. Local Markdown links, anchors, and structure are checked after edits; these checks cannot establish runtime usability, model quality, clinical effectiveness, or reviewer access to a future hosted repository.

## Part 3.2 status

The earlier audit applies to Part 1. The current implementation scope, measured behavior, failure checks, source limitations, and remaining Part 3 work are documented in [part2-verification.md](part2-verification.md) and the root Part 2 report. Part 2 now includes working Vue/FastAPI/SQLite code and actual browser/model/database evidence; earlier statements that no runtime exists describe the archived design milestone only.
