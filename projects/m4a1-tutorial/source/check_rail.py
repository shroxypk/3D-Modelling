"""Read-only reference silhouette distribution; does not copy geometry."""
import bpy,json
bpy.ops.wm.open_mainfile(filepath=r'C:\Users\Dell\Downloads\3D\M4A1\M4A1.blend')
for name in ['Cube.003','Cube.004']:
    o=bpy.data.objects[name];pts=[o.matrix_world@v.co for v in o.data.vertices]
    levels=sorted(set(round(v.z,4) for v in pts))
    print(name,'z levels',levels)
    for z in [min(levels),max(levels)]:
        print('level',z,'X',sorted(set(round(v.x,4) for v in pts if abs(v.z-z)<.0001)))
