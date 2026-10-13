# Health-App — Pause coursework design

**Current milestone: Part 3.1, design, flow, and project documentation.** The proposed application will use Vue, FastAPI, and SQLite on localhost. This repository contains the design milestone; no application runtime is included.

Repository: [abn54/Health-App](https://github.com/abn54/Health-App).

## Review Part 1

Start with [report.md](report.md), the single file to upload to Canvas. It includes the chosen skill, flow, UI sketches, model role, data/history/personalization design, research reasoning, and AI-use disclosure. Its submitted design commit identifies the supporting-document snapshot.

| File | Purpose |
| --- | --- |
| [report.md](report.md) | Single Part 1 upload |
| [AGENTS.md](AGENTS.md) | Boundaries and instructions for future coding-agent work |
| [AI-USE.md](AI-USE.md) | Tools, available model identifiers, and roles |
| [docs/design.md](docs/design.md) | Detailed flow, sketches, timing, tradeoffs, and open questions |
| [docs/architecture.md](docs/architecture.md) | Proposed model contract, state ownership, API, and SQLite records |
| [docs/dataset-design-notes.md](docs/dataset-design-notes.md) | Concrete use of the student-supplied Kaggle resource |
| [docs/sources.md](docs/sources.md) | Source provenance and inspection limits |
| [docs/evidence-log.md](docs/evidence-log.md) | Curated design decisions, revisions, and verification |

Open the files in Codex, VS Code, or another Markdown editor. A Mermaid-capable viewer renders the flow diagram; text descriptions and screen sketches are also included. No dependency installation, database, API key, or running server is needed to review Part 1.

## Design scope

Pause will present six cycles of four counts in and six counts out, for 60 seconds at one second per count. Pacing, exits, saved state, and bundled support access will be controlled by the application. An optional model will map differently phrased questions to approved application explanations.

The supplied Kaggle dataset is used as an interaction-design reference. Its inspected intent/pattern/response format informed the approved-answer structure and optional question entry. No dataset download, model training, or clinical validation is claimed. The source notes distinguish this resource from the instructor's full R/D table, which was absent from the supplied brief.

## Coursework boundaries

Use fictional scenarios only. This is a coursework prototype, not therapy, diagnosis, or a monitored service. It must not be offered or deployed as mental health support. No real person in distress participated in the design work.

No earlier travel-app or hotel-chatbot source files were supplied. The familiar course architecture patterns informed the plan; concrete code reuse is not claimed.

## Submission

Upload only the finalized report.md to Canvas. The report links to the design documents and evidence at the recorded repository commit. A working app and screen recordings belong to later milestones; the current deliverable is the documented design. Review the design and AI disclosure before uploading.
