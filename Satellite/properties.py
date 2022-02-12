

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


# I dont yet know how to handle this kind of behaviour, so im just going to avoid it for now.

# def UpdateBakeExport(self, context):
#     """
#     Updates the "Enable Bake" status once changed from the list menu.
#     Note - Do not use this in any other place apart from when an object is represented in a list.
#     """

#     # TODO: THIS WILL BREAK, NOT SURE HOW TO HANDLE IT YET.
#     self.object.CAPObj.enable_export = self.enable_export


#     return None


# def GetBakeList(scene, context):
#     """
#     Returns the list of baking operations currently created.
#     """

#     items = [
#         ("0", "None",  "", 0),
#         ]

#     preferences = context.preferences
#     bake_list = None
#     try:
#         bake_list = context.scene.SATL_SceneData
#     except KeyError:
#         return items


#     u = 1

#     for i,x in enumerate(bake_list.bake_presets):
#         items.append((str(i+1), x.name, x.name, i+1))

#     return items


class SATELLITE_FormatSkybox(PropertyGroup):
    # Used to define settings for a Skybox bake.

    # Binds a format to a specific preset, (TODO: Check this!)
    instance_id: IntProperty(default=-1)

    resolution: IntProperty(
        name="Max Resolution",
        description="Controls the resolution of the X axis.  The Y axis resolution will be half this value.",
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

    use_denoiser: BoolProperty(
        name="Use Denoiser",
        description="If true, a denoiser will be used after rendering to improve the quality of the final result.",
        default=False,
    )

    include_collection: StringProperty(
        name="Include Collection",
        description="Ensures that any collection matching this name in the scene will remain in the render.",
        default="Skybox",
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
        subtype = "FILE_PATH",
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

    # TODO: Determine whether this is needed for our list to function or not.
    # # A collection that stores the list of collections that Capsule is currently displaying in the UI list.
    # bake_list: CollectionProperty(type=BakeListItem)

    # # ???
    # bake_list_index: IntProperty(
    #     name="",
    #     description="",
    #     )

    # ## ???
    # bake_selected_list: CollectionProperty(type=BakeListItem)

    # ## ???
    # bake_selected_list_enum: EnumProperty(items=GetBakeList)

    ## The index of the currently selected collection from the UI list.  Will be -1 if not selected.
    bake_selected_list_index: IntProperty(default=0)