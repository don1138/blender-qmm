import bpy

# MESSAGE BOX
message_text = "This material already exists"
def ShowMessageBox(message = "", title = "", icon = 'INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

#CopperShaderOperator
class QMMCopper(bpy.types.Operator):
    bl_label = "QMM Copper Shader"
    bl_idname = 'shader.qmm_copper_operator'
    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        material_copper = bpy.data.materials.get("QMM Copper")
        if material_copper:
            ShowMessageBox(message_text, "QMM Copper")
            print(f"QMM Copper already exists")
            bpy.context.object.active_material = material_copper
            return {'FINISHED'}
        else:
            #CreateShader
            material_copper = bpy.data.materials.new(name = "QMM Copper")
            material_copper.use_nodes = True
            material_copper.diffuse_color = (0.47932, 0.171441, 0.0331048, 1)

            #materialoutput
            material_output = material_copper.node_tree.nodes.get('Material Output')
            material_output.location = (0,0)

            #princibledbsdf
            BSDF = material_copper.node_tree.nodes.get('Principled BSDF')
            material_copper.node_tree.nodes.remove(BSDF)

            #mixshader
            m_mix = material_copper.node_tree.nodes.new('ShaderNodeMixShader')
            m_mix.location = (-200,0)

            #m_layerweight
            m_layer_weight = material_copper.node_tree.nodes.new('ShaderNodeLayerWeight')
            m_layer_weight.location = (-400,200)
            m_layer_weight.inputs[0].default_value = 0.5

            #mixshader2
            m_mix2 = material_copper.node_tree.nodes.new('ShaderNodeMixShader')
            m_mix2.location = (-400,0)
            m_mix2.inputs[0].default_value = 0.095

            #glossyshader
            m_glossy = material_copper.node_tree.nodes.new('ShaderNodeBsdfGlossy')
            m_glossy.location = (-400,-200)
            m_glossy.inputs[0].default_value = (0.47932, 0.171441, 0.0331048, 1)

            #glossyshader2
            m_glossy2 = material_copper.node_tree.nodes.new('ShaderNodeBsdfGlossy')
            m_glossy2.location = (-600,0)
            m_glossy2.inputs[0].default_value = (0.47932, 0.171441, 0.0331048, 1)

            #diffuseshader
            m_diffuse = material_copper.node_tree.nodes.new('ShaderNodeBsdfDiffuse')
            m_diffuse.location = (-600,200)
            m_diffuse.inputs[0].default_value = (0.47932, 0.171441, 0.0331048, 1)
            m_diffuse.inputs[1].default_value = 0

            #value
            m_value = material_copper.node_tree.nodes.new('ShaderNodeValue')
            m_value.location = (-800,-200)
            m_value.outputs[0].default_value = 0.25

            material_copper.node_tree.links.new(m_value.outputs[0], m_glossy.inputs[1])
            material_copper.node_tree.links.new(m_value.outputs[0], m_glossy2.inputs[1])
            material_copper.node_tree.links.new(m_diffuse.outputs[0], m_mix2.inputs[2])
            material_copper.node_tree.links.new(m_glossy2.outputs[0], m_mix2.inputs[1])
            material_copper.node_tree.links.new(m_glossy.outputs[0], m_mix.inputs[2])
            material_copper.node_tree.links.new(m_mix2.outputs[0], m_mix.inputs[1])
            material_copper.node_tree.links.new(m_layer_weight.outputs[1], m_mix.inputs[0])
            material_copper.node_tree.links.new(m_mix.outputs[0], material_output.inputs[0])

            bpy.context.object.active_material = material_copper

            return {'FINISHED'}
