"""Tutorial 10:10–12:30 external cylinder shapes, in reference-image units."""
import bpy,bmesh,math

def mesh_object(name,vs,fs,collection):
    me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update()
    bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
    o=bpy.data.objects.new(name,me);collection.objects.link(o);o.color=(.47,.49,.52,1)
    for p in me.polygons:p.use_smooth=abs(p.normal.x)<.95
    for e in me.edges:e.use_edge_sharp=abs(me.vertices[e.vertices[0]].co.x-me.vertices[e.vertices[1]].co.x)<1e-6
    return o

def build(collection):
    # A revolved visual shell: 16 vertices per ring, continuous quad wall and lip.
    profile=[(90,56),(90.8,58),(94,60),(289,60),(293,62),(489,62),(493,58),
             (493,39),(487,37),(96,37),(92,39),(90,41)]
    vs=[((x-850)/100,r/100*math.cos(i*math.tau/16),r/100*math.sin(i*math.tau/16))
        for x,r in profile for i in range(16)]
    fs=[(k*16+i,k*16+(i+1)%16,((k+1)%len(profile))*16+(i+1)%16,((k+1)%len(profile))*16+i)
        for k in range(len(profile)) for i in range(16)]
    outer=mesh_object('01 | Front cylinder shell',vs,fs,collection)
    outer['tutorial_stage']='Front recess and edge rounds, approximately 12:30; exterior visual study only.'
    # The tutorial adds the small visible cylinder behind the side openings.
    # Closed quad-grid caps keep this a display surface, without functional internals.
    vs=[];fs=[];rings=[]
    perimeter=[(4,j) for j in range(5)]+[(i,4) for i in range(3,-1,-1)]+[(0,j) for j in range(3,-1,-1)]+[(i,0) for i in range(1,4)]
    for x in [196,1967]:
        ids={}
        for j in range(5):
            for i in range(5):
                u=(i-2)/2;v=(j-2)/2;r=max(abs(u),abs(v))
                if not r:y=z=0
                else:
                    if abs(u)>=abs(v):a=v/abs(u)*math.pi/4 if u>0 else math.pi-v/abs(u)*math.pi/4
                    else:a=math.pi/2-u/abs(v)*math.pi/4 if v>0 else -math.pi/2+u/abs(v)*math.pi/4
                    y=.368*r*math.cos(a);z=.368*r*math.sin(a)
                ids[i,j]=len(vs);vs.append(((x-850)/100,y,z))
        rings.append([ids[p] for p in perimeter])
        for j in range(4):
            for i in range(4):fs.append(tuple(ids[p] for p in [(i,j),(i+1,j),(i+1,j+1),(i,j+1)]))
    for i in range(16):fs.append((rings[0][i],rings[0][(i+1)%16],rings[1][(i+1)%16],rings[1][i]))
    inner=mesh_object('04 | Visible central cylinder',vs,fs,collection)
    inner['tutorial_stage']='Visible cylindrical silhouette behind side slots, approximately 10:40.'
    return outer,inner
