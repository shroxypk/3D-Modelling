"""Render review images in a separate process without saving scene overrides."""
import bpy,sys
from pathlib import Path
from mathutils import Vector
P=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(P/'M4A1.blend'))
s=bpy.context.scene;s.render.engine='BLENDER_WORKBENCH';s.view_settings.view_transform='Standard'
s.render.resolution_x=1100;s.render.resolution_y=700;s.render.resolution_percentage=100
s.render.image_settings.file_format='PNG'
s.display.shading.light='STUDIO';s.display.shading.color_type='OBJECT';s.display.shading.show_cavity=True
s.display.shading.background_type='WORLD';s.world=bpy.data.worlds.new('Temporary review');s.world.color=(.055,.055,.055)
c=s.camera;t=Vector((6.3,0,-1.1));c.location=t+Vector((-5,-24,10));c.rotation_euler=(t-c.location).to_track_quat('-Z','Y').to_euler();c.data.type='ORTHO';c.data.ortho_scale=32
if '--stock' in sys.argv:
 t=Vector((17.1,0,-1.45));c.location=t+Vector((-4,-14,6));c.rotation_euler=(t-c.location).to_track_quat('-Z','Y').to_euler();c.data.ortho_scale=8.5
 for o in s.objects:
  if o.type=='MESH' and not o.name.startswith(('07 |','08 |','09 |')):o.hide_render=True
if '--handguard' in sys.argv:
 t=Vector((1.9,0,-.1));c.location=t+Vector((-5,-18,9));c.rotation_euler=(t-c.location).to_track_quat('-Z','Y').to_euler();c.data.ortho_scale=13.6
 for o in s.objects:
  if o.type=='MESH' and not o.name.startswith(('02 |','03 |','05 |','06 |')):o.hide_render=True
s.render.filepath=str(P/'model.png');bpy.ops.render.render(write_still=True)
if '--stock' in sys.argv:
 t=Vector((17.1,0,-1.45));c.location=t+Vector((0,-20,0));c.rotation_euler=(t-c.location).to_track_quat('-Z','Y').to_euler();c.data.ortho_scale=7.9
for o in list(bpy.data.objects):
 if o.type!='MESH' or o.hide_render:continue
 evaluated=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=evaluated.to_mesh()
 cu=bpy.data.curves.new('Temporary wire','CURVE');cu.dimensions='3D';cu.bevel_depth=.005;cu.bevel_resolution=0
 for e in me.edges:
    sp=cu.splines.new('POLY');sp.points.add(1)
    for p,i in zip(sp.points,e.vertices):p.co=(*(o.matrix_world@me.vertices[i].co),1)
 wire=bpy.data.objects.new('Temporary wire',cu);s.collection.objects.link(wire);wire.color=(.012,.012,.012,1)
 evaluated.to_mesh_clear()
s.render.filepath=str(P/'topology.png');bpy.ops.render.render(write_still=True)
if '--stock' in sys.argv:
 for o in s.objects:
  if o.name.startswith('Temporary wire'):o.hide_render=True
 for label,delta in [('front',(-20,0,0)),('rear',(20,0,0)),('underside',(-4,-14,-8))]:
  t=Vector((17.1,0,-1.45));c.location=t+Vector(delta);c.rotation_euler=(t-c.location).to_track_quat('-Z','Y').to_euler();c.data.ortho_scale=7.9
  s.render.filepath=str(P/'review'/('stock-'+label+'.png'));bpy.ops.render.render(write_still=True)
if '--handguard' in sys.argv:
 for o in s.objects:
  if o.name.startswith('Temporary wire'):o.hide_render=True
 for label,target,delta,scale in [('side',(1.9,0,-.1),(0,-20,0),12.6),('front',(-3.6,0,-.05),(-20,0,0),4.3),('rear',(7.47,0,-.05),(20,0,0),4.3)]:
  t=Vector(target);c.location=t+Vector(delta);c.rotation_euler=(t-c.location).to_track_quat('-Z','Y').to_euler();c.data.ortho_scale=scale
  s.render.filepath=str(P/'review'/('handguard-'+label+'.png'));bpy.ops.render.render(write_still=True)
