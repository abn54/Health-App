# mello — quiet coast revision, October 31, 2026

The student asked for the assistant only at the bottom right, more exercises, a professional layout and a location background fitting “mello.” This revision keeps the localhost/coursework scope. The October 30 report and videos remain evidence of their pinned version, not recordings of this newer interface.

## Design and behavior

The top bar now has **Practice**, **Session history**, and independent **Crisis support**. Both the top AI-assistant destination and the embedded conversation panel were removed. A single bottom-right Ask mello button opens the existing accessible popup, with optional chatbot-only voice and a persistent composer. Its reserved page padding prevents the circle from covering the final content. The popup still pauses any active practice and requires explicit Resume on return.

A quiet coastal cove provides the scenic backdrop: soft seafoam water, misty headlands and warm sand. Solid task cards, dark green actions and restrained spacing support reading. Higher contrast removes the decorative hero image. All imagery is local, static, decorative, and has no role in determining a person's state. No sound or animated scenery was added.

Three direct Start cards offer:

- **Paced breathing:** the original four-count inhale / six-count exhale, six cycles, one second/count. The original engine and breathing sequence are unchanged.
- **5–4–3–2–1 grounding:** see five, feel four, hear three, smell two, taste one, in that order, twelve seconds per step.
- **STOP:** Stop; Take a step back; Observe; Proceed mindfully, fifteen seconds per step.

The latter two sequences come from the supplied assignment overview. Their instructions live in `shared/exercises.json`, outside model authority. Each guide has a 60-second intended pace, no required typing, Pause for more time, immediate End, independent support and interruption handling. Recalled sensory examples are an explicit access adaptation when a sense is unavailable; physical movement is not required in STOP. These are interface choices, not clinical efficacy claims or a blind-user evaluation.

## Persistence and model boundaries

`GuidedExercise` inherits the existing monotonic clock, pause, exit and interruption rules and replaces only the displayed step lookup. No separate interval/count source was introduced. Existing SQLite snapshot records accept two additional allowlisted content versions; no schema migration or destructive data rewrite is needed. Started-session content identity is immutable. History names the actual skill and preserves status, dates, events, timing and deletion. Legacy records still default to breathing.

The explicit reply profile remains shared by the local host. Its saved cue/last-practice tailoring is now labeled **breathing** and filters to breathing records, so a new grounding/STOP outcome cannot be misrepresented as a breathing result. Other skills still appear in History. This avoids silently expanding the profile while keeping the established opt-in controls.

Catalog `app-help-v6` and prompt `catalog-selector-v12` add one approved `skills` topic. Both mock and live paths can select it; neither can author new skill instructions or operate navigation/timing. Prepared replies remain the default. Context is approved app facts/current question, not raw history. Clinical-role limits, the independent support route and the host cap of at most 50 attempts remain.

## Verification and limits

[Actual browser cases](evidence/coast-browser-oct31.json), [selected actual timing/database evidence](evidence/coast-timing-oct31.json), [22 deterministic scenarios](evidence/coast-mocked-oct31.json), and [selected repeated live results](evidence/coast-live-oct31.json) are separate evidence types. Final actual results: **44 backend tests**, **21 client tests**, production build and **22/22 mocked scenarios** passed. Grounding completed in **60.0111s** (setup recorded separately, no pause); STOP in **60.0131s** active time (**77.5162s** wall, **17.5031s** explicit pause/support/history excluded once). Exact setup values are in the JSON. STOP retained its second step through support/history and required Resume. Browser cases verify one launcher, no top/inline assistant, reviewed new-skill answer, keyboard Escape and390/320px layouts without horizontal overflow. Larger text/higher contrast fit320px and removed the hero image.

Nine actual local selections (three authored questions × three repeats) chose skills/skills/about as expected in all9 cases, with no within-group topic variation. One counted preload gives10/50 attempts in the isolated coast-oct31 ledger. This small selection does not resolve the earlier role-topic failure or establish broad model reliability.

[Selected axe-core4.14.0 scans](evidence/coast-a11y-oct31.json) detected zero violations on the revised Ready and paused STOP screens; color-contrast checks marked incomplete are retained. An initial generic-container naming issue led to explicit region/group roles before retest. Automated scans do not certify contrast throughout photographs, WCAG conformance or real assistive-technology use.

The initial backend test run reported seven failures: five pinned the prior catalog version and two pinned prior breathing-context wording. The observed responses had the intended new v6 version and more specific breathing label. The assertions were updated to the revised copy contract, retaining semantic/state checks; the next run passed. No failed result was recast as a successful original run.

R1 still informs the one-minute guides; D2 is balanced against R4 by offering three choices on Ready but only one step during practice. D3 keeps chat, disclosure and written responses optional. D5/R4 remain explicit, reversible choices; D1 adaptation uses chosen activity, not detected distress. D6 motivates restrained static imagery, silent practice, reduced motion, and redundant words. R2/R3/D4 preserve support and exit. More choices add some entry effort; cognitive reframe remains excluded because it would require a different input/verification flow.

Real assistive-technology/blind-user testing, broader browsers, multi-tab reconciliation, natural voice-quality listening and clinical effectiveness remain untested. The [new coastal tour](recordings/coastal-tour-oct31.mp4) shows this revision and intentionally ends a practice early; it is not a full-duration timing run. Its captions/transcript disclose the actual browser-frame capture method. Original October 30 recordings show the previous layout and remain relevant to unchanged breathing and the focus fix. This revision’s screenshots and records are labeled October 31. No deployment or external support contact occurred.

## Background asset and generation disclosure

Built-in image-generation tool (model/build identifier not exposed), generated October 31. Saved project asset: `frontend/src/assets/mello-coast.png`. No stock photo or recognizable real location is asserted.

Final prompt: “Use case: photorealistic-natural. Asset type: wide landscape background for mello, a calm, professional coursework skills web app. Primary request: original tranquil coastal cove at early morning, a soft pale-sand beach curving along a sheltered sage-teal sea, low distant misty headlands, gentle tiny waves and sparse dune grass. No people or buildings. Wide cinematic 16:9 editorial landscape photography, natural textures, restrained soft seafoam, warm sand and muted blue-grey, soft diffuse dawn light with a warm horizon, peaceful spacious mood. Compose broad quiet open water and sky, shoreline lower right, low-detail negative space at left for dark UI overlay. No text, letters, logos, interface elements, watermark, dramatic cliffs, vivid sunset or excessive contrast.”
