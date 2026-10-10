"""Keep authored model data, but use the user's complete startup scene and UI."""
import bpy, hashlib, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def signature(raw=False):
    bpy.context.view_layer.update()
    rows=[]
    for o in sorted(bpy.context.scene.objects,key=lambda o:o.name):
        row={'name':o.name,'type':o.type,'matrix':[list(r) for r in o.matrix_world]}
        if o.type=='MESH':
            row['vertices']=[list(v.co) for v in o.data.vertices]
            row['faces']=[list(p.vertices) for p in o.data.polygons]
        mods=[]
        for m in o.modifiers:
            props={'name':m.name,'type':m.type}
            for p in m.bl_rna.properties:
                if p.is_readonly: continue
                if p.type in {'BOOLEAN','INT','FLOAT','STRING','ENUM'}:
                    try:
                        v=getattr(m,p.identifier)
                        props[p.identifier]=list(v) if p.is_array else sorted(v) if isinstance(v,set) else v
                    except (TypeError,AttributeError): pass
            mods.append(props)
        row['modifiers']=mods
        rows.append(row)
    return rows if raw else hashlib.sha256(json.dumps(rows,sort_keys=True).encode()).hexdigest()

def restore():
    path=ROOT/'M4A1.blend'
    startup=Path(bpy.utils.user_resource('CONFIG'))/'startup.blend'
    assert startup.is_file(), 'User startup file is missing'
    bpy.ops.wm.open_mainfile(filepath=str(path))
    before=signature()
    original_rows=signature(raw=True)
    children=[c.name for c in bpy.context.scene.collection.children]
    custom={k:v for k,v in bpy.context.scene.items() if k=='Study status'}
    camera=bpy.context.scene.camera.name if bpy.context.scene.camera else None
    bpy.ops.wm.open_mainfile(filepath=str(startup))
    s=bpy.context.scene
    # Remove the startup cube, retaining the full scene/tool/world/workspace configuration.
    for o in list(bpy.data.objects): bpy.data.objects.remove(o,do_unlink=True)
    for c in list(bpy.data.collections): bpy.data.collections.remove(c)
    with bpy.data.libraries.load(str(path),link=False) as (src,dst):
        dst.collections=children
    for c in dst.collections: s.collection.children.link(c)
    bpy.ops.object.make_local(type='ALL')
    for lib in list(bpy.data.libraries):
        if Path(bpy.path.abspath(lib.filepath)).resolve()==path.resolve():
            bpy.data.libraries.remove(lib)
    s.camera=bpy.data.objects.get(camera) if camera else None
    for k,v in custom.items(): s[k]=v
    if signature()!=before:
        after_rows=signature(raw=True)
        for a,b in zip(original_rows,after_rows):
            for key in a:
                if a[key]!=b[key]: print('DIFFERENCE',a['name'],key,str(a[key])[:600],str(b[key])[:600])
        raise AssertionError('Model or modifier data changed during startup transfer')
    # Only framing changes: preserve each workspace's shading, overlays and tools.
    from mathutils import Vector
    for screen in bpy.data.screens:
        for a in screen.areas:
            if a.type=='VIEW_3D' and screen.name=='Layout':
                region=a.spaces.active.region_3d
                region.view_location=Vector((6.4,0,-.6))
                region.view_distance=24
    bpy.context.preferences.filepaths.save_version=0
    bpy.ops.wm.save_as_mainfile(filepath=str(path))
    bpy.ops.wm.open_mainfile(filepath=str(path))
    assert signature()==before, 'Saved model data changed'
    layout=next(a.spaces.active for sc in bpy.data.screens if sc.name=='Layout' for a in sc.areas if a.type=='VIEW_3D')
    report={'source':str(startup),'model_and_modifiers_preserved':True,'signature':before,
            'engine':bpy.context.scene.render.engine,'view_transform':bpy.context.scene.view_settings.view_transform,
            'units':bpy.context.scene.unit_settings.system,'layout_light':layout.shading.light,
            'layout_matcap':layout.shading.studio_light,'workspace_count':len(bpy.data.workspaces)}
    (ROOT/'review/restored-startup-settings.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))

if __name__=='__main__': restore()
