import bpy
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'RootStudy.blend'))
s=bpy.context.scene;s.render.engine='BLENDER_WORKBENCH';s.render.resolution_x=1400;s.render.resolution_y=850;s.render.resolution_percentage=100
s.render.image_settings.file_format='PNG';s.view_settings.view_transform='Standard'
s.display.shading.light='STUDIO';s.display.shading.color_type='SINGLE';s.display.shading.single_color=(.55,.57,.6);s.display.shading.show_cavity=True
s.display.shading.background_type='WORLD';s.world=bpy.data.worlds.new('Review only');s.world.color=(.045,.045,.045)
cam=bpy.data.objects.new('Review only',bpy.data.cameras.new('Review only'));s.collection.objects.link(cam);s.camera=cam;cam.data.type='ORTHO';cam.data.ortho_scale=6.8
cam.location=(3,-8,5);cam.rotation_euler=(Vector((0,-.2,1.1))-cam.location).to_track_quat('-Z','Y').to_euler()
s.render.filepath=str(ROOT/'model.png');bpy.ops.render.render(write_still=True)
for o in list(s.objects):
    if o.type!='MESH':continue
    for m in o.modifiers:m.show_render=False
    for p in o.data.polygons:p.use_smooth=False
    cu=bpy.data.curves.new('Base cage','CURVE');cu.dimensions='3D';cu.bevel_depth=.003;cu.bevel_resolution=0
    for e in o.data.edges:
        sp=cu.splines.new('POLY');sp.points.add(1)
        for p,i in zip(sp.points,e.vertices):p.co=(*(o.matrix_world@o.data.vertices[i].co),1)
    w=bpy.data.objects.new('Base cage',cu);s.collection.objects.link(w);w.color=(.01,.01,.01,1);o.color=(.55,.57,.6,1)
s.display.shading.color_type='OBJECT';s.render.filepath=str(ROOT/'topology.png');bpy.ops.render.render(write_still=True)
