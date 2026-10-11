"""Local cap-face cleanup; never recreates objects, moves vertices or saves.

Only removes internal diagonals between coplanar triangles at the known cap
face plane. Leaves the slot lips, rim, teeth and all other housing faces alone.
No claim of final topology or subdivision readiness is made.
"""
import math

import bmesh


def refine(ob, face_x=.483, tolerance=1e-7):
    if ob.type != 'MESH' or ob.mode != 'OBJECT':
        raise RuntimeError('Cap refinement requires a mesh in Object Mode.')
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    bm.normal_update()
    original_positions = [tuple(v.co) for v in bm.verts]
    original_area = sum(f.calc_area() for f in bm.faces)
    original_nonmanifold = sum(not e.is_manifold for e in bm.edges)
    merged = 0
    while True:
        bm.verts.index_update()
        choices = []
        for edge in bm.edges:
            faces = list(edge.link_faces)
            if len(faces) != 2 or any(len(f.verts) != 3 for f in faces):
                continue
            if faces[0].material_index != faces[1].material_index or faces[0].smooth != faces[1].smooth:
                continue
            vertices = set(v for f in faces for v in f.verts)
            if len(vertices) != 4 or any(abs(v.co.x - face_x) > tolerance for v in vertices):
                continue
            if faces[0].normal.dot(faces[1].normal) < .999999:
                continue
            border = [e for f in faces for e in f.edges if e != edge]
            start = min(vertices, key=lambda v: v.index)
            loop = [start]
            for _ in range(3):
                neighbors = [e.other_vert(loop[-1]) for e in border if loop[-1] in e.verts]
                candidates = [v for v in neighbors if v not in loop]
                if not candidates:
                    break
                loop.append(min(candidates, key=lambda v: v.index))
            if len(loop) != 4:
                continue
            turns, angles = [], []
            for i in range(4):
                a = loop[(i-1) % 4].co - loop[i].co
                b = loop[(i+1) % 4].co - loop[i].co
                turns.append(a.cross(b).x)
                angles.append(a.angle(b))
            if not (all(t > 1e-12 for t in turns) or all(t < -1e-12 for t in turns)):
                continue
            old_min = min(loop.calc_angle() for f in faces for loop in f.loops)
            # Do not trade a triangle for a worse acute corner or nearly flat turn.
            if min(angles) + 1e-7 < old_min or max(angles) > math.pi - old_min:
                continue
            key = tuple(sorted(v.index for v in edge.verts))
            choices.append((min(angles), key, edge))
        if not choices:
            break
        choices.sort(key=lambda item: (-item[0], item[1]))
        bmesh.ops.dissolve_edges(bm, edges=[choices[0][2]], use_verts=False, use_face_split=False)
        merged += 1
    bm.normal_update()
    assert original_positions == [tuple(v.co) for v in bm.verts], 'Vertex positions changed'
    assert sum(not e.is_manifold for e in bm.edges) == original_nonmanifold, 'Boundary changed'
    assert abs(sum(f.calc_area() for f in bm.faces) - original_area) < 1e-7, 'Surface area changed'
    assert all(f.calc_area() > 1e-10 for f in bm.faces), 'Degenerate face'
    bm.to_mesh(ob.data)
    bm.free()
    ob.data.update()
    return {'merged_triangle_pairs': merged, 'vertex_positions_unchanged': True}
