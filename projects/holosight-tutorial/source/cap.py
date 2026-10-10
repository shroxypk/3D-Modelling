"""Ep.1 ~49:30-50:30: continuous circular side patch, neck and cap blank."""
import bpy,bmesh,math

def build(ob):
    bpy.context.view_layer.objects.active=ob
    for modifier in list(ob.modifiers):
        if modifier.type=='MIRROR':bpy.ops.object.modifier_apply(modifier=modifier.name)
    bm=bmesh.new();bm.from_mesh(ob.data)
    # Move the full transverse section together; moving only the cap side
    # twisted the underside across its centerline.
    for p in bm.verts:
        if abs(p.co.y-.590)<1e-6 and p.co.z<.443:
            p.co.y=.515
    patch={f for f in bm.faces if all(v.co.x>.33 and v.co.y>.51499 and v.co.z<.443 for v in f.verts)}
    border={e for f in patch for e in f.edges if sum(g in patch for g in e.link_faces)==1}
    verts={p for e in border for p in e.verts}
    start=min(verts,key=lambda p:p.co.z)
    neighbors=lambda p:[e.other_vert(p) for e in border if p in e.verts]
    first=max(neighbors(start),key=lambda p:p.co.y)
    outer=[start,first]
    while len(outer)<len(verts):
        options=[p for p in neighbors(outer[-1]) if p!=outer[-2]]
        outer.append(options[0])
    assert len(outer)==20, len(outer)
    bmesh.ops.delete(bm,geom=list(patch),context='FACES_ONLY')
    # Remove isolated patch edges and vertices without touching its boundary.
    loose=[e for e in bm.edges if not e.link_faces and e not in border]
    bmesh.ops.delete(bm,geom=loose,context='EDGES')
    loose=[v for v in bm.verts if not v.link_edges]
    if loose:bmesh.ops.delete(bm,geom=loose,context='VERTS')
    ring=[]
    for i in range(16):
        a=2*math.pi*i/16;z=.230-.185*math.cos(a)
        ring.append(bm.verts.new((.353-.012*(z-.025)/.410,.735+.185*math.sin(a),z)))
    # Two local 5-valence junctions on the flat rear patch reduce 20 to 16.
    oi=ii=0
    while oi<20:
        if oi in (10,16):
            bm.faces.new((outer[oi],outer[(oi+1)%20],outer[(oi+2)%20],ring[ii%16]));oi+=2
        else:
            bm.faces.new((outer[oi],outer[(oi+1)%20],ring[(ii+1)%16],ring[ii%16]));oi+=1;ii+=1
    assert ii==16
    def bridge(a,b):
        if len(a)==len(b):
            for i in range(len(a)):bm.faces.new((a[i],a[(i+1)%len(a)],b[(i+1)%len(b)],b[i]))
        else:
            assert len(a)==16 and len(b)==40
            for i in range(16):
                j=round(i*2.5);end=round((i+1)*2.5)
                bm.faces.new((a[i],a[(i+1)%16],b[end%40],b[j+1])) if end-j==2 else bm.faces.new((a[i],a[(i+1)%16],b[end%40],b[j+2]))
                if end-j==2:bm.faces.new((a[i],b[j+1],b[j]))
                else:bm.faces.new((a[i],b[j+2],b[j+1],b[j]))
    for x,r,count in ((.355,.185,16),(.363,.169,16),(.386,.169,16),(.391,.185,40),(.478,.185,40),(.483,.1806,40)):
        nxt=[bm.verts.new((x,.735+r*math.sin(2*math.pi*i/count),.230-r*math.cos(2*math.pi*i/count))) for i in range(count)]
        bridge(ring,nxt);ring=nxt
    # Local rim density is needed for narrow grip teeth, not broad panels.
    grip=[f for f in bm.faces if all(.39099<=p.co.x<=.47801 for p in f.verts) and max(p.co.x for p in f.verts)-min(p.co.x for p in f.verts)>.08]
    assert len(grip)==40,len(grip)
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.normal_update()
    bmesh.ops.inset_individual(bm,faces=grip,thickness=.00847,depth=.00444,use_even_offset=True)
    # Forty-point circular outline, filled with a regular ten-by-ten quad grid.
    bottom=[ring[i%40] for i in range(-5,6)]
    top=[ring[i] for i in range(25,14,-1)]
    left=[ring[i] for i in range(35,24,-1)]
    right=[ring[i] for i in range(5,16)]
    grid={}
    for j in range(11):
        t=j/10
        for i in range(11):
            u=i/10
            if j==0:p=bottom[i]
            elif j==10:p=top[i]
            elif i==0:p=left[j]
            elif i==10:p=right[j]
            else:
                co=(1-t)*bottom[i].co+t*top[i].co+(1-u)*left[j].co+u*right[j].co
                co-=(1-u)*(1-t)*bottom[0].co+u*(1-t)*bottom[-1].co+(1-u)*t*top[0].co+u*t*top[-1].co
                p=bm.verts.new(co)
            grid[i,j]=p
    for j in range(10):
        for i in range(10):bm.faces.new((grid[i,j],grid[i+1,j],grid[i+1,j+1],grid[i,j+1]))
    # A straight local cut divides the shoulder strips on the flat side.
    # Keep the natural triangle termination rather than collapse it to a wedge.
    bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=1e-7,
                          plane_co=(0,.465,0),plane_no=(0,1,0),clear_inner=False,clear_outer=False)
    junctions=[f for f in bm.faces if len(f.verts)>4]
    if junctions:bmesh.ops.triangulate(bm,faces=junctions,quad_method='BEAUTY',ngon_method='BEAUTY')
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
    bm.to_mesh(ob.data);bm.free();ob.data.update()
    ob['Tutorial stage']='Ep.1 ~50:30 connected 16-sided cap blank, neck and rim. Ep.1 50:40-51:00: 40 individual positive-depth grip insets, scaled from 0.4965 mm width and 0.26 mm depth; slot unfinished.'

    import importlib.util
    from pathlib import Path
    spec=importlib.util.spec_from_file_location('slot',Path(__file__).with_name('slot.py'))
    slot=importlib.util.module_from_spec(spec);spec.loader.exec_module(slot);slot.build(ob)
