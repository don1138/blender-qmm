import bpy

# MESSAGE BOX
message_text = "This material already exists"


def ShowMessageBox(message="", title="", icon='INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)

# GoldShaderOperator


class QMMGoldFresnel(bpy.types.Operator):
    """Add/Apply Gold Material to Selected Object (or Scene)"""
    bl_label = "QMM Gold Fresnel Shader"
    bl_idname = 'shader.qmm_gold_operator'

    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        if m_gold := bpy.data.materials.get("QMM Gold Fresnel"):
            ShowMessageBox(message_text, "QMM Gold Fresnel")
            # print(f"QMM Gold Fresnel already exists")
            bpy.context.object.active_material = m_gold
            return {'FINISHED'}
        else:
            self.make_shader()
        return {'FINISHED'}

    def make_shader(self):
        # CreateShader
        m_gold = bpy.data.materials.new(name="QMM Gold Fresnel")
        m_gold.use_nodes = True
        m_gold.diffuse_color = (0.658375, 0.42869, 0.0382044, 1)
        m_gold.metallic = 1
        m_gold.roughness = 0.14

        nodes = m_gold.node_tree.nodes

        # materialoutput
        material_output = nodes.get('Material Output')
        material_output.location = (0, 0)

        # princibledbsdf
        BSDF = nodes.get('Principled BSDF')
        nodes.remove(BSDF)

        # mixshader
        m_mix = nodes.new('ShaderNodeMixShader')
        m_mix.location = (-200, 0)

        # m_layerweight
        m_layer_weight = self.make_node(
            nodes, "ShaderNodeLayerWeight", -400, 200, 0.5
        )

        # mixshader2
        m_mix2 = self.make_node(
            nodes, "ShaderNodeMixShader", -400, 0, 0.095
        )

        # glossyshader
        m_glossy = self.make_node(
            nodes, "ShaderNodeBsdfGlossy", -400, -
            200, (0.658375, 0.42869, 0.0382044, 1)
        )

        # glossyshader2
        m_glossy2 = self.make_node(
            nodes, "ShaderNodeBsdfGlossy", -
            600, 0, (0.658375, 0.42869, 0.0382044, 1)
        )

        # diffuseshader
        m_diffuse = self.make_node(
            nodes, "ShaderNodeBsdfDiffuse", -
            600, 200, (0.658375, 0.42869, 0.0382044, 1)
        )
        m_diffuse.inputs[1].default_value = 0

        # value
        m_value = nodes.new('ShaderNodeValue')
        m_value.location = (-800, -200)
        m_value.outputs[0].default_value = 0.14

        links = m_gold.node_tree.links.new

        links(m_value.outputs[0], m_glossy.inputs[1])
        links(m_value.outputs[0], m_glossy2.inputs[1])
        links(m_diffuse.outputs[0], m_mix2.inputs[2])
        links(m_glossy2.outputs[0], m_mix2.inputs[1])
        links(m_glossy.outputs[0], m_mix.inputs[2])
        links(m_mix2.outputs[0], m_mix.inputs[1])
        links(m_layer_weight.outputs[1], m_mix.inputs[0])
        links(m_mix.outputs[0], material_output.inputs[0])

        bpy.context.object.active_material = m_gold

        # GoldColorsGroup
        bpy.ops.node.gold_colors_group_operator()
        nodes = m_gold.node_tree.nodes
        gold_colors_group = nodes.new("ShaderNodeGroup")
        gold_colors_group.name = "Gold Colors"
        gold_colors_group.node_tree = bpy.data.node_groups['Gold Colors']
        gold_colors_group.location = (-1000, 0)
        links(gold_colors_group.outputs[0], m_diffuse.inputs[0])
        links(gold_colors_group.outputs[0], m_glossy.inputs[0])
        links(gold_colors_group.outputs[0], m_glossy2.inputs[0])

    def make_node(self, nodes, arg1, arg2, arg3, arg4):
        result = nodes.new(arg1)
        result.location = arg2, arg3
        result.inputs[0].default_value = arg4
        return result
