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
        material_cutting_mat = bpy.data.materials.get("QMM Rubber Cutting Mat")
        if material_cutting_mat:
            ShowMessageBox(message_text, "QMM Rubber Cutting Mat")
            # print(f"QMM Rubber Cutting Mat already exists")
            bpy.context.object.active_material = material_cutting_mat
            return {'FINISHED'}
        else:
            #CreateShader
            material_cutting_mat = bpy.data.materials.new(name = "QMM Rubber Cutting Mat")
            material_cutting_mat.use_nodes = True
            material_cutting_mat.diffuse_color = (0.045186, 0.141263, 0.144129, 1)
            material_cutting_mat.roughness = 0.79

            #materialoutput
            material_output = material_cutting_mat.node_tree.nodes.get('Material Output')
            material_output.location = (0,0)

            #princibledbsdf
            BSDF = material_cutting_mat.node_tree.nodes.get('Principled BSDF')
            BSDF.location = (-300,0)
            BSDF.inputs[0].default_value = (0.045186, 0.141263, 0.144129, 1)
            BSDF.inputs[5].default_value = 0.425
            BSDF.inputs[7].default_value = 0.79

            #rgbmix
            m_mix = material_cutting_mat.node_tree.nodes.new('ShaderNodeMixRGB')
            m_mix.location = (-500,0)
            m_mix.inputs[1].default_value = (0.045186, 0.141263, 0.144129, 1)
            m_mix.inputs[2].default_value = (0.187821, 0.450786, 0.558341, 1)

            #rgbadd
            m_add = material_cutting_mat.node_tree.nodes.new('ShaderNodeMixRGB')
            m_add.blend_type = 'ADD'
            m_add.location = (-700,0)

            #bricktexture
            m_bricktexture = material_cutting_mat.node_tree.nodes.new('ShaderNodeTexBrick')
            m_bricktexture.location = (-900,0)
            m_bricktexture.offset = 0.0
            m_bricktexture.inputs[2].default_value = (0.0, 0.0, 0.0, 1)
            m_bricktexture.inputs[3].default_value = (1.0, 1.0, 1.0, 1)
            m_bricktexture.inputs[5].default_value = 0.005
            m_bricktexture.inputs[6].default_value = 0.0
            m_bricktexture.inputs[7].default_value = 1.0
            m_bricktexture.inputs[8].default_value = 1.0
            m_bricktexture.inputs[9].default_value = 1.0

            #bricktexture2
            m_bricktexture2 = material_cutting_mat.node_tree.nodes.new('ShaderNodeTexBrick')
            m_bricktexture2.location = (-900,-400)
            m_bricktexture2.offset = 0.0
            m_bricktexture2.inputs[2].default_value = (0.0, 0.0, 0.0, 1)
            m_bricktexture2.inputs[3].default_value = (1.0, 1.0, 1.0, 1)
            m_bricktexture2.inputs[5].default_value = 0.005
            m_bricktexture2.inputs[6].default_value = 0.0
            m_bricktexture2.inputs[7].default_value = 1.0
            m_bricktexture2.inputs[8].default_value = 1.0
            m_bricktexture2.inputs[9].default_value = 1.0

            #mapping
            m_mapping = material_cutting_mat.node_tree.nodes.new('ShaderNodeMapping')
            m_mapping.location = (-1100,-200)
            m_mapping.inputs[1].default_value[0] = 10.0
            m_mapping.inputs[1].default_value[1] = 10.0

            #textcoord
            m_textcoord = material_cutting_mat.node_tree.nodes.new('ShaderNodeTexCoord')
            m_textcoord.location = (-1300,-200)

            #mathmultiply
            m_multiply = material_cutting_mat.node_tree.nodes.new('ShaderNodeMath')
            m_multiply.operation = 'MULTIPLY'
            m_multiply.location = (-1100,-600)
            m_multiply.inputs[1].default_value = 0.2

            #mapscale
            m_mapscale = material_cutting_mat.node_tree.nodes.new('ShaderNodeValue')
            m_mapscale.location = (-1300,-500)
            m_mapscale.outputs[0].default_value = 0.8

            #texscale
            m_texscale = material_cutting_mat.node_tree.nodes.new('ShaderNodeValue')
            m_texscale.location = (-1300,-600)
            m_texscale.outputs[0].default_value = 50.0

            material_cutting_mat.node_tree.links.new(m_texscale.outputs[0], m_multiply.inputs[0])
            material_cutting_mat.node_tree.links.new(m_texscale.outputs[0], m_bricktexture.inputs[4])
            material_cutting_mat.node_tree.links.new(m_mapscale.outputs[0], m_mapping.inputs[3])
            material_cutting_mat.node_tree.links.new(m_textcoord.outputs[2], m_mapping.inputs[0])
            material_cutting_mat.node_tree.links.new(m_multiply.outputs[0], m_bricktexture2.inputs[4])
            material_cutting_mat.node_tree.links.new(m_mapping.outputs[0], m_bricktexture.inputs[0])
            material_cutting_mat.node_tree.links.new(m_mapping.outputs[0], m_bricktexture2.inputs[0])
            material_cutting_mat.node_tree.links.new(m_bricktexture.outputs[0], m_add.inputs[1])
            material_cutting_mat.node_tree.links.new(m_bricktexture2.outputs[0], m_add.inputs[2])
            material_cutting_mat.node_tree.links.new(m_add.outputs[0], m_mix.inputs[0])
            material_cutting_mat.node_tree.links.new(m_mix.outputs[0], BSDF.inputs[0])

            bpy.context.object.active_material = material_cutting_mat

            return {'FINISHED'}
