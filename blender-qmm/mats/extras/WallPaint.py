import bpy

# MESSAGE BOX
message_text = "This material already exists"
def ShowMessageBox(message = "", title = "", icon = 'INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

#MercuryShaderOperator
class QMMWallPaint(bpy.types.Operator):
    """Add/Apply Wall Paint Material to Selected Object (or Scene)"""
    bl_label = "QMM Wall Paint Shader"
    bl_idname = 'shader.qmm_wall_paint_operator'
    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        m_wall_paint = bpy.data.materials.get("QMM Wall Paint")
        if m_wall_paint:
            ShowMessageBox(message_text, "QMM Wall Paint")
            # print(f"QMM Wall Paint already exists")
            bpy.context.object.active_material = m_wall_paint
            return {'FINISHED'}
        else:
            #CreateShader
            m_wall_paint = bpy.data.materials.new(name = "QMM Wall Paint")
            m_wall_paint.use_nodes = True
            m_wall_paint.diffuse_color = (0.504859, 0.483713, 0.674328, 1)

            nodes = m_wall_paint.node_tree.nodes

            #materialoutput
            material_output = nodes.get('Material Output')
            material_output.location = (0,0)

            #principledbsdf
            BSDF = nodes.get('Principled BSDF')
            BSDF.location = (-300,0)
            BSDF.inputs[0].default_value = (0.504859, 0.483713, 0.674328, 1)

            #bump
            m_bump = nodes.new('ShaderNodeBump')
            m_bump.location = (-500,-500)
            m_bump.inputs[0].default_value = 0.2
            m_bump.invert = True

            #maprange
            m_maprange = nodes.new('ShaderNodeMapRange')
            m_maprange.location = (-700,-200)
            m_maprange.inputs[1].default_value = 0.4
            m_maprange.inputs[2].default_value = 0.9
            m_maprange.inputs[3].default_value = 0.25
            m_maprange.inputs[4].default_value = 1

            #colorramp2
            m_maprange2 = nodes.new('ShaderNodeMapRange')
            m_maprange2.location = (-700,-500)
            m_maprange2.inputs[1].default_value = 0.4
            m_maprange2.inputs[2].default_value = 1
            m_maprange2.inputs[3].default_value = 0
            m_maprange2.inputs[4].default_value = 1

            #noiseshader
            m_noise = nodes.new('ShaderNodeTexNoise')
            m_noise.location = (-900,-200)
            m_noise.inputs[2].default_value = 3.0
            m_noise.inputs[3].default_value = 3.0

            #voronoishader
            m_voronoi = nodes.new('ShaderNodeTexVoronoi')
            m_voronoi.location = (-900,-500)
            m_voronoi.inputs[2].default_value = 128.0

            #mapping
            m_mapping = nodes.new('ShaderNodeMapping')
            m_mapping.location = (-1100,-300)
            m_mapping.width = 140

            #texturecoordinates
            m_texcoords = nodes.new('ShaderNodeTexCoord')
            m_texcoords.location = (-1300,-300)

            #value
            m_value = nodes.new('ShaderNodeValue')
            m_value.location = (-1300,-600)
            m_value.outputs[0].default_value = 1.0

            #EnergyConservationGroup
            bpy.ops.node.ec_group_operator()
            ec_group = nodes.new("ShaderNodeGroup")
            ec_group.node_tree = bpy.data.node_groups['Energy Conservation']
            ec_group.location = (-500, -200)
            ec_group.inputs[0].default_value = 1.52
            ec_group.inputs[1].default_value = (0.504859, 0.483713, 0.674328, 1)
            ec_group.inputs[2].default_value = (0.01, 0.01, 0.01, 1)

            links = m_wall_paint.node_tree.links.new

            links(m_value.outputs[0], m_mapping.inputs[3])
            links(m_texcoords.outputs[3], m_mapping.inputs[0])
            links(m_mapping.outputs[0], m_voronoi.inputs[0])
            links(m_mapping.outputs[0], m_noise.inputs[0])
            links(m_voronoi.outputs[0], m_maprange2.inputs[0])
            links(m_noise.outputs[0], m_maprange.inputs[0])
            links(m_maprange2.outputs[0], m_bump.inputs[2])
            links(m_maprange.outputs[0], BSDF.inputs[9])
            links(ec_group.outputs[0], BSDF.inputs[0])
            links(ec_group.outputs[1], BSDF.inputs[7])
            links(ec_group.outputs[3], BSDF.inputs[16])
            links(m_bump.outputs[0], BSDF.inputs[22])

            bpy.context.object.active_material = m_wall_paint

        return {'FINISHED'}
