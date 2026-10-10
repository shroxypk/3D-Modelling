"""Local frame extraction, at explicit tutorial times. Does not modify source media."""
import bpy, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'review' / 'tutorial-frames'
OUT.mkdir(parents=True, exist_ok=True)
video = next((ROOT.parents[1] / 'vids').glob('Holosight*Ep.1 7.mp4'))
scene = bpy.context.scene
scene.sequence_editor_clear()
strip = scene.sequence_editor_create().strips.new_movie('Tutorial', str(video), channel=1, frame_start=1)
scene.render.fps = round(strip.fps)
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 70
scene.render.image_settings.file_format = 'PNG'
scene.render.use_sequencer = True
scene.view_settings.view_transform = 'Standard'
times = [int(t) for t in sys.argv[sys.argv.index('--')+1:]] if '--' in sys.argv else range(10, 231, 10)
for sec in times:
    scene.frame_set(1 + sec * scene.render.fps)
    scene.render.filepath = str(OUT / f'{sec:04d}.png')
    bpy.ops.render.render(write_still=True)
print('REVIEWED SOURCE METADATA', strip.fps, strip.frame_final_duration)
