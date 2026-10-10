"""Finish the cover's connected center groove and planar quad caps.
Run after build.py, recess.py, floor_symmetry.py. Preserve working settings.
"""
import bpy,bmesh,math,json
from pathlib import Path
from mathutils import Vector
R=Path('C:/Users/Dell/Downloads/3D/research/crnt-designers/cover')
o=bpy.data.objects['Cover'];bm=bmesh.new();bm.from_mesh(o.data)
def bridge(a,b):
 for i in range(6):bm.faces.new((a[i],a[i+1],b[i+1],b[i]))
def fill_quarter(path,z):
 # Three by three grid; the two outside borders follow the round corner.
 g={}
 for j in range(4):g[(3,j)]=path[j]
 for i in range(4):g[(i,3)]=path[6-i]
 g[(0,0)]=bm.verts.new((0,0,z))
 for i in (1,2):g[(i,0)]=bm.verts.new((path[0].co.x*i/3,0,z))
 for j in (1,2):g[(0,j)]=bm.verts.new((0,path[-1].co.y*j/3,z))
 for i in (1,2):
  for j in (1,2):
   u,v=i/3,j/3
   co=g[(i,0)].co*(1-v)+g[(i,3)].co*v+g[(0,j)].co*(1-u)+g[(3,j)].co*u
   co-=g[(0,0)].co*(1-u)*(1-v)+g[(3,0)].co*u*(1-v)+g[(0,3)].co*(1-u)*v+g[(3,3)].co*u*v
   g[(i,j)]=bm.verts.new(co)
 for i in range(3):
  for j in range(3):bm.faces.new((g[(i,j)],g[(i+1,j)],g[(i+1,j+1)],g[(i,j+1)]))
for z in (.4,0):
 f=next(f for f in bm.faces if len(f.verts)>4 and all(abs(v.co.z-z)<1e-5 for v in f.verts))
 path=sorted([v for v in f.verts if v.co.x+v.co.y>.1],key=lambda v:math.atan2(v.co.y,v.co.x))
 assert len(path)==7
 original=[v.co.copy() for v in path]
 bm.faces.remove(f)
 for e in list(bm.edges):
  if not e.link_faces:bm.edges.remove(e)
 for v in list(bm.verts):
  if not v.link_edges:bm.verts.remove(v)
 if z>.1:
  # 03:45: .015 border width, center lowered .0213; support at ~.00668.
  for v in path:v.co.x*=1.022727;v.co.y*=1.022727
  profile=((1.0126,.4),(1.0067,.3933),(1,.3787),(.9933,.3933),(.9874,.4),(.9773,.4))
 else:
  for v in path:v.co.z=.00885
  profile=((.9974,.0026),(.99115,0),(.9823,0))
 prev=path
 for scale,height in profile:
  cur=[bm.verts.new((v.x*scale,v.y*scale,height)) for v in original]
  bridge(prev,cur);prev=cur
 fill_quarter(prev,z)
bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7)
bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.normal_update()
assert all(len(f.verts)==4 for f in bm.faces)
bm.to_mesh(o.data);bm.free();o.data.update()
for p in o.data.polygons:p.use_smooth=True
sub=o.modifiers.get('Surface review') or o.modifiers.new('Surface review','SUBSURF')
sub.levels=2;sub.render_levels=2
def inspect():
 bpy.context.view_layer.update();ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh()
 b=bmesh.new();b.from_mesh(me)
 r={'vertices':len(b.verts),'faces':len(b.faces),'nonquads':sum(len(f.verts)!=4 for f in b.faces),
 'nonmanifold_edges':sum(not e.is_manifold for e in b.edges),'zero_area_faces':sum(f.calc_area()<1e-12 for f in b.faces)}
 b.free();ev.to_mesh_clear();return r
sub.show_viewport=False;base=inspect();sub.show_viewport=True;smooth=inspect()
assert base['nonmanifold_edges']==0 and smooth['nonmanifold_edges']==0
assert base['zero_area_faces']==0 and smooth['zero_area_faces']==0
report={'stage':'Center groove, planar caps and underside supports built; visual review required','mirror_base':base,'subdivision_2':smooth,'quarter_vertices':len(o.data.vertices)}
bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(R/'Cover.blend'))
(R/'validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(report)
