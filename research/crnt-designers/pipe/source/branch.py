"""Side branch placement, operand preparation and union, tutorial 00:27–01:03."""
# Called by build.py after rebuilding the opening body. No factory reset.
for m in list(o.modifiers):o.modifiers.remove(m)
old_branch=bpy.data.objects.get('Branch operand')
if old_branch:bpy.data.objects.remove(old_branch,do_unlink=True)
rad=.606;cx=-1.0359;cz=1.2
# Ring vertices follow the tutorial's 16-sided side cylinder.
bv=[]
for end in (0,1):
 for i in range(16):
  t=math.tau*i/16;y=rad*math.sin(t);z=cz+rad*math.cos(t)
  # Inner operand cap follows the main bore instead of obstructing it.
  x=cx-rad if end==0 else -math.sqrt(.8**2-y*y)-.04
  bv.append((x,y,z))
bf=[(i,(i+1)%16,16+(i+1)%16,16+i) for i in range(16)]
# Chord strips expose deliberate cap flow, rather than a triangle fan.
cap=[[0,1,7,8],[8,9,15,0],[1,2,6,7],[2,3,5,6],[3,4,5],[15,9,10,14],[14,10,11,13],[13,11,12]]
for ids in cap:
 bf.append(tuple(reversed(ids)));bf.append(tuple(16+i for i in ids))
mb=bpy.data.meshes.new('Prepared 16 side branch');mb.from_pydata(bv,[],bf);mb.update()
bb=bmesh.new();bb.from_mesh(mb);bmesh.ops.recalc_face_normals(bb,faces=list(bb.faces));bb.to_mesh(mb);bb.free()
branch=bpy.data.objects.new('Branch operand',mb);bpy.context.scene.collection.objects.link(branch)
bpy.context.view_layer.objects.active=o
union=o.modifiers.new('Tutorial side branch union','BOOLEAN');union.operation='UNION';union.solver='EXACT';union.object=branch
bpy.ops.object.modifier_apply(modifier=union.name)
bpy.data.objects.remove(branch,do_unlink=True)
if mb.users==0:bpy.data.meshes.remove(mb)
bm=bmesh.new();bm.from_mesh(o.data)
bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6)
bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
# Tutorial 01:03�01:39: collapse the short intersection edges into the
# branch's original 16 longitudinal strips, retaining its circular end ring.
ring=[(rad*math.sin(i*math.tau/16),cz+rad*math.cos(i*math.tau/16)) for i in range(16)]
def on_branch_corner(v):
 return v.co.x < -.8 and any(abs(v.co.y-y)<1e-5 and abs(v.co.z-z)<1e-5 for y,z in ring)
for iteration in range(80):
 candidates=[]
 for e in bm.edges:
  a,b=e.verts
  if not all(-1.4<v.co.x<-.7 and abs(v.co.y)<.7 and .5<v.co.z<1.9 for v in (a,b)):continue
  if e.calc_length()>=.13:continue
  pa,pb=on_branch_corner(a),on_branch_corner(b)
  if pa and pb:continue
  candidates.append((e.calc_length(),e,a if pa else b if pb else a))
 if not candidates:break
 _,e,target=min(candidates,key=lambda item:item[0]);other=e.other_vert(target)
 bmesh.ops.pointmerge(bm,verts=[target,other],merge_co=target.co.copy())
bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
report={'stage':'01:39 exterior junction cleanup; branch bore and support loops pending','vertices':len(bm.verts),'faces':len(bm.faces),'nonquads':sum(len(f.verts)!=4 for f in bm.faces),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges)}
bm.to_mesh(o.data);bm.free()
for p in o.data.polygons:p.use_smooth=False
o.show_wire=False
# Tutorial 01:51: two narrow support edges at the branch/root intersection.
bm=bmesh.new();bm.from_mesh(o.data)
junction=[e for e in bm.edges if all(on_branch_corner(v) and v.co.x>cx-rad+.05 for v in e.verts)]
assert len(junction)==16, ('Unexpected junction edge count',len(junction))
bmesh.ops.bevel(bm,geom=junction,offset=.02,segments=2,profile=1.0,affect='EDGES',clamp_overlap=True)
# The temporary cap chords served the operand preparation; the next operation opens it.
capfaces=[f for f in bm.faces if all(abs(v.co.x-(cx-rad))<1e-5 for v in f.verts)]
bmesh.ops.dissolve_faces(bm,faces=capfaces,use_verts=True)
bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
# Interior rows used by the tutorial's subsequent bore cleanup.
# Build them before the cut in the reproducible source so the intersection
# is deterministic. These rows do not change the main-bore shape.
bm=bmesh.new();bm.from_mesh(o.data)
vertical=[e for e in bm.edges if all(abs(math.hypot(v.co.x,v.co.y)-.8)<1e-5 for v in e.verts) and abs(e.verts[0].co.z-e.verts[1].co.z)>1.6]
assert len(vertical)==32
bmesh.ops.subdivide_edges(bm,edges=vertical,cuts=7,use_grid_fill=True)
bm.to_mesh(o.data);bm.free()
# Tutorial 02:15-02:27: side bore connects fully to the existing main bore.
# Radius .48 is estimated from the visible wall ratio, not an exact displayed value.
rv=.48
cv=[(x,rv*math.sin(i*math.tau/16),cz+rv*math.cos(i*math.tau/16)) for x in (-2.5,0) for i in range(16)]
cf=[(i,(i+1)%16,16+(i+1)%16,16+i) for i in range(16)]
cf += [tuple(reversed(range(16))),tuple(range(16,32))]
cm=bpy.data.meshes.new('Side bore cutter');cm.from_pydata(cv,[],cf);cm.update()
bm=bmesh.new();bm.from_mesh(cm);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(cm);bm.free()
cut=bpy.data.objects.new('Side bore cutter',cm);bpy.context.scene.collection.objects.link(cut)
mod=o.modifiers.new('Tutorial side bore','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cut
bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=mod.name)
bpy.data.objects.remove(cut,do_unlink=True)
if cm.users==0:bpy.data.meshes.remove(cm)
bm=bmesh.new();bm.from_mesh(o.data)
# Reconnect the lip explicitly with sixteen radial quads.
front=[f for f in bm.faces if all(abs(v.co.x-(cx-rad))<1e-5 for v in f.verts)]
bmesh.ops.delete(bm,geom=front,context='FACES_ONLY')
loose=[e for e in bm.edges if not e.link_faces]
if loose:bmesh.ops.delete(bm,geom=loose,context='EDGES')
loops=[]
for radius in (rad,rv):
 loop=[]
 for i in range(16):
  target=Vector((cx-rad,radius*math.sin(i*math.tau/16),cz+radius*math.cos(i*math.tau/16)))
  v=min(bm.verts,key=lambda v:(v.co-target).length)
  assert (v.co-target).length<1e-4
  loop.append(v)
 loops.append(loop)
for i in range(16):bm.faces.new((loops[0][i],loops[0][(i+1)%16],loops[1][(i+1)%16],loops[1][i]))
bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
report={'stage':'02:27 side bore opened; interior junction cleanup remains','vertices':len(bm.verts),'faces':len(bm.faces),'nonquads':sum(len(f.verts)!=4 for f in bm.faces),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'zero_area_faces':sum(f.calc_area()<1e-10 for f in bm.faces)}
bm.to_mesh(o.data);bm.free()

# Tutorial 02:39-03:03: resolve small intersection fragments on the bore wall.
bm=bmesh.new();bm.from_mesh(o.data)
bore_ring=[(rv*math.sin(i*math.tau/16),cz+rv*math.cos(i*math.tau/16)) for i in range(16)]
def bore_corner(v):
 return -.82<v.co.x<-.6 and any(abs(v.co.y-y)<1e-5 and abs(v.co.z-z)<1e-5 for y,z in bore_ring)
for _ in range(80):
 candidates=[]
 for e in bm.edges:
  a,b=e.verts
  if not all(-.82<v.co.x<-.59 and abs(v.co.y)<.55 and .65<v.co.z<1.76 for v in (a,b)):continue
  if e.calc_length()>.08:continue
  pa,pb=bore_corner(a),bore_corner(b)
  if pa and pb:continue
  candidates.append((e.calc_length(),e,a if pa else b if pb else a))
 if not candidates:break
 _,e,target=min(candidates,key=lambda item:item[0])
 bmesh.ops.pointmerge(bm,verts=[target,e.other_vert(target)],merge_co=target.co.copy())
bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
report={'stage':'03:03 interior junction cleanup in progress; no subdivision yet','vertices':len(bm.verts),'faces':len(bm.faces),'nonquads':sum(len(f.verts)!=4 for f in bm.faces),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'zero_area_faces':sum(f.calc_area()<1e-10 for f in bm.faces)}
bm.to_mesh(o.data);bm.free()
exec(compile((R/'source/finish.py').read_text(),str(R/'source/finish.py'),'exec'))
