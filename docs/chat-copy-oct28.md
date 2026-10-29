# Chat wording revision — October 28, 2026

The student requested less fictional/prototype/role wording in chat and wanted the experience to look like real data even when it is not. The implementation reduces repetition without representing prepared content as clinical data or claiming that mello is a therapist. The presentation rubric requires an honest coursework-prototype role.

## Changes

- Your question and You replace repeated fictional-question labels in the composer, chat and History. The composer character counter focuses on keyboard guidance. The shell still says coursework prototype, demo use only, with no therapy/diagnosis/human monitoring; the popup header also identifies a coursework app assistant. The profile keeps example/demo guidance.
- Prepared reply replaces Mock response in visible labels. Reply & voice options explains that prepared replies use reviewed app text and that live mode uses a local model to select from the same text. Backend source stays `mock`; saved provenance is not rewritten or relabeled as model generation/real clinical data.
- New allowlisted `about` topic answers app purpose/features directly. Explicit therapist, diagnosis and monitoring questions still select `scope` in the mocked path and receive a concise, honest limits answer. Ordinary purpose answers no longer repeat that role warning. The suggested role question becomes What can mello help me with?; the explicit limits FAQ remains.
- New chat reply metadata is behind Reply details, with source label and substantive reply visible. Per-message notes and citations remain visible. History keeps its metadata. Existing saved replies keep their original wording and versions; a new turn uses current copy.

Current catalog `app-help-v5`, selector prompt `catalog-selector-v11`, existing model `qwen2.5:3b` and profile renderer `profile-copy-v1`. The selector enum/reference/example now includes about. This is not free-form model therapy or a new dataset/model training pass. No clinical findings, diagnoses, treatment advice or outcome claims were added.

## Actual verification

**39 backend tests and 17 client tests passed; production build succeeded.** Six mocked purpose/name paraphrases select about; three direct therapy/diagnosis questions select scope. Existing persistence, profile, boundary, budget and rejection cases passed. No new live inference/preload was made. Selection relevance for the new prompt remains untested live; previous live failures are not claimed resolved.

An initial full backend run reported **38 passes and one failure** in the existing latest-practice ordering test. That test mixed current fixture dates with a fixed October 29 timestamp; after that instant, its purported newest record was no longer newest. Both test records now use fixed ordered timestamps, independently of the machine date. No application ordering logic changed. The subsequent complete run passed all 39 cases. The existing Starlette TestClient deprecation warning remains.

Actual browser checks used an isolated demonstration database: the student's purpose question returned the approved features answer labeled Prepared reply; the composer said Your question, and Reply details was collapsed. The options explained prepared/live sources. A second direct therapist question returned the explicit not-a-therapist limit. Both turns saved locally with their actual source/topic/catalog/prompt metadata; provider attempts remained zero. [Exact selected observations](evidence/chat-copy-checks-oct28.json), [purpose answer screenshot](evidence/chat-copy-purpose-oct28.jpg).

The main server was restarted to load the new catalog/prompt while preserving its database and host budget. No original conversations were exported. No new timing run, recording, acoustic assessment, accessibility audit or blind-user test is claimed for this copy revision.
