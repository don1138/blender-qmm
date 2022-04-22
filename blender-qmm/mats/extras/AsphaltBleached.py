import bpy

# MESSAGE BOX
message_text = "This material already exists"
def ShowMessageBox(message = "", title = "", icon = 'INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

#MercuryShaderOperator
class QMMAsphaltBleached(bpy.types.Operator):
    """Add/Apply Tinted Asphalt Bleached Material to Selected Object (or Scene)"""
    bl_label = "QMM Asphalt Bleached Shader"
    bl_idname = 'shader.qmm_asphalt_b_operator'
    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        m_asphalt_b = bpy.data.materials.get("QMM Asphalt Bleached")
        if m_asphalt_b:
            ShowMessageBox(message_text, "QMM Asphalt Bleached")
            # print(f"QMM Asphalt Bleached already exists")
            bpy.context.object.active_material = m_asphalt_b
            return {'FINISHED'}
        else:
            #CreateShader
            m_asphalt_b = bpy.data.materials.new(name = "QMM Asphalt Bleached")
            m_asphalt_b.use_nodes = True
            m_asphalt_b.diffuse_color = (0.333, 0.333, 0.333, 1)

            nodes = m_asphalt_b.node_tree.nodes

            #materialoutput
            material_output = nodes.get('Material Output')
            material_output.location = (0,0)

            # mixshader
            m_mixshader = nodes.new('ShaderNodeMixShader')
            m_mixshader.location = (-200,0)

            #princibledbsdf - stone
            BSDF = nodes.get('Principled BSDF')
            BSDF.location = (-800,0)
            BSDF.select = True

            #princibledbsdf - cracks
            BSDF2 = nodes.new('ShaderNodeBsdfPrincipled')
            BSDF2.location = (-500,-300)
            BSDF2.inputs[0].default_value = (0.025, 0.01875, 0.01875, 1.0)
            BSDF2.inputs[9].default_value = 1.0

            #maprange
            m_maprange = nodes.new('ShaderNodeMapRange')
            m_maprange.location = (-1100,0)
            m_maprange.inputs[1].default_value = 0.25
            m_maprange.inputs[2].default_value = 0.4
            m_maprange.inputs[3].default_value = 0.2
            m_maprange.inputs[4].default_value = 0.333

            #bump
            m_bump = nodes.new('ShaderNodeBump')
            m_bump.location = (-1100,-300)
            m_bump.inputs[0].default_value = 0.4

            #mixrgbshader
            m_mix = nodes.new('ShaderNodeMixRGB')
            m_mix.location = (-1300,-300)

            #bump2
            m_bump2 = nodes.new('ShaderNodeBump')
            m_bump2.location = (-1300,0)
            m_bump2.invert = True

            #maprange2
            m_maprange2 = nodes.new('ShaderNodeMapRange')
            m_maprange2.location = (-1600,300)
            m_maprange2.inputs[2].default_value = 0.025
            m_maprange2.inputs[3].default_value = 1
            m_maprange2.inputs[4].default_value = 0

            #maprange3
            m_maprange3 = nodes.new('ShaderNodeMapRange')
            m_maprange3.location = (-1600,0)
            m_maprange3.inputs[1].default_value = 0.4

            #voronoishader
            m_voronoi = nodes.new('ShaderNodeTexVoronoi')
            m_voronoi.location = (-1600,-300)
            m_voronoi.feature = 'DISTANCE_TO_EDGE'
            m_voronoi.inputs[2].default_value = 300.0

            #noiseshader
            m_noise = nodes.new('ShaderNodeTexNoise')
            m_noise.location = (-1600,-500)
            m_noise.inputs[3].default_value = 12.0
            m_noise.inputs[4].default_value = 0.875

            #voronoishader2
            m_voronoi2 = nodes.new('ShaderNodeTexVoronoi')
            m_voronoi2.location = (-1800,300)
            m_voronoi2.feature = 'DISTANCE_TO_EDGE'
            m_voronoi2.inputs[2].default_value = 8.0

            #noiseshader2
            m_noise2 = nodes.new('ShaderNodeTexNoise')
            m_noise2.location = (-1800,0)
            m_noise2.inputs[2].default_value = 3.0
            m_noise2.inputs[3].default_value = 12.0
            m_noise2.inputs[4].default_value = 0.875

            #mixrgbshader2
            m_mix2 = nodes.new('ShaderNodeMixRGB')
            m_mix2.location = (-2000,300)
            m_mix2.inputs[0].default_value = 0.9

            #noiseshader3
            m_noise3 = nodes.new('ShaderNodeTexNoise')
            m_noise3.location = (-2200,400)
            m_noise3.inputs[3].default_value = 10.0

            #mapping
            m_mapping = nodes.new('ShaderNodeMapping')
            m_mapping.location = (-2400,300)
            m_mapping.width = 140

            #mapping2
            m_mapping2 = nodes.new('ShaderNodeMapping')
            m_mapping2.location = (-2400,-200)
            m_mapping2.width = 140

            #value
            m_val = nodes.new('ShaderNodeValue')
            m_val.label = "Fragment Scale"
            m_val.location = (-2600,300)
            m_val.outputs[0].default_value = 1.0

            #texturecoordinates
            m_texcoords = nodes.new('ShaderNodeTexCoord')
            m_texcoords.location = (-2600,0)

            #value2
            m_val2 = nodes.new('ShaderNodeValue')
            m_val2.label = "Gravel Scale"
            m_val2.location = (-2600,-300)
            m_val2.outputs[0].default_value = 1.0

            links = m_asphalt_b.node_tree.links

            links.new(m_mixshader.outputs[0], material_output.inputs[0])
            links.new(m_maprange2.outputs[0], m_mixshader.inputs[0])
            links.new(BSDF.outputs[0], m_mixshader.inputs[1])
            links.new(BSDF2.outputs[0], m_mixshader.inputs[2])
            links.new(m_maprange.outputs[0], BSDF.inputs[0])
            links.new(m_bump.outputs[0], BSDF.inputs[22])
            links.new(m_mix.outputs[0], m_maprange.inputs[0])
            links.new(m_mix.outputs[0], m_bump.inputs[2])
            links.new(m_bump2.outputs[0], m_bump.inputs[5])
            links.new(m_maprange2.outputs[0], m_bump2.inputs[2])
            links.new(m_maprange3.outputs[0], m_mix.inputs[0])
            links.new(m_voronoi.outputs[0], m_mix.inputs[1])
            links.new(m_noise.outputs[0], m_mix.inputs[2])
            links.new(m_voronoi2.outputs[0], m_maprange2.inputs[0])
            links.new(m_noise2.outputs[0], m_maprange3.inputs[0])
            links.new(m_mix2.outputs[0], m_voronoi2.inputs[0])
            links.new(m_noise3.outputs[1], m_mix2.inputs[1])
            links.new(m_mapping.outputs[0], m_mix2.inputs[2])
            links.new(m_mapping2.outputs[0], m_noise2.inputs[0])
            links.new(m_mapping2.outputs[0], m_voronoi.inputs[0])
            links.new(m_mapping2.outputs[0], m_noise.inputs[0])
            links.new(m_val.outputs[0], m_mapping.inputs[3])
            links.new(m_texcoords.outputs[3], m_mapping.inputs[0])
            links.new(m_texcoords.outputs[3], m_mapping2.inputs[0])
            links.new(m_val2.outputs[0], m_mapping2.inputs[3])

            #SpecularGroup
            bpy.ops.node.specular_group_operator()
            nodes = m_asphalt_b.node_tree.nodes
            specular_group = nodes.new("ShaderNodeGroup")
            specular_group.node_tree = bpy.data.node_groups['Specular']
            specular_group.location = (-1100, -500)
            specular_group.inputs[0].default_value = 1.635
            links.new(specular_group.outputs[0], BSDF.inputs[7])
            links.new(specular_group.outputs[0], BSDF2.inputs[7])
            links.new(specular_group.outputs[1], BSDF.inputs[16])
            links.new(specular_group.outputs[1], BSDF2.inputs[16])

            bpy.context.object.active_material = m_asphalt_b

        return {'FINISHED'}
