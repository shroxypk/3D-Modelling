"""New restart, tutorial ~02:40–03:25: extruded body, no detail strip or slots."""
import bpy,bmesh

def build(collection):
    # Finished reference Cube.001 cross-section, scaled to the side board.
    # Width .651 is the body; projecting side attachments are later components.
    stations=[(498,450),(662,450),(672,436),(685,426),(703,420),
              (1315,420),(1338,424),(1357,436),(1374,450),(1597,450)]
    vs=[];fs=[]
    # The tutorial closes the middle cut with flat faces, not a thin shell.
    for upper in (True,False):
        offset=len(vs)
        for x,bottom in stations:
            profile=([(0,.775),(.406,.775),(.406,.618),(.651,.295),(.651,.200),(0,.200)]
                     if upper else [(0,-.195),(.651,-.195),(.651,-.278),(.406,-.730),(.406,(345-bottom)/100),(0,(345-bottom)/100)])
            vs.extend(((x-850)/100,y,z) for y,z in profile)
        for i in range(len(stations)-1):
            for j in range(5):
                a=offset+i*6+j;b=a+6;fs.append((a,b,b+1,a+1))
        for i in (0,len(stations)-1):
            a=offset+i*6
            fs.extend([(a,a+1,a+2,a+5),(a+2,a+3,a+4,a+5)])
    me=bpy.data.meshes.new('Handguard base extrusion');me.from_pydata(vs,[],fs);me.update()
    bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
    o=bpy.data.objects.new('02 | Handguard base extrusion',me);collection.objects.link(o);o.color=(.47,.49,.52,1)
    mirror=o.modifiers.new('Width symmetry','MIRROR');mirror.use_axis=(False,True,False);mirror.use_clip=True;mirror.merge_threshold=.00001
    o['tutorial_stage']='Closed upper and lower extrusions after middle-band cut at approximately 10:05. Width Mirror, no subdivision.'
    return o
