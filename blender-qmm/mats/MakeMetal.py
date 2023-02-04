import bpy
import time 


metal_values = [
    {'palladium': ['m_palladium', 'QMM Palladium', (0.734139, 0.698362, 0.650909, 1), 0.075, 1.76, (1.468314, 1.447085, 1.390112, 1)]},
    {'platinum': ['m_platinum', 'QMM Platinum', (0.679542, 0.644479, 0.590619, 1), 0.075, 1.79, (1.707216, 1.630868, 1.566421, 1)]},
    {'aluminium': ['m_aluminium', 'QMM Aluminium', (0.913098, 0.913098, 0.921582, 1), 0.2, 1.62, (1.216499, 1.169372, 1.112043, 1)]},
    {'iron': ['m_iron', 'QMM Iron', (0.533276, 0.514917, 0.496933, 1), 0.3, 2.03, (2.151289, 2.202939, 1.956144, 1)]},
    {'lead': ['m_lead', 'QMM Lead', (0.630757, 0.623960, 0.637597, 1), 0.3, 1.87, (1.572684, 1.547365, 1.409525, 1)]},
    {'lead_rough': ['m_lead_rough', 'QMM Lead Rough', (0.186, 0.188, 0.196, 1), 0.4, 1.87, (0.99, 0.99, 0.99, 1)]},
    {'nickel': ['m_nickel', 'QMM Nickel', (0.651405, 0.610495, 0.539480, 1.000000), 0.3, 1.63, (1.553379, 1.569627, 1.535934, 1)]},
    {'titanium_polished': ['m_titanium_polished', 'QMM Titanium Polished', (0.617206, 0.584078, 0.545725, 1), 0.15, 2.42, (1.939808, 1.880272, 1.764035, 1)]},
    {'zinc': ['m_zinc', 'QMM Zinc', (0.871366, 0.863156, 0.854993, 1), 0.3, 1.7, (1.241139, 1.193442, 1.147981, 1)]},
    {'brass': ['m_brass', 'QMM Brass', (0.887922, 0.791297, 0.434154, 1), 0.2, 1.45, (1.098669, 1.133579, 1.391092, 1)]},
    {'bronze': ['m_bronze', 'QMM Bronze', (0.434154, 0.266356, 0.0953075, 1), 0.33, 1.45, (0.651405, 0.577580, 0.514918, 1)]},
    {'chromium': ['m_chromium', 'QMM Chromium', (0.655879, 0.681365, 0.698525, 1), 0.075, 1.5, (2.809509, 2.227482, 1.634533, 1)]},
    {'steel': ['m_steel', 'QMM Steel', (0.42869, 0.527115, 0.590619, 1), 0.3, 2.0, (0.99, 0.99, 0.99, 1)]},
    {'mercury': ['m_mercury', 'QMM Mercury', (0.783537, 0.775822, 0.775822, 1), 0.025, 1.744, (1.500116, 1.375106, 1.247637, 1)]},
    {'silicon': ['m_silicon', 'QMM Silicon', (0.345218, 0.3668, 0.43018, 1), 0.1, 1.45, (3.630057, 4.022775, 5.870442, 1)]},
]


# MESSAGE BOX
message_text = "This material already exists"


def ShowMessageBox(message="", title="", icon='INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)


def make_metal(units):
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
    BSDF.inputs[6].default_value = 1
    BSDF.inputs[9].default_value = unit_value[3]
    # BSDF.inputs[16].default_value = unit_value[4]

    # EnergyConservationGroup
    bpy.ops.node.ec_group_operator()
    ec_group = nodes.new("ShaderNodeGroup")
    ec_group.name = "Energy Conservation v5"
    ec_group.node_tree = bpy.data.node_groups['Energy Conservation v5']
    ec_group.location = (-500, -200)
    ec_group.inputs[0].default_value = unit_value[2]
    ec_group.inputs[1].default_value = unit_value[3]
    # ec_group.inputs[2].default_value = unit_value[4]
    ec_group.inputs[4].default_value = unit_value[5]

    links = unit_value[0].node_tree.links.new

    links(ec_group.outputs[0], BSDF.inputs[0])
    links(ec_group.outputs[1], BSDF.inputs[7])
    links(ec_group.outputs[2], BSDF.inputs[9])
    links(ec_group.outputs[4], BSDF.inputs[16])

    # LOAD THE MATERIAL
    bpy.context.object.active_material = unit_value[0]


class QMMPalladium(bpy.types.Operator):
    """Add/Apply Palladium Material to Selected Object (or Scene)"""
    bl_label  = "QMM Palladium Shader"
    bl_idname = 'shader.qmm_palladium_operator'

    def execute(self, context):
        make_metal(0)
        return {'FINISHED'}


class QMMPlatinum(bpy.types.Operator):
    """Add/Apply Platinum Material to Selected Object (or Scene)"""
    bl_label  = "QMM Platinum Shader"
    bl_idname = 'shader.qmm_platinum_operator'

    def execute(self, context):
        make_metal(1)
        return {'FINISHED'}


class QMMAluminium(bpy.types.Operator):
    """Add/Apply Aluminium Material to Selected Object (or Scene)"""
    bl_label  = "QMM Aluminium Shader"
    bl_idname = 'shader.qmm_aluminium_operator'

    def execute(self, context):
        make_metal(2)
        return {'FINISHED'}


class QMMIron(bpy.types.Operator):
    """Add/Apply Iron Material to Selected Object (or Scene)"""
    bl_label  = "QMM Iron Shader"
    bl_idname = 'shader.qmm_iron_operator'

    def execute(self, context):
        make_metal(3)
        return {'FINISHED'}


class QMMLead(bpy.types.Operator):
    """Add/Apply Lead Material to Selected Object (or Scene)"""
    bl_label  = "QMM Lead Shader"
    bl_idname = 'shader.qmm_lead_operator'

    def execute(self, context):
        make_metal(4)
        return {'FINISHED'}


class QMMLeadRough(bpy.types.Operator):
    """Add/Apply Lead Rough Material to Selected Object (or Scene)"""
    bl_label  = "QMM Lead Rough Shader"
    bl_idname = 'shader.qmm_lead_rough_operator'

    def execute(self, context):
        make_metal(5)
        return {'FINISHED'}


class QMMNickel(bpy.types.Operator):
    """Add/Apply Nickel Material to Selected Object (or Scene)"""
    bl_label  = "QMM Nickel Shader"
    bl_idname = 'shader.qmm_nickel_operator'

    def execute(self, context):
        make_metal(6)
        return {'FINISHED'}


class QMMTitaniumPolished(bpy.types.Operator):
    """Add/Apply Titanium Polished Material to Selected Object (or Scene)"""
    bl_label  = "QMM Titanium Polished Shader"
    bl_idname = 'shader.qmm_titanium_p_operator'

    def execute(self, context):
        make_metal(7)
        return {'FINISHED'}


class QMMZinc(bpy.types.Operator):
    """Add/Apply Zinc Material to Selected Object (or Scene)"""
    bl_label  = "QMM Zinc Shader"
    bl_idname = 'shader.qmm_zinc_operator'

    def execute(self, context):
        make_metal(8)
        return {'FINISHED'}


class QMMBrass(bpy.types.Operator):
    """Add/Apply Brass Material to Selected Object (or Scene)"""
    bl_label  = "QMM Brass Shader"
    bl_idname = 'shader.qmm_brass_operator'

    def execute(self, context):
        make_metal(9)
        return {'FINISHED'}


class QMMBronze(bpy.types.Operator):
    """Add/Apply Bronze Material to Selected Object (or Scene)"""
    bl_label  = "QMM Bronze Shader"
    bl_idname = 'shader.qmm_bronze_operator'

    def execute(self, context):
        make_metal(10)
        return {'FINISHED'}


class QMMChromium(bpy.types.Operator):
    """Add/Apply Chromium Material to Selected Object (or Scene)"""
    bl_label  = "QMM Chromium Shader"
    bl_idname = 'shader.qmm_chromium_operator'

    def execute(self, context):
        make_metal(11)
        return {'FINISHED'}


class QMMSteel(bpy.types.Operator):
    """Add/Apply Steel Material to Selected Object (or Scene)"""
    bl_label  = "QMM Steel Shader"
    bl_idname = 'shader.qmm_steel_operator'

    def execute(self, context):
        make_metal(12)
        return {'FINISHED'}


class QMMMercury(bpy.types.Operator):
    """Add/Apply Mercury Material to Selected Object (or Scene)"""
    bl_label  = "QMM Mercury Shader"
    bl_idname = 'shader.qmm_mercury_operator'

    def execute(self, context):
        make_metal(13)
        return {'FINISHED'}


class QMMSilicon(bpy.types.Operator):
    """Add/Apply Silicon Material to Selected Object (or Scene)"""
    bl_label  = "QMM Silicon Shader"
    bl_idname = 'shader.qmm_silicon_operator'

    def execute(self, context):
        make_metal(14)
        return {'FINISHED'}
