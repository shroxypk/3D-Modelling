"""Finish the fitting's supports, mirrored branch and flange recesses."""
bm=bmesh.new();bm.from_mesh(o.data)
bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-5)
inner=[e for e in bm.edges if all(bore_corner(v) for v in e.verts)]
assert len(inner)==16,('inner junction',len(inner))
bmesh.ops.bevel(bm,geom=inner,offset=.02,segments=2,profile=1,affect='EDGES',clamp_overlap=True)
# At 03:51-04:15 the flange details are recessed and have floors.
# Four cardinal placements from a 2x2 quad patch; no Boolean cutter needed.
for t in (0,math.pi/2,math.pi,3*math.pi/2):
 c=Vector((profile[2][0]*math.cos(t),profile[2][0]*math.sin(t),profile[2][1]))
 v=min(bm.verts,key=lambda a:(a.co-c).length)
 assert (v.co-c).length<1e-4
 patch=list(v.link_faces);assert len(patch)==4
 border=[e for f in patch for e in f.edges if sum(g in patch for g in e.link_faces)==1]
 perimeter=list(set(w for e in border for w in e.verts));assert len(perimeter)==8
 # Sort in the local radial/tangent plane, starting at the outward cardinal vertex.
 def angle(w):
  d=w.co-c;a=math.atan2(-d.x*math.sin(t)+d.y*math.cos(t),d.x*math.cos(t)+d.y*math.sin(t))
  return a%math.tau
 perimeter.sort(key=angle)
 # Numerical near-zero angles belong at the start.
 start=min(range(8),key=lambda i:abs(math.atan2(math.sin(angle(perimeter[i])),math.cos(angle(perimeter[i])))))
 perimeter=perimeter[start:]+perimeter[:start]
 bmesh.ops.delete(bm,geom=patch,context='FACES_ONLY')
 loose=[e for e in list(v.link_edges) if not e.link_faces]
 if loose:bmesh.ops.delete(bm,geom=loose,context='EDGES')
 if v.is_valid and not v.link_edges:bmesh.ops.delete(bm,geom=[v],context='VERTS')
 # Support rings follow the curved flange surface; floor stays above the base.
 def surfz(x,y):
  r=math.hypot(x,y)
  return 1.3-math.sqrt(max(0,1-(r-2)**2))
 previous=perimeter
 for radius,depth in ((.165,0),(.145,0),(.145,.02),(.145,.18),(.125,.20)):
  ring=[]
  for i in range(8):
   a=t+i*math.tau/8;x=c.x+radius*math.cos(a);y=c.y+radius*math.sin(a)
   z=surfz(x,y)-depth if depth<.1 else c.z-depth
   ring.append(bm.verts.new((x,y,z)))
  for i in range(8):bm.faces.new((previous[i],previous[(i+1)%8],ring[(i+1)%8],ring[i]))
  previous=ring
 # Four quads cap the blind recess with a central vertex.
 center=bm.verts.new((c.x,c.y,c.z-.2))
 for i in range(0,8,2):bm.faces.new((previous[i],previous[(i+1)%8],previous[(i+2)%8],center))
# Support the sharp lips and flange perimeter. The flared transition remains broad.
def radius(v):return math.hypot(v.co.x,v.co.y)
def same_ring(e,r,z):return all(abs(radius(v)-r)<1e-5 and abs(v.co.z-z)<1e-5 for v in e.verts)
lips=[]
for e in bm.edges:
 if any(same_ring(e,r,z) for r,z in ((2,0),(2,.3),(.8,0),(.8,2),(1,2))):lips.append(e)
 elif all(abs(v.co.x-(cx-rad))<1e-5 for v in e.verts):
  if all(abs(math.hypot(v.co.y,v.co.z-cz)-rad)<1e-5 for v in e.verts) or all(abs(math.hypot(v.co.y,v.co.z-cz)-rv)<1e-5 for v in e.verts):lips.append(e)
bmesh.ops.bevel(bm,geom=lips,offset=.015,segments=2,profile=1,affect='EDGES',clamp_overlap=True)
bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
# Keep a genuinely connected live symmetry setup, not duplicated objects.
bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=1e-6,plane_co=(0,0,0),plane_no=(1,0,0),clear_outer=True,clear_inner=False)
bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6)
bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
mirror=o.modifiers.new('Symmetry','MIRROR');mirror.use_clip=True;mirror.use_mirror_merge=True
sub=o.modifiers.new('Surface preview','SUBSURF');sub.levels=2;sub.render_levels=2;sub.show_viewport=False;sub.show_render=False
for p in o.data.polygons:p.use_smooth=True
def stats(me):
 bm=bmesh.new();bm.from_mesh(me)
 todo=set(bm.verts);components=0
 while todo:
  components+=1;stack=[todo.pop()]
  while stack:
   a=stack.pop()
   for e in a.link_edges:
    b=e.other_vert(a)
    if b in todo:todo.remove(b);stack.append(b)
 d={'vertices':len(bm.verts),'faces':len(bm.faces),'nonquads':sum(len(f.verts)!=4 for f in bm.faces),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'zero_area_faces':sum(f.calc_area()<1e-10 for f in bm.faces),'components':components}
 bm.free();return d
bpy.context.view_layer.update();ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh()
report={'stage':'Full fitting geometry; shaded and subdivision review pending','base_half':stats(o.data),'mirrored_base':stats(me),'notes':'Four blind flange recesses; 16-sided branch bases; subdivision disabled pending review'}
ev.to_mesh_clear()
# Verified separately in shaded, base topology, side and section views.
sub.show_viewport=True;sub.show_render=True
bpy.context.view_layer.update();ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh()
report['subdivision']=stats(me)
from mathutils.bvhtree import BVHTree
check=bmesh.new();check.from_mesh(me);tree=BVHTree.FromBMesh(check)
report['open_passages']={'main_vertical':tree.ray_cast(Vector((0,0,3)),Vector((0,0,-1)),4)[0] is None,'both_branches':tree.ray_cast(Vector((-3,0,1.2)),Vector((1,0,0)),6)[0] is None}
floors=[]
for t in (0,math.pi/2,math.pi,3*math.pi/2):
 hit=tree.ray_cast(Vector((profile[2][0]*math.cos(t),profile[2][0]*math.sin(t),.6)),Vector((0,0,-1)),1)[0]
 floors.append(round(hit.z,5) if hit else None)
report['recess_floor_heights']=floors;check.free();ev.to_mesh_clear()
check=bmesh.new();check.from_mesh(o.data)
report['base_boundaries_on_mirror']=all(all(abs(v.co.x)<1e-5 for v in e.verts) for e in check.edges if not e.is_manifold);check.free()
report['stage']='Pipe fitting study pass: geometry and visual review completed'
report['notes']='Mostly quads with 20 triangles in the full base junctions; bore radius and recess dimensions visually estimated from the tutorial; no claim of exact mesh equivalence.'
