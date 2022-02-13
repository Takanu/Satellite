import bpy
from bpy.types import Menu, Panel, Operator, UIList


class SATELLITE_OT_Add(Operator):
    """Add a new Satellite"""

    bl_idname = "scene.satl_add"
    bl_label = "Add Satellite"

    def execute(self, context):
        sat_data = context.scene.SATL_SceneData
        new_render = sat_data.sat_presets.add()
        new_render.name = "Satellite " + str(len(sat_data.sat_presets))

        return {'FINISHED'}

class SATELLITE_OT_Remove(Operator):
    """Remove the selected Satellite"""

    bl_idname = "scene.satl_remove"
    bl_label = "Remove Satellite"

    def execute(self, context):
        sat_data = context.scene.SATL_SceneData
        sat_data.sat_presets.remove(sat_data.sat_selected_list_index)

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
        ui_list_column.template_list("SATELLITE_UL_PresetList", "default", sat_data, "sat_presets", 
                                    sat_data, "sat_selected_list_index", rows=3, maxrows=6)
        ui_list_column.operator("scene.satl_render_selected")
        ui_list_column.operator("scene.satl_render_all")
        ui_list_column.separator()

        ui_list_column = ui_list_area.column(align=True)
        ui_list_column.operator("scene.satl_add", text="", icon="ADD")
        ui_list_column.operator("scene.satl_remove", text="", icon="REMOVE")
        #ui_list_column.operator("scene.cap_shiftup", text="", icon="TRIA_UP")
        #ui_list_column.operator("scene.cap_shiftdown", text="", icon="TRIA_DOWN")
    

        # //////////////////////////////////
        # PRESET OPTIONS
        render_options_area = layout.column(align=False)

        count = 0
        for i, item in enumerate(sat_data.sat_presets, 1):
            count += 1
        
        list_index = sat_data.sat_selected_list_index

        if list_index > -1 and list_index < count:
            render_selected = sat_data.sat_presets[list_index]
            render_output = render_options_area.column(align=True)
            render_output.use_property_split = True
            render_output.use_property_decorate = False
            render_output.separator()

            # render_options_list.prop(render_selected, "name")
            render_output.prop(render_selected, "output_dir")
            render_output.prop(render_selected, "output_name")
            render_output.separator()
            render_output.separator()
            render_output.separator()

            render_format_selector = render_options_area.row(align=True)
            render_format_selector_split = render_format_selector.split(factor=0.4, align=True)
            render_format_selector_split.label(text="Render Type", icon="RENDER_RESULT")
            render_format_selector_split.prop(render_selected, "render_type", text="")
            render_options_area.separator()
            
            render_format_box = render_options_area.box()
            render_format_area = render_format_box.column(align=True)
            render_format_area.separator()


            if render_selected.render_type == 'Skybox':
                render_format = render_selected.data_skybox

                # First we have to splice the space up weirdly to get padding on each side
                render_tab_area = render_format_area.row(align=True)
                render_tab_area.separator()

                render_format_options = render_tab_area.column(align=True)
                render_format_options.use_property_split = True
                render_format_options.use_property_decorate = False

                # Scene Settings
                render_format_options.prop(render_format, "world_material")
                render_format_options.separator()
                render_format_options.prop(render_format, "include_collection")
                render_format_options.separator()
                render_format_options.separator()
                render_format_options.separator()
                
                # Render Engine Settings
                render_format_options.prop(render_format, "render_engine")
                render_format_options.separator()
                render_format_options.prop(render_format, "resolution")
                render_format_options.prop(render_format, "samples")
                render_format_options.separator()

                if render_format.render_engine == 'Cycles':
                    # This is used to ensure the boolean label is aligned.
                    render_format_list_denoiser = render_format_options.column(align=True, 
                        heading="Use Denoiser")
                    render_format_list_denoiser.prop(render_format, "cycles_use_denoiser", text="")

                elif render_format.render_engine == 'Eevee':
                    # This is used to ensure the boolean label is aligned.
                    render_format_list_denoiser = render_format_options.column(align=True, 
                        heading="Disable Post-Processing")
                    render_format_list_denoiser.prop(render_format, "eevee_disable_pp", text="")
                
                render_format_options.separator()
                render_format_options.separator()
                render_format_options.separator()
                render_format_col_mode = render_format_options.row(align=True)
                render_format_col_mode.prop(render_format, "color_mode", expand=True)
                render_format_options.separator()
                render_format_options.separator()

            


            if render_selected.render_type == 'Direct Camera':
                render_format = render_selected.data_camera

                # First we have to splice the space up weirdly to get padding on each side
                render_tab_area = render_format_area.row(align=True)
                render_tab_area.separator()

                # In order to get our tabs we have to use property split later
                render_format_options = render_tab_area.column(align=True)
                render_format_options.use_property_split = True
                render_format_options.use_property_decorate = False

                # Scene Settings
                render_format_options.prop(render_format, "target_camera")
                render_format_options.prop(render_format, "view_layer")
                render_format_options.separator()
                render_format_options.prop(render_format, "world_material")
                render_format_options.prop(render_format, "replacement_material")
                render_format_options.separator()
                render_format_options.separator()
                render_format_options.separator()


                # Render Engine Settings
                render_format_options.prop(render_format, "render_engine")
                render_format_options.separator()
                render_format_options.prop(render_format, "resolution_x")
                render_format_options.prop(render_format, "resolution_y")
                render_format_options.prop(render_format, "samples")
                render_format_options.separator()
                

                if render_format.render_engine == 'Cycles':
                    # This is used to ensure the boolean label is aligned.
                    render_format_list_denoiser = render_format_options.column(align=True, 
                        heading="Use Denoiser")
                    render_format_list_denoiser.prop(render_format, "cycles_use_denoiser", text="")
                
                elif render_format.render_engine == 'Eevee':
                    # This is used to ensure the boolean label is aligned.
                    render_format_list_denoiser = render_format_options.column(align=True, 
                        heading="Disable Post-Processing")
                    render_format_list_denoiser.prop(render_format, "eevee_disable_pp", text="")
                
                render_format_options.separator()
                render_format_options.separator()
                render_format_options.separator()


                # Export Format Settings
                render_format_options.prop(render_format, "file_format")
                render_format_options.separator()

                file_format = render_format.file_format

                if file_format in ['JPEG', 'CINEON', 'HDR']:
                    render_format_col_mode = render_format_options.row(align=True)
                    render_format_col_mode.prop(render_format, "color_mode_bw", expand=True)
                
                else:
                    render_format_col_mode = render_format_options.row(align=True)
                    render_format_col_mode.prop(render_format, "color_mode", expand=True)

                if file_format in ['PNG']:
                    render_format_col_depth = render_format_options.row(align=True)
                    render_format_col_depth.prop(render_format, "color_depth", expand=True)
                
                if file_format in ['PNG']:
                    render_format_options.prop(render_format, "compression")
                
                if file_format in ['JPEG']:
                    render_format_options.prop(render_format, "quality")

                render_format_options.separator()
                render_format_options.separator()

            # Adds the padding on the right side.
            render_tab_area.separator()

        