
'''
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

#This states the metadata for the plugin
bl_info = {
    "name": "Satellite",
    "author": "Takanu Kyriako.",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "Properties > Output",
    "wiki_url": "https://github.com/Takanu/Satellite",
    "description": "Quickly render HDRI images of the World Material and scene objects of your choice.",
    "tracker_url": "",
    "category": "Render"
}
    

import bpy
from bpy.types import Menu
from bpy.types import Operator
from bpy.props import IntProperty, FloatProperty, StringProperty, BoolProperty

import os
from math import radians
from mathutils import Vector
        
# -----------------------------------------------------------------------------
#   Interface + Render Operator
# -----------------------------------------------------------------------------     
class SatellitePanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""

    bl_label = "Satellite"
    bl_idname = "PROPERTIES_PT_Satellite"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "output"
    

    def draw(self, context):
        layout = self.layout
        scene = bpy.context.scene

        row = layout.column(align=True)
        row.use_property_split = True
        row.use_property_decorate = False

        row.prop(scene, "satellite_resolution")
        row.prop(scene, "satellite_samples")
        row.prop(scene, "satellite_include_col_name")
        row.prop(scene, "satellite_use_denoiser")

        row.separator()
        row.separator()
        row.prop(scene, "satellite_output_dir")
        row.prop(scene, "satellite_output_name")

        row.separator()
        row.separator()
        row.operator("scene.satl_render")


class SATELLITE_OT_Render_Skybox(Operator):
    """Renders the Skybox with the provided settings and file destination."""

    bl_idname = "scene.satl_render"
    bl_label = "Render Skybox"

    def execute(self, context):

        # store old properties for later
        old_render_settings = {}
        old_render_settings['engine'] = context.scene.render.engine
        old_render_settings['res_x'] = context.scene.render.resolution_x
        old_render_settings['res_y'] = context.scene.render.resolution_y
        old_render_settings['file_format'] = context.scene.render.image_settings.file_format
        old_render_settings['device'] = context.scene.cycles.device
        old_render_settings['preview_samples'] = context.scene.cycles.preview_samples
        old_render_settings['samples'] = context.scene.cycles.samples
        old_render_settings['use_denoising'] = context.scene.cycles.use_denoising

        
        # create a new view layer and hide everything
        bake_viewlayer = context.scene.view_layers.new(name="Satellite Bake")
        context.window.view_layer = bake_viewlayer

        for layer in bake_viewlayer.layer_collection.children:
            if layer.name != context.scene.satellite_include_col_name:
                layer.exclude = True


        # Setup rendering settings
        context.scene.render.engine = 'CYCLES'
        context.scene.render.resolution_x = context.scene.satellite_resolution
        context.scene.render.resolution_y = context.scene.satellite_resolution / 2
        context.scene.render.image_settings.file_format = 'HDR'
        context.scene.cycles.device = 'GPU'
        context.scene.cycles.samples = context.scene.satellite_samples
        context.scene.cycles.use_denoising = context.scene.satellite_use_denoiser


        # Setup the camera
        bpy.ops.object.camera_add()
        context.active_object.location = Vector((0.0, 0.0, 0.0))
        context.active_object.rotation_euler = Vector((radians(90), 0.0, 0.0))

        camera_name = context.active_object.name
        camera_bname = context.active_object.data.name
        print(camera_name)
        bpy.data.cameras[camera_bname].type = 'PANO'
        bpy.data.cameras[camera_bname].cycles.panorama_type = 'EQUIRECTANGULAR'
        

        # render this bad boy *slaps side of car*
        context.scene.camera = context.active_object
        name = context.scene.satellite_output_dir
        dir = context.scene.satellite_output_name

        destination = os.path.join(name, dir)
        bpy.context.scene.render.filepath = destination
        bpy.context.scene.render.use_single_layer = True
        bpy.ops.render.render(write_still = True)


        # ////////////////////////////////////////////////////////////////////////////
        # Clean up
        bpy.data.objects.remove(bpy.data.objects[camera_name], do_unlink=True)
        context.scene.view_layers.remove(bake_viewlayer)

        context.scene.render.engine = old_render_settings['engine']
        context.scene.render.resolution_x = old_render_settings['res_x']
        context.scene.render.resolution_y = old_render_settings['res_y']
        context.scene.render.image_settings.file_format = old_render_settings['file_format']
        context.scene.cycles.device = old_render_settings['device']
        context.scene.cycles.preview_samples = old_render_settings['preview_samples']
        context.scene.cycles.samples = old_render_settings['samples']
        context.scene.cycles.use_denoising = old_render_settings['use_denoising']

        self.report({'INFO'}, "The Skybox has been saved to " + destination + ".")
        return {'FINISHED'}



classes = (
    SatellitePanel, 
    SATELLITE_OT_Render_Skybox, 
)

         
# -----------------------------------------------------------------------------
#    Register      
# -----------------------------------------------------------------------------         
def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    
    bpy.types.Scene.satellite_resolution = IntProperty(
        name="Max Resolution",
        description="Controls the resolution of the X axis.  The Y axis resolution will be half this value.",
        subtype = 'PIXEL',
        min=4,
        max=32768,
        default=2048,
    )

    bpy.types.Scene.satellite_samples = IntProperty(
        name="Render Samples",
        description="Sets the amount of samples to be used when rendering the HDRI.",
        min=4,
        soft_max=4096,
        default=512,
    )

    bpy.types.Scene.satellite_use_denoiser = BoolProperty(
        name="Use Denoiser",
        description="If true, a denoiser will be used after rendering to improve the quality of the final result.",
        default=False,
    )

    bpy.types.Scene.satellite_include_col_name = StringProperty(
        name="Include Collection",
        description="Any collection with this name will be included in the Skybox render.",
        default="Skybox",
    )

    bpy.types.Scene.satellite_output_dir = StringProperty(
        name="Output Directory",
        description="The directory the result will be saved to.",
        default="//",
        subtype="FILE_PATH",
    )

    bpy.types.Scene.satellite_output_name = StringProperty(
        name="Output Name",
        description="The directory the result will be saved to.",
        default="",
    )

    
def unregister():
    from bpy.utils import unregister_class

    del bpy.types.Scene.satellite_resolution
    del bpy.types.Scene.satellite_samples
    del bpy.types.Scene.satellite_use_denoiser
    del bpy.types.Scene.satellite_include_col_name
    del bpy.types.Scene.satellite_output_dir
    del bpy.types.Scene.satellite_output_name

    for cls in reversed(classes):
        unregister_class(cls)
    

if __name__ == "__main__":
    register()