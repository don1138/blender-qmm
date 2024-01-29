import bpy
import time 

bv = bpy.app.version

# MESSAGE BOX
message_text = "This material already exists"


def ShowMessageBox(message="", title="", icon='INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)

def make_node(nodes, shader, locX, locY):
    result = nodes.new(shader)
    result.location = (locX, locY)
    return result

# CuttingMatShaderOperator


class QMMCuttingMat(bpy.types.Operator):
    """Add/Apply Rubber Cutting Mat Material to Selected Object (or Scene)"""
    bl_label  = "QMM Rubber Cutting Mat Shader"
    bl_idname = 'shader.qmm_cutting_mat_operator'

    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        if m_cutting_mat := bpy.data.materials.get("QMM Rubber Cutting Mat"):
            ShowMessageBox(message_text, "QMM Rubber Cutting Mat")
            # print(f"QMM Rubber Cutting Mat already exists")
            bpy.context.object.active_material = m_cutting_mat
            return {'FINISHED'}
        else:
            self.make_shader()
        return {'FINISHED'}

    def make_shader(self):
        start = time.time()

        # CreateShader
        m_cutting_mat = bpy.data.materials.new(name="QMM Rubber Cutting Mat")
        m_cutting_mat.use_nodes = True
        m_cutting_mat.diffuse_color = (0.045186, 0.141263, 0.144129, 1)
        m_cutting_mat.roughness = 0.79

        nodes = m_cutting_mat.node_tree.nodes

        # materialoutput
        material_output = nodes.get('Material Output')
        material_output.location = (0, 0)

        # princibledbsdf
        BSDF = nodes.get('Principled BSDF')
        BSDF.distribution = 'MULTI_GGX'
        BSDF.location = (-300, 0)
        BSDF.inputs[0].default_value = (0.045186, 0.141263, 0.144129, 1)
        BSDF.inputs[7].default_value = 0.425
        BSDF.inputs[9].default_value = 0.79

        # rgbmix
        if bv < (3, 4, 0):
            m_mix = make_node(nodes, 'ShaderNodeMixRGB', -700, -300)
            m_mix.inputs[1].default_value = (0.045186, 0.141263, 0.144129, 1)
            m_mix.inputs[2].default_value = (0.187821, 0.450786, 0.558341, 1)
        else:
            m_mix = make_node(nodes, 'ShaderNodeMix', -700, -300)
            m_mix.data_type = 'RGBA'
            m_mix.inputs[6].default_value = (0.045186, 0.141263, 0.144129, 1)
            m_mix.inputs[7].default_value = (0.187821, 0.450786, 0.558341, 1)

        # mathadd
        m_add = make_node(nodes, 'ShaderNodeMath', -900, -400)
        m_add.operation = 'ADD'

        # bricktexture
        m_bricktexture = make_node(nodes, 'ShaderNodeTexBrick', -1100, -200)
        m_bricktexture.offset = 0.0
        m_bricktexture.inputs[5].default_value = 0.005
        m_bricktexture.inputs[6].default_value = 0.0
        m_bricktexture.inputs[8].default_value = 1.0
        m_bricktexture.inputs[9].default_value = 1.0

        # bricktexture2
        m_bricktexture2 = make_node(nodes, 'ShaderNodeTexBrick', -1100, -600)
        m_bricktexture2.offset = 0.0
        m_bricktexture2.inputs[5].default_value = 0.01
        m_bricktexture2.inputs[6].default_value = 0.0
        m_bricktexture2.inputs[8].default_value = 1.0
        m_bricktexture2.inputs[9].default_value = 1.0

        # mapping
        m_mapping = make_node(nodes, 'ShaderNodeMapping', -1300, -400)

        # textcoord
        m_textcoord = make_node(nodes, 'ShaderNodeTexCoord', -1500, -400)

        # mathmultiply
        m_multiply = make_node(nodes, 'ShaderNodeMath', -1300, -800)
        m_multiply.operation = 'MULTIPLY'
        m_multiply.inputs[1].default_value = 5

        # mapscale
        m_mapscale = make_node(nodes, 'ShaderNodeValue', -1500, -700)
        m_mapscale.label = "Map Scale"
        m_mapscale.outputs[0].default_value = 2

        # texscale
        m_texscale = make_node(nodes, 'ShaderNodeValue', -1500, -800)
        m_texscale.label = "Texture Scale"
        m_texscale.outputs[0].default_value = 4

        # EnergyConservationGroup
        bpy.ops.node.ec_group_operator()
        ec_group = nodes.new("ShaderNodeGroup")
        ec_group.name = "Energy Conservation v5"
        ec_group.node_tree = bpy.data.node_groups['Energy Conservation v5']
        ec_group.location = (-500, -200)
        ec_group.inputs[0].default_value = (0.045186, 0.141263, 0.144129, 1)
        ec_group.inputs[1].default_value = 0.79
        ec_group.inputs[2].default_value = 1.52
        ec_group.inputs[4].default_value = (0.01, 0.01, 0.01, 1)

        links = m_cutting_mat.node_tree.links.new

        links(m_texscale.outputs[0], m_multiply.inputs[0])
        links(m_texscale.outputs[0], m_bricktexture.inputs[4])
        links(m_mapscale.outputs[0], m_mapping.inputs[3])
        links(m_textcoord.outputs[2], m_mapping.inputs[0])
        links(m_multiply.outputs[0], m_bricktexture2.inputs[4])
        links(m_mapping.outputs[0], m_bricktexture.inputs[0])
        links(m_mapping.outputs[0], m_bricktexture2.inputs[0])
        links(m_bricktexture.outputs[1], m_add.inputs[0])
        links(m_bricktexture2.outputs[1], m_add.inputs[1])
        links(m_add.outputs[0], m_mix.inputs[0])
        links(ec_group.outputs[0], BSDF.inputs[0])
        if bv < (4, 0, 0):
            links(ec_group.outputs[1], BSDF.inputs[7])
            links(ec_group.outputs[2], BSDF.inputs[9])
            links(ec_group.outputs[4], BSDF.inputs[16])
        else:
            links(ec_group.outputs[1], BSDF.inputs[12])
            links(ec_group.outputs[2], BSDF.inputs[2])
            links(ec_group.outputs[4], BSDF.inputs[3])

        if bv < (3, 4, 0):
            links(m_mix.outputs[0], ec_group.inputs[0])
        else:
            links(m_mix.outputs[2], ec_group.inputs[0])

        bpy.context.object.active_material = m_cutting_mat

        end = time.time()
        print(f"QMM Rubber Cutting Mat: {end - start} seconds")
