import bpy, json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
report={}
for label,path in [('startup',Path(bpy.utils.user_resource('CONFIG'))/'startup.blend'),('model',root/'M4A1.blend')]:
    bpy.ops.wm.open_mainfile(filepath=str(path))
    s=bpy.context.scene
    report[label]={'objects':[o.name for o in s.objects], 'collections':[c.name for c in s.collection.children],
       'engine':s.render.engine,'units':s.unit_settings.system,'scale':s.unit_settings.scale_length,
       'view_transform':s.view_settings.view_transform,'world':s.world.name if s.world else None,
       'workspaces':[w.name for w in bpy.data.workspaces],
       'viewports':[{'screen':sc.name,'light':a.spaces.active.shading.light,'studio_light':a.spaces.active.shading.studio_light,
       'floor':a.spaces.active.overlay.show_floor} for sc in bpy.data.screens for a in sc.areas if a.type=='VIEW_3D']}
(root/'review/default-settings-inspection.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
