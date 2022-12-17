import bpy

# MESSAGE BOX
message_text = "This material already exists"


def ShowMessageBox(message="", title="", icon='INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)

# AluminiumShaderOperator


class QMMAluminium(bpy.types.Operator):
    """Add/Apply Aluminium Material to Selected Object (or Scene)"""
    bl_label = "QMM Aluminium Shader"
    bl_idname = 'shader.qmm_aluminium_operator'

    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        if m_aluminium := bpy.data.materials.get("QMM Aluminium"):
            ShowMessageBox(message_text, "QMM Aluminium")
            # print(f"QMM Aluminium already exists")
            bpy.context.object.active_material = m_aluminium
            return {'FINISHED'}
        else:
            self.make_shader()
        return {'FINISHED'}

    def make_shader(self):
        # CreateShader
        m_aluminium = bpy.data.materials.new(name="QMM Aluminium")
        m_aluminium.use_nodes = True
        m_aluminium.diffuse_color = (0.912, 0.914, 0.920, 1)
        m_aluminium.metallic = 1
        m_aluminium.roughness = 0.4

        nodes = m_aluminium.node_tree.nodes

        # materialoutput
        material_output = nodes.get('Material Output')
        material_output.location = (0, 0)

        # princibledbsdf
        BSDF = nodes.get('Principled BSDF')
        BSDF.location = (-300, 0)
        BSDF.inputs[0].default_value = (0.912, 0.914, 0.920, 1)
        BSDF.inputs[6].default_value = 1
        BSDF.inputs[9].default_value = 0.4
        BSDF.inputs[16].default_value = 1.244

        # EnergyConservationGroup
        bpy.ops.node.ec_group_operator()
        ec_group = nodes.new("ShaderNodeGroup")
        ec_group.name = "Energy Conservation"
        ec_group.node_tree = bpy.data.node_groups['Energy Conservation']
        ec_group.location = (-500, -200)
        ec_group.inputs[0].default_value = 1.244
        ec_group.inputs[1].default_value = (0.912, 0.914, 0.920, 1)
        ec_group.inputs[2].default_value = (0.970, 0.979, 0.988, 1)

        links = m_aluminium.node_tree.links.new

        links(ec_group.outputs[0], BSDF.inputs[0])
        links(ec_group.outputs[1], BSDF.inputs[7])
        links(ec_group.outputs[3], BSDF.inputs[16])

        # LOAD THE MATERIAL
        bpy.context.object.active_material = m_aluminium
