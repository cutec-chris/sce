import bpy,pathlib,mathutils,math,os
def IsNewer(File1,File2):
    try:
        return os.path.getmtime(str(File1))<os.path.getmtime(str(File2))
    except:
        return True
def ExportObject(File,Object,TargetName,lod=[10],lod_ligthing=50,**kwargs):
    File = pathlib.Path(File)
    print(str(File.absolute()))
    if IsNewer(TargetName+'_10.glb',File):
        bpy.ops.wm.open_mainfile(filepath=str(File.absolute()))
        for collection in bpy.data.collections:
            collection.hide_viewport = collection.name != Object
            collection.hide_select = collection.name != Object
            collection.hide_render = collection.name != Object
            if collection.name == Object:
                print(collection.name)
                target_obj = collection
                for obj in collection.all_objects:
                    print("     obj: ", obj.name)
                    target_obj = obj
        if 10 in lod:
            bpy.ops.export_scene.gltf(filepath=TargetName+'_10.glb',use_visible=True,export_cameras=False,export_apply=True,**kwargs)
        if 0 in lod\
        and (IsNewer(TargetName+'_0.glb',File)):
            GenerateLOD0Object(target_obj,TargetName,lod_ligthing=lod_ligthing)
        #bpy.ops.wm.save_mainfile(filepath=str(File.absolute())+'out.blend')
    
def GenerateLOD0Object(target_obj,TargetName,Resolution=400,Blending='CLIP',lod_ligthing=50):
    # remove default light    
    bpy.ops.object.select_by_type(type='LIGHT')
    bpy.ops.object.delete(use_global=False)
    #add light
    bpy.ops.object.light_add(type='AREA')
    light = bpy.context.object
    light.data.energy = lod_ligthing
    #add camera for rendering
    bpy.ops.object.camera_add()
    bpy.data.cameras['Camera'].type = 'ORTHO'
    camera_object = bpy.data.objects['Camera']
    center = sum((mathutils.Vector(b) for b in target_obj.bound_box), mathutils.Vector())/8
    bpy.data.cameras['Camera'].ortho_scale = 20
    pmw = target_obj.matrix_world
    coords = [t for b in target_obj.bound_box for t in pmw @ mathutils.Vector(b)]
    #render 2 images from object
    bpy.context.scene.render.film_transparent = True
    bpy.context.scene.render.image_settings.color_mode = 'RGBA'
    for scene in bpy.data.scenes:
        scene.render.resolution_x = Resolution
        scene.render.resolution_y = Resolution
        #scene.render.image_settings.file_format = 'JPEG'

    camera_object.location = center
    camera_object.rotation_euler = (math.radians(90), 0, math.radians(-90))
    v, scale = camera_object.camera_fit_coords(bpy.context.evaluated_depsgraph_get(), coords)
    camera_object.location = v
    light.location = v
    light.rotation_euler = camera_object.rotation_euler
    bpy.data.cameras['Camera'].ortho_scale = scale
    bpy.context.scene.camera = camera_object
    bpy.context.scene.render.filepath = "orthogonal1.png"
    bpy.ops.render.render(write_still = True)

    camera_object.location = center
    camera_object.rotation_euler = (math.radians(90), 0, 0)
    v, scale = camera_object.camera_fit_coords(bpy.context.evaluated_depsgraph_get(), coords)
    camera_object.location = v
    light.location = v
    light.rotation_euler = camera_object.rotation_euler
    bpy.data.cameras['Camera'].ortho_scale = scale
    bpy.context.scene.camera = camera_object
    bpy.context.scene.render.filepath = "orthogonal2.png"
    bpy.ops.render.render(write_still = True)
    #generate 2 planes with the images
    target_obj.hide_viewport = True
    bpy.ops.mesh.primitive_plane_add(
        size=2,
        calc_uvs=True,
        enter_editmode=False,
        align='WORLD',
        location=(0, 0, 0))
    bpy.data.objects['Plane'].name = 'Plane1'
    bpy.data.objects['Plane1'].rotation_euler=(math.radians(90), 0, math.radians(90))
    bpy.data.materials.new('Mat1')
    mat1 = bpy.data.materials['Mat1']
    mat1.use_nodes = True
    mat1.blend_method = Blending
    tex1 = mat1.node_tree.nodes.new('ShaderNodeTexImage')
    img1 = bpy.data.images.load('orthogonal1.png')
    tex1.image = img1
    mat1.node_tree.links.new(mat1.node_tree.nodes['Principled BSDF'].inputs['Base Color'], tex1.outputs[0])
    mat1.node_tree.links.new(mat1.node_tree.nodes['Principled BSDF'].inputs['Alpha'], tex1.outputs[1])
    mat1.node_tree.nodes['Principled BSDF'].inputs['Specular'].default_value = 0.0
    print(mat1.node_tree.nodes['Principled BSDF'].inputs['Specular'])
    bpy.data.objects['Plane1'].active_material = mat1

    bpy.ops.mesh.primitive_plane_add(
        size=2,
        calc_uvs=True,
        enter_editmode=False,
        align='WORLD',
        location=(0, 0, 0))
    bpy.data.objects['Plane'].name = 'Plane2'
    bpy.data.objects['Plane2'].rotation_euler=(math.radians(90), 0, 0)
    bpy.data.materials.new('Mat2')
    mat2 = bpy.data.materials['Mat2']
    mat2.use_nodes = True
    mat2.blend_method = Blending
    tex2 = mat2.node_tree.nodes.new('ShaderNodeTexImage')
    img2 = bpy.data.images.load('orthogonal2.png')
    tex2.image = img2
    mat2.node_tree.links.new(mat2.node_tree.nodes['Principled BSDF'].inputs['Base Color'], tex2.outputs[0])
    mat2.node_tree.links.new(mat2.node_tree.nodes['Principled BSDF'].inputs['Alpha'], tex2.outputs[1])
    mat2.node_tree.nodes['Principled BSDF'].inputs['Specular'].default_value = 0.0
    print(mat2.node_tree.nodes['Principled BSDF'].inputs['Specular'])
    bpy.data.objects['Plane2'].active_material = mat2
    bpy.ops.export_scene.gltf(filepath=TargetName+'_0.glb',use_visible=True,export_cameras=False,export_apply=True)
    os.remove('orthogonal1.png')
    os.remove('orthogonal2.png')

    #https://blender.stackexchange.com/questions/130404/script-to-render-one-object-from-different-angles
    #https://blender.stackexchange.com/questions/128185/check-if-the-whole-plane-is-being-on-a-orthographic-camera-render-or-get-a-prop

