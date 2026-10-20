# AI-use disclosure

Historical Part 3.1 disclosure: work dates October 8 and October 13, 2026. The current Part 3.2 disclosure follows below.

This is an AI-assisted design draft prepared in response to the student's supplied assignment brief and their selection of the Part 3.1 deliverable. Student review and adoption of the design have not yet been recorded. The student should revise this disclosure if additional tools, models, source material, or personal work contribute before submission.

| Tool or model | Identifier available in this session | Role |
| --- | --- | --- |
| OpenAI Codex assistant in the desktop app | GPT-6-based Codex agent; exact serving model identifier/build was not exposed | Extracted requirements; proposed the scope, flow, architecture, model limits, data model, and evaluation plan; drafted documentation and consolidated the report and design into one Markdown upload. |
| Web browsing tool | `web.run`; version not exposed | Opened the supplied Kaggle page and official support-resource pages. Initial text-only Kaggle retrieval did not expose the dataset body. |
| Browser automation | `cua_repl`, Codex in-app browser; versions not exposed | Inspected Kaggle's public preview and used the student's signed-in GitHub browser session to publish the authorized Part 1 documents. Attempted course-source retrieval required school device authentication. |
| Codex review subagents | Inherited parent model; exact identifiers not exposed | One read-only dataset-fit review on October 8; independent requirements and design-consistency reviews on October 13. The design reviewer also revised the flow/state/timing and save-status specifications. |
| Local command and file-editing tools | `exec_command`, `apply_patch`; versions not exposed | Inspected the empty repository, wrote documentation, and checked local file/link consistency. |
| Python | Interpreter version recorded in the evidence log | Combined existing Markdown content and performed document consistency checks; did not run application or clinical tests. |
| GitHub connector | GitHub plugin profile, repository/file reads, and Git-data tools; versions not exposed | Read repository and commit metadata for verification. The later authorized write attempt returned an integration-permission error; publication used the signed-in browser instead. Earlier approval history is recorded in the evidence log. |

No application model has been selected or called. No application source code, trained model, live conversation evaluation, browser exercise test, or database implementation is included in this milestone. The model prompt in the architecture document is a proposed contract, not an executed experiment.

The dataset's public metadata and first greeting item were inspected and rechecked on October 13. The review informed the approved-answer design, direct exercise entry, and authored motion/storage/control input variations in `docs/dataset-design-notes.md`. No dataset file was downloaded, no response text was imported into the catalog, and no records were used as training data. No real person in distress participated, and no crisis service was contacted. All evaluation inputs were written as fictional cases.

See the [curated evidence log](docs/evidence-log.md) for the selected prompts, resulting artifacts, revised design approach, and verification limits. A full chat export is not included. No earlier coursework code was available to inspect or reuse.

## Part 3.2 — October 19, 2026

The earlier disclosure describes Part 1 only. Part 2 was requested explicitly by the student and includes AI-generated application code, tests, documentation, and browser verification. The Codex assistant selected the implementation structure, authored and revised the Vue/FastAPI/SQLite code, ran the checks, inspected the resulting records, and prepared the report. Student review or an independent student demonstration has not been recorded; the student should understand and adopt the work before submission.

| Tool/model | Actual identifier | Part 2 role |
| --- | --- | --- |
| Codex desktop assistant | GPT-6-based agent; exact serving build not exposed | Implementation, debugging, UI design, verification, report and disclosure |
| Vue / Vite | 3.5.44 / 8.3.4; plugin-vue 6.0.10 | Running UI and production build |
| Python / FastAPI / SQLite | Python 3.14.7; FastAPI 0.149.0; SQLite version in database evidence | API, parameterized persistence, migration, live adapter, tests |
| Node / npm | 26.7.0 / 11.19.0 | Dependency lock, build, deterministic timing tests |
| Ollama | 0.32.5 | Local model runtime on loopback |
| Qwen2.5 | `qwen2.5:0.5b`, digest `a8b0c51577010a279d933d14c2a8ab4b268079d44c5c8830c0a93900f1827c67` | Initial actual selector experiment; invalid evidence output rejected |
| Qwen2.5 | `qwen2.5:1.5b`, full digest in model evidence | Actual application-help selection; cold-load failure and semantic selection failure informed revisions |
| Browser automation | `cua_repl`, Codex in-app browser; browser build not exposed | Actual interface interactions, real duration, source-labeled replies, failure checks, screenshots |
| Official web documentation | Ollama chat API and structured outputs; FastAPI first steps; Vite guide | Checked provider request/schema and application setup contracts |
| Local tools / Git | Python, shell, apply_patch, Git | File edits, test execution, redacted evidence extraction, repository versioning |
| Hotline connector | `hotline_get_local_hotline`; version not exposed | Verified US resource links bundled in the shell; no call, text, or service chat initiated |

No subagents were used for Part 2. The Part 1 subagent work remains disclosed above. All test inputs are fictional. No real person in distress, research participant data, paid API, uploaded therapy dataset, or model training was used. The Kaggle resource's actual limited-preview adaptation is documented separately. Mock tests and live-model evidence are distinguished. Generated code is explained in the Part 2 report; observed failures and revised approaches remain in the evidence log.

## October 20, 2026 — sidebar navigation refinement

The same Codex assistant added the requested left-sidebar AI assistant entry and shared question view, adjusted narrow navigation, updated documentation/report links, built Vue, and checked actual browser navigation with fictional mocked questions. `cua_repl` captured the desktop/mobile evidence. No additional live-model inference or clinical testing was used for this refinement; the existing model/catalog and known relevance limitation remain unchanged.
