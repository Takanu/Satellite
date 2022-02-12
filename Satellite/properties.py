

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

    resolution_x: IntProperty(
        name="X Resolution",
        description="Controls the resolution of the X axis.",
        subtype = 'PIXEL',
        min=4,
        max=32768,
        default=2048,
    )

    resolution_y: IntProperty(
        name="Y Resolution",
        description="Controls the resolution of the Y axis.",
        subtype = 'PIXEL',
        min=4,
        max=32768,
        default=2048,
    )

    include_collection: StringProperty(
        name="Include Collection",
        description="Ensures that any collection matching this name in the scene will remain in the render.",
        default="Skybox",
    )

    # include an option to replace all visible object materials with one material

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