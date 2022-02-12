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
    NOTE: This will only save settings that Satellite may need to change.
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




class SATELLITE_OT_Render(Operator):
    """Renders the selected Bake Preset."""

    bl_idname = "scene.satl_render"
    bl_label = "Render Skybox"

    def execute(self, context):

        scene = bpy.context.scene
        
        # TODO: See if you can just grab .render, .engine etc and do 
        # a wholesale replace at the end.

        # store old properties for later
        old_render_settings = SaveRenderSettings(self, context)

        # Get the selected bake preset and check it's type
        sat_data = scene.SATL_SceneData
        selected_bake_index = sat_data.bake_selected_list_index
        bake_preset = sat_data.bake_presets[selected_bake_index]

        # ////////////////////////////////////////////////////////////////////////////
        # ////////////////////////////////////////////////////////////////////////////
        # ////////////////////////////////////////////////////////////////////////////
        # SKYBOX SETUP
        if bake_preset.bake_type == 'Skybox':
            bake_options = bake_preset.data_skybox

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
            name = bake_preset.output_dir
            dir = bake_preset.output_name

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
        



        # Ensure render settings have been restored.
        RestoreRenderSettings(self, context, old_render_settings)
            

        self.report({'INFO'}, "The Skybox has been saved to " + destination + ".")
        return {'FINISHED'}