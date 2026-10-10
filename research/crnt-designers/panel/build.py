"""Panel reconstruction from sequential CRNT checkpoints; continuous quad patches.
Dimensions are normalized estimates except cutter radius and center spacing read from UI.
"""
import bpy,bmesh,math,json
from pathlib import Path
from mathutils import Vector
R=Path('C:/Users/Dell/Downloads/3D/research/crnt-designers/panel')
vs=[];fs=[];cache={}
def v(x,z,y=0):
 key=tuple(round(q,7) for q in (x,y,z))
 if key not in cache:cache[key]=len(vs);vs.append(key)
 return cache[key]
def face(*ids):
 if len(set(ids))!=len(ids):raise ValueError(('collapsed',ids))
 fs.append(tuple(ids))
def bridge(a,b):
 for i in range(len(a)-1):face(a[i],a[i+1],b[i+1],b[i])
def loopbridge(a,b):bridge(a+[a[0]],b+[b[0]])
def pos(i):return vs[i]
r=.267
centers=[(-1,.39083),(-.5,.048),(0,.39083),(.5,.048),(1,.39083)]
c=[]
for x,z in centers:c.append([v(x+r*math.cos(i*math.tau/16),z+r*math.sin(i*math.tau/16)) for i in range(16)])
# 01:51-02:27: three direct quad strips across each diagonal gap.
for j in range(4):
 if j%2==0:a=[c[j][i] for i in [0,15,14,13]];b=[c[j+1][i] for i in [5,6,7,8]]
 else:a=[c[j][i] for i in [0,1,2,3]];b=[c[j+1][i] for i in [11,10,9,8]]
 bridge(a,b)
# Top arcs project to the top bend. Gaps have aligned horizontal rows.
for j in [0,2,4]:
 arc=[c[j][i] for i in [6,5,4,3,2]]
 bridge(arc,[v(pos(i)[0],.75) for i in arc])
for j in [1,3]:
 lo=c[j];left=c[j-1];right=c[j+1];x=centers[j][0]
 mid=[v(x,pos(left[i])[2]) for i in [0,1,2]]+[v(x,.75)]
 face(left[0],lo[5],lo[4],mid[0]);face(mid[0],lo[4],lo[3],right[8])
 bridge([left[i] for i in [0,1,2]]+[v(pos(left[2])[0],.75)],mid)
 bridge(mid,[right[i] for i in [8,7,6]]+[v(pos(right[6])[0],.75)])
# Outside circle arcs flow horizontally to the side.
for j,inds,x in [(0,[6,7,8,9,10],-1.5),(4,[2,1,0,15,14],1.5)]:
 a=[c[j][i] for i in inds];b=[v(x,pos(i)[2]) for i in a];bridge(a,b)
 face(a[0],v(pos(a[0])[0],.75),v(x,.75),b[0])
# Bottom contour follows the exposed lower arcs of the five-circle chain.
bot=[c[0][i] for i in [10,11,12,13]]+[c[1][i%16] for i in range(8,17)]+[c[2][i] for i in [11,12,13]]+[c[3][i%16] for i in range(8,17)]+[c[4][i] for i in [11,12,13,14]]
row=[v(pos(i)[0],-.30) for i in bot];bridge(bot,row)
for end,x in [(0,-1.5),(-1,1.5)]:face(bot[end],row[end],v(x,-.30),v(x,pos(bot[end])[2]))
# 01:27-02:39: rectangular detail with shared columns continuing from circles.
xs=[-1.5]+[pos(i)[0] for i in row]+[1.5]
zs=[-.30-j*1.10/8 for j in range(9)]
# ordered clockwise perimeter and a rounded-rectangle map, keeping floor a quad grid.
keys=[(i,0) for i in range(len(xs))]+[(len(xs)-1,j) for j in range(1,len(zs))]+[(i,len(zs)-1) for i in range(len(xs)-2,-1,-1)]+[(0,j) for j in range(len(zs)-2,0,-1)]
outer=[v(xs[i],zs[j]) for i,j in keys]
def rounded(i,j,offset=0,y=0):
 # Four quarter-circle segments per corner, with explicit tangency points.
 # Do not scale a sparse rectangular grid and clamp only its corner vertex.
 hw=1.24-offset;top=-.36-offset;bottom=-1.27+offset;rad=.12-offset
 ni=len(xs)-1;nj=len(zs)-1
 def top_point(k):
  if k<=2:
   ang=math.pi/4+k*math.pi/8
   return (-hw+rad-rad*math.cos(ang),top-rad+rad*math.sin(ang))
  if k>=ni-2:
   xx,zz=top_point(ni-k);return (-xx,zz)
  t=(xs[k]-xs[2])/(xs[ni-2]-xs[2])
  return (-hw+rad+2*(hw-rad)*t,top)
 def left_point(k):
  if k<=2:
   ang=math.pi/4-k*math.pi/8
   return (-hw+rad-rad*math.cos(ang),top-rad+rad*math.sin(ang))
  if k>=nj-2:
   xx,zz=left_point(nj-k);return (xx,top+bottom-zz)
  t=(k-2)/(nj-4)
  return (-hw,(top-rad)*(1-t)+(bottom+rad)*t)
 tx,tz=top_point(i);lx,lz=left_point(j)
 # Transfinite fill keeps the floor connected, planar, and quad-based.
 u=i/ni;vv=j/nj;corner=rad*(1-math.sqrt(.5))
 x=tx+(1-2*u)*lx-(2*u-1)*(hw-corner)
 z=(1-vv)*tz+vv*(top+bottom-tz)+lz-((1-vv)*(top-corner)+vv*(bottom+corner))
 return v(x,z,y)
prev=outer
# 04:15-04:27: narrow rim, shallow wall, supported rectangular floor.
for offset,y in [(0,0),(.012,0),(.022,.006),(.039,.022),(.048,.025),(.060,.025)]:
 cur=[rounded(i,j,offset,y) for i,j in keys];loopbridge(prev,cur);prev=cur
floor={(i,j):rounded(i,j,.060,.025) for i in range(len(xs)) for j in range(len(zs))}
for i in range(len(xs)-1):
 for j in range(len(zs)-1):face(floor[i,j],floor[i+1,j],floor[i+1,j+1],floor[i,j+1])
# 02:51-03:39: circle inset, inward step, and shallow raised floor lip.
# These stay blind, with material remaining between floor and flat rear.
for ci,(x,z) in enumerate(centers):
 prev=c[ci]
 for rr,yy in [(.255,0),(.247,.002),(.219,.024),(.211,.026),(.195,.026),(.188,.021),(.176,.021)]:
  cur=[v(x+rr*math.cos(i*math.tau/16),z+rr*math.sin(i*math.tau/16),yy) for i in range(16)]
  loopbridge(prev,cur);prev=cur
 # 4x4 quad disk from a square boundary circularized to sixteen points.
 grid={}
 boundary={ (4,2):0,(4,3):1,(4,4):2,(3,4):3,(2,4):4,(1,4):5,(0,4):6,(0,3):7,(0,2):8,(0,1):9,(0,0):10,(1,0):11,(2,0):12,(3,0):13,(4,0):14,(4,1):15}
 for a in range(5):
  for b in range(5):
   if (a,b) in boundary:grid[a,b]=prev[boundary[a,b]]
   else:grid[a,b]=v(x+(a-2)*.176*.42,z+(b-2)*.176*.42,.021)
 for a in range(4):
  for b in range(4):face(grid[a,b],grid[a+1,b],grid[a+1,b+1],grid[a,b+1])
# Bent flanges follow all their boundary columns, with support near bends and ends.
topxs=sorted(set(p[0] for p in vs if abs(p[2]-.75)<1e-6 and abs(p[1])<1e-6))
for xx,levels in [(topxs,[(.75,0),(.763,.002),(.78,.012),(.98,.212),(1.,.232)]),(xs,[(-1.40,0),(-1.413,.002),(-1.43,.012),(-1.63,.212),(-1.65,.232)])]:
 prev=[v(x,levels[0][0],levels[0][1]) for x in xx]
 for z,y in levels[1:]:
  cur=[v(x,z,y) for x in xx];bridge(prev,cur);prev=cur
# Boundary support strip holds the outline rather than letting SubD taper the sheet.
counts={}
for f in fs:
 for a,b in zip(f,f[1:]+f[:1]):
  e=tuple(sorted((a,b)));counts[e]=counts.get(e,0)+1
border=[e for e,n in counts.items() if n==1]
original={i:vs[i] for e in border for i in e}
new={}
for i,(x,y,z) in original.items():
 xx=x-math.copysign(.012,x) if abs(abs(x)-1.5)<1e-6 else x
 zz=z;yy=y
 if abs(z-1)<1e-6:zz-=.012;yy-=.012
 if abs(z+1.65)<1e-6:zz+=.012;yy-=.012
 vs[i]=(xx,yy,zz)
 new[i]=len(vs);vs.append((x,y,z))
for a,b in border:face(a,b,new[b],new[a])
# Flat back with matching boundary; all flattened radial strips remain nonzero.
n=len(vs);front=list(fs)
for x,y,z in list(vs):
 by=.045+(y if z>.75 or z<-1.40 else 0)
 vs.append((x,by,z))
fs.extend(tuple(i+n for i in reversed(f)) for f in front)
# Two thickness supports retain the perimeter under subdivision.
mids={}
for i in new.values():
 x,y,z=vs[i];yb=vs[i+n][1]
 mids[i]=[]
 for t in [.15,.85]:mids[i].append(len(vs));vs.append((x,y+(yb-y)*t,z))
for a,b in border:
 a=new[a];b=new[b]
 bridge([a,*mids[a],a+n],[b,*mids[b],b+n])
o=bpy.data.objects.get('Panel')
if o is None:raise RuntimeError('Expected Panel')
if o.mode!='OBJECT':bpy.ops.object.mode_set(mode='OBJECT')
o.modifiers.clear()
me=bpy.data.meshes.new('Panel continuous quad surface');me.from_pydata(vs,[],fs);me.update()
bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=1e-7,plane_co=(0,0,0),plane_no=(1,0,0))
bmesh.ops.delete(bm,geom=[v for v in bm.verts if v.co.x < -1e-7],context='VERTS')
bm.to_mesh(me);bm.free()
old=o.data;o.data=me
if old.users==0:bpy.data.meshes.remove(old)
o.location=(0,0,0);o.show_wire=False;o.show_all_edges=True
for p in me.polygons:p.use_smooth=True
# Corrected rectangular corner arcs and proportions; keep symmetry live.
mirror=o.modifiers.new('Live symmetry','MIRROR');mirror.use_clip=True;mirror.use_mirror_merge=True;mirror.merge_threshold=.000001
sub=o.modifiers.new('Subdivision preview after base review','SUBSURF');sub.levels=2;sub.render_levels=2;sub.show_viewport=True;sub.show_render=True
bm=bmesh.new();bm.from_mesh(me)
report={'stage':'Connected recesses, boundary supports, live Mirror and Subdivision','vertices':len(bm.verts),'faces':len(bm.faces),'nonquads':sum(len(f.verts)!=4 for f in bm.faces),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'zero_area_faces':sum(f.calc_area()<1e-10 for f in bm.faces),'min_face_area':min(f.calc_area() for f in bm.faces)}
bm.free();print(report)
(R/'validation.json').write_text(json.dumps(report,indent=2))
for a in bpy.context.screen.areas:
 if a.type=='VIEW_3D':
  rv=a.spaces.active.region_3d;rv.view_location=(0,0,-.325);rv.view_distance=4;rv.view_rotation=Vector((2,-8,2)).to_track_quat('Z','Y');rv.view_perspective='ORTHO'
bpy.context.view_layer.objects.active=o;o.select_set(True)
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(R/'Panel.blend'))
