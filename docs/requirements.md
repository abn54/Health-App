# Assignment 3 requirements

Source: the assignment overviews supplied October 8/13 and the complete October 21, 2026 overview, which adds the full R/D table and explicit milestone headings.
This document tracks the current Part 3.2 scope. Checked entries link to actual implementation/evidence; Part 3.3 work remains separate.

See the [requirements audit](requirements-audit.md) for evidence links, remaining submission gaps, and explicit later-milestone status.

## Scope and boundaries

- Individual coursework project, with three equally weighted milestones.
- Use Vue, FastAPI, and SQLite, running on localhost.
- Support at least one of the four specified skills, preserving its steps.
- Combine a conversational model with relevant context, persistent conversation and session records, and a useful saved-history view.
- Describe the application as a coursework skills prototype. Do not diagnose, claim therapy, or imply that anyone monitors the user.
- Evaluate exclusively with fictional scenarios. Do not test with a person in distress or offer the application as a support service.
- Identify components reused from earlier assignments, if any.

## Permitted skills

| Skill | Sequence to preserve | Design consideration |
| --- | --- | --- |
| Paced breathing | Inhale for four counts; exhale for six; repeat for roughly 60–90 seconds. | A clear pacing cue can carry the exercise with little reading or typing. |
| Sensory grounding | Five things seen, four felt, three heard, two smelled, one tasted. | Support the sequence without requiring unnecessary input. |
| STOP | Stop; take a step back; observe internally and externally; proceed mindfully. | Communicate the sequence clearly. |
| One-minute cognitive reframe | Identify a distressing thought; consider supporting evidence; consider an alternative interpretation. | Explain the effort and input required. |

The model must not invent therapeutic advice or alter the prescribed sequence.

## Requirements across milestones

| Area | Required outcome or evidence |
| --- | --- |
| Research grounding | Connect important design choices and tradeoffs to the supplied research findings. Mention counts and task references are not evidence of clinical effectiveness. |
| Personalization | Explain what is saved, why, how it affects the experience, and how the user can correct or override it. |
| User control | Deliberately design stopping, changing direction, saved state, and exit controls. Explain the balance between lower effort and user choice. |
| Model role | Identify the model's useful contribution, supplied context, limits, and responsibilities controlled by application code. |
| Exercise timing | Keep the intended guided sequence at or below 90 seconds, from its first instruction to its last planned step, including application delays. State assumptions about user responses. Report entry/setup time separately. Exclude user-chosen pauses and crisis-support access. Do not force completion or exit when time expires. |
| Crisis access | Clearly identify a route to crisis-support information throughout the experience. Keep it independent of model/classifier decisions and available after model-request failure. A system prompt alone is insufficient. |
| Crisis-related input | Make and document a deliberate response policy. Explain any detection logic and its limitations. |
| Persistence and history | Persist conversations and sessions in SQLite; provide a useful history review. Explain stored fields and their relationship to personalization. |
| Failure and interruption | Demonstrate failed requests and leaving an exercise. Preserve access to crisis-support information. |
| Optional speech | If included, verify input/output in the target browser and provide a usable alternative. |
| Documentation | Maintain README.md, AGENTS.md, and useful design notes. Verify clean-checkout setup before final submission. |
| AI disclosure | Include AI-USE.md in the final repository, naming tools/models, identifiers or versions where available, and their roles. |
| Evidence | Maintain a curated, redacted log linking selected prompts, changes, tests/browser observations, and decisions. Include at least one failed or revised approach. Remove credentials and private information. |

## Part 3.1 — Design

- [x] Choose the supported skill(s) and a coherent design scope.
- [x] Show the main experience with a sketch or flow diagram.
- [x] Describe model responsibilities and application-controlled behavior.
- [x] Describe proposed stored data, history, personalization, and user controls.
- [x] Explain current decisions, alternatives and research connections: [complete R/D mapping](research-findings.md), supplied October 21. The archived original report did not have this table.
- [x] Record unresolved questions.
- [x] Prepare useful README.md, AGENTS.md, and design notes.
- [x] Retain the earlier milestone report in `submissions/part1/report.md`; the current root report is for Part 3.2. Its historical source limitations are not retroactively removed.

A working application is not required at this milestone. Small experiments are optional.

## Part 3.2 — Working version

- [x] Complete at least one chosen skill through the running interface.
- [x] Demonstrate the model's contribution with relevant context.
- [x] Inspect SQLite evidence for persistent conversations and sessions.
- [x] Measure and report guided-exercise duration and entry/setup time.
- [x] Demonstrate the independent crisis-support route.
- [x] Demonstrate a failed request and leaving an exercise.
- [x] Collect browser and database evidence across the relevant application layers.
- [x] Clearly identify unfinished work.
- [x] Prepare this milestone's report.md with repository URL, submitted commit, and accessible evidence links.

Evidence: [current audit](requirements-audit.md), [verification](part2-verification.md), [research mapping](research-findings.md), and [report](../report.md). Check marks cover the stated Part 3.2 deliverables, not every possible reliability/accessibility test.

## Part 3.3 — Completion and evaluation

- [ ] Complete/refine saved-history use and personalization.
- [ ] Explain changes from the Part 3.1 design and why implementation/testing prompted them.
- [ ] Verify another person can run a clean checkout using README.md.
- [ ] Evaluate at least 15 fictional scenarios, including ordinary use, interruptions, and failures.
- [ ] Record each scenario's expected and observed result.
- [ ] Define and verify at least three explicit behavior checks that apply across cases.
- [ ] Use mocked responses for deterministic application checks and routine automated verification.
- [ ] Repeat a small relevant selection of live-model cases to examine variation; label live and mocked evidence separately.
- [ ] Report one surprising finding and one untested limitation.
- [ ] Provide a finished-application demonstration.
- [ ] Provide a process screencast showing one failure, diagnostic evidence, and the resulting decision; explain a relevant piece of generated code. One recording with marked sections or two recordings is acceptable.
- [ ] Default peer testing to mocked responses. If live calls are needed, the host sets a session cap of at most 50 model calls and returns to mocks at that cap.
- [ ] Complete AI-USE.md and the redacted evidence log.
- [ ] Prepare this milestone's report.md with repository URL, submitted commit, and accessible design, verification, and recording links.

## Research source now available

The full R1–R4 / D1–D6 table was supplied October 21, 2026. [Research findings](research-findings.md) records the actual meanings, observations, implemented decisions and tradeoffs. Earlier missing-table notices are historical. Counts describe study mentions, not clinical effectiveness. No separate clinical dataset or independent clinical research is required; Kaggle and existing-interface exploration remain optional resources.
