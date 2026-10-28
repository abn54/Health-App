# Bottom-right assistant and rounded composer — October 28, 2026

The student requested moving the launcher from the header to the bottom right and using a chat-style composer with optional voice, supplying a screenshot as visual direction. The app now uses a reserved bottom rail with a 52 px circle, a right-aligned modal, a pinned rounded message bar with labeled Send and Read replies, and scrollable conversation/options. The rail and page bottom spacing let final page controls scroll clear; focused controls have bottom scroll clearance. Voice remains optional reply playback, with Stop while busy. Existing voice/speed/model controls are under Reply & voice options. No microphone or real-time voice conversation is claimed.

Enter sends, Shift+Enter adds a line; composition events do not submit. Suggested questions remain editable. New popup turns scroll into view without moving focus. Support/Close stay outside the conversation scroll. Inert background, focus trapping/Escape return, app limits, mock default, reviewed content, silent exercise and profile/history persistence remain.

## Expected and observed

- **Send:** Enter sent a fictional duration question and produced the reviewed Mock response. Shift+Enter produced a newline without sending; the final Enter submitted. The production Send button also returned that reviewed response.
- **Voice:** Read replies enabled the existing on-device output; browser status reported Reading assistant reply aloud and conversation aria-live off. Stop turned auto-read off. These are browser events, not a human listening or acoustic test.
- **Scroll/focus:** after a new turn, scrollTop 209.5 / scrollHeight 459 / clientHeight 249. Tab from footer Close wrapped to header Close; Shift+Tab returned to footer Close; Escape focused assistant-launcher.
- **Layout:** at 667 × 798 the launcher measured 52 × 52 at (591, 734.5). At 390 px with 20 px root text and higher contrast, document scrollWidth was 390 and composer bounds left 24 / right 366 / bottom 681. The composer remained visible with its own conversation scroll. No virtual-keyboard test was performed.
- **Practice/support:** opening the popup immediately after Start paused at inhale count 1 and disabled questions/Read replies/Send. Support opened from the popup and returned. End produced a saved Stopped partial session. This is not a completed timing run.
- **Build/checks:** 17 existing client tests passed; production build and git diff --check succeeded. Production browser error log returned no entries. Backend code and contracts did not change; no new backend test run is claimed.

All inputs/records in this review were fictional and used a separate temporary database. Original local records were not exported. No model provider attempt or preload was added; the main host retained 1/50 attempts. [Manual observations](evidence/composer-manual-oct28.json), [actual production screenshot](evidence/composer-popup-final-oct28.jpg).

## Accessibility review and revisions

Initial wrapper markup caused the browser to generate a Details summary and obscure the composer; the popup now uses a flex div. A wrong CSS append path was corrected before final build. [Initial axe scan](evidence/composer-popup-initial-oct28.json) exposed the character-help text inheriting an old low-contrast color (3.61:1); the more specific final selector corrected it.

| Final selected state | Detected violations | Passed rules | Evidence |
| --- | --- | --- | --- |
| Popup with fictional reply | 0 | 35 | [Popup](evidence/composer-popup-oct28.json) |
| Phone, larger text/higher contrast | 0 | 35 | [Phone](evidence/composer-phone-oct28.json) |
| Phone, expanded voice options | 0 | 37 | [Options](evidence/composer-options-phone-oct28.json) |
| Ready and bottom rail | 0 | 40 | [Ready](evidence/composer-ready-oct28.json) |

Incomplete contrast checks remain in the files, including decorative glyphs and the prototype-description text; zero detected violations is not full WCAG conformance. No blind-user, VoiceOver/NVDA, all-browser or acoustic evaluation was done. A later production phone screenshot attempt returned scaled desktop content instead of phone reflow and was discarded; the earlier actual phone DOM/reflow measurements above remain the evidence. Browser controls required a reconnect during cleanup. These tool issues are not counted as app test passes.
