# Current requirements audit — Part 3.2

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

## Part 3.3 work remains

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
