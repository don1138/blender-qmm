import bpy
import time 

# MESSAGE BOX
message_text = "This material already exists"


def ShowMessageBox(message="", title="", icon='INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)

# SilverShaderOperator


class QMMSilverFresnel(bpy.types.Operator):
    """Add/Apply Silver Material to Selected Object (or Scene)"""
    bl_label  = "QMM Silver Fresnel Shader"
    bl_idname = 'shader.qmm_silver_operator'

    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        if m_silver := bpy.data.materials.get("QMM Silver Fresnel"):
            #ShowMessageBox(message_text, "QMM Silver Fresnel")
            # print(f"QMM Silver Fresnel already exists")
            bpy.context.object.active_material = m_silver
            return {'FINISHED'}
        else:
            self.make_shader()
        return {'FINISHED'}

    def make_shader(self):
        start = time.time()

        # CreateShader
        m_silver = bpy.data.materials.new(name="QMM Silver Fresnel")
        m_silver.use_nodes = True
        m_silver.diffuse_color = (0.401978, 0.396755, 0.417885, 1)
        m_silver.metallic = 1
        m_silver.roughness = 0.15

        nodes = m_silver.node_tree.nodes

        # materialoutput
        material_output = nodes.get('Material Output')
        material_output.location = (0, 0)

        # princibledbsdf
        BSDF = nodes.get('Principled BSDF')
        BSDF.distribution = 'MULTI_GGX'
        nodes.remove(BSDF)

        # mixshader
        m_mix = nodes.new('ShaderNodeMixShader')
        m_mix.location = (-200, 0)

        # m_layerweight
        m_layer_weight = self.make_node(
            nodes, "ShaderNodeLayerWeight", -400, 200, 0.5
        )

        # glossyshader
        m_glossy = self.make_node(
            nodes, "ShaderNodeBsdfGlossy", -
            400, 0, (0.401978, 0.396755, 0.417885, 1)
        )
        m_glossy.inputs[1].default_value = 0.15

        # glossyshader2
        m_glossy2 = self.make_node(
            nodes, "ShaderNodeBsdfGlossy", -400, -
            200, (0.401978, 0.396755, 0.417885, 1)
        )
        m_glossy2.inputs[1].default_value = 0.5

        links = m_silver.node_tree.links.new

        links(m_glossy2.outputs[0], m_mix.inputs[2])
        links(m_glossy.outputs[0], m_mix.inputs[1])
        links(m_layer_weight.outputs[1], m_mix.inputs[0])
        links(m_mix.outputs[0], material_output.inputs[0])

        bpy.context.object.active_material = m_silver

        # SilverColorsGroup
        bpy.ops.node.silver_cg_operator()
        nodes = m_silver.node_tree.nodes
        silver_colors_group = nodes.new("ShaderNodeGroup")
        silver_colors_group.name = "Silver Colors"
        silver_colors_group.node_tree = bpy.data.node_groups['Silver Colors']
        silver_colors_group.location = (-600, -100)
        links(silver_colors_group.outputs[0], m_glossy.inputs[0])
        links(silver_colors_group.outputs[0], m_glossy2.inputs[0])

        end = time.time()
        print(f"QMM Silver Fresnel: {end - start} seconds")

    def make_node(self, nodes, arg1, arg2, arg3, arg4):
        result = nodes.new(arg1)
        result.location = arg2, arg3
        result.inputs[0].default_value = arg4
        return result
