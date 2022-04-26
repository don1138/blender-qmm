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
            m_wall_paint.diffuse_color = (0.504859, 0.483713, 0.674328, 1.0)

            nodes = m_wall_paint.node_tree.nodes

            #materialoutput
            material_output = nodes.get('Material Output')
            material_output.location = (0,0)

            #princibledbsdf
            BSDF = nodes.get('Principled BSDF')
            BSDF.location = (-300,0)
            BSDF.inputs[0].default_value = (0.504859, 0.483713, 0.674328, 1.0)

            #bump
            m_bump = nodes.new('ShaderNodeBump')
            m_bump.location = (-500,-400)
            m_bump.inputs[0].default_value = 0.2
            m_bump.invert = True

            #colorramp
            m_colorramp = nodes.new('ShaderNodeValToRGB')
            m_colorramp.location = (-800,0)
            m_colorramp.color_ramp.elements[0].position = 0.4
            m_colorramp.color_ramp.elements[0].color = (0.25, 0.25, 0.25, 1.0)
            m_colorramp.color_ramp.elements[1].position = 0.8
            m_colorramp.color_ramp.elements[1].color = (0.7, 0.7, 0.7, 1.0)

            #colorramp2
            m_colorramp2 = nodes.new('ShaderNodeValToRGB')
            m_colorramp2.location = (-800,-300)
            m_colorramp2.color_ramp.elements[0].position = 0.4
            m_colorramp.color_ramp.elements[1].position = 0.9

            #noiseshader
            m_noise = nodes.new('ShaderNodeTexNoise')
            m_noise.location = (-1000,0)
            m_noise.inputs[2].default_value = 3.0
            m_noise.inputs[3].default_value = 3.0

            #noiseshader2
            m_voronoi = nodes.new('ShaderNodeTexVoronoi')
            m_voronoi.location = (-1000,-300)
            m_voronoi.inputs[2].default_value = 128.0

            #mapping
            m_mapping = nodes.new('ShaderNodeMapping')
            m_mapping.location = (-1200,-100)
            m_mapping.width = 140

            #texturecoordinates
            m_texcoords = nodes.new('ShaderNodeTexCoord')
            m_texcoords.location = (-1400,-100)

            #value
            m_value = nodes.new('ShaderNodeValue')
            m_value.location = (-1400,-400)
            m_value.outputs[0].default_value = 1.0

            links = m_wall_paint.node_tree.links

            links.new(m_value.outputs[0], m_mapping.inputs[3])
            links.new(m_texcoords.outputs[3], m_mapping.inputs[0])
            links.new(m_mapping.outputs[0], m_voronoi.inputs[0])
            links.new(m_mapping.outputs[0], m_noise.inputs[0])
            links.new(m_voronoi.outputs[0], m_colorramp2.inputs[0])
            links.new(m_noise.outputs[0], m_colorramp.inputs[0])
            links.new(m_colorramp2.outputs[0], m_bump.inputs[2])
            links.new(m_colorramp.outputs[0], BSDF.inputs[9])
            links.new(m_bump.outputs[0], BSDF.inputs[22])

            bpy.context.object.active_material = m_wall_paint

        return {'FINISHED'}
