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
    locY2 = locY + 200
    if bv < (4, 0, 0):
        result.location = (locX, locY)
    else:
        result.location = (locX, locY2)
    return result

# WallPaintShaderOperator


class QMMWallPaint(bpy.types.Operator):
    """Add/Apply Wall Paint Material to Selected Object (or Scene)"""
    bl_label  = "QMM Wall Paint Shader"
    bl_idname = 'shader.qmm_wall_paint_operator'

    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        if m_wall_paint := bpy.data.materials.get("QMM Wall Paint"):
            #ShowMessageBox(message_text, "QMM Wall Paint")
            # print(f"QMM Wall Paint already exists")
            bpy.context.object.active_material = m_wall_paint
            diffuse_bool = bpy.context.scene.diffuse_bool.diffuse_more
            m_wall_paint.diffuse_color = (0.504859, 0.483713, 0.674328, 1) if diffuse_bool else (0.8, 0.8, 0.8, 1)
            m_wall_paint.roughness = 0.5 if diffuse_bool else 0.4
            return {'FINISHED'}
        else:
            self.make_shader()
        return {'FINISHED'}

    def make_shader(self):
        start = time.time()

        # CreateShader
        m_wall_paint = bpy.data.materials.new(name="QMM Wall Paint")
        m_wall_paint.use_nodes = True
        diffuse_bool = bpy.context.scene.diffuse_bool.diffuse_more
        if diffuse_bool == True:
            m_wall_paint.diffuse_color = (0.504859, 0.483713, 0.674328, 1)
            m_wall_paint.roughness = 0.5

        nodes = m_wall_paint.node_tree.nodes

        # materialoutput
        material_output = nodes.get('Material Output')
        material_output.location = (0, 0)

        # princibledbsdf
        BSDF = nodes.get('Principled BSDF')
        BSDF.distribution = 'MULTI_GGX'
        BSDF.location = (-300, 0)
        BSDF.inputs[0].default_value = (0.504859, 0.483713, 0.674328, 1)
        if bv >= (4, 0, 0):
            BSDF.inputs[3].default_value = 1.52

        # bump
        m_bump = make_node(nodes, 'ShaderNodeBump', -500, -500)
        m_bump.inputs[0].default_value = 0.2
        m_bump.invert = True

        # maprange satin
        m_maprange = make_node(nodes, 'ShaderNodeMapRange', -700, -200)
        m_maprange.inputs[1].default_value = 0.3
        m_maprange.inputs[2].default_value = 0.5
        m_maprange.inputs[3].default_value = 0.52
        m_maprange.inputs[4].default_value = 0.7
        m_maprange.name = "Satin/Semi-gloss"
        m_maprange.label = "Satin/Semi-gloss"

        # maprange matte
        m_maprange_m = make_node(nodes, 'ShaderNodeMapRange', -700, 100)
        m_maprange_m.inputs[1].default_value = 0.6
        m_maprange_m.inputs[2].default_value = 0.7
        m_maprange_m.inputs[3].default_value = 0.52
        m_maprange_m.inputs[4].default_value = 0.7
        m_maprange_m.name = "Flat/Matte"
        m_maprange_m.label = "Flat/Matte"

        # maprange glossy
        m_maprange_g = make_node(nodes, 'ShaderNodeMapRange', -700, 400)
        m_maprange_g.inputs[1].default_value = 0.1
        m_maprange_g.inputs[2].default_value = 0.2
        m_maprange_g.inputs[3].default_value = 0.52
        m_maprange_g.inputs[4].default_value = 0.7
        m_maprange_g.name = "Glossy"
        m_maprange_g.label = "Glossy"

        # colorramp2
        m_maprange2 = make_node(nodes, 'ShaderNodeMapRange', -700, -500)
        m_maprange2.inputs[1].default_value = 0.4
        m_maprange2.inputs[2].default_value = 1
        m_maprange2.inputs[3].default_value = 0
        m_maprange2.inputs[4].default_value = 1

        # noiseshader
        m_noise = make_node(nodes, 'ShaderNodeTexNoise', -900, -200)
        m_noise.inputs[2].default_value = 3.0
        m_noise.inputs[3].default_value = 3.0

        # voronoishader
        m_voronoi = make_node(nodes, 'ShaderNodeTexVoronoi', -900, -500)
        m_voronoi.inputs[2].default_value = 512.0

        # mapping
        m_mapping = make_node(nodes, 'ShaderNodeMapping', -1100, -300)
        m_mapping.width = 140

        # texturecoordinates
        m_texcoords = make_node(nodes, 'ShaderNodeTexCoord', -1300, -300)

        # value
        m_value = make_node(nodes, 'ShaderNodeValue', -1300, -600)
        m_value.outputs[0].default_value = 1.0

        # EnergyConservationGroup
        bpy.ops.node.ec_group_operator()
        ec_group = nodes.new("ShaderNodeGroup")
        ec_group.name = "Energy Conservation v5"
        ec_group.node_tree = bpy.data.node_groups['Energy Conservation v5']
        if bv < (4, 0, 0):
            ec_group.location = (-500, -100)
        else:
            ec_group.location = (0, -200)
        ec_group.inputs[0].default_value = (0.504859, 0.483713, 0.674328, 1)
        ec_group.inputs[1].default_value = 0.5
        ec_group.inputs[2].default_value = 1.52
        ec_group.inputs[4].default_value = (0.01, 0.01, 0.01, 1)

        links = m_wall_paint.node_tree.links.new

        links(m_value.outputs[0], m_mapping.inputs[3])
        links(m_texcoords.outputs[3], m_mapping.inputs[0])
        links(m_mapping.outputs[0], m_voronoi.inputs[0])
        links(m_mapping.outputs[0], m_noise.inputs[0])
        links(m_voronoi.outputs[0], m_maprange2.inputs[0])
        links(m_noise.outputs[0], m_maprange.inputs[0])
        links(m_noise.outputs[0], m_maprange_g.inputs[0])
        links(m_noise.outputs[0], m_maprange_m.inputs[0])
        links(m_maprange2.outputs[0], m_bump.inputs[2])
        if bpy.app.version < (4, 0, 0):
            links(m_maprange.outputs[0], ec_group.inputs[1])
            links(ec_group.outputs[0], BSDF.inputs[0])
            links(ec_group.outputs[1], BSDF.inputs[7])
            links(ec_group.outputs[2], BSDF.inputs[9])
            links(ec_group.outputs[4], BSDF.inputs[16])
            links(m_bump.outputs[0], BSDF.inputs[22])
        else:
            links(m_maprange.outputs[0], BSDF.inputs[2])
            links(m_bump.outputs[0], BSDF.inputs[5])

        bpy.context.object.active_material = m_wall_paint

        end = time.time()
        print(f"QMM Wall Paint: {end - start} seconds")
