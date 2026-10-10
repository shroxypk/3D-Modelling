"""Disposable render process. Never saves temporary settings."""
import bpy
from pathlib import Path
from mathutils import Vector
R=Path('C:/Users/Dell/Downloads/3D/research/crnt-designers/cylindrical-design')
sc=bpy.context.scene;objects=[o for o in sc.objects if o.type=='MESH']
assembly=len(objects)>1
sc.render.engine='BLENDER_WORKBENCH';sc.render.resolution_x=1200;sc.render.resolution_y=800;sc.render.resolution_percentage=100
sc.render.image_settings.file_format='PNG';sc.world.color=(.065,.065,.065)
s=sc.display.shading;s.light='STUDIO';s.color_type='OBJECT';s.show_shadows=False;s.show_cavity=True;s.cavity_type='BOTH';s.background_type='WORLD'
for o in objects:o.color=(.58,.60,.63,1)
cd=bpy.data.cameras.new('Review');cam=bpy.data.objects.new('Review',cd);sc.collection.objects.link(cam);sc.camera=cam;cd.type='ORTHO';cd.ortho_scale=6.6
center=Vector((0,0,0))
def view(name,eye):
 cam.location=center+Vector(eye);cam.rotation_euler=(center-cam.location).to_track_quat('-Z','Y').to_euler()
 sc.render.filepath=str(R/'review'/f'{name}.png');bpy.ops.render.render(write_still=True)
view('model',(2,-5,2));view('front',(0,-5,0));view('rear',(0,5,0));view('top',(0,0,5))
for o in objects:
 for m in o.modifiers:m.show_viewport=False;m.show_render=False
 for p in o.data.polygons:p.use_smooth=False
bpy.context.view_layer.update();view('base',(1,-5,3))
for o in objects:
 curve=bpy.data.curves.new('Edge review','CURVE');curve.dimensions='3D';curve.bevel_depth=.0015;curve.bevel_resolution=0
 for e in o.data.edges:
  sp=curve.splines.new('POLY');sp.points.add(1)
  for j,i in enumerate(e.vertices):sp.points[j].co=(*o.data.vertices[i].co,1)
 wire=bpy.data.objects.new('Edge review',curve);sc.collection.objects.link(wire);wire.matrix_world=o.matrix_world.copy();wire.color=(.01,.01,.01,1)
view('topology',(1,-5,3))
