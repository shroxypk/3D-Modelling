"""Tutorial 02:15-03:27: repeat curved panels and fit the underlying tube.
Run after build.py. Retains linked panel geometry for consistent later edits.
"""
import bpy,bmesh,math,json
from pathlib import Path
from mathutils import Vector
R=Path('C:/Users/Dell/Downloads/3D/research/crnt-designers/cylindrical-design')
base=bpy.data.objects['CurvedPanel']
# Four panels around the circumference, two rows; gaps remain separate parts.
for row,z in enumerate((-.92,.92)):
 for k in range(4):
  name='CurvedPanel' if row==0 and k==0 else f'Panel_{row}_{k}'
  o=bpy.data.objects.get(name)
  if o is None:o=base.copy();o.data=base.data;bpy.context.scene.collection.objects.link(o);o.name=name
  o.data=base.data
  o.location=(0,0,z);o.rotation_euler=(0,0,k*math.pi/2)
# Underlying open tube: quad cross-section rings with supported upper/lower lips.
bm=bmesh.new();rings=[]
profile=[(.962,-1.67),(.962,-1.64),(.962,1.64),(.962,1.67),(.954,1.68),(.918,1.68),(.910,1.67),(.910,1.64),(.910,-1.64),(.910,-1.67),(.918,-1.68),(.954,-1.68)]
for r,z in profile:rings.append([bm.verts.new((r*math.sin(i*math.tau/64),-r*math.cos(i*math.tau/64),z)) for i in range(64)])
for j,a in enumerate(rings):
 b=rings[(j+1)%len(rings)]
 for i in range(64):bm.faces.new((a[i],a[(i+1)%64],b[(i+1)%64],b[i]))
bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));me=bpy.data.meshes.new('Open tube quad rings');bm.to_mesh(me);bm.free()
o=bpy.data.objects.get('ParentTube')
if o:
 old=o.data;o.data=me
 if old.users==0:bpy.data.meshes.remove(old)
else:o=bpy.data.objects.new('ParentTube',me);bpy.context.scene.collection.objects.link(o)
for m in list(o.modifiers):o.modifiers.remove(m)
sub=o.modifiers.new('Surface review','SUBSURF');sub.levels=2;sub.render_levels=2
for p in me.polygons:p.use_smooth=True
for area in bpy.context.screen.areas:
 if area.type=='VIEW_3D':
  rv=area.spaces.active.region_3d;rv.view_location=(0,0,0);rv.view_distance=5;rv.view_rotation=Vector((2,-5,2)).to_track_quat('Z','Y');rv.view_perspective='ORTHO'
bpy.ops.wm.save_as_mainfile(filepath=str(R/'CylindricalDesign.blend'))
print('Eight linked panels and supported open parent tube saved; bands and end rims remain.')
