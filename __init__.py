# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name"       : "QMM (Quick Metal Materials)",
    "description": "A Collection of Metal Materials",
    "author"     : "Don Schnitzius",
    "version"    : (0, 0, 3),
    "blender"    : (2, 83, 0),
    "location"   : "3D Viewport > Sidebar > Create",
    "warning"    : "",
    "wiki_url"   : "https://github.com/don1138/blender-qmm",
    "support"    : "COMMUNITY",
    "category"   : "Material"
}

import bpy

# PARENT PANEL
class BQMPanel(bpy.types.Panel):
    bl_idname = "BQM_PT_Panel"
    bl_label = "Quick Metal Materials"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "QMM"

    def draw(self, context):
        layout = self.layout


# NOBLE METALS PANEL
class BQMPanelNoble(bpy.types.Panel):
    bl_idname = "BQM_PT_Panel_Noble"
    bl_label = "Noble Metals"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "QMM"
    bl_parent_id = 'BQM_PT_Panel'

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator("shader.gold_operator", text="Gold")
        row = layout.row()
        row.operator("shader.gold_m_operator", text="Gold Metallic")

        row = layout.row()
        row.operator("shader.silver_min_operator", text="Silver")
        row = layout.row()
        row.operator("shader.silver_min_operator", text="Silver Metallic Min")
        row = layout.row()
        row.operator("shader.silver_max_operator", text="Silver Metallic Max")


# BASE METALS PANEL
class BQMPanelBase(bpy.types.Panel):
    bl_idname = "BQM_PT_Panel_Base"
    bl_label = "Base Metals & Alloys"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "QMM"
    bl_parent_id = 'BQM_PT_Panel'

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator("shader.aluminium_operator", text="Aluminium")

        row = layout.row()
        row.operator("shader.brass_operator", text="Brass")

        row = layout.row()
        row.operator("shader.bronze_operator", text="Bronze")

        row = layout.row()
        row.operator("shader.copper_operator", text="Copper")
        row = layout.row()
        row.operator("shader.copper_min_operator", text="Copper Metallic Min")
        row = layout.row()
        row.operator("shader.copper_max_operator", text="Copper Metallic Max")

        row = layout.row()
        row.operator("shader.iron_operator", text="Iron")

        row = layout.row()
        row.operator("shader.steel_operator", text="Steel")

        row = layout.row()
        row.operator("shader.titanium_operator", text="Titanium")


# EXTRAS PANEL
class BQMPanelExtras(bpy.types.Panel):
    bl_idname = "BQM_PT_Panel_Extras"
    bl_label = "Extras"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "QMM"
    bl_parent_id = 'BQM_PT_Panel'

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator("shader.mercury_operator", text="Liquid Mercury")

        row = layout.row()
        row.operator("shader.glass_operator", text="Glass Hack")


from .Aluminium import *
from .Brass import *
from .Bronze import *
from .Copper import *
from .CopperMin import *
from .CopperMax import *
from .GlassHack import *
from .Gold import *
from .GoldMetallic import *
from .Iron import *
from .Mercury import *
from .Silver import *
from .SilverMin import *
from .SilverMax import *
from .Steel import *
from .Titanium import *


from bpy.utils import register_class, unregister_class

_classes = [
    BQMPanel,
    BQMPanelNoble,
    BQMPanelBase,
    BQMPanelExtras,
    Aluminium,
    Brass,
    Bronze,
    Copper,
    CopperMin,
    CopperMax,
    Glass,
    Gold,
    GoldMetallic,
    Iron,
    Mercury,
    Silver,
    SilverMin,
    SilverMax,
    Steel,
    Titanium,
]

def register():
    for cls in _classes:
        register_class(cls)

def unregister():
    for cls in _classes:
        unregister_class(cls)

if __name__ == "__main__":
    register()
