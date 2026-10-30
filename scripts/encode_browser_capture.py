"""Encode actual Cua tab frames, retaining timestamps and disclosing idle edits.

Optional tool: imageio-ffmpeg from PyPI; never used to operate the browser.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import imageio_ffmpeg


def stamp(seconds):
    ms = round(max(0, seconds) * 1000)
    return f'{ms // 3600000:02}:{ms // 60000 % 60:02}:{ms // 1000 % 60:02}.{ms % 1000:03}'


p = argparse.ArgumentParser()
p.add_argument('capture', type=Path)
p.add_argument('output', type=Path)
a = p.parse_args()
data = json.loads(a.capture.read_text())
frames = data['frames']
start = frames[0]['at']
exercise = next((x['at'] for x in data['events'] if x['text'].startswith('Guided skill:')), None)
finished = next((x['at'] for x in data['events'] if x['text'].startswith('Completed:')), None)
timeline = []
cuts = []
elapsed = 0
lines = ['ffconcat version 1.0']
for i, frame in enumerate(frames):
    gap = (frames[i+1]['at'] - frame['at']) / 1000 if i + 1 < len(frames) else 2.5
    protected = exercise is not None and exercise - 1000 <= frame['at'] <= finished
    duration = gap if protected else min(gap, 3.0)
    if duration != gap:
        cuts.append({'after_frame': i, 'original_gap_seconds': gap, 'retained_seconds': duration})
    timeline.append({'at': frame['at'], 'video_seconds': elapsed, 'duration_seconds': duration})
    file = (a.capture.parent / frame['file']).resolve()
    lines += ["file '" + str(file).replace("'", "'\\''") + "'", f'duration {duration:.6f}']
    elapsed += duration
lines.append(lines[-2])
concat = a.capture.parent / 'frames.ffconcat'
concat.write_text('\n'.join(lines) + '\n')

def position(at):
    for i in range(len(timeline)-1, -1, -1):
        if timeline[i]['at'] <= at:
            return timeline[i]['video_seconds'] + min((at-timeline[i]['at'])/1000, timeline[i]['duration_seconds'])
    return 0

chapters = [{**e, 'video_seconds': position(e['at'])} for e in data['events']]
vtt = ['WEBVTT', '']
for i, e in enumerate(chapters):
    end = chapters[i+1]['video_seconds'] if i+1<len(chapters) else elapsed
    if end <= e['video_seconds']: continue
    vtt += [f"{stamp(e['video_seconds'])} --> {stamp(end)}", e['text'], '']
a.output.parent.mkdir(parents=True, exist_ok=True)
a.output.with_suffix('.vtt').write_text('\n'.join(vtt))
subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-hide_banner', '-loglevel', 'error', '-y', '-safe', '0', '-f', 'concat', '-i', str(concat), '-i', str(a.output.with_suffix('.vtt')), '-map', '0:v:0', '-map', '1:0', '-vf', 'scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2:color=white', '-r', '10', '-c:v', 'libx264', '-preset', 'medium', '-crf', '23', '-pix_fmt', 'yuv420p', '-c:s', 'mov_text', '-metadata:s:s:0', 'language=eng', '-disposition:s:0', 'default', '-movflags', '+faststart', str(a.output)], check=True)
metadata = {'capture_method': 'Actual Cua browser-tab screenshots sampled approximately every 500 ms within capture blocks; silent. No UI reconstruction or synthetic app frames. H.264 repeats held frames at 10 fps; original motion sampling is ~2 fps.', 'editing': 'Outside the uninterrupted exercise, gaps over 3 seconds are shortened to 3 seconds. Within the exercise all timestamp gaps are retained, holding the last captured frame. Last frame held 2.5 seconds. Enable English subtitles; full transcript accompanies video.', 'source_capture_duration_seconds': (frames[-1]['at']-start)/1000, 'video_duration_seconds_planned': elapsed, 'captured_frame_count':len(frames), 'largest_source_gap_seconds': max((frames[i+1]['at']-frames[i]['at'])/1000 for i in range(len(frames)-1)), 'idle_edits': cuts, 'chapters':chapters, 'checks': data.get('checks',[]), 'video_sha256':hashlib.sha256(a.output.read_bytes()).hexdigest(), 'ffmpeg_version': imageio_ffmpeg.get_ffmpeg_version()}
a.output.with_suffix('.json').write_text(json.dumps(metadata, indent=2)+'\n')
a.output.with_suffix('.md').write_text('# '+a.output.stem+' — accessible transcript\n\n'+metadata['capture_method']+'\n\n'+metadata['editing']+'\n\n'+'\n\n'.join(f"**{stamp(e['video_seconds'])}** — {e['text']}" for e in chapters)+'\n')
print(json.dumps({'file':str(a.output), 'frames':len(frames), 'duration_seconds':elapsed,'bytes':a.output.stat().st_size,'idle_edits':len(cuts)}))
