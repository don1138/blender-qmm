import bpy

# MESSAGE BOX
message_text = "This material already exists"


def ShowMessageBox(message="", title="", icon='INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)

# CinnabarShaderOperator


class QMMCinnabar(bpy.types.Operator):
    """Add/Apply Cinnabar Material to Selected Object (or Scene)"""
    bl_label = "QMM Cinnabar Shader"
    bl_idname = 'shader.qmm_cinnabar_operator'

    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        if m_cinnabar := bpy.data.materials.get("QMM Cinnabar"):
            ShowMessageBox(message_text, "QMM Cinnabar")
            # print(f"QMM Cinnabar already exists")
            bpy.context.object.active_material = m_cinnabar
            return {'FINISHED'}
        else:
            self.make_shader()
        return {'FINISHED'}

    def make_shader(self):
        # CreateShader
        m_cinnabar = bpy.data.materials.new(name="QMM Cinnabar")
        m_cinnabar.use_nodes = True
        m_cinnabar.diffuse_color = (0.768151, 0.054480, 0.034340, 1)
        m_cinnabar.metallic = 1
        m_cinnabar.roughness = 0.6

        nodes = m_cinnabar.node_tree.nodes

        # materialoutput
        material_output = nodes.get('Material Output')
        material_output.location = (0, 0)

        # princibledbsdf
        BSDF = nodes.get('Principled BSDF')
        BSDF.location = (-300, 0)
        BSDF.inputs[0].default_value = (0.768151, 0.054480, 0.034340, 1)
        BSDF.inputs[6].default_value = 1
        BSDF.inputs[9].default_value = 0.4
        BSDF.inputs[16].default_value = 3.02

        # colorramp
        m_colorramp = nodes.new('ShaderNodeValToRGB')
        m_colorramp.label = "Cinnabar"
        m_colorramp.location = (-800, -200)
        m_colorramp.color_ramp.elements[0].color = (
            0.768151, 0.054480, 0.034340, 1)
        m_colorramp.color_ramp.elements[1].color = (
            0.283149, 0.039546, 0.031896, 1)
        m_colorramp.color_ramp.elements[0].position = 0.2
        m_colorramp.color_ramp.elements[1].position = 0.6

        # colorrampvermillion
        m_colorramp2 = nodes.new('ShaderNodeValToRGB')
        m_colorramp2.label = "Vermillion"
        m_colorramp2.location = (-800, 100)
        m_colorramp2.color_ramp.elements[0].color = (
            0.964687, 0.066626, 0.002428, 1)
        m_colorramp2.color_ramp.elements[1].color = (
            0.473532, 0.152926, 0.001518, 1)
        m_colorramp2.color_ramp.elements[0].position = 0.2
        m_colorramp2.color_ramp.elements[1].position = 0.6

        nodes = m_cinnabar.node_tree.nodes

        # EnergyConservationGroup
        bpy.ops.node.ec_group_operator()
        ec_group = nodes.new("ShaderNodeGroup")
        ec_group.name = "Energy Conservation"
        ec_group.node_tree = bpy.data.node_groups['Energy Conservation']
        ec_group.location = (-500, -200)
        ec_group.inputs[0].default_value = 3.02
        ec_group.inputs[1].default_value = (0.768151, 0.054480, 0.034340, 1)
        ec_group.inputs[2].default_value = (0.010000, 0.000687, 0.000429, 1)

        # TexturizerGroup
        bpy.ops.node.texturizer_group_operator()
        texturizer_group = nodes.new("ShaderNodeGroup")
        texturizer_group.node_tree = bpy.data.node_groups['Texturizer']
        texturizer_group.location = (-1100, -400)
        texturizer_group.width = 240
        texturizer_group.inputs[0].default_value = (
            0.768151, 0.054480, 0.034340, 1)
        texturizer_group.inputs[1].default_value = 0.4
        texturizer_group.inputs[4].default_value = 0.0125

        # Links
        links = m_cinnabar.node_tree.links.new

        links(m_colorramp.outputs[0], ec_group.inputs[1])
        links(texturizer_group.outputs[1], m_colorramp.inputs[0])
        links(texturizer_group.outputs[3], BSDF.inputs[9])
        links(texturizer_group.outputs[5], BSDF.inputs[22])
        links(ec_group.outputs[0], BSDF.inputs[0])
        links(ec_group.outputs[1], BSDF.inputs[7])
        links(ec_group.outputs[3], BSDF.inputs[16])

        # LOAD THE MATERIAL
        bpy.context.object.active_material = m_cinnabar
