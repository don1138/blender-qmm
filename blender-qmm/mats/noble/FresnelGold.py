import bpy

# MESSAGE BOX
message_text = "This material already exists"
def ShowMessageBox(message = "", title = "", icon = 'INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

#GoldShaderOperator
class QMMGoldFresnel(bpy.types.Operator):
    """Add/Apply Gold Material to Selected Object (or Scene)"""
    bl_label = "QMM Gold Fresnel Shader"
    bl_idname = 'shader.qmm_gold_operator'
    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        m_gold = bpy.data.materials.get("QMM Gold Fresnel")
        if m_gold:
            ShowMessageBox(message_text, "QMM Gold Fresnel")
            # print(f"QMM Gold Fresnel already exists")
            bpy.context.object.active_material = m_gold
            return {'FINISHED'}
        else:
            #CreateShader
            m_gold = bpy.data.materials.new(name = "QMM Gold Fresnel")
            m_gold.use_nodes = True
            m_gold.diffuse_color = (0.658375, 0.42869, 0.0382044, 1)
            m_gold.metallic = 1

            nodes = m_gold.node_tree.nodes

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
            m_glossy.inputs[0].default_value = (0.658375, 0.42869, 0.0382044, 1)

            #glossyshader2
            m_glossy2 = nodes.new('ShaderNodeBsdfGlossy')
            m_glossy2.location = (-600,0)
            m_glossy2.inputs[0].default_value = (0.658375, 0.42869, 0.0382044, 1)

            #diffuseshader
            m_diffuse = nodes.new('ShaderNodeBsdfDiffuse')
            m_diffuse.location = (-600,200)
            m_diffuse.inputs[0].default_value = (0.658375, 0.42869, 0.0382044, 1)
            m_diffuse.inputs[1].default_value = 0

            #value
            m_value = nodes.new('ShaderNodeValue')
            m_value.location = (-800,-200)
            m_value.outputs[0].default_value = 0.2

            links = m_gold.node_tree.links

            links.new(m_value.outputs[0], m_glossy.inputs[1])
            links.new(m_value.outputs[0], m_glossy2.inputs[1])
            links.new(m_diffuse.outputs[0], m_mix2.inputs[2])
            links.new(m_glossy2.outputs[0], m_mix2.inputs[1])
            links.new(m_glossy.outputs[0], m_mix.inputs[2])
            links.new(m_mix2.outputs[0], m_mix.inputs[1])
            links.new(m_layer_weight.outputs[1], m_mix.inputs[0])
            links.new(m_mix.outputs[0], material_output.inputs[0])

            bpy.context.object.active_material = m_gold

            return {'FINISHED'}