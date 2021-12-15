import bpy

# MESSAGE BOX
message_text = "This material already exists"
def ShowMessageBox(message = "", title = "", icon = 'INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

#SteelShaderOperator
class QMMSteel(bpy.types.Operator):
    """Add/Apply Steel Material to Selected Object (or Scene)"""
    bl_label = "QMM Steel Shader"
    bl_idname = 'shader.qmm_steel_operator'
    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        m_steel = bpy.data.materials.get("QMM Steel")
        if m_steel:
            ShowMessageBox(message_text, "QMM Steel")
            # print(f"QMM Steel already exists")
            bpy.context.object.active_material = m_steel
            return {'FINISHED'}
        else:
            #CreateShader
            m_steel = bpy.data.materials.new(name = "QMM Steel")
            m_steel.use_nodes = True
            m_steel.diffuse_color = (0.42869, 0.527115, 0.590619, 1)
            m_steel.metallic = 1
            m_steel.roughness = 0.25

            nodes = m_steel.node_tree.nodes

            #materialoutput
            material_output = nodes.get('Material Output')
            material_output.location = (0,0)

            #princibledbsdf
            BSDF = nodes.get('Principled BSDF')
            BSDF.location = (-300,0)
            BSDF.inputs[0].default_value = (0.42869, 0.527115, 0.590619, 1)
            BSDF.inputs[4].default_value = 1
            BSDF.inputs[7].default_value = 0.25
            BSDF.inputs[14].default_value = 2.5

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
            m_value.outputs[0].default_value = 2.5
            m_value.label = "IOR"

            links = m_steel.node_tree.links

            links.new(m_value.outputs[0], m_add.inputs[0])
            links.new(m_value.outputs[0], m_subtract.inputs[0])
            links.new(m_add.outputs[0], m_divide2.inputs[1])
            links.new(m_subtract.outputs[0], m_divide2.inputs[0])
            links.new(m_divide2.outputs[0], m_power.inputs[0])
            links.new(m_power.outputs[0], m_divide.inputs[0])
            links.new(m_divide.outputs[0], BSDF.inputs[5])

            bpy.context.object.active_material = m_steel

            return {'FINISHED'}
