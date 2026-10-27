# Visual redesign — October 27, 2026

User request: “change the ui, layout and colors of the web app.” The earlier naming discussion did not select a replacement, so the name remains Pause.

## Current appearance and layout

The former dark green sidebar becomes a sticky horizontal navigation bar. The same Crisis support control now lives in that bar, beside Practice, AI assistant and Session history; phones use a second navigation row. Its ID, handler and independent client-shell support route are preserved.

The palette uses warm ivory `#fcf8f2`, terracotta `#a74f3b`, soft lavender `#ede5f4` and restrained sage/blue phase cues. Headlines use the system Georgia serif; controls and body use system sans-serif. Original SVG artwork provides a flower wordmark and a still landscape/stacked-stone illustration. No network fonts, image generation, third-party image assets or new dependencies are used. The unconfirmed replacement names and former registration symbol are not applied.

Ready now has a split introduction, a prominent lavender practice card, a separate cue-setting card, and a smaller neutral note. The practice card separates the Start action from the illustrative circle and rhythm guide. Intermediate-width panes stack the practice card above settings, avoiding a narrow tall card. FAQs, sources, history, summary, assistant popup and support dialog share the new typography, rounded shapes and palette. Decorative hero content appears only on Ready; active practice remains a single current instruction.

The breathing engine, skill steps, one-second counts, state transitions, API, database schema, model/catalog, preferences and attempt budget are unchanged. No new therapy, diagnosis, monitoring, stress inference or personalization behavior is added.

## Actual verification

- Production build succeeded: [current output](evidence/redesign-build-oct27.txt). The existing six client tests passed: [actual output](evidence/redesign-client-tests-oct27.txt). No new tests were written for presentation-only changes. Backend tests and live model checks were not rerun for this redesign; earlier results remain dated evidence.
- Actual browser review covered the regular in-app pane, 1280×800 desktop and 390×844 phone CSS viewport. The initial intermediate-width navigation overflowed slightly; reduced padding/gaps and a stacked medium layout resolved the observed issue. The phone document width and viewport width both measured 390 pixels. Temporary viewport override was reset.
- At 1280×800, the Start button bounds were y=681.58–727.58. During active practice End measured y=553.78–599.78 and Crisis support y=23.25–63.25. At 390×844, End measured y=509.70–555.70 and Crisis support y=13–48. These checks establish those observed layouts, not all possible sizes or assistive technologies.
- The phone's remembered Text only cue restored without changing the saved preference. Start, popup opening, disabled active question input, popup Crisis support, return still Paused at inhale count 1, immediate End and Saved locally were observed. The partial session was shown as Stopped, not Completed. No real support service was contacted.
- Selected foreground/background contrast calculations: primary 5.29:1, body 5.10:1, lilac-card small label 4.54:1, selected FAQ filter 5.36:1, prototype notice 5.04:1. These are selected palette checks, not comprehensive accessibility certification. Focus outlines, labels, redundant phase words/counts and reduced-motion rules remain.

[Current regular-pane screenshot](evidence/redesign-ready-oct27.jpg) · [desktop](evidence/redesign-desktop-oct27.jpg) · [phone](evidence/redesign-mobile-oct27.jpg) · [exercise](evidence/redesign-exercise-oct27.jpg) · [popup](evidence/redesign-popup-oct27.jpg). Full-page screenshots can place sticky controls at the capture's current scroll position; the measured viewport bounds above describe their actual on-screen positions.

## Timing evidence and limits

An attempted new full-duration observation lost its isolated browser tab before completion. Read-only SQL showed Running with no final timing; API recovery then marked Interrupted with unknown final duration. [Actual interrupted record](evidence/redesign-interrupted-run-oct27.json). It is not a successful timing run and is not excluded as a voluntary pause. No new full-duration result is claimed for this visual revision.

The prior actual 60.016600-second run remains dated [October 27 refinement evidence](ui-refinement-oct27.md); the unchanged monotonic engine retains six passing injected-clock tests. The phone Start/paused return/End workflow is a separate partial-session observation. Broader accessibility, all viewport sizes, independent clean-checkout validation, repeated live variation and Part 3.3's full evaluation/recordings remain outside this visual change.
