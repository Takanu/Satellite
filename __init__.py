# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

#This states the metadata for the plugin
bl_info = {
    "name": "Satellite",
    "author": "Takanu Kyriako.",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "Properties > Output",
    "wiki_url": "https://github.com/Takanu/Satellite",
    "description": "Batch render Skybox and Camera images with custom view layers and replacement materials",
    "tracker_url": "",
    "category": "Render"
}

import bpy
from . import auto_load
from bpy.types import AddonPreferences, PropertyGroup
from bpy.props import PointerProperty

auto_load.init()

from .properties import *

def register():
    auto_load.register()
    
    # Assign datablocks now all classes have been registered.
    bpy.types.Scene.SATL_SceneData = PointerProperty(name = 'Satellite Scene Data', type = SATELLITE_SceneData)

def unregister():
    del bpy.types.Scene.SATL_SceneData

    auto_load.unregister()
