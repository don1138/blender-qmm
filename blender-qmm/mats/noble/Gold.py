import bpy

# MESSAGE BOX
message_text = "This material already exists"
def ShowMessageBox(message = "", title = "", icon = 'INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

#GoldShaderOperator
class QMMGold(bpy.types.Operator):
    """Add/Apply Gold Material to Selected Object (or Scene)"""
    bl_label = "QMM Gold Shader"
    bl_idname = 'shader.qmm_gold_m_operator'
    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        m_gold_m = bpy.data.materials.get("QMM Gold")
        if m_gold_m:
            ShowMessageBox(message_text, "QMM Gold")
            # print(f"QMM Gold already exists")
            bpy.context.object.active_material = m_gold_m
            return {'FINISHED'}
        else:
            #CreateShader
            m_gold_m = bpy.data.materials.new(name = "QMM Gold")
            m_gold_m.use_nodes = True
            m_gold_m.diffuse_color = (0.658375, 0.428689, 0.038204, 1)
            m_gold_m.metallic = 1
            m_gold_m.roughness = 0.14

            nodes = m_gold_m.node_tree.nodes

            #materialoutput
            material_output = nodes.get('Material Output')
            material_output.location = (0,0)

            #principledbsdf
            BSDF = nodes.get('Principled BSDF')
            BSDF.location = (-300,0)
            # BSDF.inputs[0].default_value = (1, 0.564711, 0.155927, 1)
            BSDF.inputs[0].default_value = (0.944, 0.776, 0.373, 1)
            BSDF.inputs[6].default_value = 1
            BSDF.inputs[9].default_value = 0.14
            BSDF.inputs[16].default_value = 1.35

            links = m_gold_m.node_tree.links.new

            #EnergyConservationGroup
            bpy.ops.node.ec_group_operator()
            ec_group = nodes.new("ShaderNodeGroup")
            ec_group.node_tree = bpy.data.node_groups['Energy Conservation']
            ec_group.location = (-500, -200)
            ec_group.inputs[0].default_value = 1.35
            ec_group.inputs[1].default_value = (0.947307, 0.775822, 0.371238, 10)
            ec_group.inputs[2].default_value = (0.01, 0.01, 0.01, 1)
            links(ec_group.outputs[0], BSDF.inputs[0])
            links(ec_group.outputs[1], BSDF.inputs[7])
            links(ec_group.outputs[3], BSDF.inputs[16])

            #GoldColorsGroup
            bpy.ops.node.gold_colors_group_operator()
            nodes = m_gold_m.node_tree.nodes
            gold_colors_group = nodes.new("ShaderNodeGroup")
            gold_colors_group.node_tree = bpy.data.node_groups['Gold Colors']
            gold_colors_group.location = (-700, -300)
            links(gold_colors_group.outputs[1], ec_group.inputs[1])

            #LOAD THE MATERIAL
            bpy.context.object.active_material = m_gold_m

        return {'FINISHED'}
