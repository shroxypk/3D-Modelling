import bpy,math,json
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'Bracket.blend'))
o=next(o for o in bpy.context.scene.objects if o.type=='MESH')
tree=BVHTree.FromObject(o,bpy.context.evaluated_depsgraph_get())
results=[]
for kind,c,axes,target in [('upright',(0,-1.68,1.75),(0,2),.53),('upright',(0,1.68,1.75),(0,2),.53),('mount',(0,-3.56,.06),(0,1),.34),('mount',(0,3.56,.06),(0,1),.34)]:
    radii=[]
    for i in range(360):
        a=i*math.pi/180;direction=Vector((0,0,0));direction[axes[0]]=math.cos(a);direction[axes[1]]=math.sin(a)
        hit,normal,face,distance=tree.ray_cast(Vector(c),direction,2)
        if hit is not None:radii.append(distance)
    results.append({'kind':kind,'center':c,'nominal_radius':target,'hits':len(radii),'mean_radius':sum(radii)/len(radii),'min_radius':min(radii),'max_radius':max(radii)})
results.append({'shared_upright_axis_clear':tree.ray_cast(Vector((0,-5,1.75)),Vector((0,1,0)),10)[0] is None,'mount_axes_clear':[tree.ray_cast(Vector((0,y,2)),Vector((0,0,-1)),3)[0] is None for y in [-3.56,3.56]]})
(ROOT/'fit-check.json').write_text(json.dumps(results,indent=2),encoding='utf-8');print(json.dumps(results))
