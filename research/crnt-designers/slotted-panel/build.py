"""CRNT N09TEbcgavA: capsule, circle-slot flow, groove, bore, local details.
Normalized visual dimensions; ordered reconstruction with deliberate quad caps.
"""
import bpy,bmesh,math,json
from pathlib import Path
from mathutils import Vector
R=Path('C:/Users/Dell/Downloads/3D/research/crnt-designers/slotted-panel')
R.mkdir(exist_ok=True);(R/'review').mkdir(exist_ok=True)
if Path(bpy.data.filepath).name=='Cover.blend':
 bpy.context.preferences.filepaths.save_version=0
 bpy.ops.wm.save_as_mainfile(filepath=str(R/'SlottedPanel.blend'))
 old=bpy.data.objects.get('Cover')
 if old:bpy.data.objects.remove(old,do_unlink=True)
bm=bmesh.new();L=-1.8;C=1.8
fractions=[.10,.20,.45,.75,.90,1.0]
def contour(radius,outer=False):
 points=[]
 for i in range(15):
  a=math.radians(22.5+i*22.5)
  x=L+radius*math.cos(a);y=radius*math.sin(a)
  if outer and (a<math.pi/2 or a>3*math.pi/2):y=math.copysign(radius,y)
  points.append((x,y))
 x0,y0=points[-1];rr=radius if outer else radius*math.sin(math.pi/8)
 for t in fractions:points.append((x0+(C-x0)*t,-rr))
 for j in range(1,9):
  a=-math.pi/2+j*math.pi/8;points.append((C+rr*math.cos(a),rr*math.sin(a)))
 for t in reversed(fractions[:-1]):points.append((x0+(C-x0)*t,rr))
 assert len(points)==34
 return points
def verts(points,z):return [bm.verts.new((x,y,z)) for x,y in points]
def bridge(a,b):
 assert len(a)==len(b)
 return [bm.faces.new((a[i],a[(i+1)%len(a)],b[(i+1)%len(b)],b[i])) for i in range(len(a))]
def planar_surface(outline,inner,z):
 rings=[];faces=[]
 for t in (0,.25,.5,.75,1):
  rings.append(verts([(x*(1-t)+u*t,y*(1-t)+v*t) for (x,y),(u,v) in zip(outline,inner)],z))
 for a,b in zip(rings,rings[1:]):faces.append(bridge(a,b))
 return rings,faces
# 00:03-00:27: elongated rounded body; outline rounds remain explicit arcs.
outer=contour(.8,True);flat=contour(.70,True);key=contour(.44)
front,patches=planar_surface(flat,key,.30)
previous=front[0]
for radius,z in ((.706,.30),(.714,.289),(.723,.281),(.734,.281),(.744,.294),(.750,.30),(.760,.30),(.782,.277),(.8,.23),(.8,.09),(.79,.05),(.745,.014),(.715,0),(.70,0)):
 cur=verts(contour(radius,True),z);bridge(previous,cur);previous=cur
back,unused=planar_surface(flat,key,0)
# Merge the identical outer back ring after all parts are built.
back_boundary=back[0]
# 00:51-02:27: circular and narrow regions are joined before the border cut.
previous=front[-1]
for radius,z in ((.432,.30),(.424,.286),(.414,.262),(.402,.262),(.392,.286),(.384,.30),(.376,.30)):
 cur=verts(contour(radius),z);bridge(previous,cur);previous=cur
front_floor=previous
def floor_with_bore(loop,r,z):
 # Left circular sectors flow radially; the right sectors become long strips.
 hole=[bm.verts.new((L+r*math.cos(math.pi/8+i*math.pi/8),r*math.sin(math.pi/8+i*math.pi/8),z)) for i in range(16)]
 for i in range(14):bm.faces.new((loop[i],loop[i+1],hole[i+1],hole[i]))
 columns=[[hole[0],hole[15],hole[14]]]
 for top,bottom in [(0,14),(33,15),(32,16),(31,17),(30,18),(29,19),(28,20)]:
  a,b=loop[top],loop[bottom]
  columns.append([a,bm.verts.new(((a.co.x+b.co.x)/2,0,z)),b])
 for a,b in zip(columns,columns[1:]):
  for j in range(2):bm.faces.new((a[j],a[j+1],b[j+1],b[j]))
 capcenter=columns[-1][1];arc=[loop[i] for i in range(20,29)]
 for i in range(0,8,2):bm.faces.new((capcenter,arc[i],arc[i+1],arc[i+2]))
 return hole
front_hole=floor_with_bore(front_floor,.28,.30)
back_hole=floor_with_bore(back[-1],.28,0)
previous=front_hole
for r,z in ((.269,.30),(.26,.29),(.257,.275),(.257,.025),(.26,.01),(.269,0)):
 cur=[bm.verts.new((L+r*math.cos(math.pi/8+i*math.pi/8),r*math.sin(math.pi/8+i*math.pi/8),z)) for i in range(16)]
 bridge(previous,cur);previous=cur
bridge(previous,back_hole)
# 03:39-04:03: four small details, derived from surrounding faces.
# Only the upper two are constructed; live Mirror supplies the lower pair.
for start in (28,32):
 selected=[patches[r][j%34] for r in (1,2) for j in (start,start+1)]
 edges=set(e for f in selected for e in f.edges)
 boundary=list(set(v for e in edges if sum(f in selected for f in e.link_faces)==1 for v in e.verts))
 center=sum((v.co for v in boundary),Vector())/len(boundary)
 assert len(boundary)==8
 boundary.sort(key=lambda v:math.atan2(v.co.y-center.y,v.co.x-center.x))
 for f in selected:bm.faces.remove(f)
 for e in list(bm.edges):
  if not e.link_faces:bm.edges.remove(e)
 for v in list(bm.verts):
  if not v.link_edges:bm.verts.remove(v)
 angles=[math.atan2(v.co.y-center.y,v.co.x-center.x) for v in boundary]
 # Eight equal sectors aligned to each rectangular patch, not arbitrary fans.
 a0=-3*math.pi/4
 candidates=[[a0+(i+k)*math.pi/4 for i in range(8)] for k in range(8)]
 angles=min(candidates,key=lambda aa:sum(((a-b+math.pi)%(2*math.pi)-math.pi)**2 for a,b in zip(angles,aa)))
 prev=boundary
 for radius,z in ((.061,.30),(.053,.30),(.047,.294),(.047,.274),(.041,.27),(.032,.27)):
  cur=[bm.verts.new((center.x+radius*math.cos(a),center.y+radius*math.sin(a),z)) for a in angles]
  bridge(prev,cur);prev=cur
 mid=bm.verts.new((center.x,center.y,.27))
 for i in range(0,8,2):bm.faces.new((mid,prev[i],prev[(i+1)%8],prev[(i+2)%8]))
bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6)
bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=1e-6,plane_co=(0,0,0),plane_no=(0,1,0),clear_inner=True)
bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
me=bpy.data.meshes.new('Circle slot quad flow');bm.to_mesh(me);bm.free()
o=bpy.data.objects.get('SlottedPanel')
if o is None:o=bpy.data.objects.new('SlottedPanel',me);bpy.context.scene.collection.objects.link(o)
else:
 old=o.data;o.data=me
 if old.users==0:bpy.data.meshes.remove(old)
for m in list(o.modifiers):o.modifiers.remove(m)
m=o.modifiers.new('Upper lower symmetry','MIRROR');m.use_axis=(False,True,False);m.use_clip=True;m.merge_threshold=.00001
sub=o.modifiers.new('Surface review','SUBSURF');sub.levels=2;sub.render_levels=2
for p in me.polygons:p.use_smooth=True
def check(subdivision):
 sub.show_viewport=subdivision;bpy.context.view_layer.update()
 ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());mesh=ev.to_mesh();b=bmesh.new();b.from_mesh(mesh)
 out={'vertices':len(b.verts),'faces':len(b.faces),'nonquads':sum(len(f.verts)!=4 for f in b.faces),
 'nonmanifold_edges':sum(not e.is_manifold for e in b.edges),'zero_area_faces':sum(f.calc_area()<1e-12 for f in b.faces)}
 b.free();ev.to_mesh_clear();return out
report={'base':check(False),'subdivision':check(True),'stage':'Reproduction built; visual review pending'}
assert report['base']['nonmanifold_edges']==0,report
bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
for a in bpy.context.screen.areas:
 if a.type=='VIEW_3D':
  rv=a.spaces.active.region_3d;rv.view_location=(0,0,.15);rv.view_distance=6;rv.view_rotation=Vector((2,-4,7)).to_track_quat('Z','Y');rv.view_perspective='ORTHO'
bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(R/'SlottedPanel.blend'))
(R/'validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(report)
