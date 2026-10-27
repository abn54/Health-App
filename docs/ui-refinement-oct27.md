# UI and educational-content refinement — October 27, 2026

The student requested phase colors, an AI assistant popup, more visuals, more questions/FAQs, and consideration of linked resources and their in-class ideation notes. This is a refinement of the localhost prototype, not a completed Part 3.3 evaluation or a clinical service. Only fictional inputs were used.

## Changes and reasoning

- **Phase colors:** muted green inhale, muted blue exhale, neutral amber when paused. The phase word, count, expansion/contraction and cycle indicator retain the information without relying on color. Text only still removes the moving shape. The prescribed four-in/six-out, six-cycle schedule and monotonic engine are unchanged.
- **Visuals:** an original SVG rhythm guide shows a four-count rise and six-count return; six small markers show cycle position. Original SVG resource icons support reading-card scanning. No remote imagery, fonts or handbook images are loaded. Decorative SVGs are hidden from assistive technology; the rhythm guide has a text equivalent.
- **Entry and attention:** Start moved above the decorative preview. At the reviewed 1280×720 desktop viewport it was visible without scrolling. Exercise spacing was reduced after the first colored view put End below the viewport. The final desktop End bounds were y=615.5–659.5 in a 720-pixel viewport. Active instructional content stays one action at a time; FAQs/resources appear only outside active pacing.
- **Assistant popup:** explicit floating launcher, no automatic popups. It shares the same questions, mode, conversation and API as the sidebar assistant. Opening it during practice pauses; asking is disabled until the exercise ends. Its header keeps Close and Crisis support visible while the question area scrolls. Background is inert; focus enters the heading, Tab/Shift+Tab stay in the popup, Escape closes it and restores launcher focus. Closing preserves the underlying page; the explicit Return to exercise action restores the paused exercise from History too. Crisis support opens a separate higher-layer dialog and returns focus to the popup support button. Returning to practice remains paused.
- **Content:** eleven reviewed FAQ topics, three category filters and six editable suggested questions. Suggestions fill the input and require Ask; they never submit automatically. FAQs work from bundled content without a provider. A collapsed reading shelf identifies source types and limitations. `shared/help-content.json` is the single authored source for FAQ answers, backend catalog/context and source links, preventing frontend/backend copy drift. Model prompt `catalog-selector-v8`, catalog `app-help-v2`, local model remains `qwen2.5:3b` Q4_K_M.

The assistant can explain app controls and reviewed general information. It does not act as a therapist, diagnose, prescribe treatment, infer distress or claim monitoring. The student's requested therapist role was kept within the assignment's explicit no-therapy boundary. Adding references does not establish clinical validation.

## Sources actually reviewed

All public pages below were opened October 27; tracking parameters were removed from the AIS URL. No purchase, registration, clinical service contact, full-book ingestion or model training occurred.

| Source | What was accessed | Actual use and limits |
| --- | --- | --- |
| [NIMH stress fact sheet](https://www.nimh.nih.gov/health/publications/so-stressed-out-fact-sheet) | Public fact sheet | A brief paraphrased definition of stress, explicitly general information, with a source link. No personal assessment, symptom scoring, treatment recommendation or claim of benefit from this app. No NIMH image copied. |
| [AIS military/veteran page](https://www.stress.org/who-gets-stressed/military-and-veterans/) | Public population-specific resource page | Optional reading card, explicitly different from the fictional college-student audience. No inference that the page establishes the prototype's timing, efficacy or appropriateness for veterans. |
| [Grey House handbook listing](https://greyhouse.com/adolescent-mental-health) | Publisher's description of a book | Optional reference card clearly marked publisher listing/full text not supplied. The handbook itself has not been provided or incorporated. |
| [APA DSM overview](https://www.psychiatry.org/psychiatrists/practice/dsm/) | Public professional-reference overview | Explains the source type in the reading shelf. No DSM criteria, diagnosis questionnaire, disorder-matching feature or diagnostic model context is imported. |

The [Canvas ideation page](https://psu.instructure.com/courses/2484533/pages/ideation-understanding-user-state-questionnaires-and-clicking-behavior) was not accessible through text browsing. The student pasted the activity instructions and a discussion summary; these are the available sources for the activity connection. The original questionnaire, model/video materials, Austin paper and Macaulay paper were not independently accessed in this revision. No group participation, original-study verification or personal experience is fabricated. Group names and private course dashboard content are not republished.

## Connection to the supplied discussion and R/D findings

The student's notes favor easy access to familiar skills, reduced decision effort, privacy and user control, and question whether clicks can establish stress. The prototype retains direct entry without a questionnaire, explicit cue reuse/Remember/Reset, and no click-derived distress inference. The check-in FAQ explains this choice. An optional questionnaire was considered but not added: it would collect more sensitive data and add steps without a justified use in this one-skill scope (D3/R4). This is a design decision, not a claim that questionnaires are ineffective.

Phase colors and optional visuals balance a pacing cue with D6's low-stimulus concern; text/counts preserve the alternative. Optional help and reading stay outside the active view (D1/D2/D3). Immediate exit and independent support remain accessible in the popup (R2/R3/D4). Explicit personalization remains the documented D5/R4 compromise. The [full instructor-table mapping](research-findings.md) remains the research foundation. Activity resources add possibilities, not new mandatory features. Kaggle's earlier limited structural use remains separate and unchanged.

## Actual checks and results

| Check / expected behavior | Observed result |
| --- | --- |
| Green inhale / blue exhale without sequence changes | Actual rendered phases and counts observed; exhale fill `rgb(201, 223, 233)`; [inhale](evidence/inhale-color-oct27.jpg), [exhale](evidence/exhale-color-oct27.jpg) screenshots. |
| Complete six cycles within 90 seconds | **60.016600 s exercise and wall**, 0 s excluded, **18.153200 s setup**. [Exact timing](evidence/browser-timing-oct27.json), [completion](evidence/completed-oct27.jpg). Setup includes assistant inspection; not a typical-user benchmark. Subsequent CSS spacing fixes did not change timing code. |
| Popup shares reviewed answers and sources | Mock stress question displayed approved text and a NIMH link. Therapist question displayed explicit educational-role boundary. [Desktop popup](evidence/popup-desktop-oct27.jpg). |
| Popup during running exercise | Paused at inhale count 1; question input and suggestions disabled; Return and End available. Support return plus popup close still showed Paused; explicit Resume then End produced a saved Stopped record. |
| Keyboard focus | Shift+Tab from popup heading wrapped to its last Close button. Escape restored launcher focus. Returning from support restored `popup-support-control`. These checks are not full screen-reader certification. |
| Mobile layout and source shelf | At 390 CSS pixels, document scroll width was 390. FAQ categories and source descriptions opened; all four clean URLs inspected without following crisis links. Close/support bounds stayed in the viewport. [Mobile popup](evidence/popup-mobile-oct27.jpg), [reading shelf](evidence/reading-mobile-oct27.jpg). Temporary viewport reset. |
| API outage inside popup | Stopped FastAPI; question reported unavailable/unconfirmed save; popup Crisis support opened bundled information without API/model/classifier. [Outage screenshot](evidence/popup-support-offline-oct27.jpg). No service contacted. |
| Persistence after restart/reload | History retained the saved check-in answer and v8 metadata; offline unsaved question absent. [Reloaded History](evidence/history-reloaded-oct27.jpg). |
| Existing live regression | Motion/storage/controls each matched once: [actual v8 results](evidence/live-selection-catalog-selector-v8.json). |
| Expanded live questions | General stress definition, usual cue, click inference, therapist boundary and handbook sources each matched once: [actual results](evidence/live-expanded-help-v8-oct27.json). Selected authored development checks, not independent accuracy or repeated variation evidence. |
| Repeatable checks | [21 backend tests](evidence/backend-tests-oct27.txt), [6 client tests](evidence/client-tests-oct27.txt) passed; [production build](evidence/build-oct27.txt) succeeded. Mocked provider/injected-clock checks remain distinct from live/browser observations. Existing dependency warning retained. |

The isolated read-only [SQLite inspection](evidence/database-inspection-oct27.json) contains 6 sessions, 8 events, 22 messages and 9 provider attempts (eight live questions and one counted preload), integrity `ok`, no foreign-key violations. [Exact model metadata](evidence/model-oct27.json). No original user workspace data or raw database is published.

## Remaining limits

No handbook attachment has yet been supplied; its contents cannot be used or claimed as evidence. Linked book/DSM pages are not a basis for acting as a therapist. Broader model reliability, repeated variation, assistive-technology/browser coverage, independent clean-checkout verification, simultaneous tabs and crash durability remain unresolved. Part 3.3's full fifteen-scenario/three-behavior-check evaluation and demonstration/process recordings remain separate work. This revision does not establish clinical effectiveness.
