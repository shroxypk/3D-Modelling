import bpy
from pathlib import Path
from mathutils import Vector
root=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(root/'Holosight.blend'))
s=bpy.context.scene;s.render.engine='BLENDER_WORKBENCH';s.view_settings.view_transform='Standard'
s.render.resolution_x=420;s.render.resolution_y=420;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG'
s.display.shading.color_type='OBJECT';s.display.shading.light='STUDIO';s.display.shading.show_cavity=True
bpy.data.objects['01 | Hood'].hide_render=True
cam=bpy.data.objects.new('Corner review',bpy.data.cameras.new('Corner review'));s.collection.objects.link(cam);s.camera=cam
cam.data.type='ORTHO';cam.data.ortho_scale=.19
for end,y,direction in [('rear',-.295,-1),('front',.05,1)]:
 for ob in s.objects:
  if 'glass' in ob.name:ob.hide_render=('Rear' in ob.name)!=(end=='rear')
 for side,x in [('left',-.255),('right',.255)]:
  for height,z in [('lower',.468),('upper',.86)]:
   target=Vector((x,y,z));cam.location=target+Vector((0,direction*3,0));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
   s.render.filepath=str(root/'review'/f'corner-{end}-{side}-{height}.png');bpy.ops.render.render(write_still=True)
