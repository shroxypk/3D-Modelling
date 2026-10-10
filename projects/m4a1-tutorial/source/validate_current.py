"""Check evaluated topology and flat-face warp; not a reference-fidelity score."""
import bpy,bmesh,json
from pathlib import Path

def validate(root):
    report={}
    for o in bpy.context.scene.objects:
        if o.type!='MESH':continue
        ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();bm=bmesh.new();bm.from_mesh(me)
        warp=0
        for p in me.polygons:
            v=[me.vertices[i].co for i in p.vertices];n=p.normal
            warp=max(warp,max(abs((w-v[0]).dot(n)) for w in v))
        remaining=set(bm.verts);components=0
        while remaining:
            components+=1;stack=[remaining.pop()]
            while stack:
                v=stack.pop()
                for e in v.link_edges:
                    other=e.other_vert(v)
                    if other in remaining:remaining.remove(other);stack.append(other)
        report[o.name]={'faces':len(me.polygons),'quads':sum(len(p.vertices)==4 for p in me.polygons),
                       'connected_components':components,'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),
                       'zero_area_faces':sum(f.calc_area()<1e-10 for f in bm.faces),'max_face_warp':warp}
        bm.free();ev.to_mesh_clear()
        bm=bmesh.new();bm.from_mesh(o.data)
        report[o.name]['base']={'faces':len(bm.faces),'quads':sum(len(f.verts)==4 for f in bm.faces),
          'boundary_edges':sum(e.is_boundary for e in bm.edges),
          'boundary_edges_off_y_mirror_plane':sum(e.is_boundary and any(abs(v.co.y)>1e-5 for v in e.verts) for e in bm.edges),
          'edges_with_more_than_two_faces':sum(len(e.link_faces)>2 for e in bm.edges),
          'zero_area_faces':sum(f.calc_area()<1e-10 for f in bm.faces)}
        bm.free()
    (Path(root)/'validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
    return report
