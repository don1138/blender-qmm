import bpy

# MESSAGE BOX
message_text = "This material already exists"


def ShowMessageBox(message="", title="", icon='INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)

# ChromeShaderOperator


class QMMChrome(bpy.types.Operator):
    """Add/Apply Chrome Material to Selected Object (or Scene)"""
    bl_label = "QMM Chrome Shader"
    bl_idname = 'shader.qmm_chrome_operator'

    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        if m_chrome := bpy.data.materials.get("QMM Chrome"):
            ShowMessageBox(message_text, "QMM Chrome")
            # print(f"QMM Chrome already exists")
            bpy.context.object.active_material = m_chrome
            return {'FINISHED'}
        else:
            self.make_shader()
        return {'FINISHED'}

    def make_shader(self):
        # CreateShader
        m_chrome = bpy.data.materials.new(name="QMM Chrome")
        m_chrome.use_nodes = True
        m_chrome.diffuse_color = (0.262250, 0.270498, 0.266356, 1)
        m_chrome.metallic = 1
        m_chrome.roughness = 0.02

        nodes = m_chrome.node_tree.nodes

        # materialoutput
        material_output = nodes.get('Material Output')
        material_output.location = (0, 0)

        # princibledbsdf
        BSDF = nodes.get('Principled BSDF')
        BSDF.location = (-300, 0)
        BSDF.inputs[0].default_value = (0.262250, 0.270498, 0.266356, 1)
        BSDF.inputs[6].default_value = 1
        BSDF.inputs[9].default_value = 0.02
        BSDF.inputs[16].default_value = 2.3

        # EnergyConservationGroup
        bpy.ops.node.ec_group_operator()
        ec_group = nodes.new("ShaderNodeGroup")
        ec_group.name = "Energy Conservation"
        ec_group.node_tree = bpy.data.node_groups['Energy Conservation']
        ec_group.location = (-500, -200)
        ec_group.inputs[0].default_value = 2.3
        ec_group.inputs[1].default_value = (0.262250, 0.270498, 0.266356, 1)
        ec_group.inputs[2].default_value = (0.283148, 0.270498, 0.434154, 1)

        links = m_chrome.node_tree.links.new

        links(ec_group.outputs[0], BSDF.inputs[0])
        links(ec_group.outputs[1], BSDF.inputs[7])
        links(ec_group.outputs[3], BSDF.inputs[16])

        # LOAD THE MATERIAL
        bpy.context.object.active_material = m_chrome
