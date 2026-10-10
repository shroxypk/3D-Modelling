"""Ep.1 ~20:50â€“36:00: inner shell, crown, extension and connected lower closure.
Do not replace the connected floor with an intersecting separate solid.
"""
import bpy,bmesh,math

def build(collection):
    old=bpy.data.objects.get('02 | Inner housing')
    if old:bpy.data.objects.remove(old,do_unlink=True)
    # z, half width, rear y, forward y. Upper silhouette sits inside the hood.
    # The closely spaced lower shoulder rows describe the tutorial's curved
    # transition to the extended nose; they are shape rows, not support loops.
    rows=[(.025,.353,-.505,.850),(.14,.350,-.492,.850),
          (.28,.346,-.475,.850),(.39,.343,-.459,.850),
          (.435,.341,-.452,.850),(.443,.341,-.446,.490),
          (.453,.340,-.433,.360),(.468,.340,-.416,.285),
          (.490,.339,-.397,.253),(.520,.337,-.379,.213),
          (.558,.335,-.366,.184),(.605,.333,-.357,.167),
          (.660,.330,-.353,.158),(.720,.327,-.353,.149),
          (.790,.324,-.358,.138),(.825,.318,-.361,.132),
          (.856,.305,-.363,.127),(.883,.287,-.364,.123),
          (.904,.263,-.365,.120),(.919,.234,-.365,.118),
          (.928,.198,-.365,.117),(.933,.100,-.365,.116),
          (.935,0,-.365,.116)]
    # Ep.1 ~41–44: a 16-sided circular profile replaces the block nose.
    # Final tip .940, lower hood edge .520: projection .420 of hood height.
    lower=[]
    for i in range(9):
        a=math.pi*i/8
        z=.230-.205*math.cos(a)
        t=(z-.025)/.410
        lower.append((z,.353-.012*t,-.505+.053*t,.735+.205*math.sin(a)))
    rows=lower+rows[5:]
    floor_row=8
    verts=[]
    for z,x,rear,front in rows:verts.extend([(x,rear,z),(x,front,z)])
    faces=[(2*i,2*i+1,2*i+3,2*i+2) for i in range(len(rows)-1)]
    me=bpy.data.meshes.new('Housing continuous quad shell');me.from_pydata(verts,[],faces);me.update()
    bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
    ob=bpy.data.objects.new('02 | Inner housing',me);collection.objects.link(ob);ob.color=(.56,.57,.59,1)
    mi=ob.modifiers.new('Center symmetry','MIRROR');mi.use_clip=True;mi.merge_threshold=1e-5
    so=ob.modifiers.new('Housing wall thickness','SOLIDIFY');so.thickness=.045;so.offset=-1;so.use_even_offset=True
    # Ep.1 ~34â€“36: apply thickness and bridge the lower inner edges to the
    # symmetry plane. This creates a single connected housing, not a floor
    # object intersecting two side walls. Keep Mirror editable.
    mi.show_viewport=False
    bpy.context.view_layer.update()
    ev=ob.evaluated_get(bpy.context.evaluated_depsgraph_get());evaluated=ev.to_mesh()
    n=len(verts);assert len(evaluated.vertices)==2*n
    assert all((evaluated.vertices[i].co-me.vertices[i].co).length<1e-6 for i in range(n))
    v=[tuple(p.co) for p in evaluated.vertices]
    # Solidify's local offsets can differ at the two ends of a long row.
    # Keep each longitudinal strip planar rather than retaining twisted quads.
    for row in range(len(rows)):
        a=n+2*row;b=a+1
        x=(v[a][0]+v[b][0])/2;z=(v[a][2]+v[b][2])/2
        if row<=18:z=rows[row][0]
        v[a]=(x,v[a][1],z);v[b]=(x,v[b][1],z)
    for i in (n-2,n-1,2*n-2,2*n-1):v[i]=(0,v[i][1],v[i][2])
    # ~35:30: pull the lower inner boundary inward to round the opening's
    # bottom corners. These vertices also belong to the continuous floor.
    for row,x in [(8,.240),(9,.260),(10,.277),(11,.290)]:
        for end in range(2):
            i=n+2*row+end;v[i]=(x,v[i][1],v[i][2])
    # Remove inner walls beneath the floor, and the half-shell's center cap.
    removed=[set((n+2*i,n+2*i+1,n+2*i+3,n+2*i+2)) for i in range(floor_row)]
    center_cap={n-2,n-1,2*n-2,2*n-1}
    f=[tuple(p.vertices) for p in evaluated.polygons if set(p.vertices) not in removed and set(p.vertices)!=center_cap]
    ev.to_mesh_clear()
    center={}
    for i in range(floor_row+1):
        for end in range(2):
            source=n+2*i+end
            center[i,end]=len(v);v.append((0,v[source][1],v[source][2]))
    for i in range(floor_row):
        for end in range(2):
            f.append((n+2*i+end,n+2*(i+1)+end,center[i+1,end],center[i,end]))
    f.append((n,n+1,center[0,1],center[0,0]))
    f.append((n+2*floor_row,n+2*floor_row+1,center[floor_row,1],center[floor_row,0]))
    # ~36:30â€“39:00: longitudinal cuts around the tunnel, then inset narrow
    # bands for the two glass seats. Preserve shared vertices with the shell.
    back=[center[floor_row,0]]+[n+2*i for i in range(floor_row,len(rows))]
    front=[center[floor_row,1]]+[n+2*i+1 for i in range(floor_row,len(rows))]
    strip_sets=[set((back[i],front[i],front[i+1],back[i+1])) for i in range(len(back)-1)]
    f=[face for face in f if set(face) not in strip_sets]
    rings=[back]
    # Plane locations and recess depth are provisional visual estimates.
    for y,expansion in [(-.310,0),(-.305,.006),(-.285,.006),(-.280,0),
                        (.035,0),(.040,.006),(.060,.006),(.065,0)]:
        ring=[]
        for idx in back:
            x,_,z=v[idx]
            ring.append(len(v));v.append((x*(1+expansion/.30),y,z+(z-.665)*expansion/.235))
        rings.append(ring)
    rings.append(front)
    for a,b in zip(rings,rings[1:]):
        for i in range(len(a)-1):f.append((a[i],b[i],b[i+1],a[i+1]))
    completed=bpy.data.meshes.new('Housing joined floor and lower body')
    completed.from_pydata(v,[],f);completed.update()
    bm=bmesh.new();bm.from_mesh(completed)
    # Local transverse cuts cross the nose and return across its top/bottom.
    # They do not propagate through the crown or the glass seats.
    for station in (.590,.657):
        bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=1e-7,
                              plane_co=(0,station,0),plane_no=(0,1,0),clear_inner=False,clear_outer=False)
    # Collapse the tiny shoulder slivers where the local cuts meet the top.
    # This redirects each loop over the nose without triangles or pentagons.
    for station in (.590,.657):
        for outer in (True,False):
            group=[p for p in bm.verts if abs(p.co.y-station)<1e-6 and .434999<=p.co.z<.443 and (p.co.x>.30 if outer else .20<p.co.x<.30)]
            if len(group)==2:
                point=max(group,key=lambda p:p.co.z).co.copy()
                bmesh.ops.pointmerge(bm,verts=group,merge_co=point)
    for vertex in bm.verts:
        x,y,z=vertex.co
        if z>=.434999:continue
        if y<=.590001:
            vertex.co.z=.10+(z-.025)*(.335/.410)
            # Straight lower rear slope, with thickness following the same line.
            if y<-.4:
                oldrear=-.505+.053*(z-.025)/.410
                vertex.co.y=-.505+.053*(vertex.co.z-.025)/.410+(y-oldrear)
        elif y<=.657001:
            base=.10+(.230-.205*math.cos(math.pi/8)-.10)*(y-.590)/.067
            vertex.co.z=base+(z-.025)*(.435-base)/.410
        elif y<.735:
            base=(.230-.205*math.cos(math.pi/8))*(.735-y)/.078+.025*(y-.657)/.078
            vertex.co.z=base+(z-.025)*(.435-base)/.410
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(completed);bm.free()
    ob.data=completed;ob.modifiers.remove(so);mi.show_viewport=True
    # ~39â€“40:30: derive separate panes directly from the seat outline.
    # Grid fill changes the tutorial's flat n-gon cap into editable quads.
    for name,y in [('03 | Rear glass',-.295),('04 | Front glass',.050)]:
        old=bpy.data.objects.get(name)
        if old:bpy.data.objects.remove(old,do_unlink=True)
        half=[(v[idx][0]*1.01,y,.665+(v[idx][2]-.665)*(1+.003/.235)) for idx in back]
        outline=half+[(-x,y,z) for x,y,z in half[-2:0:-1]]
        # Symmetric Coons grid: distribute rows between four rounded borders.
        # Automatic grid-fill offset produced a diagonal, asymmetric flow.
        from mathutils import Vector
        def sample(points,t):
            lengths=[0.0]
            for a,b in zip(points,points[1:]):lengths.append(lengths[-1]+(Vector(b)-Vector(a)).length)
            target=t*lengths[-1]
            for j in range(len(points)-1):
                if target<=lengths[j+1]+1e-9:
                    fac=(target-lengths[j])/(lengths[j+1]-lengths[j])
                    return Vector(points[j]).lerp(Vector(points[j+1]),fac)
            return Vector(points[-1])
        def reflect(point):return (-point[0],point[1],point[2])
        # Half contour index is row-3: lower diagonal at 4, upper at 14.
        bottom=[reflect(p) for p in half[4:0:-1]]+half[:5]
        # Preserve every corner knot. Uniform arc-length resampling bridged
        # across the seat's corner vertices and left visible triangular gaps.
        bottom.insert(5,tuple((Vector(bottom[4])+Vector(bottom[5]))*.5))
        bottom.insert(4,tuple((Vector(bottom[3])+Vector(bottom[4]))*.5))
        top=[reflect(p) for p in half[14:-1]]+list(reversed(half[14:]))
        right=half[4:15];left=[reflect(p) for p in right]
        grid=[];size=10
        bl,br,tl,tr=map(Vector,(bottom[0],bottom[-1],top[0],top[-1]))
        for j in range(size+1):
            t=j/size
            for i in range(size+1):
                u=i/size
                pt=(1-t)*Vector(bottom[i])+t*Vector(top[i])+(1-u)*Vector(left[j])+u*Vector(right[j])
                pt-=(1-u)*(1-t)*bl+u*(1-t)*br+(1-u)*t*tl+u*t*tr
                grid.append(tuple(pt))
        quads=[(j*11+i,j*11+i+1,(j+1)*11+i+1,(j+1)*11+i) for j in range(10) for i in range(10)]
        pane_mesh=bpy.data.meshes.new(name)
        pane_mesh.from_pydata(grid,[],quads);pane_mesh.update()
        pane=bpy.data.objects.new(name,pane_mesh);collection.objects.link(pane);pane.color=(.22,.40,.44,1)
        for item in bpy.context.selected_objects:item.select_set(False)
        pane.select_set(True);bpy.context.view_layer.objects.active=pane
        bm=bmesh.new();bm.from_mesh(pane_mesh);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(pane_mesh);bm.free()
        thick=pane.modifiers.new('Glass thickness','SOLIDIFY');thick.thickness=.003;thick.offset=0
        pane['Tutorial stage']='Ep.1 ~40:30 separate glass derived from housing seat; quad fill instead of n-gon. Optical material unfinished.'
    ob['Tutorial stage']='Ep.1 ~44:00. Connected rounded nose, reference-constrained tip, inset seats and corner-matched quad glass panes. Finishing and silhouette audit remain.'
    import importlib.util
    from pathlib import Path
    spec=importlib.util.spec_from_file_location("cap",Path(__file__).with_name("cap.py"))
    cap=importlib.util.module_from_spec(spec);spec.loader.exec_module(cap);cap.build(ob)
    return ob
