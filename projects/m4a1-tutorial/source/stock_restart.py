"""Stock restart: follow the tutorial's primitive/extrusion topology in order.
Current stage: crown, perimeter and underside return, approximately 19:40.
"""
import bpy,bmesh,math

def make(name,verts,faces,collection,split_at=None,bevel_path=None,junction_faces=()):
    me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update()
    bm=bmesh.new();bm.from_mesh(me)
    region=bm.faces.layers.int.new('junction_region')
    bm.faces.ensure_lookup_table()
    for i in junction_faces:bm.faces[i][region]=1
    if split_at is not None:
        bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=1e-6,plane_co=(split_at,0,0),plane_no=(1,0,0))
        bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6)
    if bevel_path:
        bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.normal_update()
        from mathutils import Vector
        segments=[(Vector(verts[a]),Vector(verts[b])) for a,b in zip(bevel_path,bevel_path[1:])]
        def on_segment(v,a,b):
            d=b-a;t=(v-a).dot(d)/d.length_squared
            return -.00001<=t<=1.00001 and (v-a-t*d).length<1e-5
        selected=[e for e in bm.edges if len(e.link_faces)==2 and any(all(on_segment(v.co,a,b) for v in e.verts) for a,b in segments)]
        bmesh.ops.bevel(bm,geom=selected,offset=.035,segments=1,profile=.5,affect='EDGES',clamp_overlap=True)
        bm.normal_update()
        # Explicitly split non-planar termination faces, rather than relying on
        # Blender's hidden tessellation to shade them unpredictably.
        warped=[f for f in bm.faces if len(f.verts)>3 and max(abs((v.co-f.verts[0].co).dot(f.normal)) for v in f.verts)>1e-5]
        if warped:bmesh.ops.triangulate(bm,faces=warped,quad_method='BEAUTY',ngon_method='BEAUTY')
    if junction_faces:
        bm.normal_update()
        selected=[f for f in bm.faces if f[region] and abs(f.normal.y)>.9999]
        bmesh.ops.inset_region(bm,faces=selected,thickness=.07,depth=0,use_even_offset=True,use_boundary=True)
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
    o=bpy.data.objects.new(name,me);collection.objects.link(o);o.color=(.47,.49,.52,1)
    return o

def build(collection):
    # 16:00: a separate 16-sided front cylinder, as demonstrated.
    ring=[(.474*math.sin(i*math.tau/16),-.015+.474*math.cos(i*math.tau/16)) for i in range(16)]
    verts=[((x-850)/100,y,z) for x in (2250,2305) for y,z in ring]
    faces=[(i,(i+1)%16,16+(i+1)%16,16+i) for i in range(16)]+[tuple(reversed(range(16))),tuple(range(16,32))]
    collar=make('07 | Stock front collar',verts,faces,collection)
    for p in collar.data.polygons:p.use_smooth=len(p.vertices)==4
    # Retain the upper quarter of a 16-sided cylinder, stretch it lengthwise,
    # then extrude the side down/out and extrude the thin lower lip.
    verts=[];faces=[]
    for x in (2295,2780):
        for i in range(5):
            a=i*math.pi/8;verts.append(((x-850)/100,.528*math.sin(a),.039+.528*math.cos(a)))
    for i in range(4):faces.append((i,i+1,6+i,5+i))
    # Front and rear setbacks belong to the extrusion, not extra cap rings.
    verts.extend([((2350-850)/100,.843,-.353),((2745-850)/100,.843,-.353),
                  ((2350-850)/100,.843,-.475),((2745-850)/100,.843,-.475)])
    faces.extend([(4,9,11,10),(10,11,13,12)])
    # 16:40-17:00 rear extension: the slanted cut is one planar boundary.
    for fraction in (.30,1.):
        for i in range(5):
            _,y,z=verts[5+i];x=2865-(z-.039)*90.72580645
            verts.append(((2780+fraction*(x-2780)-850)/100,y,z))
    for start,end in ((5,14),(14,19)):
        for i in range(4):faces.append((start+i,start+i+1,end+i+1,end+i))
    # 17:20-18:10: extrude the rear band down in successive quad sections.
    def p(x,z,y=.528):
        index=len(verts);verts.append(((x-850)/100,y,(345-z)/100));return index
    underside_z=-.75+(.528-.497)*(.275/.346)
    inside=p(2780,345-100*underside_z);middle=p(2805,405);outside=p(2858,405)
    faces.extend([(9,18,middle,inside),(18,23,outside,middle),(9,11,13,inside)])
    previous=(middle,outside);rear_inner_path=[]
    rows=[((2805,405),(2858,405)),((2800,445),(2852,445)),
          ((2798,503),(2845,503)),((2794,590),(2833,598)),((2760,670),(2778,696)),
          ((2700,668),(2700,692)),((2660,666),(2660,690))]
    # 21:40-22:50: three-segment corner bevels across the existing band.
    # Carry each new row through its width bridge rather than terminating it.
    def blend(a,b,t):return tuple((1-t)*x+t*y for x,y in zip(a,b))
    rounded=[]
    for j in range(1,len(rows)-1):
        if rows[j][0][1] not in (445,590,670):rounded.append(rows[j]);continue
        start=[];end=[]
        for k in (0,1):
            a,b,c=rows[j-1][k],rows[j][k],rows[j+1][k]
            d1=math.dist(a,b);d2=math.dist(b,c)
            start.append(blend(b,a,min(8/d1,.3)));end.append(blend(b,c,min(8/d2,.3)))
        for step in range(4):
            t=step/3
            rounded.append(tuple(blend(blend(start[k],rows[j][k],t),blend(rows[j][k],end[k],t),t) for k in (0,1)))
    rounded.append(rows[-1])
    # 24:10-24:50: shape the connected inner perimeter into the junction.
    # The original three corner rows continue diagonally, as in the tutorial.
    for j,point in enumerate([(2740,420),(2740,480),(2750,491),(2763,503)]):
        rounded[j]=(point,rounded[j][1])
    junction_faces=[]
    for j,(a,b) in enumerate(rounded):
        if j<5:junction_faces.append(len(faces))
        pair=(p(*a),p(*b));faces.append((previous[0],previous[1],pair[1],pair[0]));previous=pair;rear_inner_path.append(pair[0])
    # 18:20-19:40: extrude the lip inward, connect its front/rear returns.
    # These are the same long strips and end quads visible in the tutorial.
    front_outer=p(2295,345-100*underside_z)
    front_inner=p(2295,420,.497);lip_front=p(2350,420,.497)
    lip_rear=p(2745,420,.497);rear_inner=p(2780,420,.497)
    faces.extend([(12,13,lip_rear,lip_front),(4,10,12,front_outer),
                  (front_outer,12,lip_front,front_inner),
                  (13,inside,rear_inner,lip_rear)])
    # 20:00-21:30: bridge the inside perimeter to the mirrored side.
    # A shared center row preserves the tutorial's transverse quads.
    # 23:00-23:30: transverse cut and the front lower extension.
    # Its top replaces the earlier underside bridge, avoiding internal faces.
    front_cut=p(2440,420,.497)
    lower=[p(2305,445,.497),p(2360,445,.497),p(2440,473,.497)]
    top=[front_inner,lip_front,front_cut]
    for j in range(2):faces.append((top[j],top[j+1],lower[j+1],lower[j]))
    inner_path=[front_cut,lip_rear,rear_inner,inside,middle]+rear_inner_path
    center=[]
    for i in inner_path:
        x,y,z=verts[i];center.append(len(verts));verts.append((x,0,z))
    for j in range(len(inner_path)-1):
        faces.append((inner_path[j],inner_path[j+1],center[j+1],center[j]))
    lower_center=[]
    for i in lower:
        x,y,z=verts[i];lower_center.append(len(verts));verts.append((x,0,z))
    for j in range(2):faces.append((lower[j],lower[j+1],lower_center[j+1],lower_center[j]))
    o=make('08 | Stock crown tutorial restart',verts,faces,collection,split_at=15.9,bevel_path=[middle]+rear_inner_path,junction_faces=junction_faces)
    mirror=o.modifiers.new('Stock center symmetry','MIRROR');mirror.use_axis=(False,True,False);mirror.use_clip=True;mirror.merge_threshold=1e-5
    o['tutorial_stage']='Fresh restart through approximately 24:50: crown, returns, rear perimeter, inner bridge/bevel, corner rounds, front lower extension and shaped connected rear junction perimeter. Junction inset/opening and lower diagonal remain unfinished.'
    return o
