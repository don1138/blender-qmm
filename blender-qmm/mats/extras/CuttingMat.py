import bpy

# MESSAGE BOX
message_text = "This material already exists"
def ShowMessageBox(message = "", title = "", icon = 'INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

#CuttingMatShaderOperator
class QMMCuttingMat(bpy.types.Operator):
    """Add/Apply Rubber Cutting Mat Material to Selected Object (or Scene)"""
    bl_label = "QMM Rubber Cutting Mat Shader"
    bl_idname = 'shader.qmm_cutting_mat_operator'
    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        m_cutting_mat = bpy.data.materials.get("QMM Rubber Cutting Mat")
        if m_cutting_mat:
            ShowMessageBox(message_text, "QMM Rubber Cutting Mat")
            # print(f"QMM Rubber Cutting Mat already exists")
            bpy.context.object.active_material = m_cutting_mat
            return {'FINISHED'}
        else:
            #CreateShader
            m_cutting_mat = bpy.data.materials.new(name = "QMM Rubber Cutting Mat")
            m_cutting_mat.use_nodes = True
            m_cutting_mat.diffuse_color = (0.045186, 0.141263, 0.144129, 1)
            m_cutting_mat.roughness = 0.79

            nodes = m_cutting_mat.node_tree.nodes

            #materialoutput
            material_output = nodes.get('Material Output')
            material_output.location = (0,0)

            #princibledbsdf
            BSDF = nodes.get('Principled BSDF')
            BSDF.location = (-300,0)
            BSDF.inputs[0].default_value = (0.045186, 0.141263, 0.144129, 1)
            BSDF.inputs[5].default_value = 0.425
            BSDF.inputs[9].default_value = 0.79

            #rgbmix
            m_mix = nodes.new('ShaderNodeMixRGB')
            m_mix.location = (-700,-200)
            m_mix.inputs[1].default_value = (0.045186, 0.141263, 0.144129, 1)
            m_mix.inputs[2].default_value = (0.187821, 0.450786, 0.558341, 1)

            #rgbadd
            m_add = nodes.new('ShaderNodeMixRGB')
            m_add.blend_type = 'ADD'
            m_add.location = (-900,-200)

            #bricktexture
            m_bricktexture = nodes.new('ShaderNodeTexBrick')
            m_bricktexture.location = (-1100,-200)
            m_bricktexture.offset = 0.0
            m_bricktexture.inputs[2].default_value = (0.0, 0.0, 0.0, 1)
            m_bricktexture.inputs[3].default_value = (1.0, 1.0, 1.0, 1)
            m_bricktexture.inputs[5].default_value = 0.005
            m_bricktexture.inputs[6].default_value = 0.0
            m_bricktexture.inputs[7].default_value = 1.0
            m_bricktexture.inputs[8].default_value = 1.0
            m_bricktexture.inputs[9].default_value = 1.0

            #bricktexture2
            m_bricktexture2 = nodes.new('ShaderNodeTexBrick')
            m_bricktexture2.location = (-1100,-600)
            m_bricktexture2.offset = 0.0
            m_bricktexture2.inputs[2].default_value = (0.0, 0.0, 0.0, 1)
            m_bricktexture2.inputs[3].default_value = (1.0, 1.0, 1.0, 1)
            m_bricktexture2.inputs[5].default_value = 0.005
            m_bricktexture2.inputs[6].default_value = 0.0
            m_bricktexture2.inputs[7].default_value = 1.0
            m_bricktexture2.inputs[8].default_value = 1.0
            m_bricktexture2.inputs[9].default_value = 1.0

            #mapping
            m_mapping = nodes.new('ShaderNodeMapping')
            m_mapping.location = (-1300,-400)
            m_mapping.inputs[1].default_value[0] = 10.0
            m_mapping.inputs[1].default_value[1] = 10.0

            #textcoord
            m_textcoord = nodes.new('ShaderNodeTexCoord')
            m_textcoord.location = (-1500,-400)

            #mathmultiply
            m_multiply = nodes.new('ShaderNodeMath')
            m_multiply.operation = 'MULTIPLY'
            m_multiply.location = (-1300,-800)
            m_multiply.inputs[1].default_value = 0.2

            #mapscale
            m_mapscale = nodes.new('ShaderNodeValue')
            m_mapscale.label = "Map Scale"
            m_mapscale.location = (-1500,-700)
            m_mapscale.outputs[0].default_value = 0.4

            #texscale
            m_texscale = nodes.new('ShaderNodeValue')
            m_texscale.label = "Texture Scale"
            m_texscale.location = (-1500,-800)
            m_texscale.outputs[0].default_value = 100.0

            #EnergyConservationGroup
            bpy.ops.node.ec_group_operator()
            ec_group = nodes.new("ShaderNodeGroup")
            ec_group.node_tree = bpy.data.node_groups['Energy Conservation']
            ec_group.location = (-500, -200)
            ec_group.inputs[0].default_value = 1.52
            ec_group.inputs[1].default_value = (0.045186, 0.141263, 0.144129, 1)
            ec_group.inputs[2].default_value = (0.01, 0.01, 0.01, 1)

            links = m_cutting_mat.node_tree.links.new

            links(m_texscale.outputs[0], m_multiply.inputs[0])
            links(m_texscale.outputs[0], m_bricktexture.inputs[4])
            links(m_mapscale.outputs[0], m_mapping.inputs[3])
            links(m_textcoord.outputs[2], m_mapping.inputs[0])
            links(m_multiply.outputs[0], m_bricktexture2.inputs[4])
            links(m_mapping.outputs[0], m_bricktexture.inputs[0])
            links(m_mapping.outputs[0], m_bricktexture2.inputs[0])
            links(m_bricktexture.outputs[0], m_add.inputs[1])
            links(m_bricktexture2.outputs[0], m_add.inputs[2])
            links(m_add.outputs[0], m_mix.inputs[0])
            links(m_mix.outputs[0], ec_group.inputs[1])
            links(ec_group.outputs[0], BSDF.inputs[0])
            links(ec_group.outputs[1], BSDF.inputs[7])
            # links(ec_group.outputs[2], BSDF.inputs[14])
            links(ec_group.outputs[3], BSDF.inputs[16])

            bpy.context.object.active_material = m_cutting_mat

        return {'FINISHED'}

# Source: Chris P Youtube (https://www.youtube.com/watch?v=fJyNCTXAdrQ)

# Default Cube
# Texture Scale:
# Map Scale > Grid Scale

# 100:
# 2.0  > 10x10
# 1.8  > 9x9
# 1.6  > 8x8
# 1.4  > 7x7
# 1.2  > 6x6
# 1.0  > 5x5
# 0.8  > 4x4
# 0.6  > 3x3
# 0.4  > 2x2
# 0.2  > 1x1

# 80:
# 2.5  > 10x10
# 2.25 > 9x9
# 2.0  > 8x8
# 1.75 > 7x7
# 1.5  > 6x6
# 1.25 > 5x5
# 1.0  > 4x4
# 0.75 > 3x3
# 0.5  > 2x2
# 0.25 > 1x1

# 50:
# 4.0  > 10x10
# 3.6  > 9x9
# 3.2  > 8x8
# 2.8  > 7x7
# 2.4  > 6x6
# 2.0  > 5x5
# 1.6  > 4x4
# 0.8  > 2x2
# 0.4  > 1x1
