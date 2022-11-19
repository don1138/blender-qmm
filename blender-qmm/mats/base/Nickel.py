import bpy

# MESSAGE BOX
message_text = "This material already exists"
def ShowMessageBox(message = "", title = "", icon = 'INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

#NickelShaderOperator
class QMMNickel(bpy.types.Operator):
    """Add/Apply Nickel Material to Selected Object (or Scene)"""
    bl_label = "QMM Nickel Shader"
    bl_idname = 'shader.qmm_nickel_operator'
    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        if m_nickel := bpy.data.materials.get("QMM Nickel"):
            ShowMessageBox(message_text, "QMM Nickel")
            # print(f"QMM Nickel already exists")
            bpy.context.object.active_material = m_nickel
            return {'FINISHED'}
        else:
            #CreateShader
            m_nickel = bpy.data.materials.new(name = "QMM Nickel")
            m_nickel.use_nodes = True
            m_nickel.diffuse_color = (0.649, 0.610, 0.541, 1)
            m_nickel.metallic = 1
            m_nickel.roughness = 0.35

            nodes = m_nickel.node_tree.nodes

            #materialoutput
            material_output = nodes.get('Material Output')
            material_output.location = (0,0)

            #princibledbsdf
            BSDF = nodes.get('Principled BSDF')
            BSDF.location = (-300,0)
            BSDF.inputs[0].default_value = (0.649, 0.610, 0.541, 1)
            BSDF.inputs[6].default_value = 1
            BSDF.inputs[9].default_value = 0.35
            BSDF.inputs[16].default_value = 1.08

            #EnergyConservationGroup
            bpy.ops.node.ec_group_operator()
            ec_group = nodes.new("ShaderNodeGroup")
            ec_group.name = "Energy Conservation"
            ec_group.node_tree = bpy.data.node_groups['Energy Conservation']
            ec_group.location = (-500, -200)
            ec_group.inputs[0].default_value = 1.08
            ec_group.inputs[1].default_value = (0.649, 0.610, 0.541, 1)
            ec_group.inputs[2].default_value = (0.803, 0.808, 0.862, 1)

            links = m_nickel.node_tree.links.new

            links(ec_group.outputs[0], BSDF.inputs[0])
            links(ec_group.outputs[1], BSDF.inputs[7])
            links(ec_group.outputs[3], BSDF.inputs[16])

            #LOAD THE MATERIAL
            bpy.context.object.active_material = m_nickel

        return {'FINISHED'}
