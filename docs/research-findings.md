# Research findings and implemented design

Source: the full Assignment 3 overview pasted by the student on **October 21, 2026**, Section 3, “Study findings and supporting evidence.” Earlier October 8/13/19 copies omitted this table. The mapping below is newly completed; it is not presented as a source available during the original Part 1 work. No Canvas dashboard/account content is copied into this repository.

The brief describes 15 patients, 13 clinicians, 15 prototype evaluation sessions, and 150 coded participant–task combinations. Mention counts describe the coded study material, not clinical effectiveness, independent sample sizes, diagnostic performance, or proof that this prototype benefits anyone. This coursework uses fictional scenarios only.

| Code | Supplied finding and observations (paraphrased) | Current design and reasoning | Tradeoff and evidence |
| --- | --- | --- | --- |
| **R1** | Longer than 90–100 seconds lost attention; about 60 was comfortable. 38 mentions. | Six 4-in/6-out cycles at one second/count; no typing, API, model, or save wait inside pacing. | A 60-second sequence gives margin below 90. Browser timing includes app/render delay, with setup separate; see [timing evidence](part2-verification.md). |
| **R2** | Crisis access should require minimal navigation. 30 mentions across all 15 participants. | One clearly labeled Crisis support button in the sticky shell opens bundled information directly. No question/classifier/API result gates it. | The app cannot connect anyone to a person; external resources still need user action. Actual loaded-page server-outage check is recorded. |
| **R3** | People need permission to stop/leave without a penalty. 39 mentions; all 15 raised it on the stop/leave task. | Immediate End, Pause/Resume, interruption recovery, neutral partial-session language, no streaks, completion rewards, or pressure to restart. A failed save offers Leave without saving. | Unsaved changes may be lost; already saved records remain in History. The actual failed-save exit returned to Ready and a subsequent session saved. SQLite distinguishes stopped/interrupted outcomes without treating them as a personal failure. |
| **R4** | The person controls the journey; options should be offered rather than imposed. 68 mentions. | Direct Start, optional assistant, explicit cue override, History reuse requiring a fresh Start, and explicit Resume after support/history. The model cannot navigate. | Three sidebar destinations add choice before practice; during pacing the main content is one instruction. Leaving a page interrupts rather than silently finishing. |
| **D1** | Reduce interface content as demands rise; the study does not explain how to detect distress or what must disappear. 54 mentions. | Start explicitly changes Ready's cards/settings into the simpler exercise view. No emotional state is inferred; the user can return, pause, or end. | This is activity-based simplification, not distress-responsive adaptation. Persistent exits/support/navigation remain; we do not claim a validated detector or exact reproduction of every contraction proposal. |
| **D2** | Present one atomic skill/action at a time. 100 mentions across all 15 participants. | One chosen skill, with only the current inhale/exhale instruction, count and cycle in the active main view. Optional questions sit outside the pacing task. | Sidebar options are retained for R4 and safety rather than adding a skill library. The instructional content is sequential; the shell is not claimed to contain literally one control. |
| **D3** | Reduce demands to disclose, feel, or perform. 148 mentions, covering every participant. | No diagnosis, distress rating, personal story, compulsory chat, written response, or outcome rating. Start is available without answering anything. | Saves less subjective information, so the app cannot infer whether a practice was useful. That limitation is intentional; only fictional interaction records are stored. |
| **D4** | Safety should remain visibly available inside the exercise. 31 mentions. | Sticky Crisis support remains on Ready, assistant, exercise, summary, History, loading and failure views; information is bundled independently of FastAPI/Ollama. | Initial page loading still needs the server. The loaded-page offline support test and screenshots establish this narrower claim; no service was contacted. |
| **D5** | Personalization should use prior activity without burdensome configuration. 49 mentions. | One default skill avoids repeated skill selection. An optional remembered cue restores a deliberate prior choice; History can copy the last recorded cue for review. Reset and per-session override remain visible. | We deliberately require one explicit Remember action rather than silently inferring preferences. This is a compromise with R4: less hidden adaptation, at the cost of one optional action. No emotional state or treatment need is inferred from history. |
| **D6** | Use restrained presentation and non-judgmental language; clinical/overly cheerful phrasing, saturation and motion can add demands. 97 mentions across all 15 participants. | Muted colors, neutral Completed/Stopped/Interrupted copy, no diagnosis or success promises, text-only pacing, and system reduced-motion default. | Motion remains available because it carries the prescribed pace; it is reversible and never changes timing. No clinical or comprehensive sensory-accessibility validation is claimed. |

## Why one coherent skill and a bounded model

A broad therapeutic conversation would add disclosure, reading, uncertainty, and variable timing. The model instead interprets app questions against approved facts; the app owns sequence, timing, preferences, persistence, exit and safety. The optional model can still select an irrelevant approved topic, so live relevance checks remain distinct from schema checks. All unsupported or invalid output stays inside documented limits.

The supplied Kaggle conversational resource informed the intent/pattern/response structure only ([actual use](dataset-design-notes.md)). It is not the research table, training data, a therapist-transcript audit, or evidence of clinical effectiveness.

## Evidence and limits

[Part 2 verification](part2-verification.md) separates actual browser/database/live-model observations from mocked/injected-clock tests. Research mapping explains decisions and compromises; it does not convert planned checks into observed results. Those were outside the dated Part 3.2 milestone. The October 30 Part 3.3 work now supplies the [evaluation](part3-evaluation.md), same-Mac clean-checkout verification, and [recordings](recordings/README.md); an independent human review is not claimed.


## October 27 refinement

[The dated refinement](ui-refinement-oct27.md) adds low-stimulus phase colors with redundant text (D6), optional FAQs/resources outside pacing (D1–D3), an explicitly opened popup with immediate exit/support (R2/R3/D4), and no click-derived mood inference. Explicit preference reuse remains the D5/R4 compromise. New source links provide limited general education, not replacement research findings or clinical validation.


## October 28 presentation revision

The new explicit local profile adds a reversible standard/brief reply choice and opt-in factual practice context. The latest saved terminal practice can supply a cue for explicit reuse; relevant assistant replies can refer to that record using reviewed local copy. This strengthens the D5 prior-activity example while preserving R4 correction/reset and D3's avoidance of required personal disclosure. No clinical/emotional persona is inferred. The single-skill, D1/D2 simplification and R2/D4 independent-support decisions remain. These are design choices, not new research findings or clinical evidence. [Actual checks and limits](presentation-readiness-oct28.md).


## October 30 final revision

[Final revisions](part3-revisions.md) revisit the one-skill/D2 scope, R1 timing, activity-based D1 simplification, D3 effort, D5/R4 explicit profile/history compromise, R2/D4 independent support and D6 silent/color/text choices. Actual keyboard and history races led to focus/escape and save-ordering changes. [Final evaluation](part3-evaluation.md) records six timing runs, 22 deterministic cases, repeated live limits and three explicit cross-case checks. Mention counts remain source observations, never clinical-effect measures.
