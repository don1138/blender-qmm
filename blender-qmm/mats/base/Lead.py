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
            m_lead.diffuse_color = (0.658374, 0.665387, 0.693872, 1)
            m_lead.metallic = 1
            m_lead.roughness = 0.7

            nodes = m_lead.node_tree.nodes

            #materialoutput
            material_output = nodes.get('Material Output')
            material_output.location = (0,0)

            #princibledbsdf
            BSDF = nodes.get('Principled BSDF')
            BSDF.location = (-300,0)
            BSDF.inputs[0].default_value = (0.658374, 0.665387, 0.693872, 1)
            BSDF.inputs[6].default_value = 1
            BSDF.inputs[9].default_value = 0.7
            BSDF.inputs[16].default_value = 2.01

            #EnergyConservationGroup
            bpy.ops.node.ec_group_operator()
            ec_group = nodes.new("ShaderNodeGroup")
            ec_group.name = "Energy Conservation"
            ec_group.node_tree = bpy.data.node_groups['Energy Conservation']
            ec_group.location = (-500, -200)
            ec_group.inputs[0].default_value = 2.01
            ec_group.inputs[1].default_value = (0.658374, 0.665387, 0.693872, 1)
            ec_group.inputs[2].default_value = (0.803, 0.808, 0.862, 1)

            links = m_lead.node_tree.links.new

            links(ec_group.outputs[0], BSDF.inputs[0])
            links(ec_group.outputs[1], BSDF.inputs[7])
            links(ec_group.outputs[3], BSDF.inputs[16])

            #LOAD THE MATERIAL
            bpy.context.object.active_material = m_lead

        return {'FINISHED'}
