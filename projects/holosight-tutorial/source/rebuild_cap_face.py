"""Restore the tutorial's two planar cap-front regions around the slot.

Only internal edges of faces in the cap-front plane are removed. Boundary
vertices, lips, slot walls, teeth and housing remain exactly where they were.
Planar n-gons are deliberate at this non-subdivision tutorial stage.
"""
import bmesh


def refine(ob, face_x=.483, tolerance=1e-7):
    if ob.type != 'MESH' or ob.mode != 'OBJECT':
        raise RuntimeError('Load the housing mesh in Object Mode.')
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    bm.normal_update()
    faces = {f for f in bm.faces if all(abs(v.co.x-face_x)<tolerance for v in f.verts)
             and f.normal.x > .999999}
    if not faces:
        bm.free()
        raise RuntimeError('Expected cap-front faces are absent; no edits made.')
    area = sum(f.calc_area() for f in faces)
    boundary = {e for f in faces for e in f.edges if sum(g in faces for g in e.link_faces)==1}
    boundary_positions = {v: tuple(v.co) for e in boundary for v in e.verts}
    outside = {f: tuple(tuple(v.co) for v in f.verts) for f in bm.faces if f not in faces}
    manifold = sum(not e.is_manifold for e in bm.edges)
    pending = set(faces)
    regions = []
    while pending:
        region = {pending.pop()}
        stack = list(region)
        while stack:
            f = stack.pop()
            for e in f.edges:
                for neighbor in e.link_faces:
                    if neighbor in pending:
                        pending.remove(neighbor);region.add(neighbor);stack.append(neighbor)
        regions.append(region)
    if len(regions) != 2:
        bm.free()
        raise RuntimeError(f'Expected two separate cap-front regions, got {len(regions)}')
    old_count = len(faces)
    region_vertices = {v for f in faces for v in f.verts}
    for region in regions:
        if len(region)>1:
            bmesh.ops.dissolve_faces(bm, faces=list(region), use_verts=False)
    loose = [v for v in region_vertices if v.is_valid and not v.link_edges]
    if loose:
        bmesh.ops.delete(bm,geom=loose,context='VERTS')
    bm.normal_update()
    result_faces = [f for f in bm.faces if all(abs(v.co.x-face_x)<tolerance for v in f.verts)
                    and f.normal.x > .999999]
    assert len(result_faces)==2, 'Did not produce two front faces'
    assert all(v.is_valid and tuple(v.co)==co for v,co in boundary_positions.items()), 'Boundary changed'
    assert all(f.is_valid and tuple(tuple(v.co) for v in f.verts)==coords for f,coords in outside.items()), 'Outside geometry changed'
    assert abs(sum(f.calc_area() for f in result_faces)-area)<1e-7, 'Planar surface area changed'
    assert sum(not e.is_manifold for e in bm.edges)==manifold, 'Mesh connectivity changed'
    assert all(f.calc_area()>1e-10 for f in bm.faces), 'Degenerate face introduced'
    count = len(bm.faces)
    bm.to_mesh(ob.data);bm.free();ob.data.update()
    return {'previous_cap_front_faces':old_count,'cap_front_faces':2,
            'removed_front_faces':old_count-2,'housing_faces':count,
            'boundary_and_outside_faces_unchanged':True}
