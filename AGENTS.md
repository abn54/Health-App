# Instructions for this project

## Current scope

The authorized milestone is Part 3.3: final refinement, evaluation, clean-checkout verification, and demonstration/process evidence (requested October 30, 2026). The prior Part 3.2 implementation is the baseline. Read `README.md`, `docs/design.md`, and `docs/architecture.md` before changing the design. Do not treat planned behavior or planned tests as implemented results.

## Domain boundaries

- This is a localhost coursework prototype. Use fictional inputs and demonstrations only.
- Do not diagnose, promise symptom improvement, claim therapy, or imply human monitoring.
- Do not offer or deploy the prototype as a mental health support service.
- Preserve paced breathing: inhale four counts, exhale six counts, six cycles at one second per count. The October 31 request additionally authorizes the assignment’s 5–4–3–2–1 grounding and STOP guides; keep their reviewed steps in shared/exercises.json, with one-minute intended pacing, Pause, End and independent support.
- The model may interpret questions about approved application content; it cannot change the skill, prescribe advice, set timing, write preferences, or control navigation.
- Crisis-support information must be available from the application shell independently of any API, model, or classifier. Preserve this route during loading and error states.
- Treat any phrase matching as a fallible interface cue, never a clinical assessment or proof of safety.

## Implementation conventions

- Use Vue, FastAPI, and SQLite. Bind development servers to localhost.
- Implement the exercise as an explicit client state machine with one monotonic timing source.
- Keep keys server-side. Ignore `.env` files, SQLite files, and raw local logs; provide redacted examples when needed.
- Default to mocked model responses. Require explicit live-mode configuration and enforce an aggregate host-controlled budget of at most 50 provider attempts per peer-test session, counting retries and failed calls.
- Validate model output against the approved catalog; render approved copy as text. Do not treat schema validation as semantic verification.
- Use parameterized database queries, migrations, foreign keys, and truthful save states. Model text is untrusted data.
- Keep preferences explicit and reversible. Do not infer distress, diagnoses, or treatment needs from text or usage history.
- Keep history deletion available, distinguish stopped/interrupted/completed sessions, and never invent successful persistence after a failed write.
- Prefer a small vertical slice before adding skills. Preserve keyboard access, readable labels, reduced motion, and immediate exit.

## Verification and evidence

- Treat any future evaluation plan as acceptance criteria, not as existing test coverage.
- For timing, measure the rendered first instruction through the rendered final planned step. Include app delays; report setup separately. Do not exclude automatic interruptions as if they were user-chosen pauses.
- Use mocks for repeatable tests. Label live-model evidence separately and record the model identifier, date, prompt version, and variability.
- Record actual expected and observed results. Never fabricate timings, screenshots, model calls, test passes, recordings, commits, or user feedback.
- Keep `docs/evidence-log.md`, `AI-USE.md`, and relevant documentation aligned with changes. Include revised or failed approaches with the evidence that led to the decision.
- The full R1–R4 / D1–D6 table was supplied on October 21, 2026. Use `docs/research-findings.md` for its actual labels, observations and design tradeoffs. Keep earlier missing-table notices historical; do not infer clinical effectiveness from mention counts.
- Read `docs/dataset-design-notes.md` for the actual use of the supplied Kaggle resource. Do not use it as a substitute for the instructor's research table or imply a whole-file/provenance/clinical audit from the limited preview inspection.
