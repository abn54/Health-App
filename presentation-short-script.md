# mello — short presentation script

About 4 minutes of speaking, plus the 60-second exercise and brief clicks. Brackets are actions, not spoken text. Use fictional inputs only. This is a proposed script, not evidence that a presentation or recording has occurred.

[Show Practice.]

“This is **mello**, my IST 402 coursework skills prototype, built with Vue, FastAPI and SQLite on localhost. It offers short guided practices, an optional assistant and saved history. The coastal background is decorative. The app does not provide therapy, diagnosis or human monitoring.

“My example user is Alex, a fictional student preparing for an exam. The app uses explicit choices, such as text-only pacing and reply length. It does not detect Alex’s distress from clicks, text or past activity.”

[Open Your local profile. Choose Brief reminders, enable saved-practice context, and Save profile. Choose Text only and Remember this choice. Wait for confirmed saves; reload to show restoration.]

“These choices persist. I can change or reset them. Starting a practice simplifies the page to one current instruction. This addresses D1 and D2 through the selected activity, rather than an assumed emotional state. D5 and R4 inform the explicit, reversible personalization.”

[Show the three cards, then start breathing. Demonstrate Pause, Crisis support, Return and explicit Resume. Let all six cycles finish.]

“There are three practices: paced breathing, five-senses grounding and STOP. Breathing uses four counts in and six out, repeated six times at one second per count. Grounding follows five things seen, four felt, three heard, two smelled and one tasted. STOP means Stop, Take a step back, Observe and Proceed mindfully. Nothing needs to be typed.

“Each has an intended one-minute sequence, addressing R1’s attention constraint. Pause preserves my place; End stops immediately. Support stays available independently of the model, including after a request failure. Returning leaves the exercise paused. These choices address R2, R3 and D4. The summary separates measured exercise time, setup and explicit pauses.”

[Open Session history and select the new record.]

“History shows dates, last-chat times, conversations, the chosen skill, available timing and whether a session completed, stopped or was interrupted. I can reuse settings without automatically starting, or delete records. Saved-state labels reflect actual writes; failed writes offer Retry or an unsaved exit.”

[Return to Practice. Expand Accessibility options and demonstrate selected controls.]

“Access choices include higher contrast, larger text, a simpler font, more spacing, hidden scenery and reduced motion. Reduce motion overrides saved animation while keeping the rhythm. Screen-reader updates can announce steps, phases or counts, or be switched off. Keyboard navigation, visible focus and Escape support the dialogs. These choices address D3 and D6 without asking for disability information. Display options last for this visit; saved profile settings are separate.”

[Open the bottom-right assistant. Keep Prepared replies selected. Ask: “Can I stop halfway?” Expand Reply details. Then ask: “A fictional student is worried about an upcoming exam. What could they try?”]

“The controls answer uses my brief-reply preference and, with permission, factual saved breathing history. Everyday exam answers do not infer how I feel from that history. The tone acknowledges pressure without judgment and offers choices rather than commands.

“Suggested questions are optional. I can type my own words, browse FAQs and source links, or use optional reply voice with a voice choice, speed and Stop control. Visible text remains available; practices themselves have no app-generated audio.

“I’m demonstrating prepared replies. In live mode, a local model selects a topic from reviewed content. It cannot invent treatment advice, change steps or timing, save preferences or navigate. Unknown topics ask for clarification. Live attempts, including failures and retries, are capped at fifty per host session.”

[Show the report’s verification links. For the process section, show the existing process recording and the corresponding Escape/focus code.]

“Verification includes 22 fictional scenarios, three behavior checks, 67 backend tests and 22 client tests. The behavior checks cover independent support, fixed user-controlled skills and truthful persistence. Nine recent live selections matched their expected topics; those are separate from mocked tests. A fresh checkout also ran successfully.

“A surprising earlier finding was that valid model output could still select the wrong topic. Another observed failure left keyboard focus outside the assistant after Stop voice disappeared. The process recording shows that evidence and the fix: wait for Vue’s DOM update before restoring focus, and capture Escape even when focus reaches the page body. Real blind-user screen-reader testing and broad model accuracy remain unverified.”

## Demonstration notes

- If Reduce motion is on, turn it off before demonstrating an explicit switch to Animated circle. Turning it off alone does not restart animation.
- Saved-history tailoring is breathing-specific and applies to relevant app-help answers, including the controls prompt above; do not claim the exam response used a clinical profile.
- Do not say a live call happened while Prepared replies is selected. Show a separately labeled live result if demonstrating inference.
- The process recording and full-skill recordings are dated evidence. They show earlier interface details; current accessibility/conversation checks are linked separately in report.md.
- Show the failed-request evidence or use the isolated review setup for failure simulations. Do not claim a failure demonstration occurred if you only described it.
