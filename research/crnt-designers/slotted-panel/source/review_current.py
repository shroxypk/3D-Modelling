"""Disposable image review; never saves display overrides into SlottedPanel.blend."""
import bpy
from pathlib import Path
from mathutils import Vector
R=Path('C:/Users/Dell/Downloads/3D/research/crnt-designers/slotted-panel')
o=bpy.data.objects['SlottedPanel'];sc=bpy.context.scene
sc.render.engine='BLENDER_WORKBENCH';sc.render.resolution_x=1100;sc.render.resolution_y=950;sc.render.resolution_percentage=100
sc.render.image_settings.file_format='PNG';sc.world.color=(.08,.08,.08)
s=sc.display.shading;s.light='STUDIO';s.color_type='OBJECT';s.show_shadows=False;s.show_cavity=True;s.cavity_type='BOTH';s.background_type='WORLD'
o.color=(.58,.60,.63,1)
cd=bpy.data.cameras.new('Review');cam=bpy.data.objects.new('Review',cd);sc.collection.objects.link(cam);sc.camera=cam;cd.type='ORTHO';cd.ortho_scale=5.5
center=Vector((0,0,.2))
def view(name,eye):
 cam.location=center+Vector(eye);cam.rotation_euler=(center-cam.location).to_track_quat('-Z','Y').to_euler()
 sc.render.filepath=str(R/'review'/f'{name}.png');bpy.ops.render.render(write_still=True)
view('model',(1,-3,6));view('front',(0,0,5));view('side',(0,-5,0))
view('underside',(3,4,-5))
sub=o.modifiers.get('Surface review')
if sub:sub.show_viewport=False;sub.show_render=False
for p in o.data.polygons:p.use_smooth=False
bpy.context.view_layer.update()
view('base',(3,5,4))
curve=bpy.data.curves.new('Edge review','CURVE');curve.dimensions='3D';curve.bevel_depth=.001;curve.bevel_resolution=0
evaluated=o.evaluated_get(bpy.context.evaluated_depsgraph_get());review_mesh=evaluated.to_mesh()
for e in review_mesh.edges:
 sp=curve.splines.new('POLY');sp.points.add(1)
 for j,i in enumerate(e.vertices):sp.points[j].co=(*review_mesh.vertices[i].co,1)
evaluated.to_mesh_clear()
wire=bpy.data.objects.new('Edge review',curve);sc.collection.objects.link(wire);wire.color=(.01,.01,.01,1)
view('topology',(0,0,5))

