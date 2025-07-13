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
    "name": "QMM (Quick Metal Materials)",
    "description": "A Collection of Metal Materials",
    "author": "Don Schnitzius",
    "version": (1, 20, 0),
    "blender": (3, 0, 0),
    "location": "3D Viewport > Sidebar > MAT > Quick Metal Materials",
    "warning": "",
    "doc_url": "https://github.com/don1138/blender-qmm",
    "support": "COMMUNITY",
    "category": "Material"
}


import bpy


from .localization import *


# BOOLEAN FOR PANEL
class QMMSettings(bpy.types.PropertyGroup):
    diffuse_more: bpy.props.BoolProperty(name='',default=False)
    

# PARENT PANEL
class QMMPanel(bpy.types.Panel):
    bl_idname = "QMM_PT_Panel"
    bl_label = 'Quick Metal Materials'
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MAT"
    # bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        diffuse_bool = context.scene.diffuse_bool

        srow = layout.row()
        scol = srow.column(align=True)
        scol.scale_y = 1.25
        scol.prop(diffuse_bool, "diffuse_more")

        scol = srow.column(align=True)
        scol.scale_y = 1.25
        scol.scale_x = 3.0
        scol.label(text="Set Viewport Color")


# NOBLE METALS PANEL
class QMMPanelNoble(bpy.types.Panel):
    bl_idname = "QMM_PT_Panel_Noble"
    bl_label = 'Noble Metals'
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MAT"
    bl_parent_id = 'QMM_PT_Panel'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator("shader.qmm_copper_m_operator", text='Copper')

        row = layout.row()
        row.operator("shader.qmm_gold_m_operator", text='Gold')

        row = layout.row()
        row.operator("shader.qmm_palladium_operator", text='Palladium')
        row = layout.row()
        row.operator("shader.qmm_platinum_operator", text='Platinum')

        row = layout.row()
        row.operator("shader.qmm_silver_m_operator", text='Silver')

        row = layout.row()
        row.operator("shader.qmm_copper_operator", text='Copper Fresnel')
        row = layout.row()
        row.operator("shader.qmm_gold_operator", text='Gold Fresnel')
        row = layout.row()
        row.operator("shader.qmm_silver_operator", text='Silver Fresnel')


# BASE METALS PANEL
class QMMPanelBase(bpy.types.Panel):
    bl_idname = "QMM_PT_Panel_Base"
    bl_label = 'Base Metals'
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MAT"
    bl_parent_id = 'QMM_PT_Panel'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator("shader.qmm_aluminium_operator", text='Aluminium')

        row = layout.row()
        row.operator("shader.qmm_iron_operator", text='Iron')

        row = layout.row()
        row.operator("shader.qmm_lead_operator", text='Lead')
        row = layout.row()
        row.operator("shader.qmm_lead_rough_operator", text='Lead Rough')

        row = layout.row()
        row.operator("shader.qmm_nickel_operator", text='Nickel')

        row = layout.row()
        row.operator("shader.qmm_tin_operator", text='Tin')

        row = layout.row()
        row.operator("shader.qmm_zinc_operator", text='Zinc')


# ALLOY METALS PANEL
class QMMPanelAlloy(bpy.types.Panel):
    bl_idname = "QMM_PT_Panel_Alloy"
    bl_label = 'Alloys'
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MAT"
    bl_parent_id = 'QMM_PT_Panel'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator("shader.qmm_brass_operator", text='Brass')

        row = layout.row()
        row.operator("shader.qmm_bronze_operator", text='Bronze')

        row = layout.row()
        row.operator("shader.qmm_orichalcum_operator", text='Orichalcum')

        row = layout.row()
        row.operator("shader.qmm_steel_operator", text='Steel')


# CARBON STEEL METALS PANEL
class QMMPanelCarbonSteel(bpy.types.Panel):
    bl_idname = "QMM_PT_Panel_Carbon_Steel"
    bl_label = '    Carbon Steel'
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MAT"
    bl_parent_id = 'QMM_PT_Panel_Alloy'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator("shader.qmm_carbon_steel_new_operator", text='Carbon Steel New')

        row = layout.row()
        row.operator("shader.qmm_carbon_steel_weathered_operator", text='Carbon Steel Weathered')


# STAINLESS STEEL METALS PANEL
class QMMPanelStainlessSteel(bpy.types.Panel):
    bl_idname = "QMM_PT_Panel_Stainless_Steel"
    bl_label = '    Stainless Steel'
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MAT"
    bl_parent_id = 'QMM_PT_Panel_Alloy'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator("shader.qmm_stainless_steel_304_operator", text='304 Common Stainless Steel')

        row = layout.row()
        row.operator("shader.qmm_stainless_steel_316_operator", text='316 High-Chromium Stainless Steel')

        row = layout.row()
        row.operator("shader.qmm_high_alloy_stainless_steel_operator", text='High-Alloy Stainless Steel')


# ALLOY STEEL METALS PANEL
class QMMPanelAlloySteel(bpy.types.Panel):
    bl_idname = "QMM_PT_Panel_Alloy_Steel"
    bl_label = '    Alloy Steel'
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MAT"
    bl_parent_id = 'QMM_PT_Panel_Alloy'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator("shader.qmm_alloy_steel_4140_operator", text='4140 Alloy Steel')

        row = layout.row()
        row.operator("shader.qmm_alloy_steel_4340_operator", text='4340 Alloy Steel')

        row = layout.row()
        row.operator("shader.qmm_nickel_vanadium_steel_operator", text='Nickel-Vanadium Steel')

        row = layout.row()
        row.operator("shader.qmm_manganese_steel_operator", text='Manganese Steel')

        row = layout.row()
        row.operator("shader.qmm_tool_steel_operator", text='Tool Steel')

        row = layout.row()
        row.operator("shader.qmm_spring_steel_operator", text='Spring Steel')

        row = layout.row()
        row.operator("shader.qmm_structural_steel_operator", text='Structural Steel')

        row = layout.row()
        row.operator("shader.qmm_a36_structural_steel_operator", text='A36 Structural Steel')

        row = layout.row()
        row.operator("shader.qmm_a572_structural_steel_operator", text='A572 Structural Steel')


# SPECIALTY STEEL METALS PANEL
class QMMPanelSpecialtySteel(bpy.types.Panel):
    bl_idname = "QMM_PT_Panel_Specialty_Steel"
    bl_label = '    Specialty Steel'
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MAT"
    bl_parent_id = 'QMM_PT_Panel_Alloy'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator("shader.qmm_case_hardened_steel_a_operator", text='Case-Hardened Steel A')

        row = layout.row()
        row.operator("shader.qmm_case_hardened_steel_b_operator", text='Case-Hardened Steel B')

        row = layout.row()
        row.operator("shader.qmm_hsla_steel_operator", text='HSLA Steel')

        row = layout.row()
        row.operator("shader.qmm_maraging_steel_operator", text='Maraging Steel')

        row = layout.row()
        row.operator("shader.qmm_free_machining_steel_operator", text='Free-Machining Steel')

        row = layout.row()
        row.operator("shader.qmm_galvanized_steel_operator", text='Galvanized Steel')

        row = layout.row()
        row.operator("shader.qmm_weathering_steel_operator", text='Weathering Steel')

        row = layout.row()
        row.operator("shader.qmm_virgin_weathering_steel_operator", text='Virgin Weathering Steel')


# MINOR METALS PANEL
class QMMPanelMinor(bpy.types.Panel):
    bl_idname = "QMM_PT_Panel_Minor"
    bl_label = 'Minor Metals'
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MAT"
    bl_parent_id = 'QMM_PT_Panel'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator("shader.qmm_chromium_operator", text='Chromium')

        row = layout.row()
        row.operator("shader.qmm_mercury_operator", text='Mercury')

        row = layout.row()
        row.operator("shader.qmm_silicon_operator", text='Silicon')

        row = layout.row()
        row.operator("shader.qmm_titanium_p_operator", text='Titanium Polished')

        row = layout.row()
        row.operator("shader.qmm_titanium_operator", text='Titanium Textured')


# EXTRAS PANEL
class QMMPanelExtras(bpy.types.Panel):
    bl_idname = "QMM_PT_Panel_Extras"
    bl_label = 'Extras'
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MAT"
    bl_parent_id = 'QMM_PT_Panel'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator("shader.qmm_asphalt_operator", text='Asphalt')

        row = layout.row()
        row.operator("shader.qmm_asphalt_b_operator", text='Asphalt Bleached')

        row = layout.row()
        row.operator("shader.qmm_car_paint_operator", text='Car Paint')

        row = layout.row()
        row.operator("shader.qmm_cinnabar_operator", text='Cinnabar Lacquer')

        row = layout.row()
        row.operator("shader.qmm_glass_operator", text='Glass')

        row = layout.row()
        row.operator("shader.qmm_mithryl_operator", text='Mithryl')

        row = layout.row()
        row.operator("shader.qmm_cutting_mat_operator", text='Rubber Cutting Mat')

        row = layout.row()
        row.operator("shader.qmm_plaster_operator", text='Tinted Plaster')

        row = layout.row()
        row.operator("shader.qmm_wall_paint_operator", text='Wall Paint')


class QMM_AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__  # or use your module name

    # Addon settings can go here as bpy.props, if needed

    def draw(self, context):
        layout = self.layout

        # Additional Resources Section
        box = layout.box()
        box.label(text="Additional Resources:")

        linkcol = box.column(align=True)

        # Gumroad Links
        gumbox = linkcol.box()
        gumroad = gumbox.row()
        gumroad.ui_units_y = 0.8
        gumroad.label(text="Gumroad:")

        gumrow = gumbox.row()
        gumrow.scale_y = 1.6
        gumrow.operator(
            "wm.url_open", text="Blender Quick Lighting Environment").url = "https://don1138.gumroad.com/l/blender-qle"
        gumrow.operator(
            "wm.url_open", text="Blender Quick Resize Nodes").url = "https://don1138.gumroad.com/l/blender-qrn"

        # Github Links
        gitbox = linkcol.box()
        github = gitbox.row()
        github.ui_units_y = 0.8
        github.label(text="Github:")

        gitrow = gitbox.row()
        gitrow.scale_y = 1.6
        gitrow.operator(
            "wm.url_open", text="Blender Materials").url = "https://github.com/don1138/blender-materials"
        gitrow.operator(
            "wm.url_open", text="Blender Quick Material Colors").url = "https://github.com/don1138/blender-pcoy"


from .mats.MakeMetal import *
from .mats.MakeSteel import *
from .mats.extras.Asphalt import *
from .mats.extras.AsphaltBleached import *
from .mats.extras.CarPaint import *
from .mats.extras.Cinnabar import *
from .mats.extras.CuttingMat import *
from .mats.extras.Glass import *
from .mats.extras.Mithryl import *
from .mats.extras.Plaster import *
from .mats.extras.WallPaint import *
from .mats.fresnel.FresnelCopper import *
from .mats.fresnel.FresnelGold import *
from .mats.fresnel.FresnelSilver import *
from .mats.CopperColors import *
from .mats.GoldColors import *
from .mats.SilverColors import *
from .mats.TitaniumColors import *
from .mats.AnisotrophyX import *
from .mats.Canisotrophy import *
from .mats.EnergyConservation import *
from .mats.MetalFlake import *
from .mats.PearlescentPigment import *
from .mats.Specular import *
from .mats.SteelRoughness import *
from .mats.Texturizer import *
from .mats.UnevenRoughness import *


classes = [
    QMM_AddonPreferences,
    QMMSettings,
    QMMPanel,
    QMMPanelNoble,
    QMMPanelBase,
    QMMPanelAlloy,
    QMMPanelCarbonSteel,
    QMMPanelStainlessSteel,
    QMMPanelAlloySteel,
    QMMPanelSpecialtySteel,
    QMMPanelMinor,
    QMMPanelExtras,
    QMMAluminium,
    QMMAsphalt,
    QMMAsphaltBleached,
    QMMBrass,
    QMMBronze,
    QMMCarPaint,
    QMMChromium,
    QMMCinnabar,
    QMMCopper,
    QMMCopperFresnel,
    QMMCuttingMat,
    QMMGlass,
    QMMGold,
    QMMGoldFresnel,
    QMMIron,
    QMMLead,
    QMMLeadRough,
    QMMMercury,
    QMMMithryl,
    QMMNickel,
    QMMOrichalcum,
    QMMPalladium,
    QMMPlatinum,
    QMMPlaster,
    QMMSilicon,
    QMMSilverFresnel,
    QMMSilver,
    QMMSteel,
    QMMTin,
    QMMTitanium,
    QMMTitaniumPolished,
    QMMZinc,
    QMMWallPaint,
    QMMCarbonSteelNew,
    QMMCarbonSteelWeathered,
    QMMStainlessSteel304,
    QMMStainlessSteel316,
    QMMHighAlloyStainlessSteel,
    QMMAlloySteel4140,
    QMMAlloySteel4340,
    QMMNickelVanadiumSteel,
    QMMManganeseSteel,
    QMMToolSteel,
    QMMSpringSteel,
    QMMStructuralSteel,
    QMMA36StructuralSteel,
    QMMA572StructuralSteel,
    QMMCaseHardenedSteelA,
    QMMCaseHardenedSteelB,
    QMMHSLASteel,
    QMMMaragingSteel,
    QMMFreeMachiningSteel,
    QMMGalvanizedSteel,
    QMMWeatheringSteel,
    QMMVirginWeatheringSteel,
    AnisotrophyXGroup,
    CanisotrophyGroup,
    EnergyConservationGroup,
    MetalFlakeGroup,
    PearlescentPigmentGroup,
    SpecularGroup,
    SteelRoughnessGroup,
    TexturizerGroup,
    UnevenRoughnessGroup,
    CopperColorsGroup,
    GoldColorsGroup,
    SilverColorsGroup,
    TitaniumColorsGroup,
]


def register():
    bpy.app.translations.register(__name__, langs)
    
    # Register all classes
    for cls in classes:
        bpy.utils.register_class(cls)
    
    # Register the PointerProperty on Scene AFTER class registration
    bpy.types.Scene.diffuse_bool = bpy.props.PointerProperty(type=QMMSettings)


def unregister():
    bpy.app.translations.unregister(__name__)
    
    # Remove the property first
    if hasattr(bpy.types.Scene, "diffuse_bool"):
        del bpy.types.Scene.diffuse_bool
    
    # Unregister all classes in reverse
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
