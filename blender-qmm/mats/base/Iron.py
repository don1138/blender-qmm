import bpy

# MESSAGE BOX
message_text = "This material already exists"
def ShowMessageBox(message = "", title = "", icon = 'INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

#IronShaderOperator
class QMMIron(bpy.types.Operator):
    """Add/Apply Iron Material to Selected Object (or Scene)"""
    bl_label = "QMM Iron Shader"
    bl_idname = 'shader.qmm_iron_operator'
    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        m_iron = bpy.data.materials.get("QMM Iron")
        if m_iron:
            ShowMessageBox(message_text, "QMM Iron")
            # print(f"QMM Iron already exists")
            bpy.context.object.active_material = m_iron
            return {'FINISHED'}
        else:
            #CreateShader
            m_iron = bpy.data.materials.new(name = "QMM Iron")
            m_iron.use_nodes = True
            m_iron.diffuse_color = (0.3564, 0.337164, 0.296138, 1)
            m_iron.metallic = 1
            m_iron.roughness = 0.4

            nodes = m_iron.node_tree.nodes

            #materialoutput
            material_output = nodes.get('Material Output')
            material_output.location = (0,0)

            #princibledbsdf
            BSDF = nodes.get('Principled BSDF')
            BSDF.location = (-300,0)
            BSDF.inputs[0].default_value = (0.3564, 0.337164, 0.296138, 1)
            BSDF.inputs[6].default_value = 1
            BSDF.inputs[9].default_value = 0.4
            # BSDF.inputs[16].default_value = 2.950

            #LOAD THE MATERIAL
            bpy.context.object.active_material = m_iron

            #SpecularGroup
            bpy.ops.node.specular_group_operator()
            nodes = m_iron.node_tree.nodes
            specular_group = nodes.new("ShaderNodeGroup")
            specular_group.node_tree = bpy.data.node_groups['Specular']
            specular_group.location = (-500, -300)
            specular_group.inputs[0].default_value = 2.950
            links = m_iron.node_tree.links.new
            links(specular_group.outputs[0], BSDF.inputs[7])
            links(specular_group.outputs[1], BSDF.inputs[16])

        return {'FINISHED'}
