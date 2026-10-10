"""Disposable review only: open current blend, render views, never save scene overrides."""
import bpy,bmesh,json,math
from pathlib import Path
from mathutils import Vector
R=Path('C:/Users/Dell/Downloads/3D/research/crnt-designers/panel')
o=bpy.data.objects['Panel'];sc=bpy.context.scene
report=json.loads((R/'validation.json').read_text())
def stats(mesh):
 bm=bmesh.new();bm.from_mesh(mesh)
 pending=set(bm.verts);components=0
 while pending:
  components+=1;stack=[pending.pop()]
  while stack:
   a=stack.pop()
   for e in a.link_edges:
    b=e.other_vert(a)
    if b in pending:pending.remove(b);stack.append(b)
 d={'vertices':len(bm.verts),'faces':len(bm.faces),'nonquads':sum(len(f.verts)!=4 for f in bm.faces),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'zero_area_faces':sum(f.calc_area()<1e-10 for f in bm.faces),'components':components,'signed_volume':bm.calc_volume(signed=True)}
 bm.free();return d
report['base_half']=stats(o.data)
bm=bmesh.new();bm.from_mesh(o.data)
report['base_boundaries_on_mirror']=all(all(abs(v.co.x)<1e-6 for v in e.verts) for e in bm.edges if not e.is_manifold)
bm.free()
sub=o.modifiers[-1];sub.show_viewport=False;sub.show_render=False
bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get();ev=o.evaluated_get(deps);me=ev.to_mesh();report['mirrored_base']=stats(me);ev.to_mesh_clear()
sub.show_viewport=True;sub.show_render=True;bpy.context.view_layer.update();ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();report['subdivision']=stats(me);ev.to_mesh_clear()
report['minimum_nominal_floor_thickness']=.019
(R/'validation.json').write_text(json.dumps(report,indent=2))
sc.render.engine='BLENDER_WORKBENCH';sc.render.resolution_x=1200;sc.render.resolution_y=1050;sc.render.resolution_percentage=100
sc.render.image_settings.file_format='PNG';sc.render.film_transparent=False
sc.world.color=(.08,.08,.08)
s=sc.display.shading;s.light='STUDIO';s.color_type='OBJECT';s.show_shadows=True;s.show_cavity=True;s.cavity_type='BOTH';s.show_specular_highlight=True;s.background_type='WORLD'
o.color=(.57,.60,.64,1);o.show_wire=False
camdata=bpy.data.cameras.new('Review camera');cam=bpy.data.objects.new('Review camera',camdata);sc.collection.objects.link(cam);sc.camera=cam;camdata.type='ORTHO';camdata.ortho_scale=3.8
center=Vector((0,0,-.325))
def view(name,eye):
 cam.location=center+Vector(eye);cam.rotation_euler=(center-cam.location).to_track_quat('-Z','Y').to_euler()
 sc.render.filepath=str(R/'review'/f'{name}.png');bpy.ops.render.render(write_still=True)
view('model',(3,-9,2.5));view('rear',(-2,9,2));view('side',(8,-1,0))
sub.show_viewport=False;sub.show_render=False
for p in o.data.polygons:p.use_smooth=False
bpy.context.view_layer.update();ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh()
curve=bpy.data.curves.new('Base edge overlay','CURVE');curve.dimensions='3D';curve.bevel_depth=.0011;curve.bevel_resolution=0
for e in me.edges:
 a,b=[me.vertices[i].co for i in e.vertices]
 sp=curve.splines.new('POLY');sp.points.add(1);sp.points[0].co=(*a,1);sp.points[1].co=(*b,1)
ev.to_mesh_clear()
wire=bpy.data.objects.new('Base edge overlay',curve);sc.collection.objects.link(wire);wire.color=(.015,.02,.025,1)
view('topology',(0,-9,0))
print(json.dumps(report))
