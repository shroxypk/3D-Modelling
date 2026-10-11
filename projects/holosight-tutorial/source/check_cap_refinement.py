"""Dry-run the local edit in a separate Blender process; never saves a blend.

Writes a report and two candidate images for comparison with the committed
baseline. The candidate is temporary until its visual review is accepted.
"""
import hashlib
import importlib.util
import json
from pathlib import Path

import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'review' / 'case-study'
OUT.mkdir(exist_ok=True)
spec = importlib.util.spec_from_file_location('refine_cap', ROOT/'source/refine_cap.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
ob = bpy.data.objects.get('02 | Inner housing')
if ob is None or Path(bpy.data.filepath).resolve() != (ROOT/'Holosight.blend').resolve():
    raise RuntimeError('Load the working Holosight.blend first.')

def unaffected_faces():
    return sorted(tuple(sorted(tuple(ob.data.vertices[i].co) for i in f.vertices))
                  for f in ob.data.polygons
                  if not all(abs(ob.data.vertices[i].co.x-.483)<1e-7 for i in f.vertices))

before = unaffected_faces()
result = module.refine(ob)
assert unaffected_faces() == before, 'Geometry outside the cap-face plane changed'
result['outside_cap_faces_unchanged'] = True
result['second_pass'] = module.refine(ob)
assert result['second_pass']['merged_triangle_pairs'] == 0, 'Cleanup is not idempotent'
result['blend_sha256'] = hashlib.sha256((ROOT/'Holosight.blend').read_bytes()).hexdigest()
(OUT/'refinement-check.json').write_text(json.dumps(result, indent=2)+'\n')

# Match the existing cap review camera; temporary scene overrides only.
s=bpy.context.scene
s.render.engine='BLENDER_WORKBENCH';s.view_settings.view_transform='Standard'
s.render.resolution_x=1000;s.render.resolution_y=800;s.render.resolution_percentage=100
s.render.image_settings.file_format='PNG'
s.display.shading.light='STUDIO';s.display.shading.color_type='OBJECT';s.display.shading.show_cavity=True
s.display.shading.background_type='WORLD';s.world=bpy.data.worlds.new('Temporary review');s.world.color=(.045,.045,.045)
for obj in s.objects:
    if obj.name.startswith('01 |') or obj.name.startswith('00 |'):obj.hide_render=True
data=bpy.data.cameras.new('Review');cam=bpy.data.objects.new('Review',data);s.collection.objects.link(cam);s.camera=cam
data.type='ORTHO';data.ortho_scale=.65;target=Vector((.435,.735,.230))
cam.location=target+Vector((3,2,1));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
s.render.filepath=str(OUT/'candidate-model.png');bpy.ops.render.render(write_still=True)
cu=bpy.data.curves.new('Review wires','CURVE');cu.dimensions='3D';cu.bevel_depth=.0007;cu.bevel_resolution=0
for edge in ob.data.edges:
    sp=cu.splines.new('POLY');sp.points.add(1)
    for point,idx in zip(sp.points,edge.vertices):point.co=(*(ob.matrix_world@ob.data.vertices[idx].co),1)
wire=bpy.data.objects.new('Review wires',cu);s.collection.objects.link(wire);wire.color=(.008,.008,.008,1)
s.render.filepath=str(OUT/'candidate-topology.png');bpy.ops.render.render(write_still=True)
print('REFINEMENT_CHECK',result)
