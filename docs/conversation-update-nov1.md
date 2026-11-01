# November 1 — questions in the user's own words

The student reported that an ordinary exam-pressure question received the generic unsupported/clinical-limits reply. The previous 13-topic app-help catalog and substring matcher did not cover that everyday intent. This update broadens the conversation **without claiming to answer every possible question** or turning the coursework prototype into therapy.

## What changed

Catalog `app-help-v7` adds eight reviewed topics: exam pressure, study/workload planning, feeling overwhelmed, rest/winding down, social connection, finding support, choosing a skill, and greetings. Questions need not match or use the suggestion buttons. Ordinary questions receive a supportive acknowledgement and relevant general options rather than repeated role warnings. Unclear/out-of-scope input asks a focused clarifying question. Medication, diagnosis and therapist requests still receive explicit limits; no mental state is inferred or written to a profile.

Default **Prepared reply** remains honestly labeled. Word-boundary/intent rules now separate everyday concerns from direct app commands, so “friend” or “weekend” cannot accidentally match the substring “end.” Explicit pause/resume/session questions retain app answers. Prompt `catalog-selector-v13` and the Selection schema include the new topics, so the local model can interpret differently phrased questions against the expanded reference. It still selects an ID; the application displays reviewed copy, never arbitrary model-written treatment advice. A deterministic scope check bypasses live inference for explicit role/diagnosis/medication requests. It is a content boundary, not a clinical assessment, and does not gate the manual support route.

The message composer now says **Ask in your own words** and explains that suggestions are optional. Existing voice/text alternatives, profile choices, factual-history tailoring, save/replay and independent support remain. Everyday-topic answers honor saved reply length but do not append claims about a user's emotions or treatment needs. Existing saved replies keep their original text and version metadata.

## Primary sources inspected

- [NHS Student stress](https://www.nhs.uk/mental-health/children-and-young-adults/help-for-teenagers-young-adults-and-students/student-stress-self-help-tips/): general manageable-work, breaks and social-support information. The app's small study example is authored, not a copied therapy transcript.
- [NIMH stress fact sheet](https://www.nimh.nih.gov/health/publications/so-stressed-out-fact-sheet): general stress, connection and when to seek professional support.
- [NHS Every Mind Matters: Sleep problems](https://www.nhs.uk/every-mind-matters/mental-health-issues/sleep/): general routine/winding-down information, without diagnosing insomnia or recommending medication.

These public pages were inspected November 1, 2026. That date is an inspection date, not a claim that a clinician reviewed this prototype. Source links appear under relevant answers and in the reading shelf. The instructor's research table remains separate; no new Kaggle import, training, patient data or clinical-effect evaluation was performed.

## Actual verification

- **67 backend tests passed** (the prior44 plus23 new parameterized/behavior cases). New checks cover independently worded questions, preserved draft/preferences, clear scope without a provider call, allowed live topic selection, and clarification instead of fabricated answers. The existing Starlette/httpx deprecation warning remains. The first run had five failures because a version assertion still pinnedv6; updated to the actualv7 contract, without removing content/state assertions.
- **21 client tests passed** and the production build passed. The original exercise engine, skill data, exercise timing and database schema were not changed. No new full-duration timing result is claimed for this conversation-only revision.
- [Existing22 deterministic scenarios](evidence/conversation-mocked-nov1.json) passed with zero real provider calls; synthetic timings and stub source fields remain explicit.
- [Nine actual live selections](evidence/conversation-live-nov1.json), three authored fictional questions×three repeats, selected exam/rest/overwhelmed as expected in all9 cases, with no within-case variation. Local Ollama0.32.5/qwen2.5:3b, temperature0,80-token JSON selection and8-second timeout; model digest/settings/source hashes are recorded. Nine attempts plus one counted preload used **10/50** in the new isolated `conversation-nov1` session. Original main-host accounting was preserved separately. The live evidence retains its original source hashes; a post-evaluation note identifies the later resource display-label clarification. No model context or answer text changed after that run.
- [Actual browser checks](evidence/conversation-browser-nov1.json) demonstrate a typed exam question outside suggestions, a sleep question with source, friend/weekend wording and keyboard close. Only fictional review inputs in a separate SQLite database were used; original user conversations were not exported.

### Browser finding and revision

The first exam-response screenshot showed only the tail of the longer reply because the old popup watcher scrolled every message to the absolute bottom. [Initial observation](evidence/conversation-exam-initial-scroll-nov1.png). The watcher now aligns the beginning of a new assistant answer inside the scroll area, without moving keyboard focus. [Retest](evidence/conversation-exam-nov1.png) and Q04 record the visible start. The pinned composer and ability to scroll the remainder remain. This is a selected browser regression check, not a broad accessibility certification.

## Scope and unresolved limits

This is still a fictional localhost coursework prototype, not a therapist, diagnosis/treatment engine, human-monitored service, unrestricted search engine or general-purpose chatbot. “Ask in your own words” refers to free-form input over the reviewed areas, not guaranteed coverage of every paraphrase, topic or language. Prepared rules and model selection can still choose an irrelevant topic, especially for mixed-intent or vague questions. The app does not retain or infer a clinical persona. Broad semantic accuracy, real blind-user/screen-reader behavior, acoustic quality and clinical effectiveness remain untested. Earlier role-topic failures and dated recordings stay historical; explicit clinical-scope questions now use an independent reviewed boundary instead of depending on the model to choose scope.
