import bpy,pathlib,mathutils
def ExportObject(File,Object,TargetName,**kwargs):
    File = pathlib.Path(File)
    bpy.ops.wm.open_mainfile(filepath=str(File.absolute()))
    for collection in bpy.data.collections:
        collection.hide_viewport = collection.name != Object
        if collection.name == Object:
            print(collection.name)
            target_obj = collection
            for obj in collection.all_objects:
                print("obj: ", obj.name)
                target_obj = obj
    #bpy.ops.export_scene.gltf(filepath=TargetName+'_10.glb',use_visible=True,export_cameras=False,export_apply=True,**kwargs)
    
    #camera_data = bpy.data.cameras.new(name='Camera')
    bpy.ops.object.camera_add()
    bpy.data.cameras['Camera'].type = 'ORTHO'
    #camera_object = bpy.data.objects.new('Camera', camera_data)
    camera_object = bpy.data.objects['Camera']
    center = sum((mathutils.Vector(b) for b in target_obj.bound_box), mathutils.Vector())/8
    bpy.data.cameras['Camera'].ortho_scale = 20

    print(center,target_obj.bound_box)
    
    #camera_object.location = center
    #camera_object.location.x = -camera_object.location.x
    #camera_object.rotation_euler = (90, 0, -90)
    #bpy.context.scene.camera = camera_object
    #bpy.context.scene.render.filepath = "orthogonal1.png"
    #bpy.ops.render.render(write_still = True)

    camera_object.location = center
    camera_object.location.y = -10
    camera_object.rotation_euler = (90, 0, 0)
    bpy.context.scene.camera = camera_object
    bpy.context.scene.render.filepath = "orthogonal2.png"
    bpy.ops.render.render(write_still = True)
