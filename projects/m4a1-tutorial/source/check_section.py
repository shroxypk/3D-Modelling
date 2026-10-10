import bpy,json
bpy.ops.wm.open_mainfile(filepath=r'C:\Users\Dell\Downloads\3D\M4A1\M4A1.blend')
for name in ['Cylinder.003']:
 o=bpy.data.objects[name];ps=[o.matrix_world@v.co for v in o.data.vertices];hits=[]
 for e in o.data.edges:
  a,b=[ps[i] for i in e.vertices]
  if (a.x-20)*(b.x-20)<0:
   p=a+(b-a)*((20-a.x)/(b.x-a.x));hits.append([round(p.y,4),round(p.z,4)])
 print(name,sorted(hits))
