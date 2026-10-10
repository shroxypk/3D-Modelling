import bpy,sys
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'Bracket.blend'))
diagnostic='--subd' in sys.argv
if diagnostic:
    obj=next(o for o in bpy.context.scene.objects if o.type=='MESH')
    for m in obj.modifiers:
        if m.type=='WEIGHTED_NORMAL':m.show_render=False;m.show_viewport=False
    sub=next((m for m in obj.modifiers if m.type=='SUBSURF'),None)
    if sub is None:sub=obj.modifiers.new('Temporary subdivision test','SUBSURF')
    sub.levels=2;sub.render_levels=2
s=bpy.context.scene;s.render.engine='BLENDER_WORKBENCH';s.render.resolution_x=1300;s.render.resolution_y=950;s.render.resolution_percentage=100
s.render.image_settings.file_format='PNG';s.view_settings.view_transform='Standard'
s.display.shading.light='STUDIO';s.display.shading.color_type='SINGLE';s.display.shading.single_color=(.55,.57,.6);s.display.shading.show_cavity=True
s.display.shading.background_type='WORLD';s.world=bpy.data.worlds.new('Review only');s.world.color=(.045,.045,.045)
cam=bpy.data.objects.new('Review only',bpy.data.cameras.new('Review only'));s.collection.objects.link(cam);s.camera=cam;cam.data.type='ORTHO';cam.data.ortho_scale=10.5
def render(name,loc,target=(0,0,1)):
    cam.location=loc;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();s.render.filepath=str(ROOT/(('diagnostic-' if diagnostic else '')+name));bpy.ops.render.render(write_still=True)
render('model.png',(7,-9,7))
render('side.png',(9,0,2),(0,0,1.3))
render('underside.png',(5,-8,-6),(0,0,.5))
cam.data.ortho_scale=14
render('top.png',(0,0,12),(0,0,0))
cam.data.ortho_scale=10.5
if '--reflection' in sys.argv:
    mats=[light for light in bpy.context.preferences.studio_lights if light.type=='MATCAP']
    chosen=next((light for light in mats if 'metal' in light.name.lower()),None)
    if chosen:
        s.display.shading.light='MATCAP';s.display.shading.studio_light=chosen.name
        s.display.shading.show_cavity=False
        render('reflection.png',(7,-9,7))
        print('Reflection matcap:',chosen.name)
    s.display.shading.light='STUDIO';s.display.shading.show_cavity=True
o=next(o for o in s.objects if o.type=='MESH')
for m in o.modifiers:
    if m.type!='MIRROR':m.show_render=False;m.show_viewport=False
bpy.context.view_layer.update();eo=o.evaluated_get(bpy.context.evaluated_depsgraph_get());mesh=eo.to_mesh()
cu=bpy.data.curves.new('Cage','CURVE');cu.dimensions='3D';cu.bevel_depth=.004;cu.bevel_resolution=0
for e in mesh.edges:
    sp=cu.splines.new('POLY');sp.points.add(1)
    for p,i in zip(sp.points,e.vertices):p.co=(*(o.matrix_world@mesh.vertices[i].co),1)
eo.to_mesh_clear();w=bpy.data.objects.new('Cage',cu);s.collection.objects.link(w);w.color=(.01,.01,.01,1);o.color=(.55,.57,.6,1)
for p in o.data.polygons:p.use_smooth=False
s.display.shading.color_type='OBJECT';render('topology.png',(7,-9,7))
