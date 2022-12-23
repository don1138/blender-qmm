import bpy

# MESSAGE BOX
message_text = "This material already exists"

def ShowMessageBox(message="", title="", icon='INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)

# SilverMinShaderOperator

class QMMSilver(bpy.types.Operator):
    """Add/Apply Silver (Minimum) Material to Selected Object (or Scene)"""
    bl_label = "QMM Silver Shader"
    bl_idname = 'shader.qmm_silver_m_operator'

    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        if m_silver_m := bpy.data.materials.get("QMM Silver"):
            ShowMessageBox(message_text, "QMM Silver")
            # print(f"QMM Silver already exists")
            bpy.context.object.active_material = m_silver_m
            return {'FINISHED'}
        else:
            self.make_shader()
        return {'FINISHED'}

    def make_shader(self):
        # CreateShader
        m_silver_m = bpy.data.materials.new(name="QMM Silver")
        m_silver_m.use_nodes = True
        m_silver_m.diffuse_color = (0.962, 0.949, 0.922, 1)
        m_silver_m.metallic = 1
        m_silver_m.roughness = 0.115

        nodes = m_silver_m.node_tree.nodes

        # materialoutput
        material_output = nodes.get('Material Output')
        material_output.location = (0, 0)

        # princibledbsdf
        BSDF = nodes.get('Principled BSDF')
        BSDF.location = (-300, 0)
        # BSDF.inputs[0].default_value = (0.401978, 0.396755, 0.417885, 1)
        BSDF.inputs[0].default_value = (0.962, 0.949, 0.922, 1)
        BSDF.inputs[6].default_value = 1
        BSDF.inputs[9].default_value = 0.115
        BSDF.inputs[16].default_value = 1.082

        # LOAD THE MATERIAL
        bpy.context.object.active_material = m_silver_m

        links = m_silver_m.node_tree.links.new

        # EnergyConservationGroup
        bpy.ops.node.ec_group_operator()
        ec_group = self.make_node(nodes, "Energy Conservation", 'Energy Conservation', -500)
        ec_group.inputs[0].default_value = 1.082
        ec_group.inputs[1].default_value = (0.964686, 0.947307, 0.921582, 1)
        ec_group.inputs[2].default_value = (0.999, 0.998, 0.998, 1)
        links(ec_group.outputs[0], BSDF.inputs[0])
        links(ec_group.outputs[1], BSDF.inputs[7])
        links(ec_group.outputs[3], BSDF.inputs[16])

        # SilverColorsGroup
        bpy.ops.node.silver_cg_operator()
        nodes = m_silver_m.node_tree.nodes
        silver_cg = self.make_node(nodes, "Silver Colors", 'Silver Colors', -700)

        links(silver_cg.outputs[2], ec_group.inputs[1])

    def make_node(self, nodes, arg1, arg2, arg3):
        result = nodes.new("ShaderNodeGroup")
        result.name = arg1
        result.node_tree = bpy.data.node_groups[arg2]
        result.location = arg3, -200
        return result
