"""Temporary review only. Never save camera or lighting overrides."""
import bpy
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'Holosight.blend'))
s=bpy.context.scene;s.render.engine='BLENDER_WORKBENCH';s.view_settings.view_transform='Standard'
s.render.resolution_x=1000;s.render.resolution_y=800;s.render.resolution_percentage=100
s.render.image_settings.file_format='PNG'
s.display.shading.light='STUDIO';s.display.shading.color_type='OBJECT';s.display.shading.show_cavity=True
s.display.shading.background_type='WORLD';s.world=bpy.data.worlds.new('Temporary review');s.world.color=(.045,.045,.045)
data=bpy.data.cameras.new('Review');cam=bpy.data.objects.new('Review',data);s.collection.objects.link(cam);s.camera=cam
data.type='ORTHO';data.ortho_scale=2.15;target=Vector((0,.12,.5))
def camera(delta):
    cam.location=target+Vector(delta);cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
camera((3,4,2));s.render.filepath=str(ROOT/'model.png');bpy.ops.render.render(write_still=True)
camera((0,0,5));s.render.filepath=str(ROOT/'review'/'top.png');bpy.ops.render.render(write_still=True)
for obj in list(s.objects):
    if obj.type!='MESH':continue
    ev=obj.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh()
    cu=bpy.data.curves.new('Review wires','CURVE');cu.dimensions='3D';cu.bevel_depth=.0012;cu.bevel_resolution=0
    for edge in me.edges:
        sp=cu.splines.new('POLY');sp.points.add(1)
        for point,idx in zip(sp.points,edge.vertices):point.co=(*(obj.matrix_world@me.vertices[idx].co),1)
    wire=bpy.data.objects.new('Review wires',cu);s.collection.objects.link(wire);wire.color=(.008,.008,.008,1)
    ev.to_mesh_clear()
camera((5,0,0));s.render.filepath=str(ROOT/'review'/'side.png');bpy.ops.render.render(write_still=True)
camera((3,4,2));s.render.filepath=str(ROOT/'topology.png');bpy.ops.render.render(write_still=True)
camera((0,-5,0));s.render.filepath=str(ROOT/'review'/'front.png');bpy.ops.render.render(write_still=True)
camera((0,0,5));s.render.filepath=str(ROOT/'review'/'top-topology.png');bpy.ops.render.render(write_still=True)

# Isolated profile for judging the lower body without the hood occluding it.
for obj in s.objects:
    if obj.name.startswith('01 |') or obj.name.startswith('00 |') or obj.type=='CURVE': obj.hide_render=True
camera((5,0,0));s.render.filepath=str(ROOT/'review'/'inner-side.png');bpy.ops.render.render(write_still=True)

ob=bpy.data.objects['02 | Inner housing']
cu=bpy.data.curves.new('Isolated housing wires','CURVE');cu.dimensions='3D';cu.bevel_depth=.0007;cu.bevel_resolution=0
for edge in ob.data.edges:
    sp=cu.splines.new('POLY');sp.points.add(1)
    for point,idx in zip(sp.points,edge.vertices):point.co=(*(ob.matrix_world@ob.data.vertices[idx].co),1)
wire=bpy.data.objects.new('Isolated housing wires',cu);s.collection.objects.link(wire);wire.color=(.008,.008,.008,1)
camera((5,0,0));s.render.filepath=str(ROOT/'review'/'shoulder-side.png');bpy.ops.render.render(write_still=True)

target=Vector((.435,.735,.230));data.ortho_scale=.65
for obj in s.objects:
    if obj.type=='CURVE':obj.hide_render=True
camera((3,2,1));s.render.filepath=str(ROOT/'review'/'cap-close.png');bpy.ops.render.render(write_still=True)
wire.hide_render=False
s.render.filepath=str(ROOT/'review'/'cap-topology.png');bpy.ops.render.render(write_still=True)

for obj in s.objects:
    if obj.type=='CURVE':obj.hide_render=True
target=Vector((0,.2,.19));data.ortho_scale=1.7
camera((2,3,-3));s.render.filepath=str(ROOT/'review'/'underside.png');bpy.ops.render.render(write_still=True)
wire.hide_render=False
s.render.filepath=str(ROOT/'review'/'underside-topology.png');bpy.ops.render.render(write_still=True)
