import bpy
import time

# MESSAGE BOX
message_text = "This material already exists"


def ShowMessageBox(message="", title="", icon='INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)


def make_node(nodes, shader, locX, locY):
    result = nodes.new(shader)
    result.location = (locX + 200, locY + 300)
    return result

# CuttingMatShaderOperator


class QMMCuttingMat(bpy.types.Operator):
    """Add/Apply Rubber Cutting Mat Material to Selected Object (or Scene)"""
    bl_label = "QMM Rubber Cutting Mat Shader"
    bl_idname = 'shader.qmm_cutting_mat_operator'

    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        if m_cutting_mat := bpy.data.materials.get("QMM Rubber Cutting Mat"):
            # ShowMessageBox(message_text, "QMM Rubber Cutting Mat")
            # print(f"QMM Rubber Cutting Mat already exists")
            bpy.context.object.active_material = m_cutting_mat
            diffuse_bool = bpy.context.scene.diffuse_bool.diffuse_more
            m_cutting_mat.diffuse_color = (0.045186, 0.141263, 0.144129, 1) if diffuse_bool else (0.8, 0.8, 0.8, 1)
            m_cutting_mat.roughness = 0.79 if diffuse_bool else 0.4
            return {'FINISHED'}
        else:
            self.make_shader()
        return {'FINISHED'}

    def make_shader(self):
        start = time.time()

        # CreateShader
        m_cutting_mat = bpy.data.materials.new(name="QMM Rubber Cutting Mat")
        m_cutting_mat.use_nodes = True
        diffuse_bool = bpy.context.scene.diffuse_bool.diffuse_more
        if diffuse_bool:
            m_cutting_mat.diffuse_color = (0.045186, 0.141263, 0.144129, 1)
            m_cutting_mat.roughness = 0.79

        nodes = m_cutting_mat.node_tree.nodes

        # materialoutput
        material_output = next((n for n in nodes if n.bl_idname == 'ShaderNodeOutputMaterial'), None)
        if material_output:
            material_output.location = (0, 0)

        # Principled BSDF
        BSDF = next((n for n in nodes if n.bl_idname == 'ShaderNodeBsdfPrincipled'), None)
        if BSDF:
            BSDF.distribution = 'MULTI_GGX'
            BSDF.location = (-300, 0)
            BSDF.inputs["Base Color"].default_value = (0.045186, 0.141263, 0.144129, 1)
            BSDF.inputs["Roughness"].default_value = 0.79
            BSDF.inputs["IOR"].default_value = 1.52
            BSDF.inputs["Coat Weight"].default_value = 0.425

        # RGBA mix
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
        m_bricktexture.inputs["Mortar Size"].default_value = 0.005
        m_bricktexture.inputs["Mortar Smooth"].default_value = 0.0
        m_bricktexture.inputs["Brick Width"].default_value = 1.0
        m_bricktexture.inputs["Row Height"].default_value = 1.0

        # bricktexture2
        m_bricktexture2 = make_node(nodes, 'ShaderNodeTexBrick', -1100, -600)
        m_bricktexture2.offset = 0.0
        m_bricktexture2.inputs["Mortar Size"].default_value = 0.01
        m_bricktexture2.inputs["Mortar Smooth"].default_value = 0.0
        m_bricktexture2.inputs["Brick Width"].default_value = 1.0
        m_bricktexture2.inputs["Row Height"].default_value = 1.0

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
        m_mapscale.outputs["Value"].default_value = 2

        # texscale
        m_texscale = make_node(nodes, 'ShaderNodeValue', -1500, -800)
        m_texscale.label = "Texture Scale"
        m_texscale.outputs["Value"].default_value = 4

        # EnergyConservationGroup
        bpy.ops.node.ec_group_operator()
        ec_group = nodes.new("ShaderNodeGroup")
        ec_group.name = "Energy Conservation v5"
        ec_group.node_tree = bpy.data.node_groups['Energy Conservation v5']
        ec_group.location = (0, -200)
        ec_group.inputs[0].default_value = (0.045186, 0.141263, 0.144129, 1)
        ec_group.inputs[1].default_value = 0.79
        ec_group.inputs[2].default_value = 1.52
        ec_group.inputs[4].default_value = (0.01, 0.01, 0.01, 1)

        links = m_cutting_mat.node_tree.links.new

        links(m_texscale.outputs["Value"], m_multiply.inputs[0])
        links(m_texscale.outputs["Value"], m_bricktexture.inputs["Scale"])
        links(m_mapscale.outputs["Value"], m_mapping.inputs["Scale"])
        links(m_textcoord.outputs["UV"], m_mapping.inputs["Vector"])
        links(m_multiply.outputs["Value"], m_bricktexture2.inputs["Scale"])
        links(m_mapping.outputs["Vector"], m_bricktexture.inputs["Vector"])
        links(m_mapping.outputs["Vector"], m_bricktexture2.inputs["Vector"])
        links(m_bricktexture.outputs[1], m_add.inputs[0])
        links(m_bricktexture2.outputs[1], m_add.inputs[1])
        links(m_add.outputs["Value"], m_mix.inputs[0])
        links(m_mix.outputs[2], BSDF.inputs["Base Color"])

        bpy.context.object.active_material = m_cutting_mat

        end = time.time()
        print(f"QMM Rubber Cutting Mat: {end - start} seconds")
