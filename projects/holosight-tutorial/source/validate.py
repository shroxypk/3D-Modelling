import bpy,bmesh,json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
report={}
for ob in bpy.data.collections['Holosight | Tutorial geometry'].objects:
 ev=ob.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();bm=bmesh.new();bm.from_mesh(me)
 pending=set(bm.verts);components=0
 while pending:
  components+=1;stack=[pending.pop()]
  while stack:
   vertex=stack.pop()
   for edge in vertex.link_edges:
    other=edge.other_vert(vertex)
    if other in pending:pending.remove(other);stack.append(other)
 report[ob.name]={'base_faces':len(ob.data.polygons),'base_quads':sum(len(p.vertices)==4 for p in ob.data.polygons),'evaluated_faces':len(bm.faces),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'zero_area_faces':sum(f.calc_area()<1e-10 for f in bm.faces),'components':components}
 bm.free();ev.to_mesh_clear()
(root/'validation.json').write_text(json.dumps(report,indent=2));print(report)
