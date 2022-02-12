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
        ui_list_area = layout.row(align=True)
        ui_list_column = ui_list_area.column(align=True)
        ui_list_column.template_list("SATELLITE_UL_PresetList", "default", sat_data, "bake_presets", 
                                    sat_data, "bake_selected_list_index", rows=3, maxrows=6)
        ui_list_column.operator("scene.satl_render")
        ui_list_column.separator()

        ui_list_column = ui_list_area.column(align=True)
        ui_list_column.operator("scene.satl_add_bake", text="", icon="ADD")
        ui_list_column.operator("scene.satl_remove_bake", text="", icon="REMOVE")
        #ui_list_column.operator("scene.cap_shiftup", text="", icon="TRIA_UP")
        #ui_list_column.operator("scene.cap_shiftdown", text="", icon="TRIA_DOWN")
    

        # //////////////////////////////////
        # PRESET OPTIONS
        bake_options_area = layout.column(align=False)

        count = 0
        for i, item in enumerate(sat_data.bake_presets, 1):
            count += 1
        
        list_index = sat_data.bake_selected_list_index

        if list_index > -1 and list_index < count:
            bake_selected = sat_data.bake_presets[list_index]
            bake_output = bake_options_area.column(align=True)
            bake_output.use_property_split = True
            bake_output.use_property_decorate = False
            bake_output.separator()

            # bake_options_list.prop(bake_selected, "name")
            bake_output.prop(bake_selected, "output_dir")
            bake_output.prop(bake_selected, "output_name")
            bake_output.separator()
            bake_output.separator()
            bake_output.separator()

            bake_format_selector = bake_options_area.row(align=True)
            bake_format_selector_split = bake_format_selector.split(factor=0.4, align=True)
            bake_format_selector_split.label(text="Bake Type", icon="RENDER_RESULT")
            bake_format_selector_split.prop(bake_selected, "bake_type", text="")
            bake_options_area.separator()
            
            bake_format_box = bake_options_area.box()
            bake_format_area = bake_format_box.column(align=True)
            bake_format_area.separator()


            if bake_selected.bake_type == 'Skybox':
                bake_format = bake_selected.data_skybox

                # First we have to splice the space up weirdly to get padding on each side
                bake_tab_area = bake_format_area.row(align=True)
                bake_tab_area.separator()

                bake_format_options = bake_tab_area.column(align=True)
                bake_format_options.use_property_split = True
                bake_format_options.use_property_decorate = False

                # Scene Settings
                bake_format_options.prop(bake_format, "world_material")
                bake_format_options.separator()
                bake_format_options.prop(bake_format, "include_collection")
                bake_format_options.separator()
                bake_format_options.separator()
                bake_format_options.separator()
                
                # Render Engine Settings
                bake_format_options.prop(bake_format, "render_engine")
                bake_format_options.separator()
                bake_format_options.prop(bake_format, "resolution")
                bake_format_options.prop(bake_format, "samples")
                bake_format_options.separator()

                if bake_format.render_engine == 'Cycles':
                    # This is used to ensure the boolean label is aligned.
                    bake_format_list_denoiser = bake_format_options.column(align=True, 
                        heading="Use Denoiser")
                    bake_format_list_denoiser.prop(bake_format, "cycles_use_denoiser", text="")
                    bake_format_options.separator()
                
                elif bake_format.render_engine == 'Eevee':
                    # This is used to ensure the boolean label is aligned.
                    bake_format_list_denoiser = bake_format_options.column(align=True, 
                        heading="Disable Post-Processing")
                    bake_format_list_denoiser.prop(bake_format, "eevee_disable_pp", text="")
                    bake_format_options.separator()

            


            if bake_selected.bake_type == 'Direct Camera':
                bake_format = bake_selected.data_camera

                # First we have to splice the space up weirdly to get padding on each side
                bake_tab_area = bake_format_area.row(align=True)
                bake_tab_area.separator()

                # In order to get our tabs we have to use property split later
                bake_format_options = bake_tab_area.column(align=True)
                bake_format_options.use_property_split = True
                bake_format_options.use_property_decorate = False

                # Scene Settings
                bake_format_options.prop(bake_format, "target_camera")
                bake_format_options.separator()
                bake_format_options.prop(bake_format, "world_material")
                bake_format_options.prop(bake_format, "replacement_material")
                bake_format_options.separator()
                bake_format_options.prop(bake_format, "view_layer")
                bake_format_options.separator()
                bake_format_options.separator()
                bake_format_options.separator()


                # Render Engine Settings
                bake_format_options.prop(bake_format, "render_engine")
                bake_format_options.separator()
                bake_format_options.prop(bake_format, "resolution_x")
                bake_format_options.prop(bake_format, "resolution_y")
                bake_format_options.prop(bake_format, "samples")
                bake_format_options.separator()
                

                if bake_format.render_engine == 'Cycles':
                    # This is used to ensure the boolean label is aligned.
                    bake_format_list_denoiser = bake_format_options.column(align=True, 
                        heading="Use Denoiser")
                    bake_format_list_denoiser.prop(bake_format, "cycles_use_denoiser", text="")
                
                elif bake_format.render_engine == 'Eevee':
                    # This is used to ensure the boolean label is aligned.
                    bake_format_list_denoiser = bake_format_options.column(align=True, 
                        heading="Disable Post-Processing")
                    bake_format_list_denoiser.prop(bake_format, "eevee_disable_pp", text="")
                
                bake_format_options.separator()
                bake_format_options.separator()
                bake_format_options.separator()


                # Export Format Settings
                bake_format_options.prop(bake_format, "file_format")
                bake_format_options.separator()
                bake_format_col_depth = bake_format_options.row(align=True)
                bake_format_col_depth.prop(bake_format, "color_depth", expand=True)
                bake_format_col_mode = bake_format_options.row(align=True)
                bake_format_col_mode.prop(bake_format, "color_mode", expand=True)
                bake_format_options.prop(bake_format, "compression")
                bake_format_options.separator()
                bake_format_options.separator()

            # Adds the padding on the right side.
            bake_tab_area.separator()

        