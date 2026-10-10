"""Fresh sequential tutorial build; preserves the user's saved scene settings."""
import bpy,sys,importlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'source'))
assert Path(bpy.data.filepath).resolve()==(ROOT/'M4A1.blend').resolve()
if bpy.context.object and bpy.context.object.mode!='OBJECT':bpy.ops.object.mode_set(mode='OBJECT')
collection=bpy.data.collections['01 | Tutorial geometry']
for o in list(collection.objects):
    if o.type=='MESH':bpy.data.objects.remove(o,do_unlink=True)
for m in list(bpy.data.meshes):
    if m.users==0:bpy.data.meshes.remove(m)
ref=bpy.data.objects.get('Side board | same reference as tutorial')
if ref:
    for c in ref.users_collection:c.hide_viewport=False
    ref.hide_set(False);ref.show_empty_image_orthographic=True;ref.show_empty_image_perspective=False
for name in ['outer_cylinders','handguard_base','side_strip','tutorial_rails','stock_restart']:
    module=importlib.import_module(name);importlib.reload(module);module.build(collection)
bpy.context.scene['Study status']=bpy.data.objects['08 | Stock crown tutorial restart']['tutorial_stage']
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'M4A1.blend'))
from validate_current import validate
validate(ROOT)
