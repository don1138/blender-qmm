import bpy

# MESSAGE BOX
message_text = "This material already exists"
def ShowMessageBox(message = "", title = "", icon = 'INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

#SilverMinShaderOperator
class QMMSilver(bpy.types.Operator):
    """Add/Apply Silver (Minimum) Material to Selected Object (or Scene)"""
    bl_label = "QMM Silver Shader"
    bl_idname = 'shader.qmm_silver_m_operator'
    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        m_silver_m = bpy.data.materials.get("QMM Silver")
        if m_silver_m:
            ShowMessageBox(message_text, "QMM Silver")
            # print(f"QMM Silver already exists")
            bpy.context.object.active_material = m_silver_m
            return {'FINISHED'}
        else:
            #CreateShader
            m_silver_m = bpy.data.materials.new(name = "QMM Silver")
            m_silver_m.use_nodes = True
            m_silver_m.diffuse_color = (0.401978, 0.396755, 0.417885, 1)
            m_silver_m.metallic = 1
            m_silver_m.roughness = 0.115

            nodes = m_silver_m.node_tree.nodes

            #materialoutput
            material_output = nodes.get('Material Output')
            material_output.location = (0,0)

            #princibledbsdf
            BSDF = nodes.get('Principled BSDF')
            BSDF.location = (-300,0)
            # BSDF.inputs[0].default_value = (0.401978, 0.396755, 0.417885, 1)
            BSDF.inputs[0].default_value = (0.962, 0.949, 0.922, 1)
            BSDF.inputs[6].default_value = 1
            BSDF.inputs[9].default_value = 0.115
            BSDF.inputs[16].default_value = 1.082

            #LOAD THE MATERIAL
            bpy.context.object.active_material = m_silver_m

            links = m_silver_m.node_tree.links.new

            #EnergyConservationGroup
            bpy.ops.node.ec_group_operator()
            ec_group = nodes.new("ShaderNodeGroup")
            ec_group.node_tree = bpy.data.node_groups['Energy Conservation']
            ec_group.location = (-500, -200)
            ec_group.inputs[0].default_value = 1.082
            ec_group.inputs[1].default_value = (0.964686, 0.947307, 0.921582, 1)
            ec_group.inputs[2].default_value = (0.973445, 0.955973, 0.913099, 1)
            links(ec_group.outputs[0], BSDF.inputs[0])
            links(ec_group.outputs[1], BSDF.inputs[7])
            links(ec_group.outputs[3], BSDF.inputs[16])

            #SilverColorsGroup
            bpy.ops.node.silver_colors_group_operator()
            nodes = m_silver_m.node_tree.nodes
            silver_colors_group = nodes.new("ShaderNodeGroup")
            silver_colors_group.node_tree = bpy.data.node_groups['Silver Colors']
            silver_colors_group.location = (-700, -200)
            links(silver_colors_group.outputs[2], ec_group.inputs[1])
            links(silver_colors_group.outputs[1], ec_group.inputs[2])

        return {'FINISHED'}
