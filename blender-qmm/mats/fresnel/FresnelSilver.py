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
    bl_label = "QMM Silver Fresnel Shader"
    bl_idname = 'shader.qmm_silver_operator'

    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        if m_silver := bpy.data.materials.get("QMM Silver Fresnel"):
            # ShowMessageBox(message_text, "QMM Silver Fresnel")
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
        material_output = next((n for n in nodes if n.bl_idname == 'ShaderNodeOutputMaterial'), None)
        if material_output:
            material_output.location = (0, 0)

        # princibledbsdf
        BSDF = next((n for n in nodes if n.bl_idname == 'ShaderNodeBsdfPrincipled'), None)
        if BSDF:
            BSDF.distribution = 'MULTI_GGX'
            nodes.remove(BSDF)

        # mixshader
        m_mix = nodes.new('ShaderNodeMixShader')
        m_mix.location = (-200, 0)

        # Layer Weight
        m_layer_weight = nodes.new('ShaderNodeLayerWeight')
        m_layer_weight.location = (-400, 200)
        m_layer_weight.inputs["Blend"].default_value = 0.5

        # Glossy BSDF
        m_glossy = nodes.new('ShaderNodeBsdfAnisotropic')
        m_glossy.location = (-400, 0)
        m_glossy.inputs["Color"].default_value = (0.401978, 0.396755, 0.417885, 1)
        m_glossy.inputs["Roughness"].default_value = 0.15

        # Glossy BSDF 2
        m_glossy2 = nodes.new('ShaderNodeBsdfAnisotropic')
        m_glossy2.location = (-400, -300)
        m_glossy2.inputs["Color"].default_value = (0.401978, 0.396755, 0.417885, 1)
        m_glossy2.inputs["Roughness"].default_value = 0.5

        links = m_silver.node_tree.links.new

        links(m_glossy2.outputs["BSDF"], m_mix.inputs[2])
        links(m_glossy.outputs["BSDF"], m_mix.inputs[1])
        links(m_layer_weight.outputs["Facing"], m_mix.inputs["Fac"])
        links(m_mix.outputs["Shader"], material_output.inputs["Surface"])

        # SilverColorsGroup
        bpy.ops.node.silver_cg_operator()
        nodes = m_silver.node_tree.nodes
        silver_colors_group = nodes.new("ShaderNodeGroup")
        silver_colors_group.name = "Silver Colors"
        silver_colors_group.node_tree = bpy.data.node_groups['Silver Colors']
        silver_colors_group.location = (-600, -100)

        links(silver_colors_group.outputs[0], m_glossy.inputs["Color"])
        links(silver_colors_group.outputs[0], m_glossy2.inputs["Color"])

        # LOAD THE MATERIAL
        bpy.context.object.active_material = m_silver

        end = time.time()
        print(f"QMM Silver Fresnel: {end - start} seconds")
