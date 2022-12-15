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
        if m_copper_m := bpy.data.materials.get("QMM Copper"):
            ShowMessageBox(message_text, "QMM Copper")
            # print(f"QMM Copper already exists")
            bpy.context.object.active_material = m_copper_m
            return {'FINISHED'}
        else:
            self.make_shader()
        return {'FINISHED'}

    # TODO Rename this here and in `execute`
    def make_shader(self):
        #CreateShader
        m_copper_m = bpy.data.materials.new(name = "QMM Copper")
        m_copper_m.use_nodes = True
        m_copper_m.diffuse_color = (0.926, 0.721, 0.504, 1)
        m_copper_m.metallic = 1
        m_copper_m.roughness = 0.35

        nodes = m_copper_m.node_tree.nodes

        #materialoutput
        material_output = nodes.get('Material Output')
        material_output.location = (0,0)

        #princibledbsdf
        BSDF = nodes.get('Principled BSDF')
        BSDF.location = (-300,0)
        BSDF.inputs[0].default_value = (0.926, 0.721, 0.504, 1)
        BSDF.inputs[6].default_value = 1
        BSDF.inputs[9].default_value = 0.35
        BSDF.inputs[16].default_value = 1.10

        #EnergyConservationGroup
        bpy.ops.node.ec_group_operator()
        ec_group = self.make_group_node(
            nodes, 'Energy Conservation', -500, -200
        )
        ec_group.inputs[0].default_value = 1.10
        ec_group.inputs[1].default_value = (0.926, 0.721, 0.504, 1)
        ec_group.inputs[2].default_value = (0.996, 0.957, 0.823, 1)

        ec_group.name = "Energy Conservation"
        #CopperColorsGroup
        bpy.ops.node.copper_colors_group_operator()
        nodes = m_copper_m.node_tree.nodes
        copper_colors_group = self.make_group_node(
            nodes, 'Copper Colors', -700, -300
        )
        links = m_copper_m.node_tree.links.new

        copper_colors_group.name = "Copper Colors"
        links(copper_colors_group.outputs[1], ec_group.inputs[1])
        links(ec_group.outputs[0], BSDF.inputs[0])
        links(ec_group.outputs[1], BSDF.inputs[7])
        links(ec_group.outputs[3], BSDF.inputs[16])

        #LOAD THE MATERIAL
        bpy.context.object.active_material = m_copper_m

    # TODO Rename this here and in `execute`
    def make_group_node(self, nodes, arg1, arg2, arg3):
        result = nodes.new("ShaderNodeGroup")
        result.node_tree = bpy.data.node_groups[arg1]
        result.location = arg2, arg3
        return result
