"""Recessed cover: tutorial opening through 01:15, before corner recesses."""
import bpy,bmesh,json
from pathlib import Path
from mathutils import Vector
R=Path('C:/Users/Dell/Downloads/3D/research/crnt-designers/cover')
# Keep the working scene/workspaces. The previous exercise is already saved.
if Path(bpy.data.filepath).name=='Pipe.blend':
 bpy.context.preferences.filepaths.save_version=0
 bpy.ops.wm.save_as_mainfile(filepath=str(R/'Cover.blend'))
 old=bpy.data.objects.get('Pipe')
 if old:bpy.data.objects.remove(old,do_unlink=True)
bm=bmesh.new()
rings=[]
# 00:21-00:24: .2 inset shoulder; upper region moved down .4.
# Profile sampled from the accepted 01:00 top/side silhouette, after the
# tutorial's undo/revisions. Intermediate modal bevel values are not final values.
profile=((1,0),(1,.2),(.922,.2),(.860,.223),(.823,.250),(.780,.300),(.730,.365),(.660,.400))
for half,z in profile:
 rings.append([bm.verts.new((x*half,y*half,z)) for x,y in ((-1,-1),(1,-1),(1,1),(-1,1))])
for a,b in zip(rings,rings[1:]):
 for i in range(4):bm.faces.new((a[i],a[(i+1)%4],b[(i+1)%4],b[i]))
bm.faces.new(tuple(reversed(rings[0])));bm.faces.new(rings[-1])
bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.normal_update()
# 01:03-01:12: four-segment corner rounds extend across the entire profile.
corners=[e for e in bm.edges if all(abs(abs(v.co.x)-abs(v.co.y))<1e-6 for v in e.verts) and e.verts[0].co.x*e.verts[1].co.x>0 and e.verts[0].co.y*e.verts[1].co.y>0]
bmesh.ops.bevel(bm,geom=corners,offset=.264,segments=4,profile=.5,affect='EDGES',clamp_overlap=True)
bm.normal_update()
bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
o=bpy.data.objects.get('Cover')
if o is None:
 me=bpy.data.meshes.new('Cover');o=bpy.data.objects.new('Cover',me);bpy.context.scene.collection.objects.link(o)
for mod in list(o.modifiers):o.modifiers.remove(mod)
me=bpy.data.meshes.new('Stepped cover base');bm.to_mesh(me)
report={'stage':'01:15 rounded stepped base; corner recesses pending','vertices':len(bm.verts),'faces':len(bm.faces),'nonquads':sum(len(f.verts)!=4 for f in bm.faces),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'zero_area_faces':sum(f.calc_area()<1e-10 for f in bm.faces)}
bm.free();old=o.data;o.data=me
if old.users==0:bpy.data.meshes.remove(old)
bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
for a in bpy.context.screen.areas:
 if a.type=='VIEW_3D':
  rv=a.spaces.active.region_3d;rv.view_location=(0,0,.2);rv.view_distance=3.5;rv.view_rotation=Vector((3,-5,5)).to_track_quat('Z','Y');rv.view_perspective='ORTHO'
bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(R/'Cover.blend'))
(R/'validation.json').write_text(json.dumps(report,indent=2));print(report)
