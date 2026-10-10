"""CRNT XOSZvoEypTA: curved shell, connected arm, supports, ridge, axle.
Visual normalized reconstruction; no factory reset or display overrides saved.
"""
import bpy,bmesh,math,json
from pathlib import Path
from mathutils import Vector
R=Path('C:/Users/Dell/Downloads/3D/research/crnt-designers/mechanical-joint')
R.mkdir(exist_ok=True);(R/'review').mkdir(exist_ok=True)
DETAIL=globals().get('DETAIL',True)
ASSEMBLY=globals().get('ASSEMBLY',True)
if Path(bpy.data.filepath).name=='SlottedPanel.blend':
 bpy.context.preferences.filepaths.save_version=0
 bpy.ops.wm.save_as_mainfile(filepath=str(R/'MechanicalJoint.blend'))
 old=bpy.data.objects.get('SlottedPanel')
 if old:bpy.data.objects.remove(old,do_unlink=True)
angles=sorted([i*22.5 for i in range(16)]+[82,86,94,98,262,266,274,278,11.25,33.75,146.25,168.75,191.25,213.75,326.25,348.75])
rad=[math.radians(a) for a in angles]
radius=.55;halfwidth=.44;halfheight=radius*math.sin(math.radians(56.25))

def bridge(bm,a,b):
 return [bm.faces.new((a[i],a[(i+1)%len(a)],b[(i+1)%len(a)],b[i])) for i in range(len(a))]

def gridcap(bm,loop,project=None,sample_angles=None):
 # Boundary runs CCW in YZ: four rectangular sides with matching subdivisions.
 corners=[(sample_angles or angles).index(a) for a in (45,135,225,315)]
 c0,c1,c2,c3=corners;N=len(loop)
 bot=[loop[i] for i in range(c2,c3+1)]
 right=[loop[i%N] for i in range(c3,N+c0+1)]
 top=list(reversed([loop[i] for i in range(c0,c1+1)]))
 left=list(reversed([loop[i] for i in range(c1,c2+1)]))
 nx,ny=len(bot)-1,len(left)-1;grid={}
 for i in range(nx+1):grid[i,0]=bot[i];grid[i,ny]=top[i]
 for j in range(ny+1):grid[0,j]=left[j];grid[nx,j]=right[j]
 for i in range(1,nx):
  for j in range(1,ny):
   u,v=i/nx,j/ny
   p=bot[i].co*(1-v)+top[i].co*v+left[j].co*(1-u)+right[j].co*u
   p-=bot[0].co*(1-u)*(1-v)+bot[-1].co*u*(1-v)+top[0].co*(1-u)*v+top[-1].co*u*v
   if project:p=Vector(project(p))
   grid[i,j]=bm.verts.new(p)
 for i in range(nx):
  for j in range(ny):bm.faces.new((grid[i,j],grid[i+1,j],grid[i+1,j+1],grid[i,j+1]))

def shellpoint(y,z,r=radius):return (-math.sqrt(max(1e-8,r*r-z*z)),y,z)
def rectangle(scale):
 return [(halfwidth*math.cos(a)/max(abs(math.sin(a)),abs(math.cos(a)))*scale,
          halfheight*math.sin(a)/max(abs(math.sin(a)),abs(math.cos(a)))*scale) for a in rad]

def make_arm():
 bm=bmesh.new()
 def ring(coords):return [bm.verts.new(p) for p in coords]
 # 00:03-00:39 curved retained cylinder segment with real wall thickness.
 outside=ring([shellpoint(y,z) for y,z in rectangle(1)])
 previous=outside
 for scale,r in ((1,.543),(1,.512),(.982,.505)):
  cur=ring([shellpoint(y,z,r) for y,z in rectangle(scale)]);bridge(bm,previous,cur);previous=cur
 gridcap(bm,previous,lambda p:shellpoint(p.y,p.z,.505))
 # 00:51-01:39 root patch matches the circular shaft; shared boundary edges.
 previous=outside
 for t in (0.035,.11,.50,.86,1):
  coords=[]
  for a,(y,z) in zip(rad,rectangle(1)):
   y=y*(1-t)+.34*math.cos(a)*t;z=z*(1-t)+.34*math.sin(a)*t
   x= -math.sqrt(radius*radius-z*z)
   if DETAIL:
    w=max(0,1-abs(math.cos(a))/.14)
    z+=math.copysign(.036*w*math.sin(math.pi*t/2),z)
   coords.append((x,y,z))
  cur=ring(coords);bridge(bm,previous,cur);previous=cur
 # Shaft length and end radii; ridge fades into shaft rather than floating above it.
 for x,r,h in ((-.61,.316,.040),(-.69,.302,.034),(-.80,.30,.025),(-1.05,.30,.008),(-1.30,.30,0),(-1.8,.30,0),(-2.45,.30,0),(-2.51,.30,0),(-2.55,.283,0),(-2.566,.263,0),(-2.566,.25,0)):
  coords=[]
  for a in rad:
   bump=h*max(0,1-abs(math.cos(a))/.14) if DETAIL else 0
   coords.append((x,r*math.cos(a),r*math.sin(a)+math.copysign(bump,math.sin(a))))
  cur=ring(coords);bridge(bm,previous,cur);previous=cur
 gridcap(bm,previous)
 bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
 return bm

def install(name,bm):
 me=bpy.data.meshes.new(name+' quad cage');bm.to_mesh(me);bm.free()
 o=bpy.data.objects.get(name)
 if o:
  old=o.data;o.data=me
  if old.users==0:bpy.data.meshes.remove(old)
 else:o=bpy.data.objects.new(name,me);bpy.context.scene.collection.objects.link(o)
 for m in list(o.modifiers):o.modifiers.remove(m)
 for p in me.polygons:p.use_smooth=True
 sub=o.modifiers.new('Surface review','SUBSURF');sub.levels=2;sub.render_levels=2
 return o

arm=install('JointArm',make_arm())
if ASSEMBLY:
 second=install('JointArmOpposite',make_arm());second.rotation_euler.y=math.radians(200)
 # 05:03-05:15 separate stepped axle, seated inside the curved shell.
 bm=bmesh.new();prev=None;ends=[]
 profile=[(.12,-.51),(.23,-.505),(.29,-.48),(.305,-.455),(.32,-.45),(.34,-.45),(.35,-.47),(.41,-.49),(.47,-.49),(.49,-.48),(.496,-.465),(.496,-.442),(.494,-.425),(.493,.425),(.496,.442),(.496,.465),(.49,.48),(.47,.49),(.41,.49),(.35,.47),(.34,.45),(.32,.45),(.305,.455),(.29,.48),(.23,.505),(.12,.51)]
 # Axle must use UNIFORM angular sectors: arm ridge spacing distorts circular subdivision.
 axle_angles=[i*360/32 for i in range(32)]
 axle_rad=[math.radians(a) for a in axle_angles]
 for r,y in profile:
  cur=[bm.verts.new((.975*r*math.cos(a),y,.975*r*math.sin(a))) for a in axle_rad]
  if prev:bridge(bm,prev,cur)
  else:ends.append(cur)
  prev=cur
 ends.append(prev)
 # Reuse quad patch with temporary axis swap, then restore.
 for v in bm.verts:v.co.x,v.co.y=v.co.y,v.co.x
 for loop in ends:gridcap(bm,loop,sample_angles=axle_angles)
 for v in bm.verts:v.co.x,v.co.y=v.co.y,v.co.x
 bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));install('JointAxle',bm)

def metrics(o,subdivision):
 o.modifiers['Surface review'].show_viewport=subdivision;bpy.context.view_layer.update()
 ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();bm=bmesh.new();bm.from_mesh(me)
 unseen=set(bm.verts);components=0
 while unseen:
  stack=[unseen.pop()];components+=1
  while stack:
   v=stack.pop()
   for e in v.link_edges:
    q=e.other_vert(v)
    if q in unseen:unseen.remove(q);stack.append(q)
 d={'vertices':len(bm.verts),'faces':len(bm.faces),'nonquads':sum(len(f.verts)!=4 for f in bm.faces),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'zero_area_faces':sum(f.calc_area()<1e-12 for f in bm.faces),'components':components}
 bm.free();ev.to_mesh_clear();return d
report={}
for o in bpy.context.scene.objects:
 if o.type=='MESH' and o.name.startswith('Joint'):
  report[o.name]={'base':metrics(o,False),'evaluated':metrics(o,True)}
  assert all(report[o.name]['base'][k]==0 for k in ('nonquads','nonmanifold_edges','zero_area_faces')),report
  assert report[o.name]['base']['components']==1,report
for obj in bpy.context.view_layer.objects:obj.select_set(False)
arm.select_set(True);bpy.context.view_layer.objects.active=arm
for area in bpy.context.screen.areas:
 if area.type=='VIEW_3D':
  rv=area.spaces.active.region_3d;rv.view_location=(0,0,-.3) if ASSEMBLY else (-1,0,0);rv.view_distance=6.5 if ASSEMBLY else 4;rv.view_rotation=Vector((-2,-5,3)).to_track_quat('Z','Y');rv.view_perspective='ORTHO'
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(R/'MechanicalJoint.blend'))
(R/'validation.json').write_text(json.dumps(report,indent=2));print(report)
