import bpy
import time


metal_values = [
    # {'dict_name': ['material_name', 'String Name', (color), roughness_min, roughness_max]},
    {'carbon_steel_new': ['m_carbon_steel_new', 'QMM Carbon Steel New', (0.351530, 0.351533, 0.396755, 1), 0.2, 0.4]},                                # 00
    {'carbon_steel_weathered': ['m_carbon_steel_weathered', 'QMM Carbon Steel Weathered', (0.074213, 0.074214, 0.078187, 1), 0.5, 0.8]},              # 01
    {'stainless_steel_304': ['m_stainless_steel_304', 'QMM 304 Common Stainless Steel', (0.651402, 0.651406, 0.651406, 1), 0.25, 0.35]},                # 02
    {'stainless_steel_316': ['m_stainless_steel_316', 'QMM 316 High-Chromium Stainless Steel', (0.745399, 0.745405, 0.791298, 1), 0.00, 0.04]},       # 03
    {'alloy_steel_4140': ['m_alloy_steel_4140', 'QMM 4140 Alloy Steel', (0.215859, 0.215861, 0.215861, 1), 0.2, 0.3]},                                # 04
    {'alloy_steel_4340': ['m_alloy_steel_4340', 'QMM 4340 Alloy Steel', (0.351530, 0.351533, 0.396755, 1), 0.4, 0.5]},                                # 05
    {'case_hardened_steel_a': ['m_case_hardened_steel_a', 'QMM Case-Hardened Steel A', (0.054480, 0.049707, 0.048172, 1), 0.2, 0.3]},                 # 06
    {'case_hardened_steel_b': ['m_case_hardened_steel_b', 'QMM Case-Hardened Steel B', (0.102241, 0.090842, 0.074214, 1), 0.4, 0.5]},                 # 07
    {'manganese_steel': ['m_manganese_steel', 'QMM Manganese Steel', (0.162028, 0.162030, 0.162029, 1), 0.5, 0.7]},                                   # 08
    {'tool_steel': ['m_tool_steel', 'QMM Tool Steel', (0.056128, 0.061246, 0.070360, 1), 0.3, 0.5]},                                                  # 09
    {'spring_steel': ['m_spring_steel', 'QMM Spring Steel', (0.215859, 0.215861, 0.215861, 1), 0.3, 0.5]},                                            # 10
    {'structural_steel': ['m_structural_steel', 'QMM Structural Steel', (0.155925, 0.155927, 0.155927, 1), 0.2, 0.4]},                                # 11
    {'a36_structural_steel': ['m_a36_structural_steel', 'QMM A36 Structural Steel', (0.212229, 0.212231, 0.212231, 1), 0.2, 0.4]},                    # 12
    {'a572_structural_steel': ['m_a572_structural_steel', 'QMM A572 Structural Steel', (0.165131, 0.165132, 0.165132, 1), 0.2, 0.4]},                 # 13
    {'hsla_steel': ['m_hsla_steel', 'QMM HSLA Steel', (0.223227, 0.223228, 0.223228, 1), 0.2, 0.4]},                                                  # 14
    {'maraging_steel': ['m_maraging_steel', 'QMM Maraging Steel', (0.152925, 0.152926, 0.152926, 1), 0.2, 0.4]},                                      # 15
    {'virgin_weathering_steel': ['m_virgin_weathering_steel', 'QMM Virgin Weathering Steel', (0.230739, 0.230740, 0.230740, 1), 0.2, 0.4]},           # 16
    {'free_machining_steel': ['m_free_machining_steel', 'QMM Free-Machining Steel', (0.262249, 0.262251, 0.262251, 1), 0.3, 0.5]},                    # 17
    {'galvanized_steel': ['m_galvanized_steel', 'QMM Galvanized Steel', (0.651402, 0.651406, 0.651406, 1), 0.3, 0.5]},                                # 18
    {'nickel_vanadium_steel': ['m_nickel_vanadium_steel', 'QMM Nickel-Vanadium Steel', (0.341912, 0.341915, 0.341915, 1), 0.4, 0.6]},                 # 19
    {'high_alloy_stainless_steel': ['m_high_alloy_stainless_steel', 'QMM High-Alloy Stainless Steel', (0.527112, 0.527116, 0.527115, 1), 0.2, 0.4]},  # 20
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
        # #ShowMessageBox(message_text, unit_value[1])
        bpy.context.object.active_material = m_name
        diffuse_bool = bpy.context.scene.diffuse_bool.diffuse_more
        m_name.diffuse_color = unit_value[2] if diffuse_bool else (0.8, 0.8, 0.8, 1)
        m_name.metallic = 1 if diffuse_bool else 0
        m_name.roughness = unit_value[3] if diffuse_bool else 0.4
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
    diffuse_bool = bpy.context.scene.diffuse_bool.diffuse_more
    if diffuse_bool == True:
        unit_value[0].diffuse_color = unit_value[2]
        unit_value[0].metallic = 1
        unit_value[0].roughness = unit_value[3]

    nodes = unit_value[0].node_tree.nodes

    # materialoutput
    m_output = next((n for n in nodes if n.bl_idname == 'ShaderNodeOutputMaterial'), None)
    if m_output:
        m_output.location = (0, 0)

    # princibledbsdf
    BSDF = next((n for n in nodes if n.bl_idname == 'ShaderNodeBsdfPrincipled'), None)
    if BSDF:
        BSDF.distribution = 'MULTI_GGX'
        BSDF.location = (-300, 0)
        BSDF.inputs[0].default_value = unit_value[2]
        if bpy.app.version < (4, 0, 0):
            BSDF.inputs[6].default_value = 1              # Metallic
            BSDF.inputs[9].default_value = unit_value[3]  # Roughness
            BSDF.inputs[16].default_value = 2.5           # IOR
        else:
            BSDF.inputs[1].default_value = 1              # Metallic
            BSDF.inputs[2].default_value = unit_value[3]  # Roughness
            BSDF.inputs[3].default_value = 2.5            # IOR

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

    if units == 18:
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
    bl_label = "QMM Carbon Steel New"
    bl_idname = 'shader.qmm_carbon_steel_new_operator'

    def execute(self, context):
        make_steel(0)
        return {'FINISHED'}


class QMMCarbonSteelWeathered(bpy.types.Operator):
    """Add/Apply Carbon Steel Weathered Material to Selected Object (or Scene)"""
    bl_label = "QMM Carbon Steel Weathered"
    bl_idname = 'shader.qmm_carbon_steel_weathered_operator'

    def execute(self, context):
        make_steel(1)
        return {'FINISHED'}


class QMMStainlessSteel304(bpy.types.Operator):
    """Add/Apply Stainless Steel 304 Material to Selected Object (or Scene)"""
    bl_label = "QMM 304 Common Stainless Steel"
    bl_idname = 'shader.qmm_stainless_steel_304_operator'

    def execute(self, context):
        make_steel(2)
        return {'FINISHED'}


class QMMStainlessSteel316(bpy.types.Operator):
    """Add/Apply Stainless Steel 316 Material to Selected Object (or Scene)"""
    bl_label = "QMM 316 High-Chromium Stainless Steel"
    bl_idname = 'shader.qmm_stainless_steel_316_operator'

    def execute(self, context):
        make_steel(3)
        return {'FINISHED'}


class QMMAlloySteel4140(bpy.types.Operator):
    """Add/Apply Alloy Steel 4140 Material to Selected Object (or Scene)"""
    bl_label = "QMM 4140 Alloy Steel (Cr-Mo)"
    bl_idname = 'shader.qmm_alloy_steel_4140_operator'

    def execute(self, context):
        make_steel(4)
        return {'FINISHED'}


class QMMAlloySteel4340(bpy.types.Operator):
    """Add/Apply Alloy Steel 4340 Material to Selected Object (or Scene)"""
    bl_label = "QMM 4340 Alloy Steel (Ni-Cr-Mo)"
    bl_idname = 'shader.qmm_alloy_steel_4340_operator'

    def execute(self, context):
        make_steel(5)
        return {'FINISHED'}


class QMMCaseHardenedSteelA(bpy.types.Operator):
    """Add/Apply Case-Hardened Steel A Material to Selected Object (or Scene)"""
    bl_label = "QMM Case-Hardened Steel A"
    bl_idname = 'shader.qmm_case_hardened_steel_a_operator'

    def execute(self, context):
        make_steel(6)
        return {'FINISHED'}


class QMMCaseHardenedSteelB(bpy.types.Operator):
    """Add/Apply Case-Hardened Steel B Material to Selected Object (or Scene)"""
    bl_label = "QMM Case-Hardened Steel B"
    bl_idname = 'shader.qmm_case_hardened_steel_b_operator'

    def execute(self, context):
        make_steel(7)
        return {'FINISHED'}


class QMMManganeseSteel(bpy.types.Operator):
    """Add/Apply Manganese Steel Material to Selected Object (or Scene)"""
    bl_label = "QMM Manganese Steel"
    bl_idname = 'shader.qmm_manganese_steel_operator'

    def execute(self, context):
        make_steel(8)
        return {'FINISHED'}


class QMMToolSteel(bpy.types.Operator):
    """Add/Apply Tool Steel Material to Selected Object (or Scene)"""
    bl_label = "QMM Tool Steel"
    bl_idname = 'shader.qmm_tool_steel_operator'

    def execute(self, context):
        make_steel(9)
        return {'FINISHED'}


class QMMSpringSteel(bpy.types.Operator):
    """Add/Apply Spring Steel Material to Selected Object (or Scene)"""
    bl_label = "QMM Spring Steel"
    bl_idname = 'shader.qmm_spring_steel_operator'

    def execute(self, context):
        make_steel(10)
        return {'FINISHED'}


class QMMStructuralSteel(bpy.types.Operator):
    """Add/Apply Structural Steel Material to Selected Object (or Scene)"""
    bl_label = "QMM Structural Steel"
    bl_idname = 'shader.qmm_structural_steel_operator'

    def execute(self, context):
        make_steel(11)
        return {'FINISHED'}


class QMMA36StructuralSteel(bpy.types.Operator):
    """Add/Apply A36 Structural Steel Material to Selected Object (or Scene)"""
    bl_label = "QMM A36 Structural Steel"
    bl_idname = 'shader.qmm_a36_structural_steel_operator'

    def execute(self, context):
        make_steel(12)
        return {'FINISHED'}


class QMMA572StructuralSteel(bpy.types.Operator):
    """Add/Apply A572 Structural Steel Material to Selected Object (or Scene)"""
    bl_label = "QMM A572 Structural Steel"
    bl_idname = 'shader.qmm_a572_structural_steel_operator'

    def execute(self, context):
        make_steel(13)
        return {'FINISHED'}


class QMMHSLASteel(bpy.types.Operator):
    """Add/Apply HSLA Steel Material to Selected Object (or Scene)"""
    bl_label = "QMM HSLA Steel"
    bl_idname = 'shader.qmm_hsla_steel_operator'

    def execute(self, context):
        make_steel(14)
        return {'FINISHED'}


class QMMMaragingSteel(bpy.types.Operator):
    """Add/Apply Maraging Steel Material to Selected Object (or Scene)"""
    bl_label = "QMM Maraging Steel"
    bl_idname = 'shader.qmm_maraging_steel_operator'

    def execute(self, context):
        make_steel(15)
        return {'FINISHED'}


class QMMVirginWeatheringSteel(bpy.types.Operator):
    """Add/Apply Virgin Weathering Steel Material to Selected Object (or Scene)"""
    bl_label = "QMM Virgin Weathering Steel"
    bl_idname = 'shader.qmm_virgin_weathering_steel_operator'

    def execute(self, context):
        make_steel(16)
        return {'FINISHED'}


class QMMFreeMachiningSteel(bpy.types.Operator):
    """Add/Apply Free-Machining Steel Material to Selected Object (or Scene)"""
    bl_label = "QMM Free-Machining Steel"
    bl_idname = 'shader.qmm_free_machining_steel_operator'

    def execute(self, context):
        make_steel(17)
        return {'FINISHED'}


class QMMGalvanizedSteel(bpy.types.Operator):
    """Add/Apply Galvanized Steel Material to Selected Object (or Scene)"""
    bl_label = "QMM Galvanized Steel"
    bl_idname = 'shader.qmm_galvanized_steel_operator'

    def execute(self, context):
        make_steel(18)
        return {'FINISHED'}


class QMMNickelVanadiumSteel(bpy.types.Operator):
    """Add/Apply Nickel-Vanadium Steel Material to Selected Object (or Scene)"""
    bl_label = "QMM Nickel-Vanadium Steel"
    bl_idname = 'shader.qmm_nickel_vanadium_steel_operator'

    def execute(self, context):
        make_steel(19)
        return {'FINISHED'}


class QMMHighAlloyStainlessSteel(bpy.types.Operator):
    """Add/Apply High-Alloy Stainless Steel Material to Selected Object (or Scene)"""
    bl_label = "QMM High-Alloy Stainless Steel"
    bl_idname = 'shader.qmm_high_alloy_stainless_steel_operator'

    def execute(self, context):
        make_steel(20)
        return {'FINISHED'}


class QMMWeatheringSteel(bpy.types.Operator):
    """Add/Apply Weathering Steel Material to Selected Object (or Scene)"""
    bl_label = "QMM Weathering Steel"
    bl_idname = 'shader.qmm_weathering_steel_operator'

    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        if m_weathering_steel := bpy.data.materials.get("QMM Weathering Steel"):
            #ShowMessageBox(message_text, "QMM Weathering Steel")
            # print(f"QMM Weathering Steel already exists")
            bpy.context.object.active_material = m_weathering_steel
            diffuse_bool = bpy.context.scene.diffuse_bool.diffuse_more
            m_weathering_steel.diffuse_color = (0.351531, 0.084376, 0.026241, 1) if diffuse_bool else (0.8, 0.8, 0.8, 1)
            m_weathering_steel.metallic = 1 if diffuse_bool else 0
            m_weathering_steel.roughness = 0.7 if diffuse_bool else 0.4
            return {'FINISHED'}
        else:
            self.make_shader()
        return {'FINISHED'}

    def make_shader(self):
        start = time.time()

        # CreateShader
        m_weathering_steel = bpy.data.materials.new(name="QMM Weathering Steel")
        m_weathering_steel.use_nodes = True
        diffuse_bool = bpy.context.scene.diffuse_bool.diffuse_more
        if diffuse_bool == True:
            m_weathering_steel.diffuse_color = (0.351531, 0.084376, 0.026241, 1)
            m_weathering_steel.roughness = 0.7
            m_weathering_steel.metallic = 1

        nodes = m_weathering_steel.node_tree.nodes

        # materialoutput
        material_output = next((n for n in nodes if n.bl_idname == 'ShaderNodeOutputMaterial'), None)
        if material_output:
            material_output.location = (0, 0)

        # principledbsdf
        BSDF = next((n for n in nodes if n.bl_idname == 'ShaderNodeBsdfPrincipled'), None)
        if BSDF:
            BSDF.distribution = 'MULTI_GGX'
            BSDF.location = (-300, 0)
            BSDF.inputs[0].default_value = (0.351531, 0.084376, 0.026241, 1)
            if bpy.app.version < (4, 0, 0):
                BSDF.inputs[6].default_value = 1                    #Metallic
                BSDF.inputs[9].default_value = 0.7                  #Roughness
            else:
                BSDF.inputs[1].default_value = 1                    #Metallic
                BSDF.inputs[2].default_value = 0.7                  #Roughness
            # BSDF.select = True

        # colorramp
        m_colorramp = nodes.new("ShaderNodeValToRGB")
        m_colorramp.location = (-600, 0)
        m_colorramp.color_ramp.interpolation = 'EASE'
        # Ensure there are enough elements in the color ramp
        while len(m_colorramp.color_ramp.elements) < 3:
            m_colorramp.color_ramp.elements.new(0.0)
        m_colorramp.color_ramp.elements[0].color = (0.564709, 0.201556, 0.149960, 1)
        m_colorramp.color_ramp.elements[0].position = 0
        m_colorramp.color_ramp.elements[1].color = (0.351531, 0.084376, 0.026241, 1)
        m_colorramp.color_ramp.elements[1].position = 0.333
        m_colorramp.color_ramp.elements[2].color = (0.158960, 0.076185, 0.045186, 1)
        m_colorramp.color_ramp.elements[2].position = 1

        # Uneven Roughness Group
        bpy.ops.node.uneven_roughness_group_operator()
        ur_group = nodes.new("ShaderNodeGroup")
        ur_group.name = "Uneven Roughness"
        ur_group.node_tree = bpy.data.node_groups['Uneven Roughness']
        ur_group.location = (-800, -100)
        ur_group.width = 140
        ur_group.inputs[0].default_value = 0.5
        ur_group.inputs[1].default_value = 0.9
        ur_group.inputs[2].default_value = 4
        ur_group.inputs[3].default_value = 0.5

        links = m_weathering_steel.node_tree.links.new

        links(m_colorramp.outputs[0], BSDF.inputs[0])
        if bpy.app.version < (4, 0, 0):
            links(ur_group.outputs[0], BSDF.inputs[9])
        else:
            links(ur_group.outputs[0], BSDF.inputs[2])
        links(ur_group.outputs[1], m_colorramp.inputs[0])

        bpy.context.object.active_material = m_weathering_steel

        end = time.time()
        print(f"QMM Weathering Steel: {end - start} seconds")
