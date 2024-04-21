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

# PlasterShaderOperator


class QMMPlaster(bpy.types.Operator):
    """Add/Apply Tinted Plaster Material to Selected Object (or Scene)"""
    bl_label  = "QMM Plaster Shader"
    bl_idname = 'shader.qmm_plaster_operator'

    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        if m_plaster := bpy.data.materials.get("QMM Plaster"):
            #ShowMessageBox(message_text, "QMM Plaster")
            # print(f"QMM Plaster already exists")
            bpy.context.object.active_material = m_plaster
            return {'FINISHED'}
        else:
            self.make_shader()
        return {'FINISHED'}

    def make_shader(self):
        start = time.time()

        # CreateShader
        m_plaster = bpy.data.materials.new(name="QMM Plaster")
        m_plaster.use_nodes = True
        m_plaster.diffuse_color = (0.9, 0.7, 0.9, 1)
        m_plaster.roughness = 0.86

        nodes = m_plaster.node_tree.nodes

        # materialoutput
        material_output = nodes.get('Material Output')
        material_output.location = (0, 0)

        # princibledbsdf
        BSDF = nodes.get('Principled BSDF')
        BSDF.distribution = 'MULTI_GGX'
        BSDF.location = (-300, 0)
        if bv < (4, 0, 0):
            BSDF.inputs[1].default_value = 0.02
            BSDF.inputs[3].default_value = (0.708857, 0.392564, 0.708857, 1)
            BSDF.inputs[9].default_value = 0.86
        else:
            BSDF.inputs[7].default_value = 0.02
            BSDF.inputs[2].default_value = 0.86

        # colorramp
        m_colorramp = make_node(nodes, 'ShaderNodeValToRGB', -700, -100)
        m_colorramp.color_ramp.elements[0].color = (0.708857, 0.392564, 0.708857, 1)
        m_colorramp.color_ramp.elements.new(0.2)
        m_colorramp.color_ramp.elements[1].color = (0.5, 0.5, 0.5, 1)
        m_colorramp.color_ramp.elements[2].position = 0.775
        m_colorramp.color_ramp.elements[2].color = (0.4, 0.4, 0.4, 1)
        m_colorramp.width = 140

        # mixshader
        if bv < (3, 4, 0):
            m_mix = make_node(nodes, 'ShaderNodeMixRGB', -900, -100)
        else:
            m_mix = make_node(nodes, 'ShaderNodeMix', -900, 0)
            m_mix.data_type = 'RGBA'

        # voronoishader
        m_voronoi = make_node(nodes, 'ShaderNodeTexVoronoi', -1100, -300)
        m_voronoi.distance = 'MANHATTAN'
        m_voronoi.inputs[2].default_value = 30.0

        # noiseshader
        m_noise = make_node(nodes, 'ShaderNodeTexNoise', -1300, -200)
        m_noise.inputs[2].default_value = 50.0
        m_noise.inputs[3].default_value = 5.0

        # mapping
        m_mapping = make_node(nodes, 'ShaderNodeMapping', -1500, -100)
        m_mapping.width = 140

        # texturecoordinates
        m_texcoords = make_node(nodes, 'ShaderNodeTexCoord', -1700, -100)

        # bump
        m_bump = make_node(nodes, 'ShaderNodeBump', -700, -400)
        m_bump.inputs[0].default_value = 0.5

        # bump2
        m_bump2 = make_node(nodes, 'ShaderNodeBump', -500, -500)
        m_bump2.inputs[0].default_value = 0.25

        # maprange
        m_maprange = make_node(nodes, 'ShaderNodeMapRange', -900, -300)
        m_maprange.inputs[1].default_value = 0.04
        m_maprange.inputs[2].default_value = 0.08
        m_maprange.width = 140

        # EnergyConservationGroup
        bpy.ops.node.ec_group_operator()
        ec_group = nodes.new("ShaderNodeGroup")
        ec_group.name = "Energy Conservation v5"
        ec_group.node_tree = bpy.data.node_groups['Energy Conservation v5']
        ec_group.location = (-500, -100)
        ec_group.inputs[0].default_value = (0.708857, 0.392564, 0.708857, 1)
        ec_group.inputs[1].default_value = 0.86
        ec_group.inputs[2].default_value = 1.52
        ec_group.inputs[4].default_value = (0.01, 0.01, 0.01, 1)

        links = m_plaster.node_tree.links.new

        links(m_texcoords.outputs[3], m_mapping.inputs[0])
        links(m_mapping.outputs[0], m_noise.inputs[0])
        links(m_noise.outputs[0], m_voronoi.inputs[0])
        links(m_voronoi.outputs[0], m_maprange.inputs[0])
        links(m_colorramp.outputs[0], ec_group.inputs[0])
        links(m_maprange.outputs[0], m_bump.inputs[2])
        links(m_noise.outputs[0], m_bump2.inputs[2])
        links(m_bump.outputs[0], m_bump2.inputs[3])
        links(ec_group.outputs[0], BSDF.inputs[0])
        if bv < (4, 0, 0):
            links(m_bump2.outputs[0], BSDF.inputs[22])
            links(ec_group.outputs[1], BSDF.inputs[7])
            links(ec_group.outputs[2], BSDF.inputs[9])
            links(ec_group.outputs[4], BSDF.inputs[16])
        else:
            links(m_bump2.outputs[0], BSDF.inputs[5])
            links(ec_group.outputs[1], BSDF.inputs[12])
            links(ec_group.outputs[2], BSDF.inputs[2])
            links(ec_group.outputs[4], BSDF.inputs[3])

        if bv < (3, 4, 0):
            links(m_voronoi.outputs[0], m_mix.inputs[1])
            links(m_noise.outputs[0], m_mix.inputs[2])
            links(m_mix.outputs[0], m_colorramp.inputs[0])
        else:
            links(m_voronoi.outputs[0], m_mix.inputs[6])
            links(m_noise.outputs[0], m_mix.inputs[7])
            links(m_mix.outputs[2], m_colorramp.inputs[0])

        bpy.context.object.active_material = m_plaster

        end = time.time()
        print(f"QMM Plaster: {end - start} seconds")
