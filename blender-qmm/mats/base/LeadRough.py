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
        m_lead_rough = bpy.data.materials.get("QMM Lead Rough")
        if m_lead_rough:
            ShowMessageBox(message_text, "QMM Lead Rough")
            # print(f"QMM Lead Rough already exists")
            bpy.context.object.active_material = m_lead_rough
            return {'FINISHED'}
        else:
            #CreateShader
            m_lead_rough = bpy.data.materials.new(name = "QMM Lead Rough")
            m_lead_rough.use_nodes = True
            m_lead_rough.diffuse_color = (0.186, 0.188, 0.196, 1)
            m_lead_rough.metallic = 1
            m_lead_rough.roughness = 0.565

            nodes = m_lead_rough.node_tree.nodes

            #materialoutput
            material_output = nodes.get('Material Output')
            material_output.location = (0,0)

            #principledbsdf
            BSDF = nodes.get('Principled BSDF')
            BSDF.location = (-300,0)
            BSDF.inputs[0].default_value = (0.186, 0.188, 0.196, 1)
            BSDF.inputs[6].default_value = 1
            BSDF.inputs[9].default_value = 0.565
            # BSDF.inputs[16].default_value = 2.010

            #EnergyConservationGroup
            bpy.ops.node.ec_group_operator()
            ec_group = nodes.new("ShaderNodeGroup")
            ec_group.node_tree = bpy.data.node_groups['Energy Conservation']
            ec_group.location = (-500, -200)
            ec_group.inputs[0].default_value = 2.01
            ec_group.inputs[1].default_value = (0.186, 0.188, 0.196, 1)
            ec_group.inputs[2].default_value = (0.01, 0.01, 0.01, 1)

            links = m_lead_rough.node_tree.links.new

            links(ec_group.outputs[0], BSDF.inputs[0])
            links(ec_group.outputs[1], BSDF.inputs[7])
            links(ec_group.outputs[3], BSDF.inputs[16])

            #LOAD THE MATERIAL
            bpy.context.object.active_material = m_lead_rough

        return {'FINISHED'}
