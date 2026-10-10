import bpy,bmesh,json
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
P=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(P/'M4A1.blend'))
s=bpy.context.scene;c=s.camera
o=bpy.data.objects['02 Handguard | continuous shell and slotted sides']
me=o.evaluated_get(bpy.context.evaluated_depsgraph_get()).to_mesh()
bm=bmesh.new();bm.from_mesh(me);bm.faces.ensure_lookup_table()
tree=BVHTree.FromBMesh(bm,epsilon=.0000001)
overlaps=[]
for a,b in tree.overlap(tree):
    if a>=b:continue
    if set(bm.faces[a].verts).intersection(bm.faces[b].verts):continue
    overlaps.append((a,b))
print('NONADJACENT_FACE_OVERLAPS',len(overlaps),overlaps[:20])
bounds=[(min(v.co[i] for v in me.vertices),max(v.co[i] for v in me.vertices)) for i in range(3)]
print('BOUNDS',bounds)
(P/'review'/'intersection-check.json').write_text(json.dumps({'nonadjacent_face_overlap_candidates':len(overlaps),'pairs':overlaps,'bounds':bounds},indent=2))
bm.free()
s.render.resolution_x=1200;s.render.resolution_y=800
views=[('front-junction',(-2.55,0,0),(-4,-9,4),5.0),('rear-junction',(6.6,0,0),(3,-9,3),4.3),('rear-inside',(5.0,0,0),(9,-2,2),4.6)]
for name,center,direction,scale in views:
    t=Vector(center);c.location=t+Vector(direction);c.rotation_euler=(t-c.location).to_track_quat('-Z','Y').to_euler();c.data.ortho_scale=scale
    s.render.filepath=str(P/'review'/f'{name}.png');bpy.ops.render.render(write_still=True)
