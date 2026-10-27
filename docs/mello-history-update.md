# mello, chat dates and compact assistant — October 27, 2026

The requested name is now **mello**. Current app wordmark/home label, document title, footer, API title and npm package name are updated. Historical coursework reports/evidence retain the name used when produced; existing `PAUSE_DB`/SQLite location remains compatible.

History lists **Started** and **Last chatted**, and each saved message has its own date/time. Chat timestamps include seconds and the device time zone. Last chatted is the latest saved user-question time, not session creation, a later assistant reply, an exercise save or a claimed online status. No-chat sessions say **No chat in this session**. The API derives this from existing saved rows without a migration or invented dates. List ordering uses that chat date with session creation as the fallback.

The old floating text badge is now a **46 × 46 px header circle**, **44 × 44 px on phone width**. It has a chat icon, Ask the assistant accessible name/title and keyboard focus ring. It shares the sticky header with independent Crisis support and never floats over the history/content area. The full AI assistant navigation entry also remains available.

## Actual checks

- **22 backend tests passed**: the new temporary-database case verifies no-chat null, latest user date, exclusion of later assistant dates, older-conversation ordering and deletion; the original 21 cases still pass. The existing Starlette TestClient deprecation warning remains.
- Production Vue build succeeded; `git diff --check` passed. No new client tests were added for this presentation change; the existing 17 exercise/audio cases were rerun successfully.
- Actual browser on an isolated fictional database: saved “How long is the exercise?” at **3:08:43 PM EDT**; History showed the corresponding Started/Last chatted dates and both message timestamps. Continued the same saved draft with “What gets saved?” at **3:08:53 PM EDT**; it saved successfully, kept Started, and refreshed Last chatted. No original workspace conversations were exported as evidence.
- Actual phone **390 × 844** and pane **667 × 853**: document width equaled scroll width; the final circle stayed within the sticky header. Popup opening and Escape closing worked; focus returned to `assistant-launcher`. The page title and header displayed mello. The user's main localhost tab was refreshed to the new build.
- The initial smaller floating circle still covered a phone history value, so that approach was revised before completion. The final button sits in the header, outside content. This visual check prevented claiming that reducing size alone solved overlap.

Evidence: [history and header](evidence/mello-history-oct27.jpg), [phone history](evidence/mello-history-phone-oct27.jpg), [per-message timestamps](evidence/mello-message-dates-oct27.jpg). These screenshots contain only the newly created fictional review conversation. No live-model inference, new full-duration timing run, acoustic check, recording, participant feedback or clinical result is claimed for this change. Prior voice/timing evidence remains dated separately.
