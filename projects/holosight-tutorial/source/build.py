"""Fresh Ep.1 rebuild: hood and rail alignment aid. No subdivision."""
from pathlib import Path
import bpy,bmesh,math,json
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
col=bpy.data.collections.get('Holosight | Tutorial geometry')
for ob in list(col.objects): bpy.data.objects.remove(ob,do_unlink=True)
def make(name,v,f):
 me=bpy.data.meshes.new(name);me.from_pydata(v,[],f);me.update()
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
 ob=bpy.data.objects.new(name,me);col.objects.link(ob);ob.color=(.45,.47,.50,1);return ob
# Normalized visual proportions from the supplied board, not fabrication dimensions.
sections=[(0,.410,-.520,.520),(.22,.402,-.494,.520),(.36,.397,-.480,.478),(.48,.391,-.457,.355),(.55,.387,-.442,.257),(.62,.383,-.433,.212),(.69,.379,-.425,.188),(.76,.375,-.417,.183),(.83,.371,-.409,.194),(.89,.355,-.403,.195),(.94,.323,-.400,.195),(.974,.279,-.398,.195),(.990,.218,-.397,.195),(.997,.110,-.396,.195),(1,0,-.396,.195)]
v=[]
for z,x,rear,front in sections:v.extend([(x,rear,z),(x,front,z)])
hood=make('01 | Hood',v,[(2*i,2*i+1,2*i+3,2*i+2) for i in range(len(sections)-1)])
m=hood.modifiers.new('Center symmetry','MIRROR');m.use_clip=True;m.merge_threshold=1e-5
s=hood.modifiers.new('Shell thickness','SOLIDIFY');s.thickness=.036;s.offset=-1;s.use_even_offset=True
hood['Tutorial stage']='Ep.1 ~20:10 open hood; Mirror and Solidify. Base shape checkpoint.'
p=[(-.122,-.105),(.122,-.105),(.122,-.058),(.166,-.020),(.122,.018),(-.122,.018),(-.166,-.020),(-.122,-.058)]
v=[(x,y,z) for y in (-.66,.66) for x,z in p]
f=[(i,(i+1)%8,(i+1)%8+8,i+8) for i in range(8)]
f.extend([(0,1,6,7),(1,2,5,6),(2,3,4,5),(8,15,14,9),(9,14,13,10),(10,13,12,11)])
rail=make('00 | Rail alignment placeholder',v,f);rail.color=(.25,.27,.29,1)
rail['Tutorial stage']='Ep.1 ~14:00 alignment aid; mounting details unfinished.'
refs=bpy.data.collections.get('Reference | Essentials')
for ob in list(refs.objects):bpy.data.objects.remove(ob,do_unlink=True)
im=bpy.data.images.load(str(ROOT.parents[1]/'Essentials_Holosight/Reference/UWT2_Holosight_Tutorial.jpg'),check_existing=True)
if not im.packed_file:im.pack()
for name,loc,rot in [('Rear reference',((790.5-1138)/244,1.5,(870-784)/244),(math.pi/2,0,0)),('Side reference',(-1.5,(790.5-794)/244,(870-784)/244),(math.pi/2,0,math.pi/2))]:
 ob=bpy.data.objects.new(name,None);refs.objects.link(ob);ob.empty_display_type='IMAGE';ob.data=im;ob.empty_display_size=1581/244;ob.location=loc;ob.rotation_euler=rot;ob.hide_select=True
 ob.show_empty_image_orthographic=True;ob.show_empty_image_perspective=False;ob.show_empty_image_only_axis_aligned=True;ob.empty_image_depth='BACK';ob.color[3]=.45
for ob in bpy.context.selected_objects:ob.select_set(False)
import sys,importlib
sys.path.insert(0,str(ROOT/'source'))
import housing
importlib.reload(housing)
inner=housing.build(col)
inner.select_set(True);bpy.context.view_layer.objects.active=inner
bpy.context.scene['Study status']=inner['Tutorial stage']
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'Holosight.blend'))
report={}
for ob in col.objects:
 ev=ob.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();bm=bmesh.new();bm.from_mesh(me)
 report[ob.name]={'base_faces':len(ob.data.polygons),'base_quads':sum(len(p.vertices)==4 for p in ob.data.polygons),'evaluated_faces':len(bm.faces),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'zero_area_faces':sum(f.calc_area()<1e-10 for f in bm.faces)}
 bm.free();ev.to_mesh_clear()
(ROOT/'validation.json').write_text(json.dumps(report,indent=2));print(report)
