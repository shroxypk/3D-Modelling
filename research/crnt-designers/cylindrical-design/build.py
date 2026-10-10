"""Initial curved panel, CRNT x9rApivNiGE, approximately 00:03-02:15.
Parametric cylinder projection preserves the parent curvature at base level.
"""
import bpy,bmesh,math,json
from pathlib import Path
from mathutils import Vector
R=Path('C:/Users/Dell/Downloads/3D/research/crnt-designers/cylindrical-design')
R.mkdir(exist_ok=True);(R/'review').mkdir(exist_ok=True)
if Path(bpy.data.filepath).name=='MechanicalJoint.blend':
 bpy.context.preferences.filepaths.save_version=0
 bpy.ops.wm.save_as_mainfile(filepath=str(R/'CylindricalDesign.blend'))
 for o in list(bpy.context.scene.objects):
  if o.name in ('JointArm','JointArmOpposite','JointAxle'):bpy.data.objects.remove(o,do_unlink=True)
bm=bmesh.new();N=8;us=[-.47+i*.94/N for i in range(N+1)];zs=[-.73+j*1.46/N for j in range(N+1)]
def vertex(u,z,r=1.01):return bm.verts.new((r*math.sin(u),-r*math.cos(u),z))
def uv(v):return math.atan2(v.co.x,-v.co.y),v.co.z
def bridge(a,b):
 for i in range(len(a)):bm.faces.new((a[i],a[(i+1)%len(a)],b[(i+1)%len(a)],b[i]))
def grid(r,holes=False):
 g={};faces={}
 for i,u in enumerate(us):
  for j,z in enumerate(zs):
   uu,zz=u,z
   # Explicit diagonal chamfer: midpoint and two endpoints, not a rounded corner.
   if i in (0,N) and j in (0,N):uu-=math.copysign(.045,u);zz-=math.copysign(.045,z)
   elif j in (0,N) and i in (1,N-1):uu=math.copysign(.47-.09,u)
   elif i in (0,N) and j in (1,N-1):zz=math.copysign(.73-.09,z)
   g[i,j]=vertex(uu,zz,r)
 for i in range(N):
  for j in range(N):faces[i,j]=bm.faces.new((g[i,j],g[i+1,j],g[i+1,j+1],g[i,j+1]))
 border=[g[i,0] for i in range(N)]+[g[N,j] for j in range(N)]+[g[i,N] for i in range(N,0,-1)]+[g[0,j] for j in range(N,0,-1)]
 return g,faces,border
g,faces,front=grid(1.01)
for i0,j0 in ((0,0),(6,0),(0,6),(6,6)):
 # Keep detail within the border: each 2x2 patch becomes an eight-sector rim.
 selected=[faces[i,j] for i in range(i0,i0+2) for j in range(j0,j0+2)]
 edges=set(e for f in selected for e in f.edges)
 boundary=list(set(v for e in edges if sum(f in selected for f in e.link_faces)==1 for v in e.verts))
 cu,cz=us[i0+1],zs[j0+1]
 boundary.sort(key=lambda v:math.atan2(round(uv(v)[1]-cz,5)+0.0,round(uv(v)[0]-cu,5)+0.0))
 for f in selected:bm.faces.remove(f)
 for e in list(bm.edges):
  if not e.link_faces:bm.edges.remove(e)
 for v in list(bm.verts):
  if not v.link_edges and v not in boundary:bm.verts.remove(v)
 prev=boundary
 for radius,r in ((.043,1.01),(.036,1.01),(.030,1.004),(.027,.991),(.019,.987)):
  cur=[vertex(cu+radius*math.cos(-3*math.pi/4+k*math.pi/4),cz+radius*math.sin(-3*math.pi/4+k*math.pi/4),r) for k in range(8)]
  bridge(prev,cur);prev=cur
 center=vertex(cu,cz,.987)
 for k in range(0,8,2):bm.faces.new((center,prev[k],prev[(k+1)%8],prev[(k+2)%8]))
# Extend the perimeter to supported thickness; preserve a simple curved back grid.
perimeter_rings=[front]
previous=front
for factor,r in ((1.015,1.01),(1.025,1.003),(1.025,.976),(1.015,.970)):
 cur=[vertex(uv(v)[0]*factor,uv(v)[1]*factor,r) for v in front];bridge(previous,cur);previous=cur;perimeter_rings.append(cur)
_,_,back=grid(.97);bridge(previous,back);perimeter_rings.append(back)
# Preserve the chamfer endpoints through thickness while allowing the face to smooth.
crease=bm.edges.layers.float.get('crease_edge') or bm.edges.layers.float.new('crease_edge')
endpoint_indices=[1,7,9,15,17,23,25,31]
for a,b in zip(perimeter_rings,perimeter_rings[1:]):
 for idx in endpoint_indices:
  edge=bm.edges.get((a[idx],b[idx]))
  if edge:edge[crease]=.9
bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
me=bpy.data.meshes.new('Curved panel quad cage');bm.to_mesh(me);bm.free()
o=bpy.data.objects.get('CurvedPanel')
if o:
 old=o.data;o.data=me
 if old.users==0:bpy.data.meshes.remove(old)
else:o=bpy.data.objects.new('CurvedPanel',me);bpy.context.scene.collection.objects.link(o)
for m in list(o.modifiers):o.modifiers.remove(m)
sub=o.modifiers.new('Surface review','SUBSURF');sub.levels=2;sub.render_levels=2
for p in me.polygons:p.use_smooth=True
report={}
for state in (False,True):
 sub.show_viewport=state;bpy.context.view_layer.update();e=o.evaluated_get(bpy.context.evaluated_depsgraph_get());m=e.to_mesh();b=bmesh.new();b.from_mesh(m)
 report['evaluated' if state else 'base']={'vertices':len(b.verts),'faces':len(b.faces),'nonquads':sum(len(f.verts)!=4 for f in b.faces),'nonmanifold_edges':sum(not e.is_manifold for e in b.edges),'zero_area_faces':sum(f.calc_area()<1e-12 for f in b.faces)}
 b.free();e.to_mesh_clear()
assert all(report['base'][k]==0 for k in ('nonquads','nonmanifold_edges','zero_area_faces')),report
for obj in bpy.context.view_layer.objects:obj.select_set(False)
o.select_set(True);bpy.context.view_layer.objects.active=o
for area in bpy.context.screen.areas:
 if area.type=='VIEW_3D':
  rv=area.spaces.active.region_3d;rv.view_location=(0,-.9,0);rv.view_distance=2.5;rv.view_rotation=Vector((1,-5,2)).to_track_quat('Z','Y');rv.view_perspective='ORTHO'
bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(R/'CylindricalDesign.blend'))
(R/'validation.json').write_text(json.dumps(report,indent=2));print(report)
