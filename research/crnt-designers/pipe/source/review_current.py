import bpy,bmesh,json
from pathlib import Path
from mathutils import Vector
R=Path('C:/Users/Dell/Downloads/3D/research/crnt-designers/pipe')
o=bpy.data.objects['Pipe'];sc=bpy.context.scene
sc.render.engine='BLENDER_WORKBENCH';sc.render.resolution_x=1100;sc.render.resolution_y=1000;sc.render.resolution_percentage=100
sc.render.image_settings.file_format='PNG';sc.render.film_transparent=False
sc.world.color=(.08,.08,.08)
s=sc.display.shading;s.light='STUDIO';s.color_type='OBJECT';s.show_shadows=True;s.show_cavity=True;s.cavity_type='BOTH';s.show_specular_highlight=True;s.background_type='WORLD'
o.color=(.57,.60,.64,1);o.show_wire=False
camdata=bpy.data.cameras.new('Review camera');cam=bpy.data.objects.new('Review camera',camdata);sc.collection.objects.link(cam);sc.camera=cam;camdata.type='ORTHO';camdata.ortho_scale=5.3
center=Vector((0,0,.9))
def view(name,eye):
 cam.location=center+Vector(eye);cam.rotation_euler=(center-cam.location).to_track_quat('-Z','Y').to_euler()
 sc.render.filepath=str(R/'review'/f'{name}.png');bpy.ops.render.render(write_still=True)
o.modifiers['Surface preview'].show_viewport=False;o.modifiers['Surface preview'].show_render=False
view('base',(-5,-7,5))
sub=o.modifiers.get('Surface preview')
sub.show_viewport=True;sub.show_render=True
view('model',(-5,-7,5));view('side',(0,-8,0));view('bore',(-2,-2,8))
sub.show_viewport=False;sub.show_render=False
for p in o.data.polygons:p.use_smooth=False
bpy.context.view_layer.update()
ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());mesh=ev.to_mesh()

curve=bpy.data.curves.new('Base edge overlay','CURVE');curve.dimensions='3D';curve.bevel_depth=.0015;curve.bevel_resolution=0
for e in mesh.edges:
 a,b=[mesh.vertices[i].co for i in e.vertices]
 sp=curve.splines.new('POLY');sp.points.add(1);sp.points[0].co=(*a,1);sp.points[1].co=(*b,1)
wire=bpy.data.objects.new('Base edge overlay',curve);sc.collection.objects.link(wire);wire.color=(.015,.02,.025,1)
view('topology',(-5,-7,5))
# Cross-section for inspection only. This disposable scene is never saved.
bpy.data.objects.remove(wire,do_unlink=True)
bm=bmesh.new();bm.from_mesh(mesh)
ev.to_mesh_clear()
for mod in o.modifiers:mod.show_render=False;mod.show_viewport=False
bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=1e-6,plane_co=(0,0,0),plane_no=(1,0,0),clear_outer=True,clear_inner=False)
bm.to_mesh(o.data);bm.free()
view('interior',(7,2,2))
