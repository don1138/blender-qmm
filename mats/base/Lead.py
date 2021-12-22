import bpy

# MESSAGE BOX
message_text = "This material already exists"
def ShowMessageBox(message = "", title = "", icon = 'INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

#LeadShaderOperator
class QMMLead(bpy.types.Operator):
    """Add/Apply Lead Material to Selected Object (or Scene)"""
    bl_label = "QMM Lead Shader"
    bl_idname = 'shader.qmm_lead_operator'
    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        m_lead = bpy.data.materials.get("QMM Lead")
        if m_lead:
            ShowMessageBox(message_text, "QMM Lead")
            # print(f"QMM Lead already exists")
            bpy.context.object.active_material = m_lead
            return {'FINISHED'}
        else:
            #CreateShader
            m_lead = bpy.data.materials.new(name = "QMM Lead")
            m_lead.use_nodes = True
            m_lead.diffuse_color = (0.380, 0.384, 0.4, 1.0)
            m_lead.metallic = 1
            m_lead.roughness = 0.706

            nodes = m_lead.node_tree.nodes

            #materialoutput
            material_output = nodes.get('Material Output')
            material_output.location = (0,0)

            #princibledbsdf
            BSDF = nodes.get('Principled BSDF')
            BSDF.location = (-300,0)
            BSDF.inputs[0].default_value = (0.380, 0.384, 0.4, 1.0)
            BSDF.inputs[6].default_value = 1
            BSDF.inputs[9].default_value = 0.706
            BSDF.inputs[16].default_value = 2.010

            #mathdivide
            m_divide = nodes.new('ShaderNodeMath')
            m_divide.operation = 'DIVIDE'
            m_divide.location = (-500,0)
            m_divide.inputs[1].default_value = 0.08

            #mathpower
            m_power = nodes.new('ShaderNodeMath')
            m_power.operation = 'POWER'
            m_power.location = (-700,0)
            m_power.inputs[1].default_value = 2

            #mathdivide2
            m_divide2 = nodes.new('ShaderNodeMath')
            m_divide2.operation = 'DIVIDE'
            m_divide2.location = (-900,0)

            #mathsubtract
            m_subtract = nodes.new('ShaderNodeMath')
            m_subtract.operation = 'SUBTRACT'
            m_subtract.location = (-1100,0)
            m_subtract.inputs[1].default_value = 1

            #mathadd
            m_add = nodes.new('ShaderNodeMath')
            m_add.operation = 'ADD'
            m_add.location = (-1100,-200)
            m_add.inputs[1].default_value = 1

            #value
            m_value = nodes.new('ShaderNodeValue')
            m_value.location = (-1300,0)
            m_value.outputs[0].default_value = 2.01
            m_value.label = "IOR"

            #valuesmooth
            m_value_smooth = nodes.new('ShaderNodeValue')
            m_value_smooth.location = (-500,-200)
            m_value_smooth.outputs[0].default_value = 0.361
            m_value_smooth.label = "Smooth"

            #valuematte
            m_value_matte = nodes.new('ShaderNodeValue')
            m_value_matte.location = (-500,-300)
            m_value_matte.outputs[0].default_value = 0.565
            m_value_matte.label = "Matte"

            links = m_lead.node_tree.links

            links.new(m_value.outputs[0], m_add.inputs[0])
            links.new(m_value.outputs[0], m_subtract.inputs[0])
            links.new(m_add.outputs[0], m_divide2.inputs[1])
            links.new(m_subtract.outputs[0], m_divide2.inputs[0])
            links.new(m_divide2.outputs[0], m_power.inputs[0])
            links.new(m_power.outputs[0], m_divide.inputs[0])
            links.new(m_divide.outputs[0], BSDF.inputs[7])
            links.new(m_value.outputs[0], BSDF.inputs[16])
            links.new(m_value_matte.outputs[0], BSDF.inputs[7])

            bpy.context.object.active_material = m_lead

            return {'FINISHED'}