"""Planned quad reconstruction from reviewed CRNT bracket sequence.
Dimensions are normalized estimates, not source measurements. No SubD.
"""
import bpy,bmesh,math,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath='C:/Users/Dell/AppData/Roaming/Blender Foundation/Blender/5.2/config/startup.blend')
for o in list(bpy.context.scene.objects):bpy.data.objects.remove(o,do_unlink=True)
vs=[];fs=[];lookup={}
def v(x,y,z):
    p=(round(x,8),round(y-1.2,8),round(z,8))
    if p not in lookup:lookup[p]=len(vs);vs.append(p)
    return lookup[p]
def row(points):return [v(*p) for p in points]
def bridge(a,b,closed=False):
    for i in range(len(a) if closed else len(a)-1):
        j=(i+1)%len(a);fs.append((a[i],a[j],b[j],b[i]))
N=24;zc=1.75;bottom=.7;r=.4;xs=[-1+i/3 for i in range(7)]
outers=[];inners=[]
for sign in [-1,1]:
    y=sign*.4;outer=[]
    for i in range(N):
        a=i*2*math.pi/N
        if i<=12:x,z=math.cos(a),zc+math.sin(a)
        elif i<=15:x,z=-1,zc-(zc-bottom)*(i-12)/3
        elif i<=21:x,z=-1+(i-15)/3,bottom
        else:x,z=1,bottom+(zc-bottom)*(i-21)/3
        outer.append((x,y,z))
    inner=[(.53*math.cos(i*2*math.pi/N),y,zc+.53*math.sin(i*2*math.pi/N)) for i in range(N)]
    a=row(inner);b=row(outer);bridge(a,b,True);inners.append(a);outers.append(b)
    prev=b[15:22]
    for j in range(1,5):
        angle=math.pi*j/8
        yy=sign*(.8-r*math.cos(angle));z=bottom-r*math.sin(angle)
        curr=row([(x,yy,z) for x in xs]);bridge(prev,curr);prev=curr
bridge(inners[0],inners[1],True)
bridge(outers[0][:13],outers[1][:13])
# Upright planar sides, connected into side root patches.
zs=[.3,.7,1.05,1.4,1.75]
for x in [-1,1]:
    bridge(row([(x,-.4,z) for z in zs]),row([(x,.4,z) for z in zs]))
    for sign in [-1,1]:
        points=[(x,sign*(.8-r*math.cos(math.pi*j/8)),bottom-r*math.sin(math.pi*j/8)) for j in range(5)]
        points.append((x,sign*.4,.3))
        # The polygon is concave: its arithmetic centroid is outside the patch.
        # Place the three-way planar junction inside the corner's visibility region.
        ids=row(points)
        # Keep this small planar patch simple; forced concave quads pinch under SubD.
        for i in range(4):fs.append((ids[5],ids[i],ids[i+1]))
# Front base rectangle and countersunk through-hole: 24 matching boundary points.
rect=[(-1+i/3,-2) for i in range(6)]+[(1,-2+j*.2) for j in range(6)]+[(1-i/3,-.8) for i in range(6)]+[(-1,-.8-j*.2) for j in range(6)]
outer_top=row([(x,y,.3) for x,y in rect]);outer_bottom=row([(x,y,0) for x,y in rect])
angles=[-3*math.pi/4+2*math.pi*i/N for i in range(N)]
prev=outer_top
for rad,z in [(.43,.3),(.40,.3),(.28,.18),(.28,.025),(.28,0),(.32,0)]:
    curr=row([(rad*math.cos(a),-1.4+rad*math.sin(a),z) for a in angles]);bridge(prev,curr,True);prev=curr
bridge(prev,outer_bottom,True)
# External sides of front base; rear edge attaches to main underside/root.
for i in list(range(12))+list(range(18,24)):
    j=(i+1)%24;fs.append((outer_top[i],outer_top[j],outer_bottom[j],outer_bottom[i]))
# Underside of central region and base sidewalls.
ys=[-.8,-.4,.4,.8,1.2]
for ya,yb in zip(ys,ys[1:]):
    bridge(row([(x,ya,0) for x in xs]),row([(x,yb,0) for x in xs]))
    for x in [-1,1]:fs.append(tuple(row([(x,ya,0),(x,yb,0),(x,yb,.3),(x,ya,.3)])))
bridge(row([(x,.8,.3) for x in xs]),row([(x,1.2,.3) for x in xs]))
# Ratios estimated from the source's orthographic top view at 04:56.
# Piecewise longitudinal adjustment preserves the root radius and enlarges plate length.
knots=[(0,0),(.4,.57),(.8,.97),(1.2,1.68),(1.6,2.39),(2,2.79),(3.2,4.36)]
def stretch_y(y):
    a=abs(y)
    for (u,p),(w,q) in zip(knots,knots[1:]):
        if a<=w+1e-7:return math.copysign(p+(a-u)*(q-p)/(w-u),y)
    raise ValueError(y)
adjusted=[]
for x,y,z in vs:
    rr=math.hypot(x,y+2.6)
    if abs(rr-.43)<1e-6 or abs(rr-.4)<1e-6 or abs(rr-.28)<1e-6 or abs(rr-.32)<1e-6:
        target={.43:.49,.4:.46,.28:.34,.32:.38}[round(rr,2)]
        adjusted.append((x*target/rr,-3.56+(y+2.6)*target/rr,z))
    else:adjusted.append((x,stretch_y(y),z))
vs=adjusted
me=bpy.data.meshes.new('Continuous bracket quad cage');me.from_pydata(vs,[],fs);me.update()
bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
o=bpy.data.objects.new('Bracket - connected mirrored solid',me);bpy.context.scene.collection.objects.link(o)
bpy.context.view_layer.objects.active=o;o.select_set(True)
mirror=o.modifiers.new('Second upright and welded base','MIRROR');mirror.use_axis=(False,True,False);mirror.use_clip=True;mirror.use_mirror_merge=True
bev=o.modifiers.new('Small manufactured edge breaks','BEVEL');bev.width=.025;bev.segments=3;bev.limit_method='ANGLE';bev.angle_limit=math.radians(35)
for p in me.polygons:p.use_smooth=True
normal=o.modifiers.new('Subdivision after edge support','SUBSURF');normal.levels=2;normal.render_levels=2
o['status']='Study reconstruction; top-view ratios checked; final reflection and bore-radius checks pending.'
def audit(mesh):
    b=bmesh.new();b.from_mesh(mesh);seen=set();components=0
    for vv in b.verts:
        if vv in seen:continue
        components+=1;stack=[vv];seen.add(vv)
        while stack:
            cur=stack.pop()
            for e in cur.link_edges:
                q=e.other_vert(cur)
                if q not in seen:seen.add(q);stack.append(q)
    result={'vertices':len(b.verts),'faces':len(b.faces),'nonquads':sum(len(f.verts)!=4 for f in b.faces),'components':components,'boundary_edges':sum(e.is_boundary for e in b.edges),'internal_nonmanifold':sum(not e.is_manifold and not e.is_boundary for e in b.edges),'degenerate_faces':sum(f.calc_area()<1e-10 for f in b.faces)}
    b.free();return result
report={'base':audit(me)}
bev.show_viewport=False;normal.show_viewport=False;bpy.context.view_layer.update()
eo=o.evaluated_get(bpy.context.evaluated_depsgraph_get());em=eo.to_mesh();report['mirror_only']=audit(em);eo.to_mesh_clear()
bev.show_viewport=True;normal.show_viewport=True;bpy.context.view_layer.update()
eo=o.evaluated_get(bpy.context.evaluated_depsgraph_get());em=eo.to_mesh();report['evaluated']=audit(em);eo.to_mesh_clear()
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'Bracket.blend'))
(ROOT/'validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report))
