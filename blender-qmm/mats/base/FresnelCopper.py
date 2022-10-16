import bpy

# MESSAGE BOX
message_text = "This material already exists"
def ShowMessageBox(message = "", title = "", icon = 'INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

#CopperShaderOperator
class QMMCopperFresnel(bpy.types.Operator):
    """Add/Apply Copper Material to Selected Object (or Scene)"""
    bl_label = "QMM Copper Fresnel Shader"
    bl_idname = 'shader.qmm_copper_operator'
    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        m_copper = bpy.data.materials.get("QMM Copper Fresnel")
        if m_copper:
            ShowMessageBox(message_text, "QMM Copper Fresnel")
            # print(f"QMM Copper Fresnel already exists")
            bpy.context.object.active_material = m_copper
            return {'FINISHED'}
        else:
            #CreateShader
            m_copper = bpy.data.materials.new(name = "QMM Copper Fresnel")
            m_copper.use_nodes = True
            m_copper.diffuse_color = (0.47932, 0.171441, 0.0331048, 1)
            m_copper.metallic = 1
            m_copper.roughness = 0.35

            nodes = m_copper.node_tree.nodes

            #materialoutput
            material_output = nodes.get('Material Output')
            material_output.location = (0,0)

            #princibledbsdf
            BSDF = nodes.get('Principled BSDF')
            nodes.remove(BSDF)

            #mixshader
            m_mix = nodes.new('ShaderNodeMixShader')
            m_mix.location = (-200,0)

            #m_layerweight
            m_layer_weight = nodes.new('ShaderNodeLayerWeight')
            m_layer_weight.location = (-400,200)
            m_layer_weight.inputs[0].default_value = 0.5

            #mixshader2
            m_mix2 = nodes.new('ShaderNodeMixShader')
            m_mix2.location = (-400,0)
            m_mix2.inputs[0].default_value = 0.095

            #glossyshader
            m_glossy = nodes.new('ShaderNodeBsdfGlossy')
            m_glossy.location = (-400,-200)
            m_glossy.inputs[0].default_value = (0.47932, 0.171441, 0.0331048, 1)

            #glossyshader2
            m_glossy2 = nodes.new('ShaderNodeBsdfGlossy')
            m_glossy2.location = (-600,0)
            m_glossy2.inputs[0].default_value = (0.47932, 0.171441, 0.0331048, 1)

            #diffuseshader
            m_diffuse = nodes.new('ShaderNodeBsdfDiffuse')
            m_diffuse.location = (-600,200)
            m_diffuse.inputs[0].default_value = (0.47932, 0.171441, 0.0331048, 1)
            m_diffuse.inputs[1].default_value = 0

            #value
            m_value = nodes.new('ShaderNodeValue')
            m_value.location = (-800,-200)
            m_value.outputs[0].default_value = 0.35

            links = m_copper.node_tree.links.new

            links(m_value.outputs[0], m_glossy.inputs[1])
            links(m_value.outputs[0], m_glossy2.inputs[1])
            links(m_diffuse.outputs[0], m_mix2.inputs[2])
            links(m_glossy2.outputs[0], m_mix2.inputs[1])
            links(m_glossy.outputs[0], m_mix.inputs[2])
            links(m_mix2.outputs[0], m_mix.inputs[1])
            links(m_layer_weight.outputs[1], m_mix.inputs[0])
            links(m_mix.outputs[0], material_output.inputs[0])

            #CopperColorsGroup
            bpy.ops.node.copper_colors_group_operator()
            nodes = m_copper.node_tree.nodes
            copper_colors_group = nodes.new("ShaderNodeGroup")
            copper_colors_group.node_tree = bpy.data.node_groups['Copper Colors']
            copper_colors_group.location = (-1000, 0)
            links(copper_colors_group.outputs[0], m_diffuse.inputs[0])
            links(copper_colors_group.outputs[0], m_glossy.inputs[0])
            links(copper_colors_group.outputs[0], m_glossy2.inputs[0])

            #LOAD THE MATERIAL
            bpy.context.object.active_material = m_copper

        return {'FINISHED'}
