import bpy

# MESSAGE BOX
message_text = "This material already exists"
def ShowMessageBox(message = "", title = "", icon = 'INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

#SilverShaderOperator
class QMMSilverFresnel(bpy.types.Operator):
    """Add/Apply Silver Material to Selected Object (or Scene)"""
    bl_label = "QMM Silver Fresnel Shader"
    bl_idname = 'shader.qmm_silver_operator'
    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        m_silver = bpy.data.materials.get("QMM Silver Fresnel")
        if m_silver:
            ShowMessageBox(message_text, "QMM Silver Fresnel")
            # print(f"QMM Silver Fresnel already exists")
            bpy.context.object.active_material = m_silver
            return {'FINISHED'}
        else:
            #CreateShader
            m_silver = bpy.data.materials.new(name = "QMM Silver Fresnel")
            m_silver.use_nodes = True
            m_silver.diffuse_color = (0.401978, 0.396755, 0.417885, 1)
            m_silver.metallic = 1

            nodes = m_silver.node_tree.nodes

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

            #glossyshader
            m_glossy = nodes.new('ShaderNodeBsdfGlossy')
            m_glossy.location = (-400,0)
            m_glossy.inputs[0].default_value = (0.401978, 0.396755, 0.417885, 1)
            m_glossy.inputs[1].default_value = 0.35

            #glossyshader2
            m_glossy2 = nodes.new('ShaderNodeBsdfGlossy')
            m_glossy2.location = (-400,-200)
            m_glossy2.inputs[0].default_value = (0.401978, 0.396755, 0.417885, 1)
            m_glossy2.inputs[1].default_value = 0.5

            links = m_silver.node_tree.links

            links.new(m_glossy2.outputs[0], m_mix.inputs[2])
            links.new(m_glossy.outputs[0], m_mix.inputs[1])
            links.new(m_layer_weight.outputs[1], m_mix.inputs[0])
            links.new(m_mix.outputs[0], material_output.inputs[0])

            bpy.context.object.active_material = m_silver

        return {'FINISHED'}
