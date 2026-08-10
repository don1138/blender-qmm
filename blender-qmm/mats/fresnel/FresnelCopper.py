import bpy
import time 

# MESSAGE BOX
message_text = "This material already exists"


def ShowMessageBox(message="", title="", icon='INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)

# CopperShaderOperator


class QMMCopperFresnel(bpy.types.Operator):
    """Add/Apply Copper Material to Selected Object (or Scene)"""
    bl_label  = "QMM Copper Fresnel Shader"
    bl_idname = 'shader.qmm_copper_operator'

    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        if m_copper := bpy.data.materials.get("QMM Copper Fresnel"):
            #ShowMessageBox(message_text, "QMM Copper Fresnel")
            # print(f"QMM Copper Fresnel already exists")
            bpy.context.object.active_material = m_copper
            return {'FINISHED'}
        else:
            self.make_shader()
        return {'FINISHED'}

    def make_shader(self):
        start = time.time()

        # CreateShader
        m_copper = bpy.data.materials.new(name="QMM Copper Fresnel")
        m_copper.use_nodes = True
        m_copper.diffuse_color = (0.47932, 0.171441, 0.0331048, 1)
        m_copper.metallic = 1
        m_copper.roughness = 0.35

        nodes = m_copper.node_tree.nodes

        # materialoutput
        material_output = next((n for n in nodes if n.bl_idname == 'ShaderNodeOutputMaterial'), None)
        if material_output:
            material_output.location = (0, 0)

        # princibledbsdf
        BSDF = next((n for n in nodes if n.bl_idname == 'ShaderNodeBsdfPrincipled'), None)
        if BSDF:
            BSDF.distribution = 'MULTI_GGX'
            nodes.remove(BSDF)

        # Mix Shader
        m_mix = nodes.new('ShaderNodeMixShader')
        m_mix.location = (-200, 0)

        # Layer Weight
        m_layer_weight = nodes.new('ShaderNodeLayerWeight')
        m_layer_weight.location = (-400, 200)
        m_layer_weight.inputs["Blend"].default_value = 0.5

        # Mix Shader 2
        m_mix2 = nodes.new('ShaderNodeMixShader')
        m_mix2.location = (-400, 0)
        m_mix2.inputs["Fac"].default_value = 0.095

        # Glossy BSDF
        m_glossy = nodes.new('ShaderNodeBsdfAnisotropic')
        m_glossy.location = (-400, -200)
        m_glossy.inputs["Color"].default_value = (0.47932, 0.171441, 0.0331048, 1)

        # Glossy BSDF 2
        m_glossy2 = nodes.new('ShaderNodeBsdfAnisotropic')
        m_glossy2.location = (-600, 0)
        m_glossy2.inputs["Color"].default_value = (0.47932, 0.171441, 0.0331048, 1)

        # Diffuse BSDF
        m_diffuse = nodes.new('ShaderNodeBsdfDiffuse')
        m_diffuse.location = (-600, 200)
        m_diffuse.inputs["Color"].default_value = (0.47932, 0.171441, 0.0331048, 1)
        m_diffuse.inputs["Roughness"].default_value = 0

        # Value
        m_value = nodes.new('ShaderNodeValue')
        m_value.location = (-800, -200)
        m_value.outputs["Value"].default_value = 0.35

        links = m_copper.node_tree.links.new

        links(m_value.outputs["Value"], m_glossy.inputs["Roughness"])
        links(m_value.outputs["Value"], m_glossy2.inputs["Roughness"])
        links(m_diffuse.outputs["BSDF"], m_mix2.inputs[2])
        links(m_glossy2.outputs["BSDF"], m_mix2.inputs[1])
        links(m_glossy.outputs["BSDF"], m_mix.inputs[2])
        links(m_mix2.outputs["Shader"], m_mix.inputs[1])
        links(m_layer_weight.outputs["Facing"], m_mix.inputs["Fac"])
        links(m_mix.outputs["Shader"], material_output.inputs["Surface"])

        # CopperColorsGroup
        bpy.ops.node.copper_cg_operator()
        nodes = m_copper.node_tree.nodes
        copper_colors_group = nodes.new("ShaderNodeGroup")
        copper_colors_group.name = "Copper Colors"
        copper_colors_group.node_tree = bpy.data.node_groups['Copper Colors']
        copper_colors_group.location = (-1000, 0)

        links(copper_colors_group.outputs[0], m_diffuse.inputs["Color"])
        links(copper_colors_group.outputs[0], m_glossy.inputs["Color"])
        links(copper_colors_group.outputs[0], m_glossy2.inputs["Color"])

        # LOAD THE MATERIAL
        bpy.context.object.active_material = m_copper

        end = time.time()
        print(f"QMM Copper Fresnel: {end - start} seconds")
