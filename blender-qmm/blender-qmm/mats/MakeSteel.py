import bpy
import time


metal_values = [
    # {'dict_name': ['material_name', 'String Name', (color), roughness_min, roughness_max]},
    {'carbon_steel_new': ['m_carbon_steel_new', 'QMM Carbon Steel New', (0.351530, 0.351533, 0.396755, 1), 0.5, 0.8]},                              # 00
    {'carbon_steel_weathered': ['m_carbon_steel_weathered', 'QMM Carbon Steel Weathered', (0.074213, 0.074214, 0.078187, 1), 0.5, 0.8]},            # 01
    {'stainless_steel_304': ['m_stainless_steel_304', 'QMM 304 Common Stainless Steel', (0.651402, 0.651406, 0.651406, 1), 0.1, 0.3]},              # 02
    {'stainless_steel_316': ['m_stainless_steel_316', 'QMM 316 High-Chromium Stainless Steel', (0.745399, 0.745405, 0.791298, 1), 0.05, 0.25]},     # 03
    {'alloy_steel_4140': ['m_alloy_steel_4140', 'QMM 4140 Alloy Steel (Cr-Mo)', (0.215859, 0.215861, 0.215861, 1), 0.2, 0.3]},                      # 04
    {'alloy_steel_4340': ['m_alloy_steel_4340', 'QMM 4340 Alloy Steel (Ni-Cr-Mo)', (0.351530, 0.351533, 0.396755, 1), 0.4, 0.5]},                    # 05
    {'manganese_steel': ['m_manganese_steel', 'QMM Manganese Steel', (0.162028, 0.162030, 0.162029, 1), 0.5, 0.7]},                                 # 06
    {'galvanized_steel': ['m_galvanized_steel', 'QMM Galvanized Steel', (0.651402, 0.651406, 0.651406, 1), 0.3, 0.5]},                              # 07
]


# MESSAGE BOX
message_text = "This material already exists"


def ShowMessageBox(message="", title="", icon='INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)


def make_steel(units):
    start = time.time()

    uv_dict = metal_values[units]
    unit_key = list(uv_dict.keys())[0]
    unit_value = uv_dict[unit_key]
    m_name = unit_value[0]

    # DOES THE MATERIAL ALREADY EXIST?
    if m_name := bpy.data.materials.get(unit_value[1]):
        ShowMessageBox(message_text, unit_value[1])
        bpy.context.object.active_material = m_name
        return {'FINISHED'}
    else:
        make_shader(units)

    end = time.time()
    print(f"{unit_value[1]}: {end - start} seconds")


def make_shader(units):
    uv_dict = metal_values[units]
    unit_key = list(uv_dict.keys())[0]
    unit_value = uv_dict[unit_key]

    # CreateShader
    unit_value[0] = bpy.data.materials.new(name=unit_value[1])
    unit_value[0].use_nodes = True
    unit_value[0].diffuse_color = unit_value[2]
    unit_value[0].metallic = 1
    unit_value[0].roughness = unit_value[3]

    nodes = unit_value[0].node_tree.nodes

    # materialoutput
    m_output = nodes.get('Material Output')
    m_output.location = (0, 0)

    # princibledbsdf
    BSDF = nodes.get('Principled BSDF')
    BSDF.distribution = 'MULTI_GGX'
    BSDF.location = (-300, 0)
    BSDF.inputs[0].default_value = unit_value[2]
    if bpy.app.version < (4, 0, 0):
        BSDF.inputs[6].default_value = 1              # Metallic
        BSDF.inputs[9].default_value = unit_value[3]  # Roughness
    else:
        BSDF.inputs[1].default_value = 1              # Metallic
        BSDF.inputs[2].default_value = unit_value[3]  # Roughness

    # Add Uneven Roughness Group
    bpy.ops.node.uneven_roughness_group_operator()
    ur_group = nodes.new("ShaderNodeGroup")
    ur_group.name = "Uneven Roughness"
    ur_group.node_tree = bpy.data.node_groups['Uneven Roughness']
    ur_group.location = (-500, 0)
    ur_group.width = 140
    ur_group.inputs[0].default_value = unit_value[3]
    ur_group.inputs[1].default_value = unit_value[4]
    ur_group.inputs[2].default_value = 12
    ur_group.inputs[3].default_value = 0.5

    links = unit_value[0].node_tree.links.new

    if bpy.app.version < (4, 0, 0):
        links(ur_group.outputs[0], BSDF.inputs[8])
    else:
        links(ur_group.outputs[0], BSDF.inputs[2])

    if units == 7:
        # Metal Flake Group
        bpy.ops.node.metal_flake_group_operator()
        mf_group = nodes.new("ShaderNodeGroup")
        mf_group.name = "Metal Flake"
        mf_group.node_tree = bpy.data.node_groups['Metal Flake']
        mf_group.location = (-500, -300)
        mf_group.width = 140
        mf_group.inputs[0].default_value = 3072
        mf_group.inputs[1].default_value = 0.25
        if bpy.app.version < (4, 0, 0):
            links(mf_group.outputs[0], BSDF.inputs[22])
        else:
            links(mf_group.outputs[0], BSDF.inputs[5])

    # LOAD THE MATERIAL
    bpy.context.object.active_material = unit_value[0]


class QMMCarbonSteelNew(bpy.types.Operator):
    """Add/Apply Carbon Steel New Material to Selected Object (or Scene)"""
    bl_label = "QMM Carbon Steel New Shader"
    bl_idname = 'shader.qmm_carbon_steel_new_operator'

    def execute(self, context):
        make_steel(0)
        return {'FINISHED'}


class QMMCarbonSteelWeathered(bpy.types.Operator):
    """Add/Apply Carbon Steel Weathered Material to Selected Object (or Scene)"""
    bl_label = "QMM Carbon Steel Weathered Shader"
    bl_idname = 'shader.qmm_carbon_steel_weathered_operator'

    def execute(self, context):
        make_steel(1)
        return {'FINISHED'}


class QMMStainlessSteel304(bpy.types.Operator):
    """Add/Apply Stainless Steel 304 Material to Selected Object (or Scene)"""
    bl_label = "QMM 304 Common Stainless Steel Shader"
    bl_idname = 'shader.qmm_stainless_steel_304_operator'

    def execute(self, context):
        make_steel(2)
        return {'FINISHED'}


class QMMStainlessSteel316(bpy.types.Operator):
    """Add/Apply Stainless Steel 316 Material to Selected Object (or Scene)"""
    bl_label = "QMM 316 High-Chromium Stainless Steel Shader"
    bl_idname = 'shader.qmm_stainless_steel_316_operator'

    def execute(self, context):
        make_steel(3)
        return {'FINISHED'}


class QMMAlloySteel4140(bpy.types.Operator):
    """Add/Apply Alloy Steel 4140 Material to Selected Object (or Scene)"""
    bl_label = "QMM 4140 Alloy Steel (Cr-Mo) Shader"
    bl_idname = 'shader.qmm_alloy_steel_4140_operator'

    def execute(self, context):
        make_steel(4)
        return {'FINISHED'}


class QMMAlloySteel4340(bpy.types.Operator):
    """Add/Apply Alloy Steel 4340 Material to Selected Object (or Scene)"""
    bl_label = "QMM 4340 Alloy Steel (Ni-Cr-Mo) Shader"
    bl_idname = 'shader.qmm_alloy_steel_4340_operator'

    def execute(self, context):
        make_steel(5)
        return {'FINISHED'}


class QMMManganeseSteel(bpy.types.Operator):
    """Add/Apply Manganese Steel Material to Selected Object (or Scene)"""
    bl_label = "QMM Manganese Steel Shader"
    bl_idname = 'shader.qmm_manganese_steel_operator'

    def execute(self, context):
        make_steel(6)
        return {'FINISHED'}


class QMMGalvanizedSteel(bpy.types.Operator):
    """Add/Apply Galvanized Steel Material to Selected Object (or Scene)"""
    bl_label = "QMM Galvanized Steel Shader"
    bl_idname = 'shader.qmm_galvanized_steel_operator'

    def execute(self, context):
        make_steel(7)
        return {'FINISHED'}
