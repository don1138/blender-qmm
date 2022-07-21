import bpy

# MESSAGE BOX
message_text = "This material already exists"
def ShowMessageBox(message = "", title = "", icon = 'INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

#GlassShaderOperator
class QMMGlass(bpy.types.Operator):
    """Add/Apply Glass Material to Selected Object (or Scene)"""
    bl_label = "QMM Glass Hack Shader"
    bl_idname = 'shader.qmm_glass_operator'
    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        m_glass = bpy.data.materials.get("QMM Glass Hack")
        if m_glass:
            ShowMessageBox(message_text, "QMM Glass Hack")
            # print(f"QMM Glass Hack already exists")
            bpy.context.object.active_material = m_glass
            return {'FINISHED'}
        else:
            #CreateShader
            m_glass = bpy.data.materials.new(name = "QMM Glass Hack")
            m_glass.use_nodes = True
            m_glass.diffuse_color = (1, 1, 1, 0.5)

            nodes = m_glass.node_tree.nodes

            #materialoutput
            material_output = nodes.get('Material Output')
            material_output.location = (0,0)

            #princibledbsdf
            BSDF = nodes.get('Principled BSDF')
            nodes.remove(BSDF)

            #mixshader
            m_mix = nodes.new('ShaderNodeMixShader')
            m_mix.location = (-200,0)

            #mathadd
            m_add = nodes.new('ShaderNodeMath')
            m_add.operation = 'ADD'
            m_add.location = (-400,200)

            #mixshader2
            m_mix2 = nodes.new('ShaderNodeMixShader')
            m_mix2.location = (-400,0)

            #mathadd2
            m_add2 = nodes.new('ShaderNodeMath')
            m_add2.operation = 'ADD'
            m_add2.location = (-600,300)

            #fresnel
            m_fresnel = nodes.new('ShaderNodeFresnel')
            m_fresnel.location = (-600,0)
            m_fresnel.inputs[0].default_value = 40

            #glossyshader
            m_glossy = nodes.new('ShaderNodeBsdfGlossy')
            m_glossy.location = (-600,-120)

            #transparentshader
            m_transparent = nodes.new('ShaderNodeBsdfTransparent')
            m_transparent.location = (-600,-300)
            m_transparent.inputs[0].default_value = (0.9, 0.9, 1, 1)

            #lightpath
            m_light_path = nodes.new('ShaderNodeLightPath')
            m_light_path.location = (-800,200)

            links = m_glass.node_tree.links

            links.new(m_transparent.outputs[0], m_mix2.inputs[2])
            links.new(m_glossy.outputs[0], m_mix2.inputs[1])
            links.new(m_fresnel.outputs[0], m_mix2.inputs[0])
            links.new(m_light_path.outputs[2], m_add2.inputs[1])
            links.new(m_light_path.outputs[1], m_add2.inputs[0])
            links.new(m_light_path.outputs[3], m_add.inputs[1])
            links.new(m_add2.outputs[0], m_add.inputs[0])
            links.new(m_transparent.outputs[0], m_mix.inputs[2])
            links.new(m_mix2.outputs[0], m_mix.inputs[1])
            links.new(m_add.outputs[0], m_mix.inputs[0])
            links.new(m_mix.outputs[0], material_output.inputs[0])

            bpy.context.object.active_material = m_glass

        return {'FINISHED'}
