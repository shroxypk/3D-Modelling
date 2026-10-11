"""Read-only scene audit. Run in Blender with the saved Holosight loaded.

Writes review/audit.json only. Never rebuilds geometry or saves the blend.
Raw measurements are evidence, not automatic visual acceptance thresholds.
"""
import hashlib
import json
from pathlib import Path

import bpy
import bmesh

ROOT = Path(__file__).resolve().parents[1]


def mesh_report(mesh):
    bm = bmesh.new()
    bm.from_mesh(mesh)
    pending = set(bm.verts)
    components = 0
    while pending:
        components += 1
        stack = [pending.pop()]
        while stack:
            vertex = stack.pop()
            for edge in vertex.link_edges:
                other = edge.other_vert(vertex)
                if other in pending:
                    pending.remove(other)
                    stack.append(other)
    areas = [f.calc_area() for f in bm.faces]
    lengths = [e.calc_length() for e in bm.edges]
    result = {
        'vertices': len(bm.verts), 'edges': len(bm.edges),
        'faces': len(bm.faces), 'quads': sum(len(f.verts) == 4 for f in bm.faces),
        'triangles': sum(len(f.verts) == 3 for f in bm.faces),
        'ngons': sum(len(f.verts) > 4 for f in bm.faces),
        'components': components,
        'boundary_edges': sum(e.is_boundary for e in bm.edges),
        'nonmanifold_edges': sum(not e.is_manifold for e in bm.edges),
        'loose_edges': sum(not e.link_faces for e in bm.edges),
        'loose_vertices': sum(not v.link_edges for v in bm.verts),
        'zero_area_faces_at_1e-10': sum(a < 1e-10 for a in areas),
        'minimum_face_area': min(areas, default=None),
        'minimum_edge_length': min(lengths, default=None),
        'smooth_faces': sum(f.smooth for f in bm.faces),
    }
    # Index-sensitive fingerprint: compare only without reordering the mesh.
    signature = {'vertices': [list(v.co) for v in mesh.vertices],
                 'faces': [list(p.vertices) for p in mesh.polygons]}
    result['mesh_sha256'] = hashlib.sha256(json.dumps(signature).encode()).hexdigest()
    mesh.calc_loop_triangles()
    result['tessellated_triangles'] = len(mesh.loop_triangles)
    bm.free()
    return result


def main():
    if Path(bpy.data.filepath).resolve() != (ROOT / 'Holosight.blend').resolve():
        raise RuntimeError('Load the current Holosight.blend before auditing.')
    collection = bpy.data.collections.get('Holosight | Tutorial geometry')
    if collection is None:
        raise RuntimeError('Expected tutorial geometry collection is missing.')
    report = {'blender': bpy.app.version_string,
              'blend_sha256': hashlib.sha256((ROOT / 'Holosight.blend').read_bytes()).hexdigest(),
              'source_sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                for p in sorted((ROOT / 'source').glob('*.py'))},
              'objects': {},
              'limits': ['No intersection, duplicate-surface or reference-fit certification.',
                         'Base boundaries can be intentional before Mirror/Solidify.',
                         'Source reconstruction equivalence is not established by this audit.',
                         'UV/export checks are deferred until that production stage.']}
    depsgraph = bpy.context.evaluated_depsgraph_get()
    for ob in collection.objects:
        if ob.type != 'MESH':
            continue
        evaluated = ob.evaluated_get(depsgraph)
        mesh = evaluated.to_mesh()
        report['objects'][ob.name] = {
            'base': mesh_report(ob.data), 'evaluated': mesh_report(mesh),
            'scale': list(ob.scale), 'dimensions': list(ob.dimensions),
            'modifiers': [{'name': m.name, 'type': m.type,
                           'viewport': m.show_viewport, 'render': m.show_render}
                          for m in ob.modifiers],
            'hidden_render': ob.hide_render, 'uv_layers': len(ob.data.uv_layers),
            'material_slots': len(ob.material_slots),
        }
        evaluated.to_mesh_clear()
    (ROOT / 'review').mkdir(exist_ok=True)
    (ROOT / 'review' / 'audit.json').write_text(json.dumps(report, indent=2) + '\n')
    print('AUDIT_COMPLETE', json.dumps({n: r['evaluated']['faces']
                                      for n, r in report['objects'].items()}))


if __name__ == '__main__':
    main()
