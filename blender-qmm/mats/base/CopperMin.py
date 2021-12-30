import bpy

# MESSAGE BOX
message_text = "This material already exists"
def ShowMessageBox(message = "", title = "", icon = 'INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

#CopperMinShaderOperator
class QMMCopperMin(bpy.types.Operator):
    """Add/Apply Pale Copper (Minimum) Material to Selected Object (or Scene)"""
    bl_label = "QMM Pale Copper Min Shader"
    bl_idname = 'shader.qmm_copper_min_operator'
    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        m_copper_min = bpy.data.materials.get("QMM Pale Copper Min")
        if m_copper_min:
            ShowMessageBox(message_text, "QMM Pale Copper Min")
            # print(f"QMM Pale Copper Min already exists")
            bpy.context.object.active_material = m_copper_min
            return {'FINISHED'}
        else:
            #CreateShader
            m_copper_min = bpy.data.materials.new(name = "QMM Pale Copper Min")
            m_copper_min.use_nodes = True
            m_copper_min.diffuse_color = (0.701102, 0.254152, 0.135633, 1)
            m_copper_min.metallic = 1
            m_copper_min.roughness = 0.25

            nodes = m_copper_min.node_tree.nodes

            #materialoutput
            material_output = nodes.get('Material Output')
            material_output.location = (0,0)

            #princibledbsdf
            BSDF = nodes.get('Principled BSDF')
            BSDF.location = (-300,0)
            BSDF.inputs[0].default_value = (0.701102, 0.254152, 0.135633, 1)
            BSDF.inputs[6].default_value = 1
            BSDF.inputs[9].default_value = 0.25
            # BSDF.inputs[16].default_value = 1.10

            #LOAD THE MATERIAL
            bpy.context.object.active_material = m_copper_min

            #SpecularGroup
            bpy.ops.node.specular_group_operator()
            nodes = m_copper_min.node_tree.nodes
            specular_group = nodes.new("ShaderNodeGroup")
            specular_group.node_tree = bpy.data.node_groups['Specular']
            specular_group.location = (-500, -300)
            specular_group.inputs[0].default_value = 1.10
            links = m_copper_min.node_tree.links.new
            links(specular_group.outputs[0], BSDF.inputs[7])
            links(specular_group.outputs[1], BSDF.inputs[16])

            return {'FINISHED'}
