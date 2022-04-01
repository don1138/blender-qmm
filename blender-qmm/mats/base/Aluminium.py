import bpy

# MESSAGE BOX
message_text = "This material already exists"
def ShowMessageBox(message = "", title = "", icon = 'INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

#AluminiumShaderOperator
class QMMAluminium(bpy.types.Operator):
    """Add/Apply Aluminium Material to Selected Object (or Scene)"""
    bl_label = "QMM Aluminium Shader"
    bl_idname = 'shader.qmm_aluminium_operator'
    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        m_aluminium = bpy.data.materials.get("QMM Aluminium")
        if m_aluminium:
            ShowMessageBox(message_text, "QMM Aluminium")
            # print(f"QMM Aluminium already exists")
            bpy.context.object.active_material = m_aluminium
            return {'FINISHED'}
        else:
            #CreateShader
            m_aluminium = bpy.data.materials.new(name = "QMM Aluminium")
            m_aluminium.use_nodes = True
            m_aluminium.diffuse_color = (0.23074, 0.242281, 0.250158, 1)
            m_aluminium.metallic = 1
            m_aluminium.roughness = 0.3

            nodes = m_aluminium.node_tree.nodes

            #materialoutput
            material_output = nodes.get('Material Output')
            material_output.location = (0,0)

            #princibledbsdf
            BSDF = nodes.get('Principled BSDF')
            BSDF.location = (-300,0)
            BSDF.inputs[0].default_value = (0.23074, 0.242281, 0.250158, 1)
            BSDF.inputs[6].default_value = 1
            BSDF.inputs[9].default_value = 0.3
            # BSDF.inputs[16].default_value = 1.390
            # BSDF.inputs[16].default_value = 1.244

            #LOAD THE MATERIAL
            bpy.context.object.active_material = m_aluminium

            #SpecularGroup
            bpy.ops.node.specular_group_operator()
            nodes = m_aluminium.node_tree.nodes
            specular_group = nodes.new("ShaderNodeGroup")
            specular_group.node_tree = bpy.data.node_groups['Specular']
            specular_group.location = (-500, -300)
            specular_group.inputs[0].default_value = 1.44
            links = m_aluminium.node_tree.links.new
            links(specular_group.outputs[0], BSDF.inputs[7])
            links(specular_group.outputs[1], BSDF.inputs[16])

        return {'FINISHED'}
