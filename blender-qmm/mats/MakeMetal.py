import bpy
import time 


metal_values = [
    {'palladium': ['m_palladium', 'QMM Palladium', (0.417885, 0.366252, 0.300544, 1), 0.075, 1.76, (0.930110, 0.947306, 0.964686, 1)]},
    {'platinum': ['m_platinum', 'QMM Platinum', (0.417885, 0.366252, 0.300544, 1), 0.075, 1.79, (0.577580, 0.584078, 0.571125, 1)]},
    {'aluminium': ['m_aluminium', 'QMM Aluminium', (0.806951, 0.814846, 0.822786, 1), 0.35, 1.62, (0.930110, 0.947306, 0.964686, 1)]},
    {'iron': ['m_iron', 'QMM Iron', (0.230740, 0.223228, 0.208637, 1), 0.5, 2.03, (0.283148, 0.250158, 0.300544, 1)]},
    {'lead': ['m_lead', 'QMM Lead', (0.658374, 0.665387, 0.693872, 1), 0.35, 1.87, (0.803, 0.808, 0.862, 1)]},
    {'lead_rough': ['m_lead_rough', 'QMM Lead_Rough', (0.186, 0.188, 0.196, 1), 0.5, 1.87, (0.99, 0.99, 0.99, 1)]},
    {'nickel': ['m_nickel', 'QMM Nickel', (0.376262, 0.327778, 0.250158, 1), 0.350, 1.63, (0.597201, 0.603827, 0.584079, 1)]},
    {'titanium_polished': ['m_titanium_polished', 'QMM Titanium_Polished', (0.337163, 0.296138, 0.254152, 1), 0.35, 2.42, (0.428690, 0.423267, 0.428690, 1)]},
    {'zinc': ['m_zinc', 'QMM Zinc', (0.737911, 0.723055, 0.701102, 1), 0.35, 1.7, (0.913098, 0.930110, 0.947306, 1)]},
    {'brass': ['m_brass', 'QMM Brass', (0.760524, 0.584078, 0.158961, 1), 0.35, 1.45, (0.973444, 0.947306, 0.679543, 1)]},
    {'bronze': ['m_bronze', 'QMM Bronze', (0.434154, 0.266356, 0.0953075, 1), 0.35, 1.45, (0.651405, 0.577580, 0.514918, 1)]},
    {'chrome': ['m_chrome', 'QMM Chrome', (0.262250, 0.266355, 0.266356, 1), 0.075, 1.5, (0.283148, 0.270498, 0.428690, 1)]},
    {'steel': ['m_steel', 'QMM Steel', (0.42869, 0.527115, 0.590619, 1), 0.3, 2.0, (0.99, 0.99, 0.99, 1)]},
    {'mercury': ['m_mercury', 'QMM Mercury', (0.781, 0.779, 0.779, 1), 0.075, 1.744, (0.879, 0.910, 0.941, 1)]},
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
    BSDF.inputs[16].default_value = unit_value[4]

    # EnergyConservationGroup
    bpy.ops.node.ec_group_operator()
    ec_group = nodes.new("ShaderNodeGroup")
    ec_group.name = "Energy Conservation v5"
    ec_group.node_tree = bpy.data.node_groups['Energy Conservation v5']
    ec_group.location = (-500, -200)
    ec_group.inputs[0].default_value = unit_value[2]
    ec_group.inputs[1].default_value = unit_value[3]
    ec_group.inputs[2].default_value = unit_value[4]
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


class QMMChrome(bpy.types.Operator):
    """Add/Apply Chrome Material to Selected Object (or Scene)"""
    bl_label  = "QMM Chrome Shader"
    bl_idname = 'shader.qmm_chrome_operator'

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
