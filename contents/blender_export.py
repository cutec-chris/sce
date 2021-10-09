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
    GenerateLOD0Object(target_obj,TargetName)
    
def GenerateLOD0Object(target_obj,TargetName):
    bpy.ops.object.camera_add()
    bpy.data.cameras['Camera'].type = 'ORTHO'
    camera_object = bpy.data.objects['Camera']
    center = sum((mathutils.Vector(b) for b in target_obj.bound_box), mathutils.Vector())/8
    bpy.data.cameras['Camera'].ortho_scale = 20
    pmw = target_obj.matrix_world
    coords = [t for b in target_obj.bound_box for t in pmw @ mathutils.Vector(b)]

    bpy.context.scene.render.film_transparent = True
    bpy.context.scene.render.image_settings.color_mode = 'RGBA'

    camera_object.location = center
    camera_object.rotation_euler = (90, 0, -90)
    v, scale = camera_object.camera_fit_coords(bpy.context.evaluated_depsgraph_get(), coords)
    camera_object.location = v
    bpy.data.cameras['Camera'].ortho_scale = scale
    bpy.context.scene.camera = camera_object
    bpy.context.scene.render.filepath = "orthogonal1.png"
    bpy.ops.render.render(write_still = True)

    camera_object.location = center
    camera_object.rotation_euler = (90, 0, 0)
    v, scale = camera_object.camera_fit_coords(bpy.context.evaluated_depsgraph_get(), coords)
    camera_object.location = v
    bpy.data.cameras['Camera'].ortho_scale = scale
    bpy.context.scene.camera = camera_object
    bpy.context.scene.render.filepath = "orthogonal2.png"
    bpy.ops.render.render(write_still = True)

    target_obj.hide_viewport = True
    bpy.ops.mesh.primitive_plane_add(
        size=2,
        calc_uvs=True,
        enter_editmode=False,
        align='WORLD',
        location=(0, 0, 0),
        rotation=(0, 0, 0))
    bpy.data.materials.new('Mat1')
    mat1 = bpy.data.materials['Mat1']
    mat1.use_nodes = True
    tex1 = mat1.node_tree.nodes.new('ShaderNodeTexImage')
    img1 = bpy.data.images.load('orthogonal1.png')
    tex1.image = img1
    mat1.node_tree.links.new(mat1.node_tree.nodes['Principled BSDF'].inputs['Base Color'], tex1.outputs[0])

    bpy.ops.export_scene.gltf(filepath=TargetName+'_0.glb',use_visible=True,export_cameras=False,export_apply=True)

    #https://blender.stackexchange.com/questions/130404/script-to-render-one-object-from-different-angles
    #https://blender.stackexchange.com/questions/128185/check-if-the-whole-plane-is-being-on-a-orthographic-camera-render-or-get-a-prop
