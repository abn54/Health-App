# Part 3.3 recordings

October 31 revision: [coastal interface tour](coastal-tour-oct31.mp4) · [transcript](coastal-tour-oct31.md) · [captions](coastal-tour-oct31.vtt). This new silent, agent-operated browser recording shows the three practice cards, an intentionally stopped Grounding session, sole bottom-right assistant and skill-labeled History. It does not replace the separately measured full runs. The two videos below show the October 30 interface and unchanged breathing/focus behavior.

Two actual, silent browser recordings were made October 30, 2026, operated by the disclosed Codex assistant using fictional scenarios. They are not recordings of the student speaking or a peer test. Enable the embedded English subtitle track, use the `.vtt` captions, or read the linked full transcripts. Pause to inspect code or dense responses.

| Recording | Content | Accessible alternatives |
| --- | --- | --- |
| [Finished application — MP4](part3-demo.mp4) | Explicit profile save, cue override, uninterrupted full breathing exercise, completion/timing, dated History, personalized prepared answer, actual live selection, independent support, contrast/text options. | [Transcript](part3-demo.md), [captions](part3-demo.vtt), [timestamps/edit metadata](part3-demo.json) |
| [Process screencast — MP4](part3-process.mp4) | Reproduced Stop/Escape failure in baseline `49ea522`, corrected focus/Escape in final app, actual evidence, decision and generated Vue code explanation. | [Transcript](part3-process.md), [captions](part3-process.vtt), [timestamps/checks/edit metadata](part3-process.json) |

## Capture method and verification

These videos encode actual Cua task-tab screenshots sampled approximately twice per second within capture blocks; no app UI was reconstructed. H.264 holds/repeats those frames at 10 fps, which does not imply 10 fps source sampling. Idle gaps above three seconds **outside the full exercise** are shortened and listed in metadata; the uninterrupted exercise keeps original timestamp durations, including holds between capture blocks. The last frame is held 2.5 seconds. Recording duration is not the exercise timing measurement. No audio, microphone or private third-party browser content is included.

A native capture attempt did not produce a verified output file, so the submitted videos use the disclosed browser-frame method. Both final MP4s were fully decoded by FFmpeg without error, with sample frames inspected. Encoding tool: optional `imageio-ffmpeg` 0.6.0 / FFmpeg 7.1; [encoder](../../scripts/encode_browser_capture.py). Media tooling is not needed to run the app. The [local player](player.html) supports captions when served over HTTP; GitHub's raw MP4 links permit downloading without running the application.

## Student review before submission

Watch both videos, inspect the actual source, and be ready to explain why the watcher waits for Vue's `nextTick`, why the document listener uses capture, how close restores focus, and why neither change controls breathing timing. The process transcript explains the evidence and decision, but it does not certify the student's understanding or substitute for a requested personal presentation. Upload only the final root `report.md` to Canvas; the report links these files. No Canvas upload has been performed.
