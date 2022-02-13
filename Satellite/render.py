import bpy
from bpy.types import Menu
from bpy.types import Operator
from bpy.props import IntProperty, FloatProperty, StringProperty, BoolProperty

import os
from math import radians
from mathutils import Vector


def SaveRenderSettings(self, context):
    """
    Saves all relevant render settings before attempting to render with Satellite.
    NOTE: This will only save settings that Satellite may need to change, not every
    possible rendering feature.
    """

    saved_render_settings = {}
    cycles_settings = {}
    eevee_settings = {}
    render_settings = {}
    

    # CYCLES SETTINGS (the API page is missing, do your best, avoid preview settings)
    cycles = context.scene.cycles
    cycles_settings['device'] = cycles.device
    cycles_settings['feature_set'] = cycles.feature_set

    cycles_settings['adaptive_threshold'] = cycles.adaptive_threshold
    cycles_settings['samples'] = cycles.samples
    cycles_settings['adaptive_min_samples'] = cycles.adaptive_min_samples
    cycles_settings['use_denoising'] = cycles.use_denoising
    

    # EEVEE SETTINGS
    eevee = context.scene.eevee
    eevee_settings["taa_render_samples"] = eevee.taa_render_samples
    eevee_settings["use_gtao"] = eevee.use_gtao
    eevee_settings["use_bloom"] = eevee.use_bloom
    eevee_settings["use_ssr"] = eevee.use_ssr
    eevee_settings["use_motion_blur"] = eevee.use_motion_blur

    # RENDER SETTINGS
    render = context.scene.render
    render_settings['engine'] = render.engine
    render_settings['resolution_x'] = render.resolution_x
    render_settings['resolution_y'] = render.resolution_y
    render_settings['resolution_percentage'] = render.resolution_percentage
    render_settings['pixel_aspect_x'] = render.pixel_aspect_x
    render_settings['pixel_aspect_y'] = render.pixel_aspect_y
    render_settings['use_border'] = render.use_border

    render_settings['use_multiview'] = render.use_multiview
    render_settings['use_file_extension'] = render.use_file_extension
    render_settings['use_render_cache'] = render.use_render_cache
    render_settings['use_overwrite'] = render.use_overwrite

    render_settings['file_format'] = render.image_settings.file_format
    render_settings['color_mode'] = render.image_settings.color_mode
    render_settings['compression'] = render.image_settings.compression
    render_settings['quality'] = render.image_settings.quality
    render_settings['color_depth'] = render.image_settings.color_depth

    saved_render_settings['cycles'] = cycles_settings
    saved_render_settings['eevee'] = eevee_settings
    saved_render_settings['render'] = render_settings


    return saved_render_settings


# /////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////////////


def RestoreRenderSettings(self, context, saved_render_settings):
    """
    Restores all previously saved render settings.
    """

    cycles_settings = saved_render_settings['cycles']
    eevee_settings = saved_render_settings['eevee']
    render_settings = saved_render_settings['render']
    

    # CYCLES SETTINGS (the API page is missing, do your best, avoid preview settings)
    cycles = context.scene.cycles
    cycles.device = cycles_settings["device"]
    cycles.feature_set = cycles_settings["feature_set"]

    cycles.adaptive_threshold = cycles_settings["adaptive_threshold"]
    cycles.samples = cycles_settings["samples"]
    cycles.adaptive_min_samples = cycles_settings["adaptive_min_samples"]
    cycles.use_denoising = cycles_settings["use_denoising"]
    

    # EEVEE SETTINGS
    eevee = context.scene.eevee
    eevee.taa_render_samples = eevee_settings["taa_render_samples"]
    eevee.use_gtao = eevee_settings["use_gtao"]
    eevee.use_bloom = eevee_settings["use_bloom"]
    eevee.use_ssr = eevee_settings["use_ssr"]
    eevee.use_motion_blur = eevee_settings["use_motion_blur"]


    # RENDER SETTINGS
    render = context.scene.render
    render.engine = render_settings["engine"]
    render.resolution_x = render_settings["resolution_x"]
    render.resolution_y = render_settings["resolution_y"]
    render.resolution_percentage = render_settings["resolution_percentage"]
    render.pixel_aspect_x = render_settings["pixel_aspect_x"]
    render.pixel_aspect_y = render_settings["pixel_aspect_y"]
    render.use_border = render_settings["use_border"]

    render.use_multiview = render_settings["use_multiview"]
    render.use_file_extension = render_settings["use_file_extension"]
    render.use_render_cache = render_settings["use_render_cache"]
    render.use_overwrite = render_settings["use_overwrite"]

    render.image_settings.file_format = render_settings["file_format"]
    render.image_settings.color_mode = render_settings["color_mode"]
    render.image_settings.compression = render_settings["compression"]
    render.image_settings.quality = render_settings["quality"]
    render.image_settings.color_depth = render_settings["color_depth"]

    pass

# /////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////////////

def RenderSkybox(self, context, satellite):
    """Renders a skybox defined by the satellite input"""

    scene = bpy.context.scene
    render_options = satellite.data_skybox

    # create a new view layer and hide everything
    render_viewlayer = context.scene.view_layers.new(name="Satellite Render")
    context.window.view_layer = render_viewlayer

    for layer in render_viewlayer.layer_collection.children:
        if render_options.include_collection in layer.name:
            layer.exclude = True


    # ///////////////////////////////////////
    # CAMERA + WORLD
    scene.render.resolution_x = int(render_options.resolution)
    scene.render.resolution_y = int(render_options.resolution / 2)
    scene.render.image_settings.file_format = 'HDR'

    # ensure some render settings are at their defaults
    scene.render.resolution_percentage = 100
    scene.render.pixel_aspect_x = 1.0
    scene.render.pixel_aspect_y = 1.0
    scene.render.use_border = False

    scene.render.use_multiview = False
    scene.render.use_file_extension = True
    scene.render.use_render_cache = False
    scene.render.use_overwrite = True

    if render_options.render_engine == 'Cycles':
        scene.render.engine = 'CYCLES'
        scene.cycles.samples = render_options.samples
        scene.cycles.use_denoising = render_options.cycles_use_denoiser
    
    elif render_options.render_engine == 'Eevee':
        scene.render.engine = 'EEVEE'
        scene.eevee.taa_render_samples = render_options.samples

        if render_options.eevee_disable_pp is True:
            scene.eevee.use_gtao = False
            scene.eevee.use_bloom = False
            scene.eevee.use_ssr = False
            scene.eevee.use_motion_blur = False
    

    # ///////////////////////////////////////
    # CAMERA + WORLD
    # Setup the camera
    bpy.ops.object.camera_add()
    context.active_object.location = Vector((0.0, 0.0, 0.0))
    context.active_object.rotation_euler = Vector((radians(90), 0.0, 0.0))

    camera_name = context.active_object.name
    camera_bname = context.active_object.data.name
    print(camera_name)
    bpy.data.cameras[camera_bname].type = 'PANO'
    bpy.data.cameras[camera_bname].cycles.panorama_type = 'EQUIRECTANGULAR'

    # If a World Material has been defined, use it.
    old_world = scene.world
    if render_options.world_material is not None:
        scene.world = render_options.world_material
    
    # ///////////////////////////////////////
    # RENDER
    # render this bad boy *slaps side of car*
    context.scene.camera = context.active_object
    name = satellite.output_dir
    dir = satellite.output_name

    destination = os.path.join(name, dir)
    bpy.context.scene.render.filepath = destination
    bpy.context.scene.render.use_single_layer = True
    bpy.ops.render.render(write_still = True)


    # ////////////////////////////////////////
    # CLEAN UP
    if render_options.world_material is not None:
        scene.world = old_world

    bpy.data.objects.remove(bpy.data.objects[camera_name], do_unlink=True)
    context.scene.view_layers.remove(render_viewlayer)
    
    report  = {}
    report['status'] = 'FINISHED'
    report['destination'] = destination
    return report


# /////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////////////

def RenderDirectCamera(self, context, satellite):
    """Renders a direct camera defined by the satellite input"""

    scene = bpy.context.scene
    render_options = satellite.data_skybox


    # ///////////////////////////////////////
    # SCENE SETUP
    

    # If we have a Replacement Material set we need to 
    # save all renderable object materials before switching 

    # If a World Material has been defined, use it.
    old_world = scene.world
    if render_options.world_material is not None:
        scene.world = render_options.world_material


    # ///////////////////////////////////////
    # OUTPUT
    scene.render.resolution_x = int(render_options.resolution_x)
    scene.render.resolution_y = int(render_options.resolution_y)
    scene.render.image_settings.file_format = render_options.file_format
    scene.render.image_settings.color_depth = render_options.color_depth
    scene.render.image_settings.color_mode = render_options.color_mode
    scene.render.image_settings.compression = render_options.compression

    # ensure some render settings are at their defaults
    scene.render.resolution_percentage = 100
    scene.render.pixel_aspect_x = 1.0
    scene.render.pixel_aspect_y = 1.0
    scene.render.use_border = False

    scene.render.use_multiview = False
    scene.render.use_file_extension = True
    scene.render.use_render_cache = False
    scene.render.use_overwrite = True
    

    # ///////////////////////////////////////
    # RENDER
    if render_options.render_engine == 'Cycles':
        scene.render.engine = 'CYCLES'
        scene.cycles.samples = render_options.samples
        scene.cycles.use_denoising = render_options.cycles_use_denoiser
    
    elif render_options.render_engine == 'Eevee':
        scene.render.engine = 'EEVEE'
        scene.eevee.taa_render_samples = render_options.samples

        if render_options.eevee_disable_pp is True:
            scene.eevee.use_gtao = False
            scene.eevee.use_bloom = False
            scene.eevee.use_ssr = False
            scene.eevee.use_motion_blur = False

    # render this bad boy *slaps side of car*
    context.scene.camera = render_options.target_camera
    name = satellite.output_dir
    dir = satellite.output_name

    destination = os.path.join(name, dir)
    bpy.context.scene.render.filepath = destination
    bpy.context.scene.render.use_single_layer = True
    bpy.ops.render.render(write_still = True)


    # ////////////////////////////////////////
    # CLEAN UP
    if render_options.world_material is not None:
        scene.world = old_world
    


    report  = {}
    report['status'] = 'FINISHED'
    report['destination'] = destination
    return report

    pass

# /////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////////////


def VerifyRenderSettings(self, context, verify_all):
    """Checks that all settings have been correctly set before rendering"""

    report = {}

    scene = context.scene
    sat_data = scene.SATL_SceneData
    satellites = sat_data.sat_presets
    sat_selected = sat_data.sat_selected_list_index

    satellite_queue = []
    if verify_all is True:
        for sat in satellites:
            if sat.is_active is True:
                satellite_queue.append(satellites)
    else:
        satellite_queue.append(satellites[sat_selected])

    for sat in satellite_queue:

        # check output directories
        if sat.output_dir == "":
            report['status'] = 'FAILED'
            report['info'] = "The Satellite " + sat.name + " needs an Output Directory set before rendering."
            return report

        if sat.output_name == "":
            report['status'] = 'FAILED'
            report['info'] = "The Satellite " + sat.name + " needs an Output Name set before rendering."
            return report
        
        # check for cameras
        if sat.render_type == 'Direct Camera':
            sat_settings = sat.data_camera

            if sat_settings.target_camera is None:
                report['status'] = 'FAILED'
                report['info'] = "The Satellite " + sat.name + " needs a Target Camera set before rendering."
                return report
            
            if sat_settings.view_layer is not None:
                vl = sat_settings.view_layer
                if scene.view_layers.find(vl) == -1:
                    report['status'] = 'FAILED'
                    report['info'] = "The Satellite " + sat.name + "'s Target View Layer doesn't exist, please double-check the name provided."
                    return report
                

    
    report['status'] = 'SUCCESS'
    return report


# /////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////////////

class SATELLITE_OT_RenderSelected(Operator):
    """Renders the selected Satellite"""

    bl_idname = "scene.satl_render"
    bl_label = "Render Selected"

    def execute(self, context):

        scene = bpy.context.scene
        
        # Perform some safety checks to ensure we have what we need
        verify_settings = VerifyRenderSettings(self, context, False)
        if verify_settings['status'] != 'SUCCESS':
            self.report({'WARNING'}, verify_settings['info'])
            return {'FINISHED'}


        # store old properties for later
        old_render_settings = SaveRenderSettings(self, context)

        # Get the selected render preset and check it's type
        sat_data = scene.SATL_SceneData
        selected_render_index = sat_data.sat_selected_list_index
        satellite = sat_data.sat_presets[selected_render_index]

        # ////////////////////////////////////////////////////////////////////////////
        # SKYBOX SETUP
        report = None

        if satellite.render_type == 'Skybox':
            report = RenderSkybox(self, context, satellite)
        elif satellite.render_type == 'Skybox':
            report = RenderSkybox(self, context, satellite)


        # Ensure render settings have been restored.
        RestoreRenderSettings(self, context, old_render_settings)
        
        # TODO: Add a status bar and some flexible info dumps.
            
        if report != None:
            self.report({'INFO'}, "The Skybox has been saved to " + report['destination'] + ".")

        return {'FINISHED'}