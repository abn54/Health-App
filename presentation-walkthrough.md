# mello — presentation walkthrough

Prepared October 28, 2026 for the four equally weighted presentation criteria supplied by the student. This is a suggested demonstration/script, not a recording or a guaranteed grade. Use the running app at <http://127.0.0.1:8000/>. Allow roughly 6–8 minutes if your instructor has not specified a different length; one full breathing run needs about a minute.

## Before presenting

Use fictional inputs only. **Alex** is a fictional college student preparing for an imagined class presentation. Alex prefers less movement and short explanations, may stop partway through an exercise, and wants to control what is remembered. This is a design persona, not a participant or diagnosis. The app stores choices and activity; it does not invent Alex’s emotions or save a name/biography.

Keep Reply mode **Mock** for a repeatable demonstration and say that explicitly. A real local model is optional, configured separately; do not call a mock an AI inference. Keep voice off unless you plan to demonstrate it and have checked the device’s voice/volume. Do not contact any support service while demonstrating the support panel.

Avoid deleting existing coursework records to prepare. If you need a clean fictional demonstration database, use a separate ignored SQLite path through `PAUSE_DB` when launching a dedicated localhost host. The default app has one shared local profile, not authenticated accounts for multiple people.

## 1. User state and interface adaptation — 25 points

**Show:** On Practice, choose **Text only**, select **Remember this choice**, and wait for **Preference remembered**. Expand **Your local profile**, choose **Brief reminders**, enable **Use my cue and saved practice history in replies**, then **Save profile**. Wait for the confirmed save status. Reload: the saved cue and profile should restore. Show the same settings can be reset or changed.

**Say:** “mello uses explicit choices: the current pacing cue, a remembered cue, reply length and an optional permission to use factual practice history. It also reads the device’s reduced-motion setting as the initial cue when no preference is saved. It does not detect distress from typing, clicks, a questionnaire or physiological data. Choosing Text only removes the moving circle; Brief reminders selects shorter reviewed answers. Start simplifies the page to the current breathing instruction. These changes follow chosen activity and preferences, not an assumed clinical state.”

**Show the override:** During the exercise, use **Pacing cue → Animated circle**. The phase/count continues from the same point. That changes this visit/session; it does not overwrite the remembered Text only choice. Return/reload after the session to demonstrate restoration, or point to the retained remembered-setting label. **Reset preference** restores the system default. **Reset profile** independently restores standard replies and turns saved context off. A new practice still requires Start.

**Explain the assumption:** One local profile belongs to whoever uses this localhost host. A reduced-motion preference is an accessibility signal, not proof of an emotional state. History records actions/outcomes, not usefulness or symptom change.

## 2. Skill walkthrough and research grounding — 25 points

**Show a complete run:** Start directly, without a question. Walk through **four one-second inhale counts, six one-second exhale counts, repeated six times**. Allow the full planned sequence to finish and show the neutral Completed summary and actual measured duration/save status. You can explain the following while it runs.

| Finding | What to point to | Reason/tradeoff to explain |
| --- | --- | --- |
| R1 | Six 10-second cycles, no typing or model wait inside pacing | The supplied study favored roughly 60 seconds and reported attention loss beyond 90–100 seconds. App/render delays are included in measured duration. |
| D1 / D2 | Practice cards contract into one current phase/count | The chosen activity simplifies the interface. No distress detector is claimed. Shell navigation/support remain as a deliberate user-control tradeoff. |
| R2 / D4 | Sticky **Crisis support** control | The panel is bundled with the page and opens independently of the model/API after initial load. |
| R3 / R4 | **Pause**, **Resume**, **End exercise** | The user can leave without penalty. Returning from support/history does not automatically resume. |
| D3 / D6 | No required story/rating; neutral colors/outcomes; Text only | Less disclosure/reading effort and no pressure to prove that the exercise helped. |
| D5 with R4 | Remember, profile Save/Reset and explicit history cue reuse | Prior choices reduce repeat setup, with an explicit action instead of hidden adaptation. |

**Demonstrate stop/support separately:** Start a second short run, override to Animated circle if useful, open **Crisis support**, and return. Show **Paused** and the separate Resume choice. Select **End exercise**. Explain that Stopped is a partial session, not Completed, and is not described as personal failure. You need not finish this second run.

**Say:** “The study’s R/D mention counts are design observations, not proof of clinical benefit. The model cannot change this sequence, timing, preferences or navigation. The Kaggle resource informed intent/pattern organization from a limited preview; it was not training data or a substitute for the instructor’s research table.”

Full source mapping: [docs/research-findings.md](docs/research-findings.md). The instructor overview link could not be opened through the web tool; the supplied October 21 table and this pasted presentation rubric are the project’s assignment sources.

## 3. User persona, interaction choices and accessibility — 25 points

**Show persistence and history:** Open Session history after the stopped run. Point to Started/Last chatted, recorded outcome, initial/final cue, actual available timing, and saved conversation. Completed, Stopped, Interrupted and Not started are distinct. No-chat sessions say so. Reopen Practice and expand Your local profile: its most recent saved practice now describes the stopped run and last recorded cue, if context is enabled.

**Concrete personalization:** Reload so remembered Text only returns. Expand Your local profile and select **Use last practice cue for this visit**. If the latest run used Animated circle, that cue is copied for review without starting practice or overwriting Text only. This demonstrates profile plus usage history changing the UI. The user can override it again. No follow-up is imposed.

**Say:** “Alex’s local profile is deliberately small: remembered cue, reply length and a context permission. SQLite persists those explicit choices. Saved sessions provide factual history. Only successful saves count; failure messages mean the app cannot confirm a change. Profile reset keeps history and cue; deleting a session removes its events/messages; confirmed Delete all resets history, cue and profile. Old conversation replies keep the context they actually used at the time.”

**Show interaction/accessibility choices:** Named keyboard controls and visible focus; Escape closes the assistant and restores the circular launcher’s focus. Words and counts duplicate phase colors. Text only removes pacing motion; system reduced-motion supplies the initial default. Breathing has no app-generated audio. Accessibility options provide Phase and cycle / Each count / Off for a user’s own screen reader; announcements may lag, and Pause/End remain available. Chatbot-only read-aloud is optional, blue Play/Preview and red Stop also have labels/symbols, and automatic reading is off after reload. Higher contrast and Larger text are optional. Enhanced voice-name options rank first when installed; sound quality depends on the device. No microphone/voice recognition is required. Narrow layouts keep the small assistant circle in the header, outside page text.

**State the limit:** Keyboard/narrow-layout checks are development observations. Do not claim comprehensive screen-reader, sensory-accessibility or clinical validation. Voice availability and device volume vary.

## 4. Chatbot tone and limits — 25 points

**Show a tailored response:** With Brief reminders and saved context on, ask **“Can I stop halfway?”** after the stopped run. With Animated circle current, Text only remembered, and the last run stopped with Animated circle, the approved reply includes:

> “Your current cue is Animated circle. Your remembered cue is Text only; you can override it without changing the saved choice. Your latest saved practice was stopped. A fresh start is optional; finishing is not required.”

This is app-authored copy, not a quotation from research. The exact context sentences depend on the real saved record. Do not say the run was stopped if the latest record is Completed or Interrupted. Show the **Brief reply · Explicit profile + saved practice context** label. These sentences were observed in the October 28 fictional browser check.

**Explain the tone:** “The wording describes the recorded action without judgment. It offers an optional fresh start and does not congratulate, shame, diagnose or promise improvement. The user controls whether history is referenced. Reset profile, then ask the same question: new replies return to the standard explanation without that practice context. Earlier replies remain honest historical records.”

**Show the boundary:** Ask **“Can you be my therapist?”** The reply describes an educational coursework assistant, says it is not a therapist, and refuses diagnosis, treatment and monitoring. Point to the permanent fictional-coursework notice and independent Crisis support control.

**Explain the model’s role accurately:** “In Mock, deterministic matching selects an approved topic. In optional Live local model mode, Ollama `qwen2.5:3b` interprets the current question and selects an allowed topic ID. It does not write arbitrary displayed advice. A reviewed local rendering layer applies the saved reply-length choice and optional factual practice context. The model does not receive raw history or the profile. Current prompt/catalog are `catalog-selector-v10` / `app-help-v4`; a live therapist request still selected the general limits topic, so both limits answers explicitly state that the app is not a therapist. This is a documented relevance limit, not a claim the prompt solved it. This is chatbot personalization, with the application controlling it rather than asking a model to infer a persona.”

“Invalid output or a failed optional request produces a fixed fallback. Live attempts, including failures/retries, are capped by a host ledger at 50. A valid ID can still be an irrelevant choice; schema validation is not semantic accuracy or clinical safety. The skill and support work without waiting for a model response.”

## Presenter check before ending

Make sure the audience has actually seen preference restore **and override**, one complete skill, separate stop/support behavior, saved history influencing a visible UI choice, a profile/history-tailored reply, reset/opt-out behavior and the honest assistant boundary. An explanation alone does not replace the running demonstration. No grade is predicted here.

This file is presentation preparation. It does not claim that the presentation, screen recording, process screencast, independent checkout or complete Part 3.3 evaluation has been performed. Consult the separate submission instructions for recording/upload requirements; this four-point rubric alone does not specify them.


Current October 28 popup layout: open the bottom-right circle. The rounded composer stays visible below the scrollable conversation; Send or Enter submits, Shift+Enter adds a line. Toggle Read replies for optional spoken output, with Stop while playing. Expand Reply & voice options for the existing voice/speed and mock/live controls. This is reply playback, not microphone dictation or a live voice conversation.
