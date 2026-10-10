"""Read-only cross sections of reference meshes; no assets are modified."""
import bpy,json
bpy.ops.wm.open_mainfile(filepath=r'C:\Users\Dell\Downloads\3D\M4A1\M4A1.blend')
for name in ['Cube.001','Cube.002','Cube.003']:
 o=bpy.data.objects[name];ps=[o.matrix_world@v.co for v in o.data.vertices]
 print('OBJECT',name)
 for xx in [-20,-15,-10]:
  hits=[]
  for face in o.data.polygons:
   points=[]
   for i,j in zip(face.vertices,list(face.vertices[1:])+[face.vertices[0]]):
    a,b=ps[i],ps[j]
    if (a.x-xx)*(b.x-xx)<0:
     p=a+(b-a)*((xx-a.x)/(b.x-a.x));points.append([round(p.y,4),round(p.z,4)])
   if points:hits.append(points)
  print('SECTION',xx,json.dumps(hits))
