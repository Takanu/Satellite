

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
    # Used to define settings for a Skybox bake.

    # Binds a format to a specific preset, (TODO: Check if we need this!)
    instance_id: IntProperty(default=-1)

    world_material: PointerProperty(
        type = bpy.types.World,
        name = "Skybox Material",
        description = "Defines the world material that will be used for Skybox baking.  If left blank the currently defined World Material will be used"
    )
    
    include_collection: StringProperty(
        name="Include Collection",
        description="Ensures that any collection matching this name in the scene will remain in the render",
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

    

    #TODO: Include different image format types.


class SATELLITE_FormatCamera(PropertyGroup):
    # Used to define settings for a Direct Camera render.

    # Binds a format to a specific preset, (TODO: Check this!)
    instance_id: IntProperty(default=-1)

    target_camera: PointerProperty(
        type = bpy.types.Camera,
        name = "Target Camera",
        description = "Defines the camera to be used",
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

    view_layer: StringProperty(
        name="Target View Layer",
        description="If defined, this View Layer will be used when rendering the scene",
        default="",
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

    color_depth: EnumProperty(
        name = "Color Depth",
        items =
            (
            ('8', "8", "8-bit color channels"),
            ('10', "10", "10-bit color channels"),
            ('12', "12", "12-bit color channels"),
            ('16', "16", "16-bit color channels"),
            ('32', "32", "32-bit color channels"),
            ),
        default = '8',
        description = "The bit depth per channel",
    )

    color_mode: EnumProperty(
        name = "Color Mode",
        items =
            (
            ('BW', "BW", "Export using the PNG format"),
            ('RGB', "RGB", "Export using the JPEG format"),
            ('RGBA', "RGBA", "Export using the Targa format"),
            ),
        default = 'BW',
        description = "The bit depth per channel",
    )

    compression: FloatProperty(
        name = "Compression",
        description = "The amount of time taken for Blender to determine the best compression for the file.  0 will result in no compression with a fast file output time and 100 will result in the maximum lossless compression with the slowest output time",
        default = 15,
        min = 0,
        max = 100,
        precision = 1,
        subtype = 'PERCENTAGE',
    )

    

    #TODO: Include additional settings.


class SATELLITE_BakePreset(PropertyGroup):
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
        description = "Determines whether this camera will be baked or not if 'Bake All Active' is used.",
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

    bake_type: EnumProperty(
        name="Bake Type",
        items=
            (
            ('Skybox', "Skybox", "Bake a defined World Material into an HDRI Image.  Satellite will setup the camera and scene for you."),
            ('Direct Camera', "Direct Camera", "Bake an image from a specific camera in the scene."),
            ),
            
        description="Defines the purpose of the bake and the sets of settings Satellite will use in order to perform it.",
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
    bake_presets: CollectionProperty(type=SATELLITE_BakePreset)

    ## The index of the currently selected collection from the UI list.  Will be -1 if not selected.
    bake_selected_list_index: IntProperty(default=0)

    # the menu toggle for Skybox Bake Presets
    skybox_ui_options: EnumProperty(
        name = "Skybox Bake Options",
        description = "bonk",
        items =
            (
            ('Scene', "Scene", "bonk"),
            ('Render', "Render", "bonk"),
            ),
    )

    # the menu toggle for Direct Camera Bake Presets
    camera_ui_options: EnumProperty(
        name = "FUCKKkkKK",
        description = "boop",
        items =
            (
            ('Scene', "Scene", "bonk"),
            ('Render', "Render", "bonk"),
            ('Format', "Format", "bonk"),
            ),
        
    )

    obj_menu_options: EnumProperty(
        name="Export Options",
        description="",
        items=(
        ('File', 'File', 'A tab containing file format-specific data sets like custom properties.'),
        ('Scene', 'Scene', 'A tab containing options for scene units, transform data and object type export filters.'),
        ('Mesh', 'Mesh', 'A tab containing options for how object geometry and mesh-related assets are exported.'),
        ),
    )

    