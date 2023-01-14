import bpy
import time 

# MESSAGE BOX
message_text = "This material already exists"


def ShowMessageBox(message="", title="", icon='INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)

# RedMetalShaderOperator


class QMMRedMetal(bpy.types.Operator):
    """Add/Apply Red Metal Material to Selected Object (or Scene)"""
    bl_label  = "QMM Red Metal Shader"
    bl_idname = 'shader.qmm_red_metal_operator'

    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        if m_red_metal := bpy.data.materials.get("QMM Red Metal"):
            ShowMessageBox(message_text, "QMM Red Metal")
            # print(f"QMM Red Metal already exists")
            bpy.context.object.active_material = m_red_metal
            return {'FINISHED'}
        else:
            self.make_shader()
        return {'FINISHED'}

    def make_shader(self):
        start = time.time()

        # CreateShader
        m_red_metal = bpy.data.materials.new(name="QMM Red Metal")
        m_red_metal.use_nodes = True
        m_red_metal.diffuse_color = (0.768151, 0.054480, 0.034340, 1)
        m_red_metal.metallic = 1
        m_red_metal.roughness = 0.6

        nodes = m_red_metal.node_tree.nodes

        # materialoutput
        material_output = nodes.get('Material Output')
        material_output.location = (0, 0)

        # princibledbsdf
        BSDF = nodes.get('Principled BSDF')
        BSDF.distribution = 'MULTI_GGX'
        BSDF.location = (-300, 0)
        BSDF.inputs[0].default_value = (0.768151, 0.054480, 0.034340, 1)
        BSDF.inputs[6].default_value = 1
        BSDF.inputs[9].default_value = 0.4
        BSDF.inputs[16].default_value = 3.256

        # colorramp
        m_colorramp = nodes.new('ShaderNodeValToRGB')
        m_colorramp.label = "Red Metal"
        m_colorramp.location = (-800, -200)
        m_colorramp.color_ramp.elements[0].color = (
            0.768151, 0.054480, 0.034340, 1)
        m_colorramp.color_ramp.elements[1].color = (
            0.964687, 0.066626, 0.002428, 1)
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

        nodes = m_red_metal.node_tree.nodes

        # EnergyConservationGroup
        bpy.ops.node.ec_group_operator()
        ec_group = nodes.new("ShaderNodeGroup")
        ec_group.name = "Energy Conservation"
        ec_group.node_tree = bpy.data.node_groups['Energy Conservation']
        ec_group.location = (-500, -200)
        ec_group.inputs[0].default_value = 3.256
        ec_group.inputs[1].default_value = (0.768151, 0.054480, 0.034340, 1)
        ec_group.inputs[3].default_value = (0.010000, 0.000687, 0.000429, 1)

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
        links = m_red_metal.node_tree.links.new

        links(m_colorramp.outputs[0], ec_group.inputs[1])
        links(texturizer_group.outputs[1], m_colorramp.inputs[0])
        links(texturizer_group.outputs[3], BSDF.inputs[9])
        links(texturizer_group.outputs[5], BSDF.inputs[22])
        links(ec_group.outputs[0], BSDF.inputs[0])
        links(ec_group.outputs[1], BSDF.inputs[7])
        links(ec_group.outputs[3], BSDF.inputs[16])

        # LOAD THE MATERIAL
        bpy.context.object.active_material = m_red_metal

        end = time.time()
        print(f"QMM Red Metal: {end - start} seconds")
