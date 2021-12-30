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
    "version"    : (1, 3, 2),
    "blender"    : (3, 0, 0),
    "location"   : "3D Viewport > Sidebar > MAT > Quick Metal Materials",
    "warning"    : "",
    "wiki_url"   : "https://github.com/don1138/blender-qmm",
    "support"    : "COMMUNITY",
    "category"   : "Material"
}


import bpy


# Updater ops import, all setup in this file.
from . import addon_updater_ops


# PARENT PANEL
class BQMPanel(bpy.types.Panel):
    bl_idname = "BQM_PT_Panel"
    bl_label = "Quick Metal Materials"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MAT"

    def draw(self, context):
        layout = self.layout


# NOBLE METALS PANEL
class BQMPanelNoble(bpy.types.Panel):
    bl_idname = "BQM_PT_Panel_Noble"
    bl_label = "Noble Metals"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MAT"
    bl_parent_id = 'BQM_PT_Panel'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator("shader.qmm_gold_m_operator", text="Gold")
        row = layout.row()
        row.operator("shader.qmm_pale_gold_m_operator", text="Pale Gold")
        row = layout.row()
        row.operator("shader.qmm_gold_operator", text="Gold (Fresnel)")

        row = layout.row()
        row.operator("shader.qmm_silver_min_operator", text="Silver Min")
        row = layout.row()
        row.operator("shader.qmm_silver_max_operator", text="Silver Max")
        row = layout.row()
        row.operator("shader.qmm_pale_silver_m_operator", text="Pale Silver")
        row = layout.row()
        row.operator("shader.qmm_silver_operator", text="Silver (Fresnel)")


# BASE METALS PANEL
class BQMPanelBase(bpy.types.Panel):
    bl_idname = "BQM_PT_Panel_Base"
    bl_label = "Base Metals"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MAT"
    bl_parent_id = 'BQM_PT_Panel'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator("shader.qmm_aluminium_operator", text="Aluminium")

        row = layout.row()
        row.operator("shader.qmm_copper_min_operator", text="Copper Min")
        row = layout.row()
        row.operator("shader.qmm_copper_max_operator", text="Copper Max")
        row = layout.row()
        row.operator("shader.qmm_copper_operator", text="Copper (Fresnel)")

        row = layout.row()
        row.operator("shader.qmm_iron_operator", text="Iron")

        row = layout.row()
        row.operator("shader.qmm_lead_operator", text="Lead")
        row = layout.row()
        row.operator("shader.qmm_lead_rough_operator", text="Lead Rough")

        row = layout.row()
        row.operator("shader.qmm_titanium_operator", text="Titanium")


# ALLOY METALS PANEL
class BQMPanelAlloy(bpy.types.Panel):
    bl_idname = "BQM_PT_Panel_Alloy"
    bl_label = "Alloys"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MAT"
    bl_parent_id = 'BQM_PT_Panel'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator("shader.qmm_brass_operator", text="Brass")

        row = layout.row()
        row.operator("shader.qmm_bronze_operator", text="Bronze")

        row = layout.row()
        row.operator("shader.qmm_chrome_operator", text="Chrome")

        row = layout.row()
        row.operator("shader.qmm_steel_operator", text="Steel")


# EXTRAS PANEL
class BQMPanelExtras(bpy.types.Panel):
    bl_idname = "BQM_PT_Panel_Extras"
    bl_label = "Extras"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MAT"
    bl_parent_id = 'BQM_PT_Panel'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator("shader.qmm_glass_operator", text="Glass Hack")

        row = layout.row()
        row.operator("shader.qmm_mercury_operator", text="Liquid Mercury")

        row = layout.row()
        row.operator("shader.qmm_cutting_mat_operator", text="Rubber Cutting Mat")

        row = layout.row()
        row.operator("shader.qmm_plaster_operator", text="Tinted Plaster")


@addon_updater_ops.make_annotations
class AutoUpdaterPreferences(bpy.types.AddonPreferences):
	"""Blender QMM updater preferences"""
	bl_idname = __package__

	# Addon updater preferences.

	auto_check_update = bpy.props.BoolProperty(
		name="Auto-check for Update",
		description="If enabled, auto-check for updates using an interval",
		default=False)

	updater_interval_months = bpy.props.IntProperty(
		name='Months',
		description="Number of months between checking for updates",
		default=0,
		min=0)

	updater_interval_days = bpy.props.IntProperty(
		name='Days',
		description="Number of days between checking for updates",
		default=7,
		min=0,
		max=31)

	updater_interval_hours = bpy.props.IntProperty(
		name='Hours',
		description="Number of hours between checking for updates",
		default=0,
		min=0,
		max=23)

	updater_interval_minutes = bpy.props.IntProperty(
		name='Minutes',
		description="Number of minutes between checking for updates",
		default=0,
		min=0,
		max=59)

	def draw(self, context):
		layout = self.layout

		# Works best if a column, or even just self.layout.
		mainrow = layout.row()
		col = mainrow.column()

		# Updater draw function, could also pass in col as third arg.
		addon_updater_ops.update_settings_ui(self, context)


from .mats.alloys.Brass import *
from .mats.alloys.Bronze import *
from .mats.alloys.Chrome import *
from .mats.alloys.Steel import *
from .mats.base.Aluminium import *
from .mats.base.CopperMin import *
from .mats.base.CopperMax import *
from .mats.base.FresnelCopper import *
from .mats.base.Iron import *
from .mats.base.Lead import *
from .mats.base.LeadRough import *
from .mats.base.Titanium import *
from .mats.extras.CuttingMat import *
from .mats.extras.GlassHack import *
from .mats.extras.Mercury import *
from .mats.extras.Plaster import *
from .mats.noble.FresnelGold import *
from .mats.noble.FresnelSilver import *
from .mats.noble.Gold import *
from .mats.noble.PaleGoldMetallic import *
from .mats.noble.PaleSilverMetallic import *
from .mats.noble.SilverMin import *
from .mats.noble.SilverMax import *
from .SpecularGroupNode import *


classes = [
    BQMPanel,
    BQMPanelNoble,
    BQMPanelBase,
    BQMPanelAlloy,
    BQMPanelExtras,
    AutoUpdaterPreferences,
    QMMAluminium,
    QMMBrass,
    QMMBronze,
    QMMChrome,
    QMMCopperFresnel,
    QMMCopperMin,
    QMMCopperMax,
    QMMCuttingMat,
    QMMGlass,
    QMMGold,
    QMMGoldFresnel,
    QMMIron,
    QMMLead,
    QMMLeadRough,
    QMMMercury,
    QMMPaleGold,
    QMMPaleSilverMax,
    QMMPlaster,
    QMMSilverFresnel,
    QMMSilverMin,
    QMMSilverMax,
    QMMSteel,
    QMMTitanium,
    SpecularGroup,
]


def register():
	# Addon updater code and configurations.
	# In case of a broken version, try to register the updater first so that
	# users can revert back to a working version.
	addon_updater_ops.register(bl_info)

	# Register the example panel, to show updater buttons.
	for cls in classes:
		addon_updater_ops.make_annotations(cls)  # Avoid blender 2.8 warnings.
		bpy.utils.register_class(cls)


def unregister():
	# Addon updater unregister.
	addon_updater_ops.unregister()
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
