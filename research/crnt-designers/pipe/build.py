"""CRNT pipe fitting study: opening body, joined branches, bore cleanup and supports."""
import bpy,bmesh,math,json
from pathlib import Path
from mathutils import Vector
R=Path('C:/Users/Dell/Downloads/3D/research/crnt-designers/pipe')
# The tutorial starts with 32 radial sides on the main tube.
# Neck radius 1, height 2, flange radius 2, flange thickness .3.
profile=[(2,0),(2,.3)]
for k in range(5,-1,-1):
 t=k*math.pi/12;profile.append((2-math.cos(t),1.3-math.sin(t)))
profile += [(1,1.533333),(1,1.766667),(1,2),(.8,2),(.8,.3),(.8,0)]
vs=[(r*math.cos(i*math.tau/32),r*math.sin(i*math.tau/32),z) for r,z in profile for i in range(32)]
fs=[]
for j in range(len(profile)):
 for i in range(32):fs.append((j*32+i,j*32+(i+1)%32,((j+1)%len(profile))*32+(i+1)%32,((j+1)%len(profile))*32+i))
o=bpy.data.objects.get('Pipe')
if o is None:
 me=bpy.data.meshes.new('Pipe');o=bpy.data.objects.new('Pipe',me);bpy.context.scene.collection.objects.link(o)
me=bpy.data.meshes.new('Pipe flange and bore');me.from_pydata(vs,[],fs);me.update()
bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me)
report={'stage':'00:24 flared body and main bore','vertices':len(bm.verts),'faces':len(bm.faces),'nonquads':sum(len(f.verts)!=4 for f in bm.faces),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges)};bm.free()
old=o.data;o.data=me
if old.users==0:bpy.data.meshes.remove(old)
o.show_wire=True;o.show_all_edges=True
bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
for a in bpy.context.screen.areas:
 if a.type=='VIEW_3D':
  rv=a.spaces.active.region_3d;rv.view_location=(0,0,1);rv.view_distance=6;rv.view_rotation=Vector((-5,-7,4)).to_track_quat('Z','Y');rv.view_perspective='ORTHO'
# Opening body remains reproducible; continue sequentially with the branch.
exec(compile((R/'source/branch.py').read_text(),str(R/'source/branch.py'),'exec'))
bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(R/'Pipe.blend'))
(R/'validation.json').write_text(json.dumps(report,indent=2));print(report)
