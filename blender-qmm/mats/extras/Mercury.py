import bpy

# MESSAGE BOX
message_text = "This material already exists"
def ShowMessageBox(message = "", title = "", icon = 'INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

#MercuryShaderOperator
class QMMMercury(bpy.types.Operator):
    """Add/Apply Liquid Mercury Material to Selected Object (or Scene)"""
    bl_label = "QMM Mercury Liquid Shader"
    bl_idname = 'shader.qmm_mercury_operator'
    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        m_mercury = bpy.data.materials.get("QMM Mercury Liquid")
        if m_mercury:
            ShowMessageBox(message_text, "QMM Mercury Liquid")
            # print(f"QMM Mercury Liquid already exists")
            bpy.context.object.active_material = m_mercury
            return {'FINISHED'}
        else:
            #CreateShader
            m_mercury = bpy.data.materials.new(name = "QMM Mercury Liquid")
            m_mercury.use_nodes = True
            m_mercury.diffuse_color = (0.174647, 0.198069, 0.219526, 1)
            m_mercury.metallic = 1
            m_mercury.roughness = 0.0

            nodes = m_mercury.node_tree.nodes

            #materialoutput
            material_output = nodes.get('Material Output')
            material_output.location = (0,0)

            #princibledbsdf
            BSDF = nodes.get('Principled BSDF')
            BSDF.location = (-300,0)
            BSDF.inputs[0].default_value = (0.174647, 0.198069, 0.219526, 1)
            BSDF.inputs[6].default_value = 1
            BSDF.inputs[9].default_value = 0
            BSDF.inputs[16].default_value = 1.620

            #LOAD THE MATERIAL
            bpy.context.object.active_material = m_mercury

            #SpecularGroup
            bpy.ops.node.specular_group_operator()
            nodes = m_mercury.node_tree.nodes
            specular_group = nodes.new("ShaderNodeGroup")
            specular_group.node_tree = bpy.data.node_groups['Specular']
            specular_group.location = (-500, -300)
            specular_group.inputs[0].default_value = 1.620
            links = m_mercury.node_tree.links.new
            links(specular_group.outputs[0], BSDF.inputs[7])
            links(specular_group.outputs[1], BSDF.inputs[16])

            return {'FINISHED'}
