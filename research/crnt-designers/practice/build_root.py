"""Focused open-surface adaptation of bracket hole-to-root routing, not full replica.
Two root profiles with equal nominal radius; live SubD then thickness.
"""
import bpy,bmesh,math,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath='C:/Users/Dell/AppData/Roaming/Blender Foundation/Blender/5.2/config/startup.blend')
for o in list(bpy.context.scene.objects):bpy.data.objects.remove(o,do_unlink=True)
report=[]
for case,segments in enumerate([1,4]):
    N=24;verts=[];faces=[];zc=1.45;bottom=.4;radius=.4
    def ring(points):
        first=len(verts);verts.extend(points);return list(range(first,len(verts)))
    def bridge(a,b,closed=True):
        for i in range(len(a) if closed else len(a)-1):
            j=(i+1)%len(a);faces.append((a[i],a[j],b[j],b[i]))
    outer=[]
    for i in range(N):
        a=i*2*math.pi/N
        if i<=12: x,z=math.cos(a),zc+math.sin(a)
        elif i<=15: x,z=-1,zc-(zc-bottom)*(i-12)/3
        elif i<=21: x,z=-1+(i-15)/3,bottom
        else: x,z=1,bottom+(zc-bottom)*(i-21)/3
        outer.append((x,0,z))
    inner=[(.53*math.cos(i*2*math.pi/N),0,zc+.53*math.sin(i*2*math.pi/N)) for i in range(N)]
    rings=[]
    for t in [0,.06,.88,1]:
        rings.append(ring([tuple((1-t)*p[k]+t*q[k] for k in range(3)) for p,q in zip(inner,outer)]))
        if len(rings)>1:bridge(rings[-2],rings[-1])
    previous=rings[-1][15:22]
    xs=[verts[i][0] for i in previous]
    for j in range(1,segments+1):
        a=(math.pi/2)*j/segments
        y=-radius+radius*math.cos(a);z=bottom-radius*math.sin(a)
        current=ring([(x,y,z) for x in xs]);bridge(previous,current,False);previous=current
    for y in [-.48,-1.05,-1.12]:
        current=ring([(x,y,0) for x in xs]);bridge(previous,current,False);previous=current
    me=bpy.data.meshes.new('Connected annulus and root strips');me.from_pydata(verts,[],faces);me.update()
    bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me)
    o=bpy.data.objects.new(f'Root profile - {segments} segment(s)',me);bpy.context.scene.collection.objects.link(o);o.location.x=(case-.5)*2.7
    for p in me.polygons:p.use_smooth=True
    sub=o.modifiers.new('Subdivision inspection','SUBSURF');sub.levels=2;sub.render_levels=2
    thick=o.modifiers.new('Coupon thickness - not full bracket','SOLIDIFY');thick.thickness=.10;thick.offset=0
    seen=set();components=0
    for v in bm.verts:
        if v in seen:continue
        components+=1;stack=[v];seen.add(v)
        while stack:
            for e in stack.pop().link_edges:
                for q in e.verts:
                    if q not in seen:seen.add(q);stack.append(q)
    base={'vertices':len(bm.verts),'faces':len(bm.faces),'nonquads':sum(len(f.verts)!=4 for f in bm.faces),'components':components,'boundary_edges':sum(e.is_boundary for e in bm.edges),'internal_nonmanifold':sum(not e.is_manifold and not e.is_boundary for e in bm.edges),'degenerate_faces':sum(f.calc_area()<1e-10 for f in bm.faces)}
    bm.free();thick.show_viewport=False;bpy.context.view_layer.update()
    mid=o.evaluated_get(bpy.context.evaluated_depsgraph_get());sample=mid.to_mesh()
    radii=[math.hypot(v.co.y+radius,v.co.z-bottom) for v in sample.vertices if abs(v.co.x)<1e-5 and -.38<v.co.y<-.02 and .02<v.co.z<.38]
    base['root_midline_sample_count']=len(radii)
    base['target_root_radius']=radius
    base['root_midline_max_radius_error']=max(abs(r-radius) for r in radii) if radii else None
    mid.to_mesh_clear();thick.show_viewport=True;bpy.context.view_layer.update()
    evaluated=o.evaluated_get(bpy.context.evaluated_depsgraph_get());ev=evaluated.to_mesh();bm=bmesh.new();bm.from_mesh(ev)
    base['evaluated_nonmanifold_edges']=sum(not e.is_manifold for e in bm.edges)
    base['evaluated_degenerate_faces']=sum(f.calc_area()<1e-10 for f in bm.faces)
    bm.free();evaluated.to_mesh_clear();report.append({'root_segments':segments,**base})
    o['study_limit']='Open surface coupon with live thickness; not complete tutorial bracket. No base mounting holes.'
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'RootStudy.blend'))
(ROOT/'validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report))
