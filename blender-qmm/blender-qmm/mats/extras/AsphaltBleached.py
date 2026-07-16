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

# AsphaltBleachedShaderOperator

class QMMAsphaltBleached(bpy.types.Operator):
    """Add/Apply Tinted Asphalt Bleached Material to Selected Object (or Scene)"""
    bl_label  = "QMM Asphalt Bleached Shader"
    bl_idname = 'shader.qmm_asphalt_b_operator'

    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        if m_asphalt_b := bpy.data.materials.get("QMM Asphalt Bleached"):
            #ShowMessageBox(message_text, "QMM Asphalt Bleached")
            # print(f"QMM Asphalt Bleached already exists")
            bpy.context.object.active_material = m_asphalt_b
            diffuse_bool = bpy.context.scene.diffuse_bool.diffuse_more
            m_asphalt_b.diffuse_color = (0.333, 0.333, 0.333, 1) if diffuse_bool else (0.8, 0.8, 0.8, 1)
            return {'FINISHED'}
        else:
            self.make_shader()
        return {'FINISHED'}

    def make_shader(self):
        start = time.time()

        # CreateShader
        m_asphalt_b = bpy.data.materials.new(name="QMM Asphalt Bleached")
        m_asphalt_b.use_nodes = True
        diffuse_bool = bpy.context.scene.diffuse_bool.diffuse_more
        if diffuse_bool:
            m_asphalt_b.diffuse_color = (0.333, 0.333, 0.333, 1)

        nodes = m_asphalt_b.node_tree.nodes

        # materialoutput
        material_output = next((n for n in nodes if n.bl_idname == 'ShaderNodeOutputMaterial'), None)
        if material_output:
            material_output.location = (0, 0)

        # mixshader
        m_mixshader = make_node(nodes, 'ShaderNodeMixShader', -200, 0)

        # displacement
        m_disp = make_node(nodes, 'ShaderNodeDisplacement', -200, -200)

        # lessthan
        m_lessthan = make_node(nodes, 'ShaderNodeMath', -400, -200)
        m_lessthan.operation = 'LESS_THAN'

        # principledbsdf - stone
        BSDF = next((n for n in nodes if n.bl_idname == 'ShaderNodeBsdfPrincipled'), None)
        if BSDF:
            BSDF.distribution = 'MULTI_GGX'
            BSDF.location = (-700, 300)
            BSDF.inputs["Roughness"].default_value = 0.56
            BSDF.inputs["IOR"].default_value = 1.635
            # BSDF.select = True

        # principledbsdf - cracks
        BSDF2 = make_node(nodes, 'ShaderNodeBsdfPrincipled', -700, -400)
        BSDF2.distribution = 'MULTI_GGX'
        BSDF2.inputs["Base Color"].default_value = (0.025, 0.01875, 0.01875, 1)
        BSDF2.inputs["Roughness"].default_value = 1.0
        BSDF2.inputs["IOR"].default_value = 1.52

        # maprange
        m_maprange = make_node(nodes, 'ShaderNodeMapRange', -1100, 100)
        m_maprange.inputs[1].default_value = 0.25
        m_maprange.inputs[2].default_value = 0.4
        m_maprange.inputs[3].default_value = 0.2
        m_maprange.inputs[4].default_value = 0.333

        # bump
        m_bump = make_node(nodes, 'ShaderNodeBump', -900, -200)
        m_bump.inputs["Strength"].default_value = 0.4

        # mixrgbshader
        m_mix = make_node(nodes, 'ShaderNodeMix', -1300, -100)
        m_mix.data_type = 'RGBA'

        # bump2
        m_bump2 = make_node(nodes, 'ShaderNodeBump', -1100, -300)
        m_bump2.invert = True

        # maprange2
        m_maprange2 = make_node(nodes, 'ShaderNodeMapRange', -1300, -500)
        m_maprange2.inputs[2].default_value = 0.02
        m_maprange2.inputs[3].default_value = 1
        m_maprange2.inputs[4].default_value = 0

        # maprange3
        m_maprange3 = make_node(nodes, 'ShaderNodeMapRange', -1700, 300)
        m_maprange3.inputs[1].default_value = 0.4

        # voronoishader
        m_voronoi = make_node(nodes, 'ShaderNodeTexVoronoi', -1900, 0)
        m_voronoi.feature = 'DISTANCE_TO_EDGE'
        m_voronoi.inputs["Scale"].default_value = 300.0

        # noiseshader
        m_noise = make_node(nodes, 'ShaderNodeTexNoise', -1900, -200)
        m_noise.inputs["Detail"].default_value = 12.0
        m_noise.inputs["Roughness"].default_value = 0.875

        # voronoishader2
        m_voronoi2 = make_node(nodes, 'ShaderNodeTexVoronoi', -1500, -500)
        m_voronoi2.feature = 'DISTANCE_TO_EDGE'
        m_voronoi2.inputs["Scale"].default_value = 8.0

        # noiseshader2
        m_noise2 = make_node(nodes, 'ShaderNodeTexNoise', -1900, 300)
        m_noise2.inputs["Scale"].default_value = 3.0
        m_noise2.inputs["Detail"].default_value = 12.0
        m_noise2.inputs["Roughness"].default_value = 0.875

        # mixrgbshader2
        m_mix2 = make_node(nodes, 'ShaderNodeMix', -1700, -500)
        m_mix2.data_type = 'RGBA'
        m_mix2.inputs[0].default_value = 0.9

        # noiseshader3
        m_noise3 = make_node(nodes, 'ShaderNodeTexNoise', -1900, -500)
        m_noise3.inputs["Detail"].default_value = 10.0

        # mapping
        m_mapping = make_node(nodes, 'ShaderNodeMapping', -2200, -600)
        m_mapping.width = 140

        # mapping2
        m_mapping2 = make_node(nodes, 'ShaderNodeMapping', -2200, 100)
        m_mapping2.width = 140

        # value
        m_val = make_node(nodes, 'ShaderNodeValue', -2400, -800)
        m_val.label = "Fragment Scale"
        m_val.outputs["Value"].default_value = 1.0

        # texturecoordinates
        m_texcoords = make_node(nodes, 'ShaderNodeTexCoord', -2500, -300)

        # value2
        m_val2 = make_node(nodes, 'ShaderNodeValue', -2400, -100)
        m_val2.label = "Gravel Scale"
        m_val2.outputs["Value"].default_value = 1.0

        links = m_asphalt_b.node_tree.links.new

        links(m_mixshader.outputs["Shader"], material_output.inputs["Surface"])
        links(m_maprange2.outputs["Result"], m_mixshader.inputs["Fac"])
        links(BSDF.outputs["BSDF"], m_mixshader.inputs[1])
        links(BSDF2.outputs["BSDF"], m_mixshader.inputs[2])
        links(m_maprange.outputs["Result"], BSDF.inputs["Base Color"])
        links(m_bump.outputs["Normal"], BSDF.inputs["Normal"])
        links(m_bump2.outputs["Normal"], m_bump.inputs["Normal"])
        links(m_maprange2.outputs["Result"], m_bump2.inputs["Height"])
        links(m_maprange3.outputs["Result"], m_mix.inputs[0])
        links(m_voronoi2.outputs["Distance"], m_maprange2.inputs["Value"])
        links(m_noise2.outputs["Fac"], m_maprange3.inputs["Value"])
        links(m_mapping.outputs["Vector"], m_noise3.inputs["Vector"])
        links(m_mapping2.outputs["Vector"], m_noise2.inputs["Vector"])
        links(m_mapping2.outputs["Vector"], m_voronoi.inputs["Vector"])
        links(m_mapping2.outputs["Vector"], m_noise.inputs["Vector"])
        links(m_val.outputs["Value"], m_mapping.inputs["Scale"])
        links(m_texcoords.outputs["Object"], m_mapping.inputs["Vector"])
        links(m_texcoords.outputs["Object"], m_mapping2.inputs["Vector"])
        links(m_val2.outputs["Value"], m_mapping2.inputs["Scale"])

        links(m_mix.outputs[2], m_maprange.inputs["Value"])
        links(m_mix.outputs[2], m_bump.inputs["Height"])
        links(m_voronoi.outputs["Distance"], m_mix.inputs[6])
        links(m_noise.outputs["Fac"], m_mix.inputs[7])
        links(m_mix2.outputs[2], m_voronoi2.inputs["Vector"])
        links(m_noise3.outputs["Color"], m_mix2.inputs[6])
        links(m_mapping.outputs["Vector"], m_mix2.inputs[7])

        links(m_maprange2.outputs["Result"], m_lessthan.inputs[0])
        links(m_lessthan.outputs["Value"], m_disp.inputs["Height"])
        links(m_disp.outputs["Displacement"], material_output.inputs["Displacement"])

        bpy.context.object.active_material = m_asphalt_b

        end = time.time()
        print(f"QMM Asphalt Bleached: {end - start} seconds")
