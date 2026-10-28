# Optional voice and sound — October 27, 2026

**Historical feature snapshot.** The October 28 user request removes all app-generated breathing speech/tones and keeps voice in the chatbot only. [Current accessibility/voice update](accessibility-update-oct28.md) supersedes the breathing-audio controls described below; this dated evidence is preserved.

The requested addition is implemented within the Part 3.2 localhost prototype. It does not add a skill, therapy, microphone input, an audio recording or a hosted service.

## Controls and behavior

- **Voice & sound** in Ready and the active exercise: Off / Spoken inhale–exhale / Soft tones. Pick an on-device English voice; Preview is available outside practice. Tones rise for inhale and fall for exhale, once per phase, rather than counting aloud.
- The full-page assistant and popup share **Reply voice**, **Read new replies aloud**, and each confirmed assistant message's **Read reply aloud**. Mock/live/fixed source labels remain visible. Only approved reply text is spoken, not fictional user questions, citations or provider metadata.
- **Stop audio** cancels playback and switches breathing sound and automatic reply reading off. Both default off after reload. Voice/settings are page memory, not silently remembered in SQLite.
- Start cancels assistant speech. Pause, End/completion, support, route changes, popup close, hidden page and page exit cancel output. Resume and changing sound mid-phase wait for the next phase boundary. A pending response cannot begin automatic speech after cancellation/navigation.
- The original visible instructions, 4 counts in / 6 out × 6 cycles, text-only/reduced-motion option, immediate End, truthful saves and independent shell Crisis support remain available. Audio does not drive, await, reset or extend the exercise timer.

Implementation: `frontend/src/audio.js`, `VoiceSettings.vue`, the shared assistant panel and App lifecycle integration. No new dependencies, API route, database migration, prompt/catalog version, paid TTS call or recording permission was introduced. Voices are filtered by the browser's local English metadata. Browser-reported local processing is not a platform security audit; browser/device volume and playback remain outside this app's control.

## Actual verification

Fictional inputs only; Codex in-app browser on this Mac. Samantha (en-US) was selected for the complete run; Daniel (en-GB) was subsequently selected and its Preview reported start/finish, and the assistant showed the same selection. Browser speech events demonstrate the browser reporting playback; no human listening or recorded sound-quality assessment is claimed.

| Check | Expected | Observed |
| --- | --- | --- |
| Six-cycle spoken exercise | Exactly 12 alternating phase starts; completion independent of speech | Six Inhale and six Exhale `onstart` observations, no duplicate count cues or late-start errors; Completed, Saved locally. **60.016200 s** exercise/wall, **0 s** excluded, **0.500500 s** setup. |
| Optional assistant auto-read | New confirmed mock reply read only after opt-in | Fictional “How long is the exercise?” displayed the approved mock answer, speech start then finish. |
| Manual reply / Stop | Explicit read starts; Stop disables automatic output | Manual read started; Stop reported output stopped and the checkbox became unchecked. |
| Support during reply | Immediately cancel speech; support remains independent | Manual reply start followed by support cancellation; support dialog and Return were available. No real service was contacted. |
| Soft tones + Pause/Resume/End | Inhale/exhale tones, no replay on mid-phase resume, immediate exit | Both phase tone states observed. Pause stopped output; Resume followed by End produced a Stopped partial record (6.30 s displayed), not Completed; no extra phase cue between Resume and End. |
| Phone popup (390 × 844) | Voice/read/Stop/close/support controls usable without horizontal overflow | Mock reply and manual read worked; document width and scroll width both 390. Controls remained within scrollable popup; Close/support stayed in header. |
| Keyboard popup exit | Tab wraps within popup; Escape restores launcher focus | Tab from footer Close focused header Close; Escape closed the popup and restored `assistant-launcher`. |
| Reload defaults | Audio choices not persisted | Breathing sound Off and auto-read unchecked after reload. Existing remembered text cue remained unchanged. |
| Repeatable tests | Cancellation, unavailable/late speech and original timing stay correct | **17 client tests passed** (11 audio + original 6); **21 backend tests passed**; production build succeeded; `git diff --check` clean. Existing Starlette TestClient deprecation warning retained. |

Evidence: [speech events](evidence/voice-breathing-oct27.txt), [exact persisted timing](evidence/voice-timing-oct27.json), [assistant playback/cancellation](evidence/voice-assistant-oct27.txt), [selected tone/stop observations](evidence/voice-tone-stop-oct27.txt), [settings screenshot](evidence/voice-settings-oct27.jpg), [phone popup screenshot](evidence/voice-assistant-phone-oct27.jpg). The assistant event file's first preview was still labeled “Reading assistant reply aloud”; Preview now has distinct playing/finished labels, subsequently checked with Daniel. Status timestamps are rounded page-relative diagnostic milliseconds, not replacement measurements of assignment duration. Only the newly created fictional completed session's selected fields were exported; existing workspace history/database were not published.

## Revised approach and limits

The first browser Preview failed with `TypeError: Illegal invocation`: assigning native timer functions directly as controller methods changed their receiver. Explicit timer wrappers fixed this. Initial injected-fake tests did not catch the native-browser binding issue; the actual browser check did. The corrected preview, automatic/manual reply playback and entire exercise were then verified. A read-only SQL extraction initially assumed timing columns; this schema stores a JSON snapshot, so the corrected extraction read selected fields from that snapshot. Neither failed attempt is counted as successful evidence.

Unavailable voices, voice-discovery exceptions, rejected voice objects, speech errors, blocked/late startup, stale callbacks and missing/blocked Web Audio are deterministic fake-API cases, not claims that every platform/browser was tested. A startup watchdog cancels speech that does not start (900 ms for a phase, four seconds for a reply); a phase also validates current cycle/phase and age before speaking. No timing waits on those watchdogs. Only this Mac/browser's available voices and the listed scenarios were observed; screen-reader certification, acoustic quality, all voice variants, independent checkout and Part 3.3 evaluation/recordings remain unclaimed. No new live-model inference was needed; the existing model/prompt/catalog remain `qwen2.5:3b` / `catalog-selector-v8` / `app-help-v2`.

Primary API references: [SpeechSynthesis queue/cancellation/voice discovery](https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesis), [utterance start/end/error events](https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesisUtterance), [browser-reported localService](https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesisVoice/localService). These describe browser APIs, not clinical evidence.
