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
    bl_label = "QMM Glass Shader"
    bl_idname = 'shader.qmm_glass_operator'
    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        m_glass = bpy.data.materials.get("QMM Glass")
        if m_glass:
            ShowMessageBox(message_text, "QMM Glass")
            # print(f"QMM Glass already exists")
            bpy.context.object.active_material = m_glass
            return {'FINISHED'}
        else:
            #CreateShader
            m_glass = bpy.data.materials.new(name = "QMM Glass")
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
            m_glossy.distribution = 'SHARP'
            m_glossy.inputs[0].default_value = (1, 1, 1, 1)
            m_glossy.inputs[1].default_value = 0

            #transparentshader
            m_transparent = nodes.new('ShaderNodeBsdfTransparent')
            m_transparent.location = (-600,-300)
            m_transparent.inputs[0].default_value = (1, 1, 1, 1)

            #lightpath
            m_light_path = nodes.new('ShaderNodeLightPath')
            m_light_path.location = (-800,200)

            #mixrgb
            m_mixrgb = nodes.new('ShaderNodeMixRGB')
            m_mixrgb.location = (-800,-300)
            m_mixrgb.inputs[0].default_value = 0.38196
            m_mixrgb.inputs[1].default_value = (1.61804, 1.61804, 1.61804, 1)

            #noise
            m_noise = nodes.new('ShaderNodeTexNoise')
            m_noise.location = (-1000,-300)
            m_noise.inputs[2].default_value = 3.14159
            m_noise.inputs[3].default_value = 0
            m_noise.inputs[4].default_value = 1

            links = m_glass.node_tree.links.new

            links(m_noise.outputs[0], m_mixrgb.inputs[2])
            links(m_mixrgb.outputs[0], m_transparent.inputs[0])
            links(m_transparent.outputs[0], m_mix2.inputs[2])
            links(m_glossy.outputs[0], m_mix2.inputs[1])
            links(m_fresnel.outputs[0], m_mix2.inputs[0])
            links(m_light_path.outputs[2], m_add2.inputs[1])
            links(m_light_path.outputs[1], m_add2.inputs[0])
            links(m_light_path.outputs[3], m_add.inputs[1])
            links(m_add2.outputs[0], m_add.inputs[0])
            links(m_transparent.outputs[0], m_mix.inputs[2])
            links(m_mix2.outputs[0], m_mix.inputs[1])
            links(m_add.outputs[0], m_mix.inputs[0])
            links(m_mix.outputs[0], material_output.inputs[0])

            bpy.context.object.active_material = m_glass
            bpy.context.object.active_material.blend_method = 'BLEND'
            bpy.context.object.active_material.shadow_method = 'NONE'

        return {'FINISHED'}
