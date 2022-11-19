import bpy

# MESSAGE BOX
message_text = "This material already exists"
def ShowMessageBox(message = "", title = "", icon = 'INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

#MercuryShaderOperator
class QMMPlaster(bpy.types.Operator):
    """Add/Apply Tinted Plaster Material to Selected Object (or Scene)"""
    bl_label = "QMM Plaster Shader"
    bl_idname = 'shader.qmm_plaster_operator'
    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        if m_plaster := bpy.data.materials.get("QMM Plaster"):
            ShowMessageBox(message_text, "QMM Plaster")
            # print(f"QMM Plaster already exists")
            bpy.context.object.active_material = m_plaster
            return {'FINISHED'}
        else:
            #CreateShader
            m_plaster = bpy.data.materials.new(name = "QMM Plaster")
            m_plaster.use_nodes = True
            m_plaster.diffuse_color = (0.9, 0.7, 0.9, 1)
            m_plaster.roughness = 0.86

            nodes = m_plaster.node_tree.nodes

            #materialoutput
            material_output = nodes.get('Material Output')
            material_output.location = (0,0)

            #princibledbsdf
            BSDF = nodes.get('Principled BSDF')
            BSDF.location = (-300,0)
            BSDF.inputs[1].default_value = 0.02
            BSDF.inputs[3].default_value = (0.708857, 0.392564, 0.708857, 1)
            BSDF.inputs[9].default_value = 0.86


            #colorramp
            m_colorramp = nodes.new('ShaderNodeValToRGB')
            m_colorramp.location = (-700,-100)
            m_colorramp.color_ramp.elements[0].color = (0.708857, 0.392564, 0.708857, 1)
            m_colorramp.color_ramp.elements.new(0.2)
            m_colorramp.color_ramp.elements[1].color = (0.5, 0.5, 0.5, 1)
            m_colorramp.color_ramp.elements[2].position = 0.775
            m_colorramp.color_ramp.elements[2].color = (0.4, 0.4, 0.4, 1)
            m_colorramp.width = 140

            #mixshader
            m_mix = nodes.new('ShaderNodeMixRGB')
            m_mix.location = (-900,-100)

            #voronoishader
            m_voronoi = nodes.new('ShaderNodeTexVoronoi')
            m_voronoi.location = (-1100,-300)
            m_voronoi.distance = 'MANHATTAN'
            m_voronoi.inputs[2].default_value = 30.0

            #noiseshader
            m_noise = nodes.new('ShaderNodeTexNoise')
            m_noise.location = (-1300,-200)
            m_noise.inputs[2].default_value = 50.0
            m_noise.inputs[3].default_value = 5.0

            #mapping
            m_mapping = nodes.new('ShaderNodeMapping')
            m_mapping.location = (-1500,-100)
            m_mapping.width = 140

            #texturecoordinates
            m_texcoords = nodes.new('ShaderNodeTexCoord')
            m_texcoords.location = (-1700,-100)

            #bump
            m_bump = nodes.new('ShaderNodeBump')
            m_bump.location = (-700,-400)
            m_bump.inputs[0].default_value = 0.5

            #bump2
            m_bump2 = nodes.new('ShaderNodeBump')
            m_bump2.location = (-500,-500)
            m_bump2.inputs[0].default_value = 0.25

            #maprange
            m_maprange = nodes.new('ShaderNodeMapRange')
            m_maprange.location = (-900,-300)
            m_maprange.inputs[1].default_value = 0.04
            m_maprange.inputs[2].default_value = 0.08
            m_maprange.width = 140

            #EnergyConservationGroup
            bpy.ops.node.ec_group_operator()
            ec_group = nodes.new("ShaderNodeGroup")
            ec_group.name = "Energy Conservation"
            ec_group.node_tree = bpy.data.node_groups['Energy Conservation']
            ec_group.location = (-500, -200)
            ec_group.inputs[0].default_value = 1.52
            ec_group.inputs[1].default_value = (0.708857, 0.392564, 0.708857, 1)
            ec_group.inputs[2].default_value = (0.01, 0.01, 0.01, 1)

            links = m_plaster.node_tree.links.new

            links(m_texcoords.outputs[3], m_mapping.inputs[0])
            links(m_mapping.outputs[0], m_noise.inputs[0])
            links(m_noise.outputs[0], m_voronoi.inputs[0])
            links(m_voronoi.outputs[0], m_mix.inputs[1])
            links(m_voronoi.outputs[0], m_maprange.inputs[0])
            links(m_noise.outputs[0], m_mix.inputs[2])
            links(m_mix.outputs[0], m_colorramp.inputs[0])
            links(m_colorramp.outputs[0], ec_group.inputs[1])
            links(m_maprange.outputs[0], m_bump.inputs[2])
            links(m_noise.outputs[0], m_bump2.inputs[2])
            links(m_bump.outputs[0], m_bump2.inputs[3])
            links(m_bump2.outputs[0], BSDF.inputs[22])
            links(ec_group.outputs[0], BSDF.inputs[0])
            links(ec_group.outputs[1], BSDF.inputs[7])
            links(ec_group.outputs[3], BSDF.inputs[16])

            bpy.context.object.active_material = m_plaster

        return {'FINISHED'}
