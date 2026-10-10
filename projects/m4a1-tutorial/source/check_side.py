import bpy
from pathlib import Path
from mathutils import Vector
P=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(P/'M4A1.blend'))
s=bpy.context.scene; c=s.camera
t=Vector((-.025,0,.025)); c.location=t+Vector((0,-20,0)); c.rotation_euler=(t-c.location).to_track_quat('-Z','Y').to_euler()
c.data.ortho_scale=15.65
s.render.resolution_x=1565; s.render.resolution_y=245; s.render.film_transparent=True
s.render.filepath=str(P/'review'/'side-check.png'); bpy.ops.render.render(write_still=True)
