import bpy

# MESSAGE BOX
message_text = "This material already exists"
def ShowMessageBox(message = "", title = "", icon = 'INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

#CopperMaxShaderOperator
class QMMCopperMax(bpy.types.Operator):
    """Add/Apply Pale Copper (Maximum) Material to Selected Object (or Scene)"""
    bl_label = "QMM Pale Copper Max Shader"
    bl_idname = 'shader.qmm_copper_max_operator'
    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        m_copper_max = bpy.data.materials.get("QMM Pale Copper Max")
        if m_copper_max:
            ShowMessageBox(message_text, "QMM Pale Copper Max")
            # print(f"QMM Pale Copper Max already exists")
            bpy.context.object.active_material = m_copper_max
            return {'FINISHED'}
        else:
            #CreateShader
            m_copper_max = bpy.data.materials.new(name = "QMM Pale Copper Max")
            m_copper_max.use_nodes = True
            m_copper_max.diffuse_color = (0.701102, 0.254152, 0.135633, 1)
            m_copper_max.metallic = 1
            m_copper_max.roughness = 0.4

            nodes = m_copper_max.node_tree.nodes

            #materialoutput
            material_output = nodes.get('Material Output')
            material_output.location = (0,0)

            #princibledbsdf
            BSDF = nodes.get('Principled BSDF')
            BSDF.location = (-300,0)
            BSDF.inputs[0].default_value = (0.701102, 0.254152, 0.135633, 1)
            BSDF.inputs[6].default_value = 1
            BSDF.inputs[9].default_value = 0.4
            # BSDF.inputs[16].default_value = 2.430

            #LOAD THE MATERIAL
            bpy.context.object.active_material = m_copper_max

            #SpecularGroup
            bpy.ops.node.specular_group_operator()
            nodes = m_copper_max.node_tree.nodes
            specular_group = nodes.new("ShaderNodeGroup")
            specular_group.node_tree = bpy.data.node_groups['Specular']
            specular_group.location = (-500, -300)
            specular_group.inputs[0].default_value = 2.430
            links = m_copper_max.node_tree.links.new
            links(specular_group.outputs[0], BSDF.inputs[7])
            links(specular_group.outputs[1], BSDF.inputs[16])

            #CopperColorsGroup
            bpy.ops.node.copper_colors_group_operator()
            nodes = m_copper_max.node_tree.nodes
            copper_colors_group = nodes.new("ShaderNodeGroup")
            copper_colors_group.node_tree = bpy.data.node_groups['Copper Colors']
            copper_colors_group.location = (-500, 0)
            links = m_copper_max.node_tree.links.new
            links(copper_colors_group.outputs[1], BSDF.inputs[0])

        return {'FINISHED'}
