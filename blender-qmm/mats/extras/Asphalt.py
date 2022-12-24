import bpy
import time 

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

def set_ec(nodes, locX, locY, ior, diff, spec):
    result = nodes.new("ShaderNodeGroup")
    result.name = "Energy Conservation"
    result.node_tree = bpy.data.node_groups['Energy Conservation']
    result.location = (locX, locY)
    result.inputs[0].default_value = ior
    result.inputs[1].default_value = diff
    result.inputs[3].default_value = spec
    return result

# AsphaltShaderOperator


class QMMAsphalt(bpy.types.Operator):
    """Add/Apply Tinted Asphalt Material to Selected Object (or Scene)"""
    bl_label = "QMM Asphalt Shader"
    bl_idname = 'shader.qmm_asphalt_operator'

    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        if m_asphalt := bpy.data.materials.get("QMM Asphalt"):
            ShowMessageBox(message_text, "QMM Asphalt")
            # print(f"QMM Asphalt already exists")
            bpy.context.object.active_material = m_asphalt
            return {'FINISHED'}
        else:
            self.make_shader()
        return {'FINISHED'}

    def make_shader(self):
        start = time.time()

        # CreateShader
        m_asphalt = bpy.data.materials.new(name="QMM Asphalt")
        m_asphalt.use_nodes = True
        m_asphalt.diffuse_color = (0.02, 0.02, 0.02, 1)

        nodes = m_asphalt.node_tree.nodes

        # materialoutput
        material_output = nodes.get('Material Output')
        material_output.location = (0, 0)

        # mixshader
        m_mixshader = make_node(nodes, 'ShaderNodeMixShader', -200, 0)

        # displacement
        m_disp = make_node(nodes, 'ShaderNodeDisplacement', -200, -200)

        # lessthan
        m_lessthan = make_node(nodes, 'ShaderNodeMath', -400, -200)
        m_lessthan.operation = 'LESS_THAN'

        # principledbsdf - stone
        BSDF = nodes.get('Principled BSDF')
        BSDF.location = (-700, 300)
        BSDF.inputs[9].default_value = 0.56
        # BSDF.select = True

        # principledbsdf - cracks
        BSDF2 = make_node(nodes, 'ShaderNodeBsdfPrincipled', -700, -400)
        BSDF2.inputs[0].default_value = (0.025, 0.01875, 0.01875, 1)
        BSDF2.inputs[9].default_value = 1.0

        # colorramp
        m_colorramp = make_node(nodes, 'ShaderNodeValToRGB', -1200, 100)
        m_colorramp.color_ramp.elements[0].color = (0.02, 0.02, 0.02, 1)
        m_colorramp.color_ramp.elements[0].position = 0.25
        m_colorramp.color_ramp.elements[1].color = (0.333, 0.333, 0.333, 1)
        m_colorramp.color_ramp.elements[1].position = 0.4
        m_colorramp.color_ramp.interpolation = 'B_SPLINE'

        # bump
        m_bump = make_node(nodes, 'ShaderNodeBump', -900, -200)
        m_bump.inputs[0].default_value = 0.4

        # mixrgbshader
        m_mix = make_node(nodes, 'ShaderNodeMixRGB', -1400, -100)

        # bump2
        m_bump2 = make_node(nodes, 'ShaderNodeBump', -1100, -300)
        m_bump2.invert = True

        # colorramp2
        m_colorramp2 = make_node(nodes, 'ShaderNodeValToRGB', -1400, -500)
        m_colorramp2.color_ramp.elements[0].color = (1.0, 1.0, 1.0, 1)
        m_colorramp2.color_ramp.elements[1].color = (0.0, 0.0, 0.0, 1)
        m_colorramp2.color_ramp.elements[1].position = 0.025

        # colorramp3
        m_colorramp3 = make_node(nodes, 'ShaderNodeValToRGB', -1800, 300)
        m_colorramp3.color_ramp.elements[0].position = 0.4

        # voronoishader
        m_voronoi = make_node(nodes, 'ShaderNodeTexVoronoi', -2000, 0)
        m_voronoi.feature = 'DISTANCE_TO_EDGE'
        m_voronoi.inputs[2].default_value = 300.0

        # noiseshader
        m_noise = make_node(nodes, 'ShaderNodeTexNoise', -2000, -200)
        m_noise.inputs[3].default_value = 12.0
        m_noise.inputs[4].default_value = 0.875

        # voronoishader2
        m_voronoi2 = make_node(nodes, 'ShaderNodeTexVoronoi', -1600, -500)
        m_voronoi2.feature = 'DISTANCE_TO_EDGE'
        m_voronoi2.inputs[2].default_value = 8.0

        # noiseshader2
        m_noise2 = make_node(nodes, 'ShaderNodeTexNoise', -2000, 300)
        m_noise2.inputs[2].default_value = 3.0
        m_noise2.inputs[3].default_value = 12.0
        m_noise2.inputs[4].default_value = 0.875

        # mixrgbshader2
        m_mix2 = make_node(nodes, 'ShaderNodeMixRGB', -1800, -500)
        m_mix2.inputs[0].default_value = 0.9

        # noiseshader3
        m_noise3 = make_node(nodes, 'ShaderNodeTexNoise', -2000, -500)
        m_noise3.inputs[3].default_value = 10.0

        # mapping
        m_mapping = make_node(nodes, 'ShaderNodeMapping', -2300, -600)
        m_mapping.width = 140

        # mapping2
        m_mapping2 = make_node(nodes, 'ShaderNodeMapping', -2300, 100)
        m_mapping2.width = 140

        # value
        m_val = make_node(nodes, 'ShaderNodeValue', -2500, -800)
        m_val.label = "Fragment Scale"
        m_val.outputs[0].default_value = 1.0

        # texturecoordinates
        m_texcoords = make_node(nodes, 'ShaderNodeTexCoord', -2600, -300)

        # value2
        m_val2 = make_node(nodes, 'ShaderNodeValue', -2500, -100)
        m_val2.label = "Gravel Scale"
        m_val2.outputs[0].default_value = 1.0

        # EnergyConservationGroup
        bpy.ops.node.ec_group_operator()
        ec_group = set_ec(nodes, -900, 200, 1.635, (0.2, 0.2, 0.2, 1), (0.01, 0.01, 0.01, 1))

        # EnergyConservationGroup2
        ec_group2 = set_ec(nodes, -900, -600, 1.52, (0.025000, 0.018750, 0.018750, 1), (0.01, 0.01, 0.01, 1))

        links = m_asphalt.node_tree.links.new

        links(m_mixshader.outputs[0], material_output.inputs[0])
        links(m_colorramp2.outputs[0], m_mixshader.inputs[0])
        links(BSDF.outputs[0], m_mixshader.inputs[1])
        links(BSDF2.outputs[0], m_mixshader.inputs[2])
        links(m_colorramp.outputs[0], ec_group.inputs[1])
        links(m_bump.outputs[0], BSDF.inputs[22])
        links(m_mix.outputs[0], m_colorramp.inputs[0])
        links(m_mix.outputs[0], m_bump.inputs[2])
        links(m_bump2.outputs[0], m_bump.inputs[3])
        links(m_colorramp2.outputs[0], m_bump2.inputs[2])
        links(m_colorramp3.outputs[0], m_mix.inputs[0])
        links(m_voronoi.outputs[0], m_mix.inputs[1])
        links(m_noise.outputs[0], m_mix.inputs[2])
        links(m_voronoi2.outputs[0], m_colorramp2.inputs[0])
        links(m_noise2.outputs[0], m_colorramp3.inputs[0])
        links(m_mix2.outputs[0], m_voronoi2.inputs[0])
        links(m_noise3.outputs[1], m_mix2.inputs[1])
        links(m_mapping.outputs[0], m_noise3.inputs[0])
        links(m_mapping.outputs[0], m_mix2.inputs[2])
        links(m_mapping2.outputs[0], m_noise2.inputs[0])
        links(m_mapping2.outputs[0], m_voronoi.inputs[0])
        links(m_mapping2.outputs[0], m_noise.inputs[0])
        links(m_val.outputs[0], m_mapping.inputs[3])
        links(m_texcoords.outputs[3], m_mapping.inputs[0])
        links(m_texcoords.outputs[3], m_mapping2.inputs[0])
        links(m_val2.outputs[0], m_mapping2.inputs[3])

        links(ec_group.outputs[0], BSDF.inputs[0])
        links(ec_group.outputs[1], BSDF.inputs[7])
        links(ec_group.outputs[3], BSDF.inputs[16])

        links(ec_group2.outputs[0], BSDF2.inputs[0])
        links(ec_group2.outputs[1], BSDF2.inputs[7])
        links(ec_group2.outputs[3], BSDF2.inputs[16])

        links(m_colorramp2.outputs[0], m_lessthan.inputs[0])
        links(m_lessthan.outputs[0], m_disp.inputs[0])
        links(m_disp.outputs[0], material_output.inputs[2])

        bpy.context.object.active_material = m_asphalt

        end = time.time()
        print(f"QMM Asphalt: {end - start} seconds")
