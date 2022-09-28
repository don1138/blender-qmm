import bpy

# MESSAGE BOX
message_text = "This material already exists"
def ShowMessageBox(message = "", title = "", icon = 'INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

#CopperShaderOperator
class QMMCopper(bpy.types.Operator):
    """Add/Apply Pale Copper (Minimum) Material to Selected Object (or Scene)"""
    bl_label = "QMM Copper Shader"
    bl_idname = 'shader.qmm_copper_m_operator'
    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        m_copper_m = bpy.data.materials.get("QMM Copper")
        if m_copper_m:
            ShowMessageBox(message_text, "QMM Copper")
            # print(f"QMM Copper already exists")
            bpy.context.object.active_material = m_copper_m
            return {'FINISHED'}
        else:
            #CreateShader
            m_copper_m = bpy.data.materials.new(name = "QMM Copper")
            m_copper_m.use_nodes = True
            m_copper_m.diffuse_color = (0.701102, 0.254152, 0.135633, 1)
            m_copper_m.metallic = 1
            m_copper_m.roughness = 0.4

            nodes = m_copper_m.node_tree.nodes

            #materialoutput
            material_output = nodes.get('Material Output')
            material_output.location = (0,0)

            #princibledbsdf
            BSDF = nodes.get('Principled BSDF')
            BSDF.location = (-300,0)
            # BSDF.inputs[0].default_value = (0.701102, 0.254152, 0.135633, 1)
            BSDF.inputs[0].default_value = (0.926, 0.721, 0.504, 1)
            BSDF.inputs[6].default_value = 1
            BSDF.inputs[9].default_value = 0.4
            # BSDF.inputs[16].default_value = 1.10

            #EnergyConservationGroup
            bpy.ops.node.ec_group_operator()
            ec_group = nodes.new("ShaderNodeGroup")
            ec_group.node_tree = bpy.data.node_groups['Energy Conservation']
            ec_group.location = (-500, -200)
            ec_group.inputs[0].default_value = 1.10
            ec_group.inputs[1].default_value = (0.926, 0.721, 0.504, 1)
            ec_group.inputs[2].default_value = (0.01, 0.01, 0.01, 1)

            #CopperColorsGroup
            bpy.ops.node.copper_colors_group_operator()
            nodes = m_copper_m.node_tree.nodes
            copper_colors_group = nodes.new("ShaderNodeGroup")
            copper_colors_group.node_tree = bpy.data.node_groups['Copper Colors']
            copper_colors_group.location = (-700, -300)

            links = m_copper_m.node_tree.links.new

            links(copper_colors_group.outputs[0], ec_group.inputs[1])
            links(ec_group.outputs[0], BSDF.inputs[0])
            links(ec_group.outputs[1], BSDF.inputs[7])
            links(ec_group.outputs[3], BSDF.inputs[16])

            #LOAD THE MATERIAL
            bpy.context.object.active_material = m_copper_m

        return {'FINISHED'}
