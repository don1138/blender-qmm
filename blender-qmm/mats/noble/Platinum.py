import bpy

# MESSAGE BOX
message_text = "This material already exists"
def ShowMessageBox(message = "", title = "", icon = 'INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

#PlatinumShaderOperator
class QMMPlatinum(bpy.types.Operator):
    """Add/Apply Platinum Material to Selected Object (or Scene)"""
    bl_label = "QMM Platinum Shader"
    bl_idname = 'shader.qmm_platinum_operator'
    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        if m_platinum := bpy.data.materials.get("QMM Platinum"):
            ShowMessageBox(message_text, "QMM Platinum")
            # print(f"QMM Platinum already exists")
            bpy.context.object.active_material = m_platinum
            return {'FINISHED'}
        else:
            #CreateShader
            m_platinum = bpy.data.materials.new(name = "QMM Platinum")
            m_platinum.use_nodes = True
            m_platinum.diffuse_color = (0.679, 0.642, 0.588, 1)
            m_platinum.metallic = 1
            m_platinum.roughness = 0.11

            nodes = m_platinum.node_tree.nodes

            #materialoutput
            material_output = nodes.get('Material Output')
            material_output.location = (0,0)

            #principledbsdf
            BSDF = nodes.get('Principled BSDF')
            BSDF.location = (-300,0)
            BSDF.inputs[0].default_value = (0.679, 0.642, 0.588, 1)
            BSDF.inputs[6].default_value = 1
            BSDF.inputs[9].default_value = 0.11
            BSDF.inputs[16].default_value = 2.33

            #EnergyConservationGroup
            bpy.ops.node.ec_group_operator()
            ec_group = nodes.new("ShaderNodeGroup")
            ec_group.name = "Energy Conservation"
            ec_group.node_tree = bpy.data.node_groups['Energy Conservation']
            ec_group.location = (-500, -200)
            ec_group.inputs[0].default_value = 2.33
            ec_group.inputs[1].default_value = (0.679, 0.642, 0.588, 1)
            ec_group.inputs[2].default_value = (0.785, 0.789, 0.784, 1)

            links = m_platinum.node_tree.links.new

            links(ec_group.outputs[0], BSDF.inputs[0])
            links(ec_group.outputs[1], BSDF.inputs[7])
            links(ec_group.outputs[3], BSDF.inputs[16])

            #LOAD THE MATERIAL
            bpy.context.object.active_material = m_platinum

        return {'FINISHED'}
