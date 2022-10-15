import bpy

# MESSAGE BOX
message_text = "This material already exists"
def ShowMessageBox(message = "", title = "", icon = 'INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

#ZincShaderOperator
class QMMZinc(bpy.types.Operator):
    """Add/Apply Zinc Material to Selected Object (or Scene)"""
    bl_label = "QMM Zinc Shader"
    bl_idname = 'shader.qmm_zinc_operator'
    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        m_zinc = bpy.data.materials.get("QMM Zinc")
        if m_zinc:
            ShowMessageBox(message_text, "QMM Zinc")
            # print(f"QMM Zinc already exists")
            bpy.context.object.active_material = m_zinc
            return {'FINISHED'}
        else:
            #CreateShader
            m_zinc = bpy.data.materials.new(name = "QMM Zinc")
            m_zinc.use_nodes = True
            m_zinc.diffuse_color = (0.737911, 0.723055, 0.701102, 1)
            m_zinc.metallic = 1
            m_zinc.roughness = 0.3

            nodes = m_zinc.node_tree.nodes

            #materialoutput
            material_output = nodes.get('Material Output')
            material_output.location = (0,0)

            #principledbsdf
            BSDF = nodes.get('Principled BSDF')
            BSDF.location = (-300,0)
            BSDF.inputs[0].default_value = (0.491020, 0.552011, 0.577580, 1)
            BSDF.inputs[6].default_value = 1
            BSDF.inputs[9].default_value = 0.3
            BSDF.inputs[16].default_value = 1.517
            # BSDF.inputs[16].default_value = 2.368

            #EnergyConservationGroup
            bpy.ops.node.ec_group_operator()
            ec_group = nodes.new("ShaderNodeGroup")
            ec_group.node_tree = bpy.data.node_groups['Energy Conservation']
            ec_group.location = (-500, -200)
            ec_group.inputs[0].default_value = 1.517
            ec_group.inputs[1].default_value = (0.491020, 0.552011, 0.577580, 1)
            ec_group.inputs[2].default_value = (0.01, 0.01, 0.01, 1)

            links = m_zinc.node_tree.links.new

            links(ec_group.outputs[0], BSDF.inputs[0])
            links(ec_group.outputs[1], BSDF.inputs[7])
            links(ec_group.outputs[3], BSDF.inputs[16])

            #LOAD THE MATERIAL
            bpy.context.object.active_material = m_zinc

        return {'FINISHED'}
