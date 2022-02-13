import bpy
from bpy.types import Menu
from bpy.types import Operator
from bpy.props import IntProperty, FloatProperty, StringProperty, BoolProperty

import os
from math import radians
from mathutils import Vector


def SaveRenderSettings(self, context):
    """
    Saves all relevant render settings before attempting to bake with Satellite.
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
    bake_options = satellite.data_skybox

    # create a new view layer and hide everything
    bake_viewlayer = context.scene.view_layers.new(name="Satellite Bake")
    context.window.view_layer = bake_viewlayer

    for layer in bake_viewlayer.layer_collection.children:
        if bake_options.include_collection in layer.name:
            layer.exclude = True


    # ///////////////////////////////////////
    # CAMERA + WORLD
    scene.render.engine = 'CYCLES'
    scene.render.resolution_x = int(bake_options.resolution)
    scene.render.resolution_y = int(bake_options.resolution / 2)
    scene.render.image_settings.file_format = 'HDR'

    # ensure some render settings are at their defaults
    scene.render.resolution_percentage
    scene.render.pixel_aspect_x
    scene.render.pixel_aspect_y
    scene.render.use_border

    scene.render.use_multiview
    scene.render.use_file_extension
    scene.render.use_render_cache
    scene.render.use_overwrite

    if bake_options.render_engine == 'Cycles':
        scene.cycles.samples = bake_options.samples
        scene.cycles.use_denoising = bake_options.cycles_use_denoiser
    
    elif bake_options.render_engine == 'Eevee':
        scene.eevee.taa_render_samples = bake_options.samples

        if bake_options.eevee_disable_pp is True:
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
    if bake_options.world_material is not None:
        scene.world = bake_options.world_material
    
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
    if bake_options.world_material is not None:
        scene.world = old_world

    bpy.data.objects.remove(bpy.data.objects[camera_name], do_unlink=True)
    context.scene.view_layers.remove(bake_viewlayer)
    
    report  = {}
    report['status'] = 'FINISHED'
    report['destination'] = destination
    return report


# /////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////////////

def RenderDirectCamera(self, context, satellite):
    """Renders a direct camera defined by the satellite input"""
    pass

# /////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////////////


def VerifyBakeSettings(self, context, verify_all):
    """Checks that all settings have been correctly set before baking"""

    

    # check output directories

    # DIRECT CAMERA
    # check for cameras


    pass


# /////////////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////////////

class SATELLITE_OT_RenderSelected(Operator):
    """Renders the selected Satellite"""

    bl_idname = "scene.satl_render"
    bl_label = "Render Selected"

    def execute(self, context):

        scene = bpy.context.scene
        
        # Perform some safety checks to ensure we have what we need





        # store old properties for later
        old_render_settings = SaveRenderSettings(self, context)

        # Get the selected bake preset and check it's type
        sat_data = scene.SATL_SceneData
        selected_bake_index = sat_data.sat_selected_list_index
        satellite = sat_data.sat_presets[selected_bake_index]

        # ////////////////////////////////////////////////////////////////////////////
        # SKYBOX SETUP
        report = None

        if satellite.bake_type == 'Skybox':
            report = RenderSkybox(self, context, satellite)
        elif satellite.bake_type == 'Skybox':
            report = RenderSkybox(self, context, satellite)


        # Ensure render settings have been restored.
        RestoreRenderSettings(self, context, old_render_settings)
        
        # TODO: Add a status bar and some flexible info dumps.
            
        if report != None:
            self.report({'INFO'}, "The Skybox has been saved to " + report['destination'] + ".")

        return {'FINISHED'}