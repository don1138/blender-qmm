import bpy

# MESSAGE BOX
message_text = "This material already exists"
def ShowMessageBox(message = "", title = "", icon = 'INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

#MercuryShaderOperator
class QMMMercury(bpy.types.Operator):
    """Add/Apply Mercury Material to Selected Object (or Scene)"""
    bl_label = "QMM Mercury Shader"
    bl_idname = 'shader.qmm_mercury_operator'
    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        m_mercury = bpy.data.materials.get("QMM Mercury")
        if m_mercury:
            ShowMessageBox(message_text, "QMM Mercury")
            # print(f"QMM Mercury already exists")
            bpy.context.object.active_material = m_mercury
            return {'FINISHED'}
        else:
            #CreateShader
            m_mercury = bpy.data.materials.new(name = "QMM Mercury")
            m_mercury.use_nodes = True
            m_mercury.diffuse_color = (0.781, 0.779, 0.779, 1)
            m_mercury.metallic = 1
            m_mercury.roughness = 0.0

            nodes = m_mercury.node_tree.nodes

            #materialoutput
            material_output = nodes.get('Material Output')
            material_output.location = (0,0)

            #princibledbsdf
            BSDF = nodes.get('Principled BSDF')
            BSDF.location = (-300,0)
            # BSDF.inputs[0].default_value = (0.174647, 0.198069, 0.219526, 1)
            BSDF.inputs[0].default_value = (0.781, 0.779, 0.779, 1)
            BSDF.inputs[6].default_value = 1
            BSDF.inputs[9].default_value = 0
            BSDF.inputs[16].default_value = 1.620

            #EnergyConservationGroup
            bpy.ops.node.ec_group_operator()
            ec_group = nodes.new("ShaderNodeGroup")
            ec_group.node_tree = bpy.data.node_groups['Energy Conservation']
            ec_group.location = (-500, -200)
            ec_group.inputs[0].default_value = 1.62
            ec_group.inputs[1].default_value = (0.781, 0.779, 0.779, 1)
            ec_group.inputs[2].default_value = (0.879, 0.910, 0.941, 1)

            links = m_mercury.node_tree.links.new

            links(ec_group.outputs[0], BSDF.inputs[0])
            links(ec_group.outputs[1], BSDF.inputs[7])
            links(ec_group.outputs[3], BSDF.inputs[16])

            #LOAD THE MATERIAL
            bpy.context.object.active_material = m_mercury

        return {'FINISHED'}
