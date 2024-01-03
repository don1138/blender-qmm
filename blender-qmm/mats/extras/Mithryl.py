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

# MithrylShaderOperator

class QMMMithryl(bpy.types.Operator):
    """Add/Apply Tinted Mithryl Material to Selected Object (or Scene)"""
    bl_label  = "QMM Mithryl Shader"
    bl_idname = 'shader.qmm_mithryl_operator'

    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        if m_mithryl := bpy.data.materials.get("QMM Mithryl"):
            ShowMessageBox(message_text, "QMM Mithryl")
            # print(f"QMM Mithryl already exists")
            bpy.context.object.active_material = m_mithryl
            return {'FINISHED'}
        else:
            self.make_shader()
        return {'FINISHED'}

    def make_shader(self):
        start = time.time()

        # CreateShader
        m_mithryl = bpy.data.materials.new(name="QMM Mithryl")
        m_mithryl.use_nodes = True
        m_mithryl.diffuse_color = (0.590619, 0.625682, 0.679542, 1)
        m_mithryl.roughness = 0.075
        m_mithryl.metallic = 1

        nodes = m_mithryl.node_tree.nodes

        # materialoutput
        material_output = nodes.get('Material Output')
        material_output.location = (0, 0)

        # principledbsdf - stone
        BSDF = nodes.get('Principled BSDF')
        BSDF.distribution = 'MULTI_GGX'
        BSDF.location = (-300, 0)
        BSDF.inputs[0].default_value = (0.590619, 0.625682, 0.679542, 1)
        if bpy.app.version < (4, 0, 0):
            BSDF.inputs[6].default_value = 1
            BSDF.inputs[9].default_value = 0.075
            BSDF.inputs[19].default_value = (0.590619, 0.625682, 0.679542, 1)
        else:
            BSDF.inputs[1].default_value = 1
            BSDF.inputs[2].default_value = 0.075
            BSDF.inputs[26].default_value = (0.590619, 0.625682, 0.679542, 1)
        # BSDF.select = True

        # mixshader
        if bpy.app.version < (4, 0, 0):
            m_mixshader = make_node(nodes, 'ShaderNodeMixShader', -500, 0)
        else:
            m_mixshader = make_node(nodes, 'ShaderNodeMix', -500, 0)
        m_mixshader.data_type = 'RGBA'
        m_mixshader.inputs[7].default_value = (0.590619, 0.625682, 0.679542, 1)

        # maprange
        m_maprange = make_node(nodes, 'ShaderNodeMapRange', -500, -400)
        m_maprange.width = 140
        m_maprange.inputs[1].default_value = 0.666667
        m_maprange.inputs[4].default_value = 0.16

        # maprange2
        m_maprange2 = make_node(nodes, 'ShaderNodeMapRange', -700, 0)
        m_maprange2.width = 140
        m_maprange2.inputs[1].default_value = 0.3
        m_maprange2.inputs[2].default_value = 0.7

        # mixshader2
        if bpy.app.version < (4, 0, 0):
            m_mixshader2 = make_node(nodes, 'ShaderNodeMixShader', -700, -300)
        else:
            m_mixshader2 = make_node(nodes, 'ShaderNodeMix', -700, -300)
        m_mixshader2.data_type = 'RGBA'
        m_mixshader2.inputs[0].default_value = 0.333
        m_mixshader2.inputs[7].default_value = (0.590619, 0.625682, 0.679542, 1)

        # power
        m_power = make_node(nodes, 'ShaderNodeMath', -900, -100)
        m_power.operation = 'POWER'
        m_power.inputs[1].default_value = 2
        m_power.use_clamp = True

        # colorramp
        m_colorramp = make_node(nodes, 'ShaderNodeValToRGB', -1000, -300)
        m_colorramp.color_ramp.interpolation = 'B_SPLINE'
        # Ensure there are enough elements in the color ramp
        while len(m_colorramp.color_ramp.elements) < 4:
            m_colorramp.color_ramp.elements.new(0.0)
        m_colorramp.color_ramp.elements[0].color = (0.973445, 0.955973, 0.913099, 1)
        m_colorramp.color_ramp.elements[0].position = 0
        m_colorramp.color_ramp.elements[1].color = (0, 0.900000, 0.703024, 1)
        m_colorramp.color_ramp.elements[1].position = 0.1
        m_colorramp.color_ramp.elements[2].color = (0.333333, 1, 1, 1)
        m_colorramp.color_ramp.elements[2].position = 0.12
        m_colorramp.color_ramp.elements[3].color = (0.590619, 0.625682, 0.679542, 1)
        m_colorramp.color_ramp.elements[3].position = 1

        # layerweight
        m_layerweight = make_node(nodes, 'ShaderNodeLayerWeight', -1200, -100)
        m_layerweight.inputs[0].default_value = 0.9

        # layerweight2
        m_layerweight2 = make_node(nodes, 'ShaderNodeLayerWeight', -1200, -500)

        links = m_mithryl.node_tree.links.new

        links(m_layerweight2.outputs[1], m_colorramp.inputs[0])
        links(m_layerweight2.outputs[1], m_maprange.inputs[0])
        links(m_layerweight.outputs[1], m_power.inputs[0])
        links(m_power.outputs[0], m_maprange2.inputs[0])
        if bpy.app.version < (4, 0, 0):
            links(m_colorramp.outputs[0], m_mixshader2.inputs[1])
            links(m_mixshader2.outputs[0], m_mixshader.inputs[1])
            links(m_maprange2.outputs[0], m_mixshader.inputs[0])
            links(m_maprange.outputs[0], BSDF.inputs[19])
            links(m_mixshader.outputs[0], BSDF.inputs[0])
        else:
            links(m_colorramp.outputs[0], m_mixshader2.inputs[6])
            links(m_mixshader2.outputs[2], m_mixshader.inputs[6])
            links(m_maprange2.outputs[0], m_mixshader.inputs[0])
            links(m_maprange.outputs[0], BSDF.inputs[26])
            links(m_mixshader.outputs[2], BSDF.inputs[0])

        bpy.context.object.active_material = m_mithryl

        end = time.time()
        print(f"QMM Mithryl: {end - start} seconds")
