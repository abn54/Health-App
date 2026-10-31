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


## October 21, 2026 — complete research source and Part 3.2 revision

The student supplied the complete assignment overview and requested “develop 3.2.” That source includes the previously unavailable R1–R4 / D1–D6 table. Codex mapped all ten findings, explained the D1/D2 and D5/R4 compromises, refreshed the requirements audit, and retained the historical source limitation rather than backdating access. Dashboard/account material from the paste is excluded from published evidence.

The same GPT-6-based Codex agent revised generated Vue save/exit handling and the local model prompt, ran the existing 16 backend and 6 client tests, built the UI, performed browser checks with `cua_repl`, inspected an isolated fictional SQLite database read-only, and drafted the current report. No subagents were used for this revision. Student understanding, independent review and a Canvas upload are not claimed.

Actual new model: **Ollama 0.32.5 / `qwen2.5:3b` Q4_K_M**, digest `357c53fb659c5076de1d65ccb0b397446227b71a42be9d1603d46168015c9e4b`. Prompt `catalog-selector-v7`; catalog `app-help-v1`. The official [model page](https://ollama.com/library/qwen2.5:3b) was inspected; the model was obtained from Ollama's official registry, and weights are not redistributed. The model page identifies the Qwen research license for this 3b variant. Earlier actual 1.5b and 3b v6 failures are retained. Current v7 examples and test inputs are authored fictional app questions, not therapy transcripts or Kaggle training data.

The isolated October 21 verification host recorded 13 provider attempts, including two counted preloads and unsuccessful development selections. The separate original host retains its prior attempt ledger; restarting it did not reset that ledger. No paid provider, real person in distress, clinical evaluation, external service contact, new dataset download, training, recording or independent clean-checkout check was used. Selected live observations are separate from mocked tests and from the Part 3 variation study still to do. [Current verification](docs/part2-verification.md) records exact results and limits.


## October 27, 2026 — requested visual and educational-help refinement

The same GPT-6-based Codex assistant authored phase colors, original SVG rhythm/resource graphics, a reusable Vue assistant panel/popup, categorized FAQs and shared reviewed JSON content. It reviewed the student's pasted activity summary and opened the supplied AIS, Grey House and APA pages plus the NIMH stress fact sheet with `web.run`. The Sites skill's local-only workflow was consulted; no hosted Site, source synchronization or deployment was created. No subagent was used. No image-generation model, remote photograph or handbook image was used.

The assistant authored five additional mocked API integration cases, ran 21 backend and 6 client tests/build, performed actual browser checks with `cua_repl`, and inspected a separate fictional SQLite database. Actual app model remains Ollama 0.32.5 / `qwen2.5:3b` Q4_K_M with unchanged digest; prompt `catalog-selector-v8`, catalog `app-help-v2`. Eight selected live requests and one host-counted preload were recorded in the isolated October 27 ledger, cap 50. No paid provider or training was used. Model evidence is separate from mocks.

Handbook files have not been attached or ingested. The Grey House listing is not full-book review, and the DSM overview is not diagnostic logic. The assistant does not impersonate a therapist or provide personal treatment. Original activity papers were not obtained and group participation is not claimed. Private group names/course dashboard content are omitted from public documentation. [Dated evidence and limits](docs/ui-refinement-oct27.md). The earlier Part 2 report is archived before updating the root report.


## October 27 — full visual redesign request

The same Codex assistant replaced the layout/stylesheet, created original SVG flower/landscape artwork, updated Ready copy and verified actual desktop/phone controls with `cua_repl`. The Sites skill's local-only workflow was reused. System fonts and code-native SVGs required no image model, remote asset, added dependency or clinical source. No subagent or live provider call was used for this visual change. The existing six client tests and production build passed; backend tests were not rerun. An isolated attempted full-duration browser observation lost its tab and was recovered as Interrupted with unknown timing; no completion is claimed. The actual observations and selected contrast checks are in [visual-redesign.md](docs/visual-redesign.md). The name remains Pause because no replacement was selected.

## October 27 — requested voice output

The same Codex assistant authored optional browser speech/tone output, shared voice controls, cancellation/phase gating and eleven fake-API audio cases (17 total client tests), and ran 21 backend tests plus the production build. It consulted MDN's primary Web Speech documentation and used `cua_repl` for actual Mac in-app-browser checks and screenshots. A native timer-binding failure found during Preview was corrected and retained in the dated notes; fake tests alone had missed it. No subagents, external TTS provider, microphone, audio recording, paid call, clinical study or new live-model request was used. The complete spoken exercise measured 60.016200 seconds with twelve browser-reported phase starts. Browser events are not a claim of listening or acoustic quality. Only selected fields of the new fictional session were exported; original workspace records remain local. See [voice-output.md](docs/voice-output.md) for expected/observed results and limits.

## October 27 — mello rename, dated history and smaller assistant button

The same Codex assistant updated the current branding, added a read-only last-chat aggregate and local-time message display, excluded that read-only field when reopening drafts, and moved a compact circular launcher into the sticky header. Actual phone inspection found that the first smaller floating circle still covered a history value; the header revision resolved that overlap. The Sites local-only workflow was reused, with no hosted deployment or subagent. One new mocked API test plus the existing cases passed (22 backend); the existing 17 client cases/build were rerun. Browser evidence uses an isolated fictional conversation and checks saved-draft continuation, timestamps, phone/pane layout and keyboard close/focus return. No new live inference, recording or full-duration timing result is claimed. [Dated verification](docs/mello-history-update.md).

## October 28 — presentation rubric, explicit profile and walkthrough

The student supplied the presentation rubric and selected both application updates and presentation preparation. The same Codex assistant audited the four criteria, authored a minimal local profile/migration, controlled reviewed reply variants/context rendering, visible profile/history cue reuse, tests and `presentation-walkthrough.md`. No subagents, identity service, personal questionnaire, clinical persona, external TTS or recording were used. The Sites local-only workflow was reused; no deployment. The linked authenticated overview could not be accessed via web tooling; the supplied rubric and actual earlier pasted R/D table were used instead.

Actual verification: 33 backend and 17 existing client tests/build passed; an isolated fictional browser scenario demonstrated save/reload, cue override, support/stop, profile-tailored reply, reset comparison, phone controls, failed profile save with support available, and a complete run measured at 60.008600 seconds. Only that new fictional database’s selected evidence was exported. Main workspace preferences/history remain preserved. Student delivery, recording/upload, independent checkout and the full Part 3.3 evaluation are not claimed.

Actual local model remains Ollama 0.32.5 / qwen2.5:3b Q4_K_M. The isolated ledger retained seven attempts including one preload: v9 and v10 both chose unsupported instead of the expected scope for a therapist request. The added few-shot example did not fix that selection. Final catalog app-help-v4 explicitly states not a therapist in both boundary answers; final prompt is catalog-selector-v10, personalization profile-copy-v1. All outputs remain reviewed text. These authored one-shot development examples are not independent semantic/clinical validation. The model receives the question and approved facts, not raw profile/history; reviewed local rules apply explicit preferences/factual records. [Actual results, failed/revised approaches and limits](docs/presentation-readiness-oct28.md).

## Later October 28 — chatbot-only voice and accessibility request

The same Codex assistant removed breathing speech/tone code and controls, simplified synthesis to chatbot replies/previews, ranked installed on-device voice options while hiding novelty names, and added labeled color-coded actions/speed controls. It added skip navigation, corrected landmarks/ARIA, assistive announcement text, visit-only contrast/text options and responsive focus/navigation improvements. No subagent, paid voice service, voice download, microphone, audio recording, new model request or training was used. Optional existing local Ollama service was restored after an interruption; no inference/preload was added for this revision.

It consulted the W3C WCAG/APG, MDN localService and official axe-core documentation. Pinned axe-core 4.14.0 is a dev-only dependency/harness, absent from production. Actual scans exposed contrast/landmark/ARIA defects; manual 320 px review found navigation overlap automation missed, and the design was corrected. Initial findings and incomplete checks are preserved. 17 revised client tests and 33 backend tests/build passed; actual silent production run measured 60.015400 seconds. Browser speech events are not a human listening or naturalness assessment. No VoiceOver/NVDA/blind-user test or full WCAG certification is claimed. [Exact changes, evidence and limits](docs/accessibility-update-oct28.md). The presentation walkthrough/current README were updated; older voice evidence remains historical.


## October 28 — local server recovery

Codex diagnosed an actual connection refusal and absent localhost listeners after the student reported a broken frontend. It restarted the existing built app and optional local Ollama service without model inference/preload or changing application code. It verified HTTP 200 for the page/assets/health, rendered UI and an accessibility disclosure, saved a page screenshot and added restart guidance. Processes were detached from the tool session; no OS autostart service was installed and no reboot-persistence guarantee is claimed. Existing local data and host budget were preserved. No additional unit-test pass, recording or clinical result is claimed.


## Later October 28 — bottom-right assistant composer

Codex used the Sites skill local-only workflow to implement the requested bottom-right launcher and screenshot-inspired rounded composer. It reused the existing approved response/voice paths, authored SVG send/waveform controls, kept explicit labels and optional reply playback, and made no microphone/voice-recognition/provider addition. It corrected a hidden-composer wrapper, CSS path mistake and detected contrast issue using actual browser evidence. Mocked fictional review used a separate SQLite database. 17 client tests/build passed; no new live inference, acoustic judgment, full timing, recording, clinical result or real assistive-technology test was made. [Exact observations and limitations](docs/composer-update-oct28.md).


## Late October 28 — simpler, accurate chat wording

Codex revised the chat labels and reviewed catalog to reduce repetitive fictional/role warnings, while preserving accurate prototype/source disclosures and explicit clinical-role limits. It did not represent mocks as real clinical data or claim therapist credentials. It added and mocked the about topic, revised the selector prompt/version, and kept saved history unchanged. Actual isolated purpose and therapist turns were checked; 39 backend/17 client tests and build passed after correcting an existing machine-date-dependent test fixture. No new live call, training, provider preload, full-duration run, recording or accessibility certification was performed. [Exact evidence](docs/chat-copy-oct28.md).


## October 30, 2026 — Part 3.3

The student requested “3.3 now.” The same GPT-6-based Codex desktop assistant (exact serving build not exposed) read the supplied overview and project instructions, refined generated Vue focus/history code, authored two evaluation runners, ran tests, operated fictional browser scenarios, inspected a separate local database read-only, and drafted final documentation/report. No subagents were used in this milestone. The Sites local-only workflow was reused; no hosting/deployment or remote source synchronization occurred. No previous travel/hotel source was supplied or copied.

Actual stack identifiers remain Vue3.5.44/Vite8.3.4, Python3.14.7/FastAPI0.149.0, Node26.7.0/npm11.19.0. SQLite version is recorded in prior database evidence. Browser tool: cua_repl/in-app browser (build not exposed). Shell/Python/Git performed tests and curated export. No new clinical sources, dataset downloads, training, paid API, credentials, real personal story or handbook ingestion were used. The Kaggle preview adaptation and research table remain separately attributed.

Actual local model: Ollama0.32.5, qwen2.5:3b Q4_K_M, digest357c53fb659c5076de1d65ccb0b397446227b71a42be9d1603d46168015c9e4b; catalog-selector-v11/app-help-v5/profile-copy-v1. Fifteen repeated selections plus one preload and one recorded demo selection used17/50 host attempts. The repeated role-topic error remains visible. Mock/stub checks are separate from this model evidence. No prompt/model/catalog change was made in Part3.3.

Recording capture used actual Cua task-tab screenshots, not generated UI images; optional imageio-ffmpeg0.6.0 / FFmpeg7.1 encoded silent H.264 with captions/transcripts and disclosed idle edits. A native recording attempt did not produce verified output and is not claimed as submitted evidence. These are AI-operated demos, not student narration, a personal presentation, peer feedback or proof of student understanding. Media tools are not needed for the application.

Observed failures, generated-code explanation, expected/observed cases and limits are in [Part3 evaluation](docs/part3-evaluation.md), [revisions](docs/part3-revisions.md), [recordings](docs/recordings/README.md) and [evidence log](docs/evidence-log.md). Final GitHub clean-checkout verification was on the same Mac with a fresh environment, not an independent reviewer. Student review and final Canvas submission have not been performed by the assistant.


## October 31 — requested coastal redesign and additional exercises

The same GPT-6-based Codex assistant (exact serving build unavailable) used Sites' local-only workflow, built-in image generation, Vue/FastAPI/SQLite edits, Cua browser checks and Python/Git evidence curation. No subagent, hosted deployment, paid API, external TTS, personal participant data or clinical study was used. Original scenic raster: frontend/src/assets/mello-coast.png, generated with the built-in image tool (image model/build not exposed), copied into the repo; exact prompt is in docs/coastal-update-oct31.md. No real location is claimed.

The two new skill sequences derive from the supplied assignment overview, not model-invented therapy instructions. New app model metadata: Ollama0.32.5 / qwen2.5:3b, unchanged model digest, catalog-selector-v12/app-help-v6. Actual nine repeated selector calls and one preload in an isolated fictional host used10/50 attempts; routine checks used mocks. Generated GuidedExercise extends the existing monotonic state machine; new tests check order, pause/exit/interruption and truthful skill identity/history. Test-copy/version failures were reviewed and corrected, with the initial failure retained in the dated notes. All other actual results and untested access/model limits are linked in the same notes. Older October30 videos remain explicitly historical, not evidence of the new layout.

A short additional October31 tour was captured from actual task-tab frames and encoded with the existing imageio-ffmpeg0.6.0/FFmpeg7.1 workflow, silent with captions and a transcript. It intentionally demonstrates a partial Grounding exit, not a completed timing run. The existing process video still explains the unchanged focus fix. No student narration or personal presentation is claimed. Selected axe-core4.14.0 scans found no detected violations on Ready/paused STOP, while contrast-incomplete findings are retained; explicit region/group roles resolved the initial naming concern.
