import bpy

# MESSAGE BOX
message_text = "This material already exists"
def ShowMessageBox(message = "", title = "", icon = 'INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

#GoldShaderOperator
class QMMPaleGold(bpy.types.Operator):
    """Add/Apply Pale Gold Material to Selected Object (or Scene)"""
    bl_label = "QMM Pale Gold Shader"
    bl_idname = 'shader.qmm_pale_gold_m_operator'
    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        m_pale_gold_m = bpy.data.materials.get("QMM Pale Gold")
        if m_pale_gold_m:
            ShowMessageBox(message_text, "QMM Pale Gold")
            # print(f"QMM Pale Gold already exists")
            bpy.context.object.active_material = m_pale_gold_m
            return {'FINISHED'}
        else:
            #CreateShader
            m_pale_gold_m = bpy.data.materials.new(name = "QMM Pale Gold")
            m_pale_gold_m.use_nodes = True
            m_pale_gold_m.diffuse_color = (1.0, 0.766, 0.336, 1)
            m_pale_gold_m.metallic = 1
            m_pale_gold_m.roughness = 0.25

            nodes = m_pale_gold_m.node_tree.nodes

            #materialoutput
            material_output = nodes.get('Material Output')
            material_output.location = (0,0)

            #princibledbsdf
            BSDF = nodes.get('Principled BSDF')
            BSDF.location = (-300,0)
            BSDF.inputs[0].default_value = (1.0, 0.766, 0.336, 1)
            BSDF.inputs[6].default_value = 1
            BSDF.inputs[9].default_value = 0.25
            # BSDF.inputs[16].default_value = 0.47

            #LOAD THE MATERIAL
            bpy.context.object.active_material = m_pale_gold_m

            #SpecularGroup
            bpy.ops.node.specular_group_operator()
            nodes = m_pale_gold_m.node_tree.nodes
            specular_group = nodes.new("ShaderNodeGroup")
            specular_group.node_tree = bpy.data.node_groups['Specular']
            specular_group.location = (-500, -300)
            specular_group.inputs[0].default_value = 0.47
            links = m_pale_gold_m.node_tree.links.new
            links(specular_group.outputs[0], BSDF.inputs[7])
            links(specular_group.outputs[1], BSDF.inputs[16])

            #GoldColorsGroup
            bpy.ops.node.gold_colors_group_operator()
            nodes = m_pale_gold_m.node_tree.nodes
            gold_colors_group = nodes.new("ShaderNodeGroup")
            gold_colors_group.node_tree = bpy.data.node_groups['Gold Colors']
            gold_colors_group.location = (-500, 0)
            links = m_pale_gold_m.node_tree.links.new
            links(gold_colors_group.outputs[1], BSDF.inputs[0])

        return {'FINISHED'}
