import bpy

# MESSAGE BOX
message_text = "This material already exists"


def ShowMessageBox(message="", title="", icon='INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)

def make_node(nodes, shader, locX, locY):
    result = nodes.new(shader)
    result.location = (locX, locY)
    return result

# GlassShaderOperator


class QMMGlass(bpy.types.Operator):
    """Add/Apply Glass Material to Selected Object (or Scene)"""
    bl_label = "QMM Glass Hack Shader"
    bl_idname = 'shader.qmm_glass_operator'

    def execute(self, context):
        if m_glass := bpy.data.materials.get("QMM Glass Hack"):
            ShowMessageBox(message_text, "QMM Glass Hack")
            # print(f"QMM Glass Hack already exists")
            bpy.context.object.active_material = m_glass
            return {'FINISHED'}
        else:
            self.make_shader()
        return {'FINISHED'}

    def make_shader(self):
        # CreateShader
        m_glass = bpy.data.materials.new(name="QMM Glass Hack")
        m_glass.use_nodes = True
        m_glass.diffuse_color = (1, 1, 1, 0.5)

        nodes = m_glass.node_tree.nodes

        # materialoutput
        material_output = nodes.get('Material Output')
        material_output.location = (0, 0)

        # princibledbsdf
        BSDF = nodes.get('Principled BSDF')
        nodes.remove(BSDF)

        # mixshader
        m_mix = make_node(nodes, 'ShaderNodeMixShader', -200, 0)

        # mathadd
        m_add = make_node(nodes, 'ShaderNodeMath', -400, 200)
        m_add.operation = 'ADD'

        # mixshader2
        m_mix2 = make_node(nodes, 'ShaderNodeMixShader', -400, 0)

        # mathadd2
        m_add2 = make_node(nodes, 'ShaderNodeMath', -600, 300)
        m_add2.operation = 'ADD'

        # fresnel
        m_fresnel = make_node(nodes, 'ShaderNodeFresnel', -600, 0)
        m_fresnel.inputs[0].default_value = 40

        # glossyshader
        m_glossy = make_node(nodes, 'ShaderNodeBsdfGlossy', -600, -120)

        # transparentshader
        m_transparent = make_node(nodes, 'ShaderNodeBsdfTransparent', -600, -300)
        m_transparent.inputs[0].default_value = (0.9, 0.9, 1, 1)

        # lightpath
        m_light_path = make_node(nodes, 'ShaderNodeLightPath', -800, 200)

        links = m_glass.node_tree.links.new

        links(m_transparent.outputs[0], m_mix2.inputs[2])
        links(m_glossy.outputs[0], m_mix2.inputs[1])
        links(m_fresnel.outputs[0], m_mix2.inputs[0])
        links(m_light_path.outputs[2], m_add2.inputs[1])
        links(m_light_path.outputs[1], m_add2.inputs[0])
        links(m_light_path.outputs[3], m_add.inputs[1])
        links(m_add2.outputs[0], m_add.inputs[0])
        links(m_transparent.outputs[0], m_mix.inputs[2])
        links(m_mix2.outputs[0], m_mix.inputs[1])
        links(m_add.outputs[0], m_mix.inputs[0])
        links(m_mix.outputs[0], material_output.inputs[0])

        bpy.context.object.active_material = m_glass
