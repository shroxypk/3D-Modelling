"""Curved connecting strips and end rims; detail pass remains separate."""
import bpy,bmesh,math
from pathlib import Path
R=Path('C:/Users/Dell/Downloads/3D/research/crnt-designers/cylindrical-design')
def install(name,bm):
 bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));me=bpy.data.meshes.new(name+' quads');bm.to_mesh(me);bm.free()
 o=bpy.data.objects.get(name)
 if o:
  old=o.data;o.data=me
  if old.users==0:bpy.data.meshes.remove(old)
 else:o=bpy.data.objects.new(name,me);bpy.context.scene.collection.objects.link(o)
 for m in list(o.modifiers):o.modifiers.remove(m)
 sub=o.modifiers.new('Surface review','SUBSURF');sub.levels=2;sub.render_levels=2
 for p in me.polygons:p.use_smooth=True
 return o
def strip(name,halfangle,halfheight):
 bm=bmesh.new();verts={}
 vertical=name.startswith('Vertical')
 aa=[-halfangle,-halfangle+.009,-.13,0,.13,halfangle-.009,halfangle] if vertical else [-halfangle,-halfangle+.009,-.70,-.59,-.48,-.34,0,.34,.48,.59,.70,halfangle-.009,halfangle]
 zz=[-halfheight,-halfheight+.009,-.66,-.54,-.42,0,.42,.54,.66,halfheight-.009,halfheight] if vertical else [-halfheight,-halfheight+.009,-.12,0,.12,halfheight-.009,halfheight]
 faces={}
 for side,r in enumerate((1.007,.972)):
  for i,a in enumerate(aa):
   for j,z in enumerate(zz):verts[side,i,j]=bm.verts.new((r*math.sin(a),-r*math.cos(a),z))
  for i in range(len(aa)-1):
   for j in range(len(zz)-1):faces[side,i,j]=bm.faces.new(tuple(verts[side,x,y] for x,y in ((i,j),(i+1,j),(i+1,j+1),(i,j+1))))
 border=[(i,0) for i in range(len(aa)-1)]+[(len(aa)-1,j) for j in range(len(zz)-1)]+[(i,len(zz)-1) for i in range(len(aa)-1,0,-1)]+[(0,j) for j in range(len(zz)-1,0,-1)]
 for k,(i,j) in enumerate(border):
  x,y=border[(k+1)%len(border)];bm.faces.new((verts[0,i,j],verts[0,x,y],verts[1,x,y],verts[1,i,j]))
 # Local 2x2 patches become connected circular or slot recesses.
 specs=[(2,2,False),(2,6,False)] if vertical else [(2,2,False),(8,2,False),(5,2,True)]
 for i0,j0,slot in specs:
  selected=[faces[0,i,j] for i in (i0,i0+1) for j in (j0,j0+1)]
  edges=set(e for f in selected for e in f.edges)
  boundary=list(set(v for e in edges if sum(f in selected for f in e.link_faces)==1 for v in e.verts))
  cu,cz=aa[i0+1],zz[j0+1]
  boundary.sort(key=lambda v:math.atan2(round(v.co.z-cz,5)+0.,round(math.atan2(v.co.x,-v.co.y)-cu,5)+0.))
  for f in selected:bm.faces.remove(f)
  for e in list(bm.edges):
   if not e.link_faces:bm.edges.remove(e)
  for v in list(bm.verts):
   if not v.link_edges:bm.verts.remove(v)
  prev=boundary
  for size,r in ((1,1.007),(.88,1.007),(.76,.998),(.73,.983),(.60,.980)):
   cur=[]
   for k in range(8):
    a=-3*math.pi/4+k*math.pi/4
    du=(.26 if slot else .074)*math.cos(a)*size;dz=(.075 if slot else .074)*math.sin(a)*size
    if slot:
     du=(.26 if math.cos(a)>.1 else -.26 if math.cos(a)<-.1 else 0)*size
     dz=(.095 if math.sin(a)>.1 else -.095 if math.sin(a)<-.1 else 0)*size
    cur.append(bm.verts.new((r*math.sin(cu+du),-r*math.cos(cu+du),cz+dz)))
   for k in range(8):bm.faces.new((prev[k],prev[(k+1)%8],cur[(k+1)%8],cur[k]))
   prev=cur
  center=bm.verts.new((.980*math.sin(cu),-.980*math.cos(cu),cz))
  for k in range(0,8,2):bm.faces.new((center,prev[k],prev[(k+1)%8],prev[(k+2)%8]))
 return install(name,bm)
for k in range(4):
 for row,z in enumerate((-.92,.92)):
  o=strip(f'VerticalBand_{row}_{k}',.292,.739);o.rotation_euler.z=math.pi/4+k*math.pi/2;o.location.z=z
 o=strip(f'MiddleBand_{k}',math.pi/4-.006,.164);o.rotation_euler.z=k*math.pi/2
for sign in (-1,1):
 bm=bmesh.new();rings=[]
 for r,z in ((.915,1.635),(.915,1.71),(.920,1.722),(1.026,1.722),(1.04,1.710),(1.04,1.666),(1.030,1.650),(.970,1.650),(.961,1.635)):
  rings.append([bm.verts.new((r*math.sin(i*math.tau/64),-r*math.cos(i*math.tau/64),sign*z)) for i in range(64)])
 for j,a in enumerate(rings):
  b=rings[(j+1)%len(rings)]
  for i in range(64):bm.faces.new((a[i],a[(i+1)%64],b[(i+1)%64],b[i]))
 install('EndRimTop' if sign>0 else 'EndRimBottom',bm)
bpy.ops.wm.save_as_mainfile(filepath=str(R/'CylindricalDesign.blend'))
print('Curved bands and end rims saved; connected circular and slot band details included.')
