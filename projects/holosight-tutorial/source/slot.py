"""Cap slot: open-ended recess with small bevels on the long lips."""
import bpy,bmesh,math
from mathutils import Vector

def build(ob):
    # Slot direction is 30 degrees off vertical in the cap's YZ plane.
    normal=Vector((0,math.cos(math.pi/6),math.sin(math.pi/6)))
    along=Vector((0,-math.sin(math.pi/6),math.cos(math.pi/6)))
    center=Vector((0,.735,.230));half=.026
    verts=[]
    for x in (.448,.55):
        for u,v in ((-half,-.24),(half,-.24),(half,.24),(-half,.24)):
            pt=center+normal*u+along*v;pt.x=x;verts.append(pt)
    me=bpy.data.meshes.new('Temporary slot cutter');me.from_pydata(verts,[],[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]);me.update()
    cutter=bpy.data.objects.new('Temporary slot cutter',me);ob.users_collection[0].objects.link(cutter)
    bpy.context.view_layer.objects.active=ob
    mod=ob.modifiers.new('Slot construction','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cutter
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(cutter,do_unlink=True);bpy.data.meshes.remove(me)
    bm=bmesh.new();bm.from_mesh(ob.data);bm.normal_update()
    lips=[]
    for edge in bm.edges:
        if not all(abs(v.co.x-.483)<1e-5 for v in edge.verts):continue
        distances=[(v.co-center).dot(normal) for v in edge.verts]
        if all(abs(abs(d)-half)<1e-5 for d in distances) and distances[0]*distances[1]>0:lips.append(edge)
    if lips:bmesh.ops.bevel(bm,geom=lips,offset=.003,segments=1,affect='EDGES',clamp_overlap=True)
    ngons=[f for f in bm.faces if len(f.verts)>4]
    if ngons:bmesh.ops.triangulate(bm,faces=ngons,quad_method='BEAUTY',ngon_method='BEAUTY')
    bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6)
    bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-6)
    bm.normal_update()
    # Remove coplanar internal diagonals on the slot walls and floor.
    # Their dense fan came from triangulating Boolean output, not shape.
    flat_edges=[e for e in bm.edges if len(e.link_faces)==2 and
                all(v.co.x>=.4479 for f in e.link_faces for v in f.verts) and
                e.link_faces[0].normal.dot(e.link_faces[1].normal)>.999999 and
                abs(e.link_faces[0].normal.x)<.999]
    if flat_edges:bmesh.ops.dissolve_edges(bm,edges=flat_edges,use_verts=True,use_face_split=False)
    floors=[e for e in bm.edges if len(e.link_faces)==2 and all(abs(v.co.x-.448)<1e-5 for f in e.link_faces for v in f.verts)]
    if floors:bmesh.ops.dissolve_edges(bm,edges=floors,use_verts=True,use_face_split=False)
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(ob.data);bm.free();ob.data.update()
    # Local, shape-preserving cleanup also used on the saved checkpoint.
    import importlib.util
    from pathlib import Path
    spec=importlib.util.spec_from_file_location('refine_cap',Path(__file__).with_name('refine_cap.py'))
    refinement=importlib.util.module_from_spec(spec);spec.loader.exec_module(refinement)
    refinement.refine(ob)
    ob['Tutorial stage']='Ep.1 ~52:00: raised grip teeth and open-ended diagonal screwdriver slot; final edge finishing pending.'
