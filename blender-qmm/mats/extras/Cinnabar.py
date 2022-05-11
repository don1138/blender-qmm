import bpy

# MESSAGE BOX
message_text = "This material already exists"
def ShowMessageBox(message = "", title = "", icon = 'INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

#CinnabarShaderOperator
class QMMCinnabar(bpy.types.Operator):
    """Add/Apply Cinnabar Material to Selected Object (or Scene)"""
    bl_label = "QMM Cinnabar Shader"
    bl_idname = 'shader.qmm_cinnabar_operator'
    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        m_cinnabar = bpy.data.materials.get("QMM Cinnabar")
        if m_cinnabar:
            ShowMessageBox(message_text, "QMM Cinnabar")
            # print(f"QMM Cinnabar already exists")
            bpy.context.object.active_material = m_cinnabar
            return {'FINISHED'}
        else:
            #CreateShader
            m_cinnabar = bpy.data.materials.new(name = "QMM Cinnabar")
            m_cinnabar.use_nodes = True
            m_cinnabar.diffuse_color = (0.768151, 0.054480, 0.034340, 1.0)
            m_cinnabar.metallic = 1
            m_cinnabar.roughness = 0.6

            nodes = m_cinnabar.node_tree.nodes

            #materialoutput
            material_output = nodes.get('Material Output')
            material_output.location = (0,0)

            #princibledbsdf
            BSDF = nodes.get('Principled BSDF')
            BSDF.location = (-300,0)
            BSDF.inputs[0].default_value = (0.768151, 0.054480, 0.034340, 1.0)
            BSDF.inputs[6].default_value = 1
            BSDF.inputs[9].default_value = 0.4
            BSDF.inputs[16].default_value = 3.2

            #colorramp
            m_colorramp = nodes.new('ShaderNodeValToRGB')
            m_colorramp.label = "Cinnabar"
            m_colorramp.location = (-600,0)
            m_colorramp.color_ramp.elements[0].color = (0.283149, 0.039546, 0.031896, 1.0)
            m_colorramp.color_ramp.elements[1].color = (0.768151, 0.054480, 0.034340, 1.0)

            nodes = m_cinnabar.node_tree.nodes

            #TexturizerGroup
            bpy.ops.node.texturizer_group_operator()
            texturizer_group = nodes.new("ShaderNodeGroup")
            texturizer_group.node_tree = bpy.data.node_groups['Texturizer']
            texturizer_group.location = (-900, -200)
            texturizer_group.width = 240
            texturizer_group.inputs[0].default_value = (0.768151, 0.054480, 0.034340, 1.0)
            texturizer_group.inputs[1].default_value = 0.4
            texturizer_group.inputs[4].default_value = 0.0125

            #SpecularGroup
            bpy.ops.node.specular_group_operator()
            specular_group = nodes.new("ShaderNodeGroup")
            specular_group.node_tree = bpy.data.node_groups['Specular']
            specular_group.location = (-600, -400)
            specular_group.width = 240
            specular_group.inputs[0].default_value = 3.2

            #Links
            links = m_cinnabar.node_tree.links.new
            links(m_colorramp.outputs[0], BSDF.inputs[0])
            links(texturizer_group.outputs[3], m_colorramp.inputs[0])
            links(texturizer_group.outputs[3], BSDF.inputs[9])
            links(texturizer_group.outputs[5], BSDF.inputs[22])
            links(specular_group.outputs[0], BSDF.inputs[7])
            links(specular_group.outputs[1], BSDF.inputs[16])

            #LOAD THE MATERIAL
            bpy.context.object.active_material = m_cinnabar

        return {'FINISHED'}
