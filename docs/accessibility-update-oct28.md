# Chatbot-only voice and accessibility — October 28, 2026

The student requested removal of breathing audio, clearer color-coded controls, less robotic chatbot voice choices, and better access for people who cannot see. This revision improves concrete keyboard, screen-reader and low-vision behavior. It does not claim universal accessibility, a completed blind-user test or WCAG certification.

## Current behavior

- **Breathing is silent from the app.** Removed all phase-triggered synthesis, soft tones, Web Audio/oscillators, `PhaseCues`, the Voice & sound controls and `VoiceSettings.vue`. The prescribed 4-count inhale / 6-count exhale × 6 schedule and immediate Pause/End/support remain. Nothing waits on speech.
- **A screen reader can still read the exercise.** Accessibility options select Phase and cycle (default), Each count or Off for one persistent polite/atomic live region. This is accessible text, not the app's speech synthesizer. The user's assistive technology owns its voice/queue and may lag; Pause and End remain available. Words/counts/progress describe what color and motion show. Decorative cycle dots no longer have invalid/redundant ARIA labels.
- **Chatbot voice only.** Blue Preview/Read and red Stop controls have explicit text and symbols. A playing-state label, optional auto-read, three speed choices and unique per-reply accessible names make the actions distinguishable without color. Stop also turns auto-read off. The conversation live region is off while optional auto-read/manual speech is active to avoid competing automatic readings; text remains readable by a screen reader. Auto-read defaults off after reload.
- **Voice choices:** browser-reported local English voices only; known novelty names such as Kathy, Fred, Bells and robotic effects are hidden. Enhanced/premium/natural/neural/Siri name hints rank first when available, followed by neutral installed defaults. Voice names/metadata do not establish acoustic quality. This Mac offered standard voices; Moira was selected and its preview reported start/finish. No enhanced voice was installed/downloaded, no cloud provider used, and no human listening/naturalness judgment is claimed.
- **Access controls:** Skip to main content; one banner/main/footer structure; named navigation and route-heading focus; existing inert/focus-managed dialogs; visible focus; increased touch targets; visit-only Higher contrast and Larger text. Navigation stacks in very narrow/large-text layouts. A ResizeObserver measures the sticky header for focus scroll offsets. Reduced-motion/default text cue and explicit remembered-cue reset remain.

Voice, contrast, text-size and announcement choices are page memory. Existing explicit cue/profile preferences and local records are preserved. No model/catalog/API/database contract changed in this revision. The model remains `qwen2.5:3b`, prompt `catalog-selector-v10`, catalog `app-help-v4`; no new live inference was made.

## Actual checks

All browser inputs/evidence below use a separate fictional database. No original workspace conversations were exported.

| Check | Expected | Actual observation |
| --- | --- | --- |
| Silent full run, production build | Complete all six cycles with no speech/tones invoked | Text only run Completed and saved. **60.015400 s exercise/wall**, **0 s excluded**, **0.340300 s setup**. Review log contained only three chatbot cancellation messages, no playback start. Source inspection also found no breathing synthesis/tone paths. [Timing](evidence/silent-exercise-timing-oct28.json), [events](evidence/silent-exercise-events-oct28.txt). |
| Screen-reader text | Phase/count/paused information available without app audio | Actual accessibility tree exposed “Cycle 1 of 6. Inhale for 4 one-second counts.” and paused cycle/phase/count with explicit Resume/End. Each-count and Off are covered by deterministic text tests. No VoiceOver/NVDA listening result is claimed. |
| Chat voice | Curated choices, preview/manual read and immediate Stop | Samantha/default and Moira were available; Kathy/Fred/effects were absent from the list. Moira preview reported start/finish; manual reply and auto-read reported speech starts. Stop reported cancelled/auto-read off. Device volume/acoustic quality was not recorded. |
| Duplicate announcements | Optional speech and automatic log announcements do not compete | With auto-read checked, the actual reply spoke and conversation `aria-live` was `off`; Stop changed it back to `polite`. This DOM behavior is observed, not a claim about every assistive-technology queue. |
| Keyboard | Skip/focus, modal cycle and Escape return work | Skip focused `main-content`; popup last Tab wrapped to header Close; Shift+Tab returned to footer Close; Escape restored `assistant-launcher`. History navigation focused its H1. |
| Narrow/large text | No overlapping navigation or horizontal overflow | 320 px with 20 px root text initially exposed overlapping navigation despite a zero-violation scan. The final stacked layout removed overlap. At 390 × 844 with Larger text + Higher contrast, scroll width equaled 390; measured header offset was 244.5 px. No 200% browser-zoom certification is claimed. |
| Repeatable checks | Changed speech/announcement code and existing invariants pass | **17 client tests passed**: 8 chatbot speech/voice-selection cases, 3 announcement-text cases and the original 6 engine/phrase cases. Removed phase/tone cases because that functionality was deleted. **33 backend tests passed**, production build succeeded, `git diff --check` passed. The existing Starlette TestClient warning remains. |

[Manual observations/actual voice list](evidence/accessibility-manual-oct28.json), [chatbot controls](evidence/chatbot-voice-controls-oct28.jpg), [phone accessibility options](evidence/accessibility-options-phone-oct28.jpg).

## Automated accessibility review and revisions

Added pinned **axe-core 4.14.0 as a development dependency**. The Vite-only `?a11y-review` harness runs a manually requested scan of the current DOM with WCAG 2 A/AA, 2.1 AA, 2.2 AA and best-practice tags. It does not operate app controls or certify usability. The harness is excluded from its own scans and absent from the production bundle. Its first large results panel covered a form field during testing, so the dev panel was made small; the production app never included that overlay. A wrong working-directory path during harness setup was corrected before testing resumed.

Initial scans found low-contrast brand/intro/FAQ/source labels, duplicate banner/outside-landmark notice, popup eyebrow contrast, invalid ARIA labels on decorative dots and weak paused-state contrast. Those were corrected rather than ignored. Initial/revised evidence is retained.

| Actual scanned state | Final detected violations | Passed rule count | Evidence |
| --- | --- | --- | --- |
| Ready | 0 | 39 | [Ready](evidence/accessibility-ready-oct28.json) |
| Expanded options/profile/reading | 0 | 43 | [Expanded](evidence/accessibility-expanded-oct28.json) |
| Popup | 0 | 36 | [Popup](evidence/accessibility-popup-oct28.json) |
| Popup with fictional reply | 0 | 36 | [Reply](evidence/accessibility-popup-with-reply-oct28.json) |
| Independent support | 0 | 30 | [Support](evidence/accessibility-support-oct28.json) |
| Paused exercise | 0 | 42 | [Exercise](evidence/accessibility-exercise-oct28.json) |
| History | 0 | 39 | [History](evidence/accessibility-history-oct28.json) |
| 320 px larger text + higher contrast | 0 | 44 | [Larger text/contrast](evidence/accessibility-large-contrast-oct28.json) |

Zero **detected violations** is narrower than “fully accessible.” The JSON files also retain `incomplete` checks, mostly decorative glyph/contrast inspection and some support/phase text. Selected essential text color pairs were calculated separately: Play **7.127:1**, Stop **8.265:1**, inhale/exhale text over circle fills **6.512:1 / 6.740:1**, paused text **5.822:1**, support paragraph **5.235:1**, resource note **4.516:1**. [Method and selected pairs](evidence/accessibility-selected-contrast-oct28.json). These calculations do not replace a complete visual, non-text or assistive-technology audit.

Initial retained findings: [Ready/structure](evidence/accessibility-initial-oct28.json), [popup](evidence/accessibility-popup-initial-oct28.json), [exercise](evidence/accessibility-exercise-initial-oct28.json), [first narrow scan](evidence/accessibility-large-contrast-initial-oct28.json). Manual narrow-layout inspection caught overlap that automation missed. An interruption stopped the development servers; they were restarted using the same isolated data, with no test result inferred from the interruption.

## Limits and references

No blind participant, VoiceOver/NVDA audio walkthrough, full keyboard journey for every record/error path, all browsers, forced-colors environment, 200% zoom, acoustic comparison or clinical evaluation was performed. Those require further targeted review. The app cannot guarantee assistive-technology announcement latency. It provides Pause/End and an Off option rather than promising precise spoken timing.

The implementation was informed by [W3C WCAG 2.2 Quick Reference](https://www.w3.org/WAI/WCAG22/quickref/) for keyboard, structure, labels, contrast, color redundancy, focus and reflow; [WAI modal-dialog guidance](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/) for focus containment/return; [MDN localService](https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesisVoice/localService) for browser-reported local/remote voice distinction; and [axe-core’s official documentation](https://github.com/dequelabs/axe-core) for automated checks and their limits. These are implementation references, not proof of certification.
