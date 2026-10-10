"""Continue the accepted base with the tutorial's first blind corner recess.

Reconstruct the cleaned twelve-edge patch directly, rather than retaining
the Boolean's short intersection edges. Run after build.py.
"""
import bpy,bmesh,json,math
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path('C:/Users/Dell/Downloads/3D/research/crnt-designers/cover')
o=bpy.data.objects['Cover']
bm=bmesh.new();bm.from_mesh(o.data);bm.normal_update()
surface=BVHTree.FromBMesh(bm)
c=1.0256/math.sqrt(2)
patch=[f for f in bm.faces if len(f.verts)==4
 and all(v.co.x>.50 and v.co.y>.50 and abs(v.co.x-v.co.y)<.205 for v in f.verts)
 and min(v.co.z for v in f.verts)>.19
 and max(v.co.z for v in f.verts)<.36
 and max(v.co.z for v in f.verts)>.205
 and min(v.co.z for v in f.verts)<.30]
assert len(patch)==8,len(patch)
pe=set(e for f in patch for e in f.edges)
border=[e for e in pe if sum(f in patch for f in e.link_faces)==1]
boundary=list(set(v for e in border for v in e.verts))
assert len(boundary)==12,len(boundary)
boundary.sort(key=lambda v:math.atan2(v.co.y-c,v.co.x-c))
bmesh.ops.delete(bm,geom=patch,context='FACES_ONLY')
for e in list(bm.edges):
 if not e.link_faces:bm.edges.remove(e)
for v in list(bm.verts):
 if not v.link_edges:bm.verts.remove(v)
# Align twelve equal sectors with the diagonal symmetry of the corner.
angles=[-math.pi*11/12+i*math.pi/6 for i in range(12)]
# Choose a cyclic alignment, never cross boundary connections.
# Explicit nearest-angle fit is robust across the atan2 branch cut.
shift=min(range(12),key=lambda k:sum((((math.atan2(v.co.y-c,v.co.x-c)-angles[(i+k)%12]+math.pi)%(2*math.pi))-math.pi)**2 for i,v in enumerate(boundary)))
angles=[angles[(i+shift)%12] for i in range(12)]
def bridge(a,b):
 for i in range(12):bm.faces.new((a[i],a[(i+1)%12],b[(i+1)%12],b[i]))
def ring(radius,z=None,drop=0):
 out=[]
 for a in angles:
  x,y=c+radius*math.cos(a),c+radius*math.sin(a)
  hit=surface.ray_cast(Vector((x,y,1)),Vector((0,0,-1)))[0]
  assert hit is not None
  out.append(bm.verts.new((x,y,hit.z-drop if z is None else z)))
 return out
# The rim follows the shoulder. A small corner support replaces the
# tutorial's two-segment profile-1 bevel without making a flat washer.
outer=ring(.11095);lip=ring(.103);wall=ring(.103,drop=.00795)
floor=ring(.103,z=.32691-.173)
for a,b in ((boundary,outer),(outer,lip),(lip,wall),(wall,floor)):bridge(a,b)
bm.faces.new(floor)
bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.normal_update()
seen=set();components=0
for v in bm.verts:
 if v in seen:continue
 components+=1;todo=[v];seen.add(v)
 while todo:
  q=todo.pop()
  for e in q.link_edges:
   w=e.other_vert(q)
   if w not in seen:seen.add(w);todo.append(w)
report={'stage':'First cleaned blind recess, rim support; floor detailing and symmetry pending',
 'vertices':len(bm.verts),'faces':len(bm.faces),'nonquads':sum(len(f.verts)!=4 for f in bm.faces),
 'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),
 'zero_area_faces':sum(f.calc_area()<1e-10 for f in bm.faces),'components':components,
 'recess_radius':.103,'floor_z':.15391}
assert report['nonmanifold_edges']==0 and report['zero_area_faces']==0 and components==1,report
bm.to_mesh(o.data);bm.free();o.data.update()
bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(R/'Cover.blend'))
(R/'validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(report)
