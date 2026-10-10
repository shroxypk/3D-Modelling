"""Tutorial 04:00–07:10 side-strip extrusion and connected raised front ribs."""
import bpy,bmesh,math

def build(collection):
    profile=[(489,.918),(505,.918),(505,.731),(520,.731),(520,.918),
             (535,.918),(535,.731),(551,.731),(551,.918),(566,.918),
             (566,.731),(582,.731),(582,.918),(597,.918),(597,.731),
             (613,.731),(613,.918),(658,.918),(665,.907),(674,.857),
             (683,.790),(691,.748),(700,.731),(1493,.731),
             (1499,.744),(1507,.800),(1515,.867),(1522,.907),(1528,.918),
             (1570,.918),(1570,.835),(1597,.835)]
    # Small real chamfer width at each rib shoulder; avoid collapsed sweep faces.
    for i in range(len(profile)-1):
        if profile[i][0]==profile[i+1][0]:
            profile[i]=(profile[i][0]-.8,profile[i][1])
    vs=[];fs=[];lookup={}
    def v(x,y,z):
        p=(round(x,7),round(y,7),round(z,7))
        if p not in lookup:lookup[p]=len(vs);vs.append(p)
        return lookup[p]
    top=.286;bottom=-.299
    rows=[top+(bottom-top)*i/4 for i in range(5)]
    for (a,da),(b,db) in zip(profile,profile[1:]):
        if a==700 and b==1493:continue
        for za,zb in zip(rows,rows[1:]):
            fs.append((v((a-850)/100,da,za),v((b-850)/100,db,za),
                       v((b-850)/100,db,zb),v((a-850)/100,da,zb)))
    bounds=[700,850,976,1103.5,1230,1357,1493]
    centers=[782,913,1040,1167,1294,1425]
    for a,b,c in zip(bounds,bounds[1:],centers):
        left=(a-850)/100;right=(b-850)/100;w=right-left;h=top-bottom
        outer=[(left+w*.25,top),(left+w*.5,top),(left+w*.75,top),(right,top),
               (right,top-h*.25),(right,top-h*.5),(right,top-h*.75),(right,bottom),
               (left+w*.75,bottom),(left+w*.5,bottom),(left+w*.25,bottom),(left,bottom),
               (left,bottom+h*.25),(left,bottom+h*.5),(left,bottom+h*.75),(left,top)]
        cx=(c-850)/100;cz=-.005;hw=.52;hh=.14;rad=.08;s=math.sqrt(.5)
        l=cx-hw;r=cx+hw;t=cz+hh;bt=cz-hh
        inner=[(l+rad,t),(cx,t),(r-rad,t),(r-rad+rad*s,t-rad+rad*s),
               (r,t-rad),(r,cz),(r,bt+rad),(r-rad+rad*s,bt+rad-rad*s),
               (r-rad,bt),(cx,bt),(l+rad,bt),(l+rad-rad*s,bt+rad-rad*s),
               (l,bt+rad),(l,cz),(l,t-rad),(l+rad-rad*s,t-rad+rad*s)]
        loops=[[v(x,.731,z) for x,z in loop] for loop in [outer,inner]]
        for j in range(16):fs.append((loops[0][j],loops[0][(j+1)%16],loops[1][(j+1)%16],loops[1][j]))
    # Bridge to the symmetry plane: a single width-spanning perforated piece.
    front_faces=list(fs)
    edge_counts={}
    for face in front_faces:
        for a,b in zip(face,face[1:]+face[:1]):
            key=tuple(sorted((a,b)));edge_counts[key]=edge_counts.get(key,0)+1
    for (a,b),count in edge_counts.items():
        if count!=1:continue
        pa,pb=vs[a],vs[b]
        outer=(abs(pa[2]-top)<1e-6 and abs(pb[2]-top)<1e-6) or (abs(pa[2]-bottom)<1e-6 and abs(pb[2]-bottom)<1e-6) or (abs(pa[0]-pb[0])<1e-6 and (abs(pa[0]+3.61)<1e-6 or abs(pa[0]-7.47)<1e-6))
        ca=v(pa[0],0,pa[2]);cb=v(pb[0],0,pb[2])
        if outer:
            ia=v(pa[0],.651,pa[2]);ib=v(pb[0],.651,pb[2])
            fs.extend([(a,b,ib,ia),(ia,ib,cb,ca)])
        else:fs.append((a,b,cb,ca))
    me=bpy.data.meshes.new('Connected side strip');me.from_pydata(vs,[],fs);me.update()
    bm=bmesh.new();bm.from_mesh(me)
    bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7)
    degenerate=[f for f in bm.faces if f.calc_area()<1e-10]
    bmesh.ops.delete(bm,geom=degenerate,context='FACES_ONLY')
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
    o=bpy.data.objects.new('03 | Side strips and integral ribs',me);collection.objects.link(o);o.color=(.47,.49,.52,1)
    mirror=o.modifiers.new('Opposite side','MIRROR');mirror.use_axis=(False,True,False);mirror.use_clip=True;mirror.merge_threshold=.00001
    weights=me.attributes.new('bevel_weight_edge','FLOAT','EDGE')
    for e in me.edges:
        a,b=[me.vertices[i].co for i in e.vertices]
        horizontal=abs(a.z-b.z)<1e-6 and (abs(a.z-top)<1e-6 or abs(a.z-bottom)<1e-6)
        if horizontal and min(a.y,b.y)>.83:weights.data[e.index].value=1
    bevel=o.modifiers.new('Raised rib edge chamfers','BEVEL');bevel.limit_method='WEIGHT';bevel.width=.073;bevel.segments=1;bevel.use_clamp_overlap=False
    o['tutorial_stage']='Connected side strip, front ribs and six through-openings through approximately 09:35.'
    return o
