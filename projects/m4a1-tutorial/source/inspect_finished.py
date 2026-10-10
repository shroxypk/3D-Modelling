"""Read-only inspection of the user-supplied finished Blender reference."""
import bpy,json
from pathlib import Path
from mathutils import Vector
P=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=r'C:\Users\Dell\Downloads\3D\M4A1\M4A1.blend')
report=[]
for o in bpy.data.objects:
    if o.type!='MESH':continue
    bbox=[o.matrix_world@Vector(v) for v in o.bound_box]
    report.append(dict(name=o.name,vertices=len(o.data.vertices),faces=len(o.data.polygons),
                       bounds=[(min(v[a] for v in bbox),max(v[a] for v in bbox)) for a in range(3)],
                       modifiers=[dict(name=m.name,type=m.type) for m in o.modifiers]))
(P/'review'/'finished-reference-inventory.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report))

stock=bpy.data.objects.get('Cylinder.003')
for o in bpy.data.objects:o.hide_render=(o!=stock)
stock.color=(.48,.5,.53,1)
s=bpy.context.scene
s.render.engine='BLENDER_WORKBENCH'
s.display.shading.light='STUDIO';s.display.shading.color_type='OBJECT'
s.display.shading.show_cavity=True;s.display.shading.cavity_type='BOTH'
s.display.shading.background_type='WORLD'
s.world=bpy.data.worlds.new('Reference inspection');s.world.color=(.055,.055,.055)
s.view_settings.view_transform='Standard'
cam=bpy.data.objects.new('Temporary reference camera',bpy.data.cameras.new('Temporary reference camera'))
s.collection.objects.link(cam);s.camera=cam
target=Vector((22.8,0,9.8));cam.location=target+Vector((-11,-30,14))
cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
cam.data.type='ORTHO';cam.data.ortho_scale=16
s.render.resolution_x=1200;s.render.resolution_y=900;s.render.resolution_percentage=100
s.render.filepath=str(P/'review'/'finished-stock-reference.png');bpy.ops.render.render(write_still=True)
world=[stock.matrix_world@v.co for v in stock.data.vertices]
sections={}
for x in [18,20,22,24,26,28]:
    hits=[]
    for e in stock.data.edges:
        a,b=[world[i] for i in e.vertices]
        if (a.x-x)*(b.x-x)<0:
            p=a+(b-a)*((x-a.x)/(b.x-a.x));hits.append([p.y,p.z])
    sections[x]=hits
(P/'review'/'finished-stock-sections.json').write_text(json.dumps(sections,indent=2))
