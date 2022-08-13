import bpy

# MESSAGE BOX
message_text = "This material already exists"
def ShowMessageBox(message = "", title = "", icon = 'INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

#ChromeShaderOperator
class QMMChrome(bpy.types.Operator):
    """Add/Apply Chrome Material to Selected Object (or Scene)"""
    bl_label = "QMM Chrome Shader"
    bl_idname = 'shader.qmm_chrome_operator'
    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        m_chrome = bpy.data.materials.get("QMM Chrome")
        if m_chrome:
            ShowMessageBox(message_text, "QMM Chrome")
            # print(f"QMM Chrome already exists")
            bpy.context.object.active_material = m_chrome
            return {'FINISHED'}
        else:
            #CreateShader
            m_chrome = bpy.data.materials.new(name = "QMM Chrome")
            m_chrome.use_nodes = True
            m_chrome.diffuse_color = (1.0, 1.0, 1.0,1.0)
            m_chrome.metallic = 1
            m_chrome.roughness = 0.012

            nodes = m_chrome.node_tree.nodes

            #materialoutput
            material_output = nodes.get('Material Output')
            material_output.location = (0,0)

            #princibledbsdf
            BSDF = nodes.get('Principled BSDF')
            BSDF.location = (-300,0)
            BSDF.inputs[0].default_value = (0.552011, 0.558340, 0.552011, 1.0)
            BSDF.inputs[6].default_value = 1
            BSDF.inputs[9].default_value = 0.012
            BSDF.inputs[16].default_value = 2.37

            #LOAD THE MATERIAL
            bpy.context.object.active_material = m_chrome

            #SpecularGroup
            bpy.ops.node.specular_group_operator()
            nodes = m_chrome.node_tree.nodes
            specular_group = nodes.new("ShaderNodeGroup")
            specular_group.node_tree = bpy.data.node_groups['Specular']
            specular_group.location = (-500, -300)
            specular_group.inputs[0].default_value = 2.37
            links = m_chrome.node_tree.links.new
            links(specular_group.outputs[0], BSDF.inputs[7])
            links(specular_group.outputs[1], BSDF.inputs[16])

        return {'FINISHED'}
