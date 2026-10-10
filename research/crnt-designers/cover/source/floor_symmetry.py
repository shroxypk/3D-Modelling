"""Tutorial 02:27-03:15: concentric floor detail, flange support, symmetry.
Run after build.py and recess.py. Floor cap uses quads instead of a fan.
"""
import bpy,bmesh,json,math
from pathlib import Path
R=Path('C:/Users/Dell/Downloads/3D/research/crnt-designers/cover')
o=bpy.data.objects['Cover'];bm=bmesh.new();bm.from_mesh(o.data)
c=1.0256/math.sqrt(2)
f=next(f for f in bm.faces if len(f.verts)==12 and abs(f.calc_center_median().z-.15391)<1e-5)
outer=sorted(f.verts,key=lambda v:math.atan2(v.co.y-c,v.co.x-c))
angles=[math.atan2(v.co.y-c,v.co.x-c) for v in outer]
bm.faces.remove(f)
# Preserve the first floor's elevation; construct the .030931-deep groove
# and the .0273 raised center seen at 02:42-02:45. Small support widths
# reconstructed from the subsequent accepted close-up.
for v in outer:v.co.z=.158
previous=outer
for radius,z in ((.099,.15391),(.078,.15391),(.0736,.150),
                 (.0736,.127),(.070,.122979),(.066,.122979),
                 (.063,.127),(.063,.1455),(.059,.150279),(.0542,.150279)):
 current=[bm.verts.new((c+radius*math.cos(a),c+radius*math.sin(a),z)) for a in angles]
 for i in range(12):bm.faces.new((previous[i],previous[(i+1)%12],current[(i+1)%12],current[i]))
 previous=current
def quad_cap(bm,loop):
 perimeter=[(0,0),(1,0),(2,0),(3,0),(3,1),(3,2),(3,3),(2,3),(1,3),(0,3),(0,2),(0,1)]
 grid=dict(zip(perimeter,loop))
 for i in (1,2):
  for j in (1,2):
   u,v=i/3,j/3
   co=(grid[(i,0)].co*(1-v)+grid[(i,3)].co*v+grid[(0,j)].co*(1-u)+grid[(3,j)].co*u
       -grid[(0,0)].co*(1-u)*(1-v)-grid[(3,0)].co*u*(1-v)-grid[(0,3)].co*(1-u)*v-grid[(3,3)].co*u*v)
   grid[(i,j)]=bm.verts.new(co)
 for i in range(3):
  for j in range(3):bm.faces.new([grid[(i,j)],grid[(i+1,j)],grid[(i+1,j+1)],grid[(i,j+1)]])
quad_cap(bm,previous)
bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.normal_update()
# Support the outer flange's upper edge, as in the 03:03 frame.
flange=[e for e in bm.edges if all(abs(v.co.z-.2)<1e-5 for v in e.verts)
 and len(e.link_faces)==2 and min(abs(f.normal.z) for f in e.link_faces)<.2
 and max(abs(f.normal.z) for f in e.link_faces)>.7]
bmesh.ops.bevel(bm,geom=flange,offset=.00885,segments=2,profile=1,affect='EDGES',clamp_overlap=True)
# Retain the constructed quadrant and use a live, welded two-axis Mirror.
for normal in ((1,0,0),(0,1,0)):
 bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),
  dist=1e-6,plane_co=(0,0,0),plane_no=normal,clear_inner=True,clear_outer=False)
bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.normal_update()
bm.to_mesh(o.data);bm.free();o.data.update()
for m in list(o.modifiers):o.modifiers.remove(m)
m=o.modifiers.new('Four connected corners','MIRROR');m.use_axis=(True,True,False)
m.use_clip=True;m.use_mirror_merge=True;m.merge_threshold=.00001
bpy.context.view_layer.update()
ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());mesh=ev.to_mesh()
check=bmesh.new();check.from_mesh(mesh)
seen=set();components=0
for v in check.verts:
 if v in seen:continue
 components+=1;todo=[v];seen.add(v)
 while todo:
  q=todo.pop()
  for e in q.link_edges:
   w=e.other_vert(q)
   if w not in seen:seen.add(w);todo.append(w)
report={'stage':'Four mirrored blind recesses with connected stepped floors; central panel finishing pending',
 'base_vertices':len(o.data.vertices),'evaluated_vertices':len(check.verts),'evaluated_faces':len(check.faces),
 'evaluated_nonquads':sum(len(f.verts)!=4 for f in check.faces),'components':components,
 'nonmanifold_edges':sum(not e.is_manifold for e in check.edges),
 'zero_area_faces':sum(f.calc_area()<1e-10 for f in check.faces)}
assert components==1 and report['nonmanifold_edges']==0 and report['zero_area_faces']==0,report
check.free();ev.to_mesh_clear()
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(R/'Cover.blend'))
(R/'validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(report)
