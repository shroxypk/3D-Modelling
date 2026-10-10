"""Tutorial 12:40–15:40: alternating face extrusions on separate rail strips."""
import bpy,bmesh

def rail(collection,name,start,end,teeth,width,base,deck,tip,root_width=None,tip_width=None):
    root_width=width if root_width is None else root_width
    tip_width=width if tip_width is None else tip_width
    segments=teeth*2-1;vs=[];fs=[]
    for i in range(segments+1):
        x=(start+(end-start)*i/segments-850)/100
        vs.extend([(x,-root_width,base),(x,root_width,base),(x,width,deck),(x,-width,deck)])
    for i in range(segments):
        a=i*4;b=a+4
        fs.extend([(a,b,b+1,a+1),(a+1,b+1,b+2,a+2),(a+3,b+3,b,a)])
        top=(a+3,a+2,b+2,b+3)
        if i%2:
            fs.append(top)
        else:
            lifted=[]
            for j in top:
                x,y,z=vs[j];lifted.append(len(vs));vs.append((x,tip_width if y>0 else -tip_width,tip))
            fs.append(tuple(lifted))
            for k in range(4):fs.append((top[k],top[(k+1)%4],lifted[(k+1)%4],lifted[k]))
    fs.extend([(0,1,2,3),tuple(range(segments*4,segments*4+4))])
    me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update()
    bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
    o=bpy.data.objects.new(name,me);collection.objects.link(o);o.color=(.47,.49,.52,1)
    o['construction']='Alternating connected face extrusions, as shown in tutorial; base cage without subdivision.'
    return o

def build(collection):
    rail(collection,'05 | Upper rail extrusion',498,1597,31,.458,.773,.879,.964,.406,.406)
    rail(collection,'06 | Lower front rail extrusion',498,675,7,.247,-.973,-1.024,-1.087)
