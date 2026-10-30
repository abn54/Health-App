# Requirements audit — Part 3.3

October 30 final status: the earlier Part 3.2/presentation audit below is retained as dated history. [Final evaluation](part3-evaluation.md), [revisions](part3-revisions.md), [recordings](recordings/README.md) and the final root report supersede its earlier future-work statements.

| Part 3.3 requirement | Actual evidence |
| --- | --- |
| Completed application, history and personalization | Fixed 4/6 skill, explicit persistent profile, cue override/reset, dated records and local context; recorded final app. |
| Revisit design choices | [Part 3.1 → 3.3 reasoning and tradeoffs](part3-revisions.md), all ten R/D codes in research mapping. |
| Fresh checkout from README | [Final clone 83ddf65](evidence/part3-final-clean-checkout-oct30.json), fresh environment/build/start/tests/assets; same Mac, not independent human review. |
| ≥15 fictional scenarios, expected/observed | [22 deterministic scenarios](evidence/part3-mocked-oct30.json), [24 browser checks plus failed/retested cases](evidence/part3-browser-checks-oct30.json). |
| Three explicit behavior checks | B1 independent support, B2 fixed skill/control, B3 explicit personalization/truthful persistence in final evaluation. |
| Mocks and repeated live selection | Zero-call 22-case runner; five live questions × three repeats; prompt/model/settings/hash and 17/50 final ledger disclosed. |
| Surprising finding and untested limit | Consistent wrong role-topic selection; real blind-user/screen-reader validation untested. |
| Finished app and process screencast | Two actual browser videos, captions/transcripts, reproduced failure, evidence, decision and generated-code explanation. Silent agent-operated recording method and idle edits disclosed. |
| AI disclosure and curated failures | Updated AI-USE and evidence log; no private third-party browser content/raw database included. |
| One submission file | Root report.md links repository, implementation commit, docs, evidence and recordings; student review and Canvas upload not performed. |

## Historical Part 3.2 audit

October 27 refinement: [phase colors, assistant popup, shared FAQs/resources and actual verification](ui-refinement-oct27.md). The original requirements and Part 3.3 boundary below remain unchanged.

Updated October 21, 2026 against the complete overview supplied that day, including its research table. The earlier October 13 design-only audit is preserved in Git history, including [the original snapshot](https://github.com/abn54/Health-App/blob/c89cef1c918eda2e570e7f800d1d8a6c641c4bd9/docs/requirements-audit.md). Its missing-source and not-implemented statuses no longer describe this checkout.

| Part 3.2 / shared requirement | Current implementation and evidence |
| --- | --- |
| Complete at least one prescribed skill | Vue 4–6 breathing, six cycles, one second/count; deterministic engine; actual browser completion in [verification](part2-verification.md). |
| Relevant model contribution | Server-grounded selection over authored app facts; schema/reference limits, explicit Mock/Live/Fixed labels; actual live evidence and failures kept separately. |
| Conversation and session persistence | FastAPI/SQLite snapshots, message turns, events and preferences; actual inspection plus repeatable temporary-database checks. |
| Useful history and explicit personalization | Outcomes, timing, conversation, initial/last cue and events; optional Remember, Reset, override and explicit cue reuse. No inferred distress. |
| Measured duration and response assumptions | Actual browser timing, app/render delay included; setup separate; no typing/response/model wait during pacing; only explicit pause/support union excluded. |
| Independent crisis route | Sticky client-shell control and bundled information; works from a loaded page with API stopped and after optional request failure. Phrase cues are fallible and never gate manual access. |
| Failed request and leaving an exercise | Fixed failure response, honest failed-save state, immediate End, reload interruption with unknown timing, and unsaved-exit choice; expected/observed evidence in verification. |
| Research grounding and tradeoffs | All R1–R4 and D1–D6 now mapped from the actual table in [research-findings.md](research-findings.md), including D1 uncertainty and the D5/R4 explicit-preference compromise. |
| Current project documentation | README, AGENTS, design/architecture, source/dataset notes and requirements checklist maintained. |
| Submission and process evidence | One root report, repository/implementation commit links, screenshots, SQL/test/live evidence, AI-USE and curated failed/revised approaches. No Canvas upload or student understanding is claimed by the assistant. |
| Responsible scope | Fictional localhost coursework, no diagnosis/therapy/improvement/monitoring claims, no service deployment or testing with a real person in distress. |

The implementation is a coherent Part 3.2 prototype, not a claim of clinical effectiveness or flawless model interpretation. Actual expected/observed outcomes and remaining limitations are retained in [verification](part2-verification.md). The final report's pinned commit identifies the submitted implementation/evidence snapshot; later report-only metadata commits do not change that code.

## Historical Part 3.3 boundary (superseded October 30)

The complete fifteen-scenario evaluation and three cross-case behavior checks, repeated relevant live cases, independent clean-checkout review, final demonstration, process screencast and student explanation belong to Part 3.3. Earlier Part 3.1 plans are not passed tests. Broader browsers/assistive technologies, multi-tab reconciliation and crash durability remain untested limits. More skills, speech, a paid provider, clinical research and Character.AI registration are not required for Part 3.2.


## October 28 presentation rubric audit

The student supplied the four 25-point criteria on October 28 and authorized both app updates and a presentation walkthrough. This is a readiness mapping, not a grade or claim the student has presented.

| Presentation criterion | Concrete demonstration now supported |
| --- | --- |
| User state and interface adaptation | Explicit cue/reduced-motion default, remembered choice and override; standard/brief answer preference; chosen activity simplifies the main view. No distress sensor/inference. |
| Skill walkthrough and research grounding | Actual full 4/6 × 6 run, separate stopped/support behavior, and complete supplied R/D mapping/tradeoffs. Walkthrough tells the presenter what to show and say. |
| Persona, interaction choices and accessibility | One persistent minimal local profile and optional factual latest-practice summary; actual reload, reset and cue reuse, history dates/messages, keyboard/phone and optional audio. Fictional Alex is a design persona, not an authenticated account/clinical profile. |
| Chatbot tone and limits | Actual profile/history-tailored approved answer, explicit source/context label, reset comparison, honest mello/therapist boundary; optional model selects topic, local reviewed renderer applies profile/history. No claim that raw history is sent to the model. |

[Presentation walkthrough](../presentation-walkthrough.md) and [dated expected/observed evidence](presentation-readiness-oct28.md). Full Part 3.3 evaluation, student delivery and recording/upload remain separate; this rubric does not supply recording submission instructions.


## Later October 28 accessibility revision

The student's new request removes app-generated breathing speech/tones and keeps optional voice only in the chatbot. Added stronger color redundancy/contrast, keyboard/landmark/focus improvements, configurable assistive text updates and visit-only larger text/higher contrast. The presentation walkthrough now describes these current choices. [Actual scans, manual findings and limits](accessibility-update-oct28.md) records zero detected violations in selected final states, not full conformance or a blind-user test. Historical voice/timing snapshots remain dated separately.
