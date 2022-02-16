

import bpy
from bpy.types import AddonPreferences, PropertyGroup
from bpy.props import (
    IntProperty, 
    FloatProperty, 
    BoolProperty, 
    StringProperty, 
    PointerProperty, 
    CollectionProperty, 
    EnumProperty,
)



class SATELLITE_FormatSkybox(PropertyGroup):
    # Used to define settings for a Skybox render.

    # Binds a format to a specific preset, (TODO: Check if we need this!)
    instance_id: IntProperty(default=-1)

    world_material: PointerProperty(
        type = bpy.types.World,
        name = "Skybox Material",
        description = "Defines the world material that will be used for Skybox baking.  If left blank the currently defined World Material will be used"
    )
    
    include_collection: StringProperty(
        name="Include Collection",
        description="Skybox baking by default will hide all objects in the Scene from rendering.  If this is defined any Collection with matching text will be included in the render",
        default="Skybox",
    )

    render_engine: EnumProperty(
        name="Render Engine",
        items=
            (
            ('Eevee', "Eevee", "Use the Eevee Rendering Engine to render this skybox"),
            ('Cycles', "Cycles", "Use the Cycles Rendering Engine to render this skybox.  WARNING - Satellite will use the Compute Device you have selected, check this setting under Properties Panel > Render for optimal performance"),
            ),
            
        description="The Render Engine that will be used to perform the render.  WARNING - Some World Material nodes can only be rendered using a certain Render Engine, ensure you select the one that is compatible with your World Material",
    )

    resolution: IntProperty(
        name="Max Resolution",
        description="Controls the resolution of the X axis.  The Y axis resolution will be half this value",
        subtype = 'PIXEL',
        min=4,
        max=32768,
        default=2048,
    )

    samples: IntProperty(
        name="Render Samples",
        description="Sets the amount of samples to be used when rendering the HDRI.",
        min=4,
        soft_max=4096,
        default=512,
    )

    cycles_use_denoiser: BoolProperty(
        name="Use Denoiser",
        description="(Cycles Only) If true, the currently active Denoiser and Denoiser Settings will be used for this render (check under Properties Panel > Render > Sampling > Render)",
        default=False,
    )

    eevee_disable_pp: BoolProperty(
        name="Disable Post-Processing",
        description="(Eevee Only) If checked, Satellite will disable any post-processing effects you currently have enabled in Eevee to render the skybox (Ambient Occlusion, Bloom, Screen Space Reflections and Motion Blur)",
        default=False,
    )

    color_mode: EnumProperty(
        name = "Color Mode",
        items =
            (
            ('BW', "BW", "Images get saved in 8-bit grayscale"),
            ('RGB', "RGB", "Images are saved with RGB (color) data"),
            ),
        default = 'RGB',
        description = "Choose BW for saving grayscale images, RGB for saving red, green and blue channels, and RGBA for saving red, green, blue and alpha channels",
    )



# Ensures all color mode properties are synced wherever possible.
def UPDATE_ColorModeBW(self, context):
    self.color_mode = self.color_mode_bw

def UPDATE_ColorModeFull(self, context):
    if self.color_mode != 'RGBA':
        self.color_mode_bw = self.color_mode
    


class SATELLITE_FormatCamera(PropertyGroup):
    # Used to define settings for a Direct Camera render.

    # Binds a format to a specific preset, (TODO: Check this!)
    instance_id: IntProperty(default=-1)

    target_camera: PointerProperty(
        type = bpy.types.Object,
        name = "Target Camera",
        description = "Defines the camera to be used.  This camera will take on the name of the Camera datablock so it may be named differently to the name of the Camera when seen in the 3D or Hierarchy Views (you can check under Properties Panel > Object Data)",
    )

    view_layer: StringProperty(
        name="Target View Layer",
        description="If defined the View Layer's Viewport Visibility will be used to decide what objects in the scene will be rendered (this is due to the fact that Render Visibility cannot change between View Layers)",
        default="",
    )

    world_material: PointerProperty(
        type = bpy.types.World,
        name = "World Material",
        description = "Defines the world material that will be used in the render instead of the one currently used for the scene.  If left blank the currently defined World Material will be used"
    )

    replacement_material: PointerProperty(
        type = bpy.types.Material,
        name = "Replacement Material",
        description = "If defined, any object included in the render will have their material replaced with the one defined here.  This is commonly used in conjunction with the camera to create world-space maps for use in shaders"
    )

    render_engine: EnumProperty(
        name="Render Engine",
        items=
            (
            ('Eevee', "Eevee", "Use the Eevee Rendering Engine to render this skybox"),
            ('Cycles', "Cycles", "Use the Cycles Rendering Engine to render this skybox.  WARNING - Satellite will use the Compute Device you have selected, check this setting under Properties Panel > Render for optimal performance"),
            ),
            
        description="The Render Engine that will be used to perform the render.  WARNING - Some Materials can only be properly rendered using a certain Render Engine, ensure you select the one that is compatible with your World Material",
    )

    resolution_x: IntProperty(
        name="X Resolution",
        description="Controls the resolution of the X axis",
        subtype = 'PIXEL',
        min=4,
        max=32768,
        default=2048,
    )

    resolution_y: IntProperty(
        name="Y Resolution",
        description="Controls the resolution of the Y axis",
        subtype = 'PIXEL',
        min=4,
        max=32768,
        default=2048,
    )

    samples: IntProperty(
        name="Render Samples",
        description="Sets the amount of samples to be used when rendering",
        min=4,
        soft_max=4096,
        default=512,
    )

    cycles_use_denoiser: BoolProperty(
        name="Use Denoiser",
        description="(Cycles Only) If true, the currently active Denoiser and Denoiser Settings will be used for this render (check under Properties Panel > Render > Sampling > Render)",
        default=False,
    )

    eevee_disable_pp: BoolProperty(
        name="Disable Post-Processing",
        description="(Eevee Only) If checked, Satellite will disable any post-processing effects you currently have enabled in Eevee to render the skybox (Ambient Occlusion, Bloom, Screen Space Reflections and Motion Blur)",
        default=False,
    )


    # im going to need file format options here!  pick the best ones.
    file_format: EnumProperty(
        name = "File Format",
        items =
            (
            ('PNG', "PNG", "Export using the PNG format"),
            ('JPEG', "JPEG", "Export using the JPEG format"),
            ('TARGA', "TARGA", "Export using the Targa format"),
            ('TARGA', "TARGA", "Export using the Targa format"),
            ('TARGA_RAW', "TARGA Raw", "Export using the Targa Raw format"),
            ('HDR', "Radiance HDR", "Export using the Radiance HDR format"),
            ),
        default = 'PNG',
        description = "The file type to save the rendered image as.",
    )

    # only PNG, JPEG 2000, DPX and TIFF file formats offer color depth options
    # only PNG is currently offered by Satellite so no need for the other channels right now.
    color_depth: EnumProperty(
        name = "Color Depth",
        items =
            (
            ('8', "8", "8-bit color channels"),
            # ('10', "10", "10-bit color channels"),
            # ('12', "12", "12-bit color channels"),
            ('16', "16", "16-bit color channels"),
            # ('32', "32", "32-bit color channels"),
            ),
        default = '8',
        description = "The bit depth per channel.  WARNING - Not all file formats support all color depth options, check the Output panel for more info",
    )

    # BONK - This is the one that gets used by the renderer.
    # supported by all but the formats in the next property.
    color_mode: EnumProperty(
        name = "Color Mode",
        items =
            (
            ('BW', "BW", "Images get saved in 8-bit grayscale"),
            ('RGB', "RGB", "Images are saved with RGB (color) data"),
            ('RGBA', "RGBA", "Images are saved with RGB and Alpha data"),
            ),
        default = 'RGB',
        description = "Choose BW for saving grayscale images, RGB for saving red, green and blue channels, and RGBA for saving red, green, blue and alpha channels.  WARNING - Not all file formats support all color modes, check the Output panel for more info",
        update = UPDATE_ColorModeFull,
    )

    # the only range supported by JPG, Cineon, Radiance HDR
    color_mode_bw: EnumProperty(
        name = "Color Mode",
        items =
            (
            ('BW', "BW", "Images get saved in 8-bit grayscale"),
            ('RGB', "RGB", "Images are saved with RGB (color) data"),
            ),
        default = 'RGB',
        description = "Choose BW for saving grayscale images and RGB for saving red, green and blue channels",
        update = UPDATE_ColorModeBW,
    )

    compression: IntProperty(
        name = "Compression",
        description = "The amount of time taken for Blender to determine the best compression for the file.  0 will result in no compression with a fast file output time and 100 will result in the maximum lossless compression with the slowest output time",
        default = 15,
        min = 0,
        max = 100,
        subtype = 'PERCENTAGE',
    )

    quality: IntProperty(
        name = "Quality",
        description = "Quality for image formats that support lossy compression",
        default = 90,
        min = 0,
        max = 100,
        subtype = 'PERCENTAGE',
    )

    

    #TODO: Include additional settings.


class SATELLITE_Preset(PropertyGroup):
    """
    Defines a single baking preset.
    """

    name: StringProperty(
        name = "Preset Name",
        description="The name of the export preset.",
        default=""
        )
    
    is_active: BoolProperty(
        name = "Active",
        description = "Determines whether this camera will be rendered or not if 'Render All Active' is used.",
        default = True,
    )

    output_dir: StringProperty(
        name = "Output Directory",
        description = "The directory the result will be saved to.",
        default = "//",
        subtype = "DIR_PATH",
    )

    output_name: StringProperty(
        name = "Output Name",
        description = "The name of the result.",
        default = "",
    )

    render_type: EnumProperty(
        name="Render Type",
        items=
            (
            ('Skybox', "Skybox", "render a defined World Material into an HDRI Image.  Satellite will setup the camera and scene for you."),
            ('Direct Camera', "Direct Camera", "render an image from a specific camera in the scene."),
            ),
            
        description="Defines the purpose of the render and the sets of settings Satellite will use in order to perform it.",
    )
    
    # might need this for satellite, undetermined
    # instance_id: IntProperty(
    #     name = "Instance ID",
    #     description="INTERNAL ONLY - Unique ID used to pair with format data, that holds the full export settings for the chosen file type."
    #     )
    
    # the data stored for FBX presets.
    data_skybox: PointerProperty(type=SATELLITE_FormatSkybox)

    # the data stored for OBJ presets.
    data_camera: PointerProperty(type=SATELLITE_FormatCamera)


class SATELLITE_SceneData(PropertyGroup):
    """
    An assortment of user-interface states and the list of baking operations.
    """

    # the available baking presets
    sat_presets: CollectionProperty(type=SATELLITE_Preset)

    ## The index of the currently selected collection from the UI list.  Will be -1 if not selected.
    sat_selected_list_index: IntProperty(default=0)

    # the menu toggle for Skybox render Presets, tabs didnt work out so this is muted for now
    # skybox_ui_options: EnumProperty(
    #     name = "Skybox Render Options",
    #     description = "bonk",
    #     items =
    #         (
    #         ('Scene', "Scene", "bonk"),
    #         ('Render', "Render", "bonk"),
    #         ),
    # )

    # # the menu toggle for Direct Camera render Presets
    # camera_ui_options: EnumProperty(
    #     name = "Direct Camera Render Options",
    #     description = "boop",
    #     items =
    #         (
    #         ('Scene', "Scene", "bonk"),
    #         ('Render', "Render", "bonk"),
    #         ('Format', "Format", "bonk"),
    #         ),
        
    # )


    