import bpy
import time 

bv = bpy.app.version

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
    bl_label  = "QMM Glass Shader"
    bl_idname = 'shader.qmm_glass_operator'

    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        if m_glass := bpy.data.materials.get("QMM Glass"):
            #ShowMessageBox(message_text, "QMM Glass")
            # print(f"QMM Glass already exists")
            bpy.context.object.active_material = m_glass
            diffuse_bool = bpy.context.scene.diffuse_bool.diffuse_more
            m_glass.diffuse_color = (1, 1, 1, 0.5) if diffuse_bool else (0.8, 0.8, 0.8, 1)
            m_glass.roughness = 0 if diffuse_bool else 0.4
            return {'FINISHED'}
        else:
            self.make_shader()
        return {'FINISHED'}

    def make_shader(self):
        start = time.time()

        # CreateShader
        m_glass = bpy.data.materials.new(name="QMM Glass")
        m_glass.use_nodes = True
        diffuse_bool = bpy.context.scene.diffuse_bool.diffuse_more
        if diffuse_bool == True:
            m_glass.diffuse_color = (1, 1, 1, 0.5)
            m_glass.roughness = 0

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

        m_glossy = make_node(nodes, 'ShaderNodeBsdfGlossy', -600, -120)
        m_glossy.inputs[0].default_value = (1, 1, 1, 1)
        m_glossy.inputs[1].default_value = 0
        if bv < (4, 0, 0):
            m_glossy.distribution = 'SHARP'
        else:
            m_glossy.distribution = 'MULTI_GGX'

        m_transparent = make_node(nodes, 'ShaderNodeBsdfTransparent', -600, -300)
        m_transparent.inputs[0].default_value = (1, 1, 1, 1)

        # lightpath
        m_light_path = make_node(nodes, 'ShaderNodeLightPath', -800, 200)

        # mixrgb
        if bv < (3, 4, 0):
            m_mixrgb = make_node(nodes, 'ShaderNodeMixRGB', -800, -300)
            m_mixrgb.inputs[1].default_value = (1.6180339, 1.6180339, 1.6180339, 1)
        else:
            m_mixrgb = make_node(nodes, 'ShaderNodeMix', -800, -300)
            m_mixrgb.data_type = 'RGBA'
            m_mixrgb.inputs[6].default_value = (1.6180339, 1.6180339, 1.6180339, 1)
        m_mixrgb.inputs[0].default_value = 0.38196

        # noise
        m_noise = make_node(nodes, 'ShaderNodeTexNoise', -1000, -300)
        m_noise.inputs[2].default_value = 3.14159
        m_noise.inputs[3].default_value = 0
        m_noise.inputs[4].default_value = 1

        links = m_glass.node_tree.links.new

        if bv < (3, 4, 0):
            links(m_noise.outputs[0], m_mixrgb.inputs[2])
            links(m_mixrgb.outputs[0], m_transparent.inputs[0])
        else:
            links(m_noise.outputs[0], m_mixrgb.inputs[7])
            links(m_mixrgb.outputs[2], m_transparent.inputs[0])

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
        if bv < (4, 3, 0):
            bpy.context.object.active_material.blend_method = 'BLEND'
            bpy.context.object.active_material.shadow_method = 'NONE'
        else:
            bpy.context.object.active_material.surface_render_method = 'BLENDED'

        end = time.time()
        print(f"QMM Glass: {end - start} seconds")
