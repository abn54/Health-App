# part3-process — accessible transcript

Actual Cua browser-tab screenshots sampled approximately every 500 ms within capture blocks; silent. No UI reconstruction or synthetic app frames. H.264 repeats held frames at 10 fps; original motion sampling is ~2 fps.

Outside the uninterrupted exercise, gaps over 3 seconds are shortened to 3 seconds. Within the exercise all timestamp gaps are retained, holding the last captured frame. Last frame held 2.5 seconds. Enable English subtitles; full transcript accompanies video.

**00:00:00.000** — Baseline before fix: clean checkout 49ea522 on port 8002. Fictional app question; prepared reply.

**00:00:08.892** — Failure reproduced: Stop removed its focused button; Escape left the popup open. Inspect focus and event scope.

**00:00:12.496** — Revised application: restore focus after speech stops and capture Escape while a dialog is open.

**00:00:16.955** — Retest passes: focus stayed on Read replies; Escape closed the popup and returned to the launcher.

**00:00:19.544** — Evidence and diagnosis: BODY focus bypassed the local popup keydown handler. A profile reset behind the still-inert popup had not reached the database.

**00:00:24.573** — Generated code: the watcher waits for Vue DOM updates before restoring lost focus. A document capture listener receives Escape and calls the existing close function. Timing and model control are unchanged.
