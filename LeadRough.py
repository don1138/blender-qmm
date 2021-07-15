import bpy

# MESSAGE BOX
message_text = "This material already exists"
def ShowMessageBox(message = "", title = "", icon = 'INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

#LeadRoughShaderOperator
class QMMLeadRough(bpy.types.Operator):
    """Add/Apply Lead Rough Material to Selected Object (or Scene)"""
    bl_label = "QMM Lead Rough Shader"
    bl_idname = 'shader.qmm_lead_rough_operator'
    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        material_lead_rough = bpy.data.materials.get("QMM Lead Rough")
        if material_lead_rough:
            ShowMessageBox(message_text, "QMM Lead Rough")
            # print(f"QMM Lead Rough already exists")
            bpy.context.object.active_material = material_lead_rough
            return {'FINISHED'}
        else:
            #CreateShader
            material_lead_rough = bpy.data.materials.new(name = "QMM Lead Rough")
            material_lead_rough.use_nodes = True
            material_lead_rough.diffuse_color = (0.186, 0.188, 0.196, 1.0)
            material_lead_rough.metallic = 1
            material_lead_rough.roughness = 0.565

            #materialoutput
            material_output = material_lead_rough.node_tree.nodes.get('Material Output')
            material_output.location = (0,0)

            #princibledbsdf
            BSDF = material_lead_rough.node_tree.nodes.get('Principled BSDF')
            BSDF.location = (-300,0)
            BSDF.inputs[0].default_value = (0.186, 0.188, 0.196, 1.0)
            BSDF.inputs[4].default_value = 1
            BSDF.inputs[7].default_value = 0.565
            BSDF.inputs[14].default_value = 2.010

            #mathdivide
            m_divide = material_lead_rough.node_tree.nodes.new('ShaderNodeMath')
            m_divide.operation = 'DIVIDE'
            m_divide.location = (-500,0)
            m_divide.inputs[1].default_value = 0.08

            #mathpower
            m_power = material_lead_rough.node_tree.nodes.new('ShaderNodeMath')
            m_power.operation = 'POWER'
            m_power.location = (-700,0)
            m_power.inputs[1].default_value = 2

            #mathdivide2
            m_divide2 = material_lead_rough.node_tree.nodes.new('ShaderNodeMath')
            m_divide2.operation = 'DIVIDE'
            m_divide2.location = (-900,0)

            #mathsubtract
            m_subtract = material_lead_rough.node_tree.nodes.new('ShaderNodeMath')
            m_subtract.operation = 'SUBTRACT'
            m_subtract.location = (-1100,0)
            m_subtract.inputs[1].default_value = 1

            #mathadd
            m_add = material_lead_rough.node_tree.nodes.new('ShaderNodeMath')
            m_add.operation = 'ADD'
            m_add.location = (-1100,-200)
            m_add.inputs[1].default_value = 1

            #value
            m_value = material_lead_rough.node_tree.nodes.new('ShaderNodeValue')
            m_value.location = (-1300,0)
            m_value.outputs[0].default_value = 2.01
            m_value.label = "IOR"

            material_lead_rough.node_tree.links.new(m_value.outputs[0], m_add.inputs[0])
            material_lead_rough.node_tree.links.new(m_value.outputs[0], m_subtract.inputs[0])
            material_lead_rough.node_tree.links.new(m_add.outputs[0], m_divide2.inputs[1])
            material_lead_rough.node_tree.links.new(m_subtract.outputs[0], m_divide2.inputs[0])
            material_lead_rough.node_tree.links.new(m_divide2.outputs[0], m_power.inputs[0])
            material_lead_rough.node_tree.links.new(m_power.outputs[0], m_divide.inputs[0])
            material_lead_rough.node_tree.links.new(m_divide.outputs[0], BSDF.inputs[5])

            bpy.context.object.active_material = material_lead_rough

            return {'FINISHED'}
