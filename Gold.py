import bpy

# MESSAGE BOX
message_text = "This material already exists"
def ShowMessageBox(message = "", title = "", icon = 'INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

#GoldShaderOperator
class QMMGold(bpy.types.Operator):
    bl_label = "QMM Gold Shader"
    bl_idname = 'shader.qmm_gold_operator'
    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        material_gold = bpy.data.materials.get("QMM Gold")
        if material_gold:
            ShowMessageBox(message_text, "QMM Gold")
            print(f"QMM Gold already exists")
            bpy.context.object.active_material = material_gold
            return {'FINISHED'}
        else:
            #CreateShader
            material_gold = bpy.data.materials.new(name = "QMM Gold")
            material_gold.use_nodes = True
            material_gold.diffuse_color = (0.658375, 0.42869, 0.0382044, 1)

            #materialoutput
            material_output = material_gold.node_tree.nodes.get('Material Output')
            material_output.location = (0,0)

            #princibledbsdf
            BSDF = material_gold.node_tree.nodes.get('Principled BSDF')
            material_gold.node_tree.nodes.remove(BSDF)

            #mixshader
            m_mix = material_gold.node_tree.nodes.new('ShaderNodeMixShader')
            m_mix.location = (-200,0)

            #m_layerweight
            m_layer_weight = material_gold.node_tree.nodes.new('ShaderNodeLayerWeight')
            m_layer_weight.location = (-400,200)
            m_layer_weight.inputs[0].default_value = 0.5

            #mixshader2
            m_mix2 = material_gold.node_tree.nodes.new('ShaderNodeMixShader')
            m_mix2.location = (-400,0)
            m_mix2.inputs[0].default_value = 0.095

            #glossyshader
            m_glossy = material_gold.node_tree.nodes.new('ShaderNodeBsdfGlossy')
            m_glossy.location = (-400,-200)
            m_glossy.inputs[0].default_value = (0.658375, 0.42869, 0.0382044, 1)

            #glossyshader2
            m_glossy2 = material_gold.node_tree.nodes.new('ShaderNodeBsdfGlossy')
            m_glossy2.location = (-600,0)
            m_glossy2.inputs[0].default_value = (0.658375, 0.42869, 0.0382044, 1)

            #diffuseshader
            m_diffuse = material_gold.node_tree.nodes.new('ShaderNodeBsdfDiffuse')
            m_diffuse.location = (-600,200)
            m_diffuse.inputs[0].default_value = (0.658375, 0.42869, 0.0382044, 1)
            m_diffuse.inputs[1].default_value = 0

            #value
            m_value = material_gold.node_tree.nodes.new('ShaderNodeValue')
            m_value.location = (-800,-200)
            m_value.outputs[0].default_value = 0.2

            material_gold.node_tree.links.new(m_value.outputs[0], m_glossy.inputs[1])
            material_gold.node_tree.links.new(m_value.outputs[0], m_glossy2.inputs[1])
            material_gold.node_tree.links.new(m_diffuse.outputs[0], m_mix2.inputs[2])
            material_gold.node_tree.links.new(m_glossy2.outputs[0], m_mix2.inputs[1])
            material_gold.node_tree.links.new(m_glossy.outputs[0], m_mix.inputs[2])
            material_gold.node_tree.links.new(m_mix2.outputs[0], m_mix.inputs[1])
            material_gold.node_tree.links.new(m_layer_weight.outputs[1], m_mix.inputs[0])
            material_gold.node_tree.links.new(m_mix.outputs[0], material_output.inputs[0])

            bpy.context.object.active_material = material_gold

            return {'FINISHED'}
