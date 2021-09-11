import bpy,pathlib
def ExportObject(File,Object,TargetName):
    File = pathlib.Path(File)
    bpy.ops.wm.open_mainfile(filepath=str(File.absolute()))
    for collection in bpy.data.collections:
        collection.hide_viewport = collection.name != Object
        if collection.name == Object:
            print(collection.name)
            for obj in collection.all_objects:
                print("obj: ", obj.name)
    bpy.ops.export_scene.gltf(filepath=TargetName,use_visible=True)