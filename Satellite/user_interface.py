import bpy
from bpy.types import Menu, Panel, Operator, UIList


class SATELLITE_OT_AddBake(Operator):
    """Add a new Bake Preset"""

    bl_idname = "scene.satl_add_bake"
    bl_label = "Add Bake Preset"

    def execute(self, context):
        sat_data = context.scene.SATL_SceneData
        new_bake = sat_data.bake_presets.add()
        new_bake.name = "Bake " + str(len(sat_data.bake_presets))

        return {'FINISHED'}

class SATELLITE_OT_RemoveBake(Operator):
    """Remove the selected Bake Preset"""

    bl_idname = "scene.satl_remove_bake"
    bl_label = "Remove Bake Preset"

    def execute(self, context):
        sat_data = context.scene.SATL_SceneData
        sat_data.bake_presets.remove(sat_data.bake_selected_list_index)

        return {'FINISHED'}


class SATELLITE_UL_PresetList(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):

        layout.prop(item, "name", text="", emboss=False)
        layout.prop(item, "is_active", text="")


class SATELLITE_UL_MainMenu(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""

    bl_label = "Satellite"
    bl_idname = "PROPERTIES_PT_Satellite"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "output"

    def draw(self, context):

        layout = self.layout
        scene = bpy.context.scene
        sat_data = scene.SATL_SceneData

        # //////////////////////////////////
        # LIST MENU
        ui_list = layout.row(align=True)
        ui_list.template_list("SATELLITE_UL_PresetList", "default", sat_data, "bake_presets", 
                                    sat_data, "bake_selected_list_index", rows=3, maxrows=6)

        ui_list.separator()

        ui_list_column = ui_list.column(align=True)
        ui_list_column.operator("scene.satl_add_bake", text="", icon="ADD")
        ui_list_column.operator("scene.satl_remove_bake", text="", icon="REMOVE")
        #ui_list_column.operator("scene.cap_shiftup", text="", icon="TRIA_UP")
        #ui_list_column.operator("scene.cap_shiftdown", text="", icon="TRIA_DOWN")
    

        # //////////////////////////////////
        # PRESET OPTIONS
        bake_options_list = layout.column(align=False)
        bake_options_list.use_property_split = True
        bake_options_list.use_property_decorate = False
        bake_options_list.separator()

        count = 0
        for i, item in enumerate(sat_data.bake_presets, 1):
            count += 1
        
        list_index = sat_data.bake_selected_list_index

        if list_index > -1 and list_index < count:
            bake_selected = sat_data.bake_presets[list_index]
            bake_options_list.prop(bake_selected, "name")
            bake_options_list.prop(bake_selected, "output_dir")
            bake_options_list.prop(bake_selected, "output_name")
            bake_options_list.separator()
            bake_options_list.separator()
            bake_options_list.separator()

            bake_format_selector = bake_options_list.row(align=True)
            bake_format_selector_split = bake_format_selector.split(factor=0.4, align=True)
            bake_format_selector_split.label(text="Bake Type", icon="RENDER_RESULT")
            bake_format_selector_split.prop(bake_selected, "bake_type", text="")
            #bake_format_selector.separator()
            bake_options_list.separator()

            
            bake_format_box = bake_options_list.box()
            bake_format_list = bake_format_box.column(align=True)
            bake_format_list.separator()
            #bake_format_selector.separator()
            #
            # bake_options_list.prop(bake_selected, "bake_type", icon="RENDER_RESULT")
            # 
            # 

            if bake_selected.bake_type == 'Skybox':
                bake_format = bake_selected.data_skybox
                bake_format_list.prop(bake_format, "world_material")
                bake_format_list.separator()

                bake_format_list.prop(bake_format, "resolution")
                bake_format_list.prop(bake_format, "samples")
                bake_format_list.separator()

                bake_format_list_denoiser = bake_format_list.column(align=True, heading="Use Denoiser")
                bake_format_list_denoiser.prop(bake_format, "use_denoiser", text="")
                bake_format_list.separator()

                bake_format_list.prop(bake_format, "include_collection")
                bake_format_list.separator()


            else:
                bake_format = bake_selected.data_skybox


        bake_options_list.separator()
        bake_options_list.operator("scene.satl_render")