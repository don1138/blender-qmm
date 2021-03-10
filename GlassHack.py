import bpy

# MESSAGE BOX
message_text = "This material already exists"
def ShowMessageBox(message = "", title = "", icon = 'INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

#GlassShaderOperator
class Glass(bpy.types.Operator):
    bl_label = "Glass Hack Shader"
    bl_idname = 'shader.glass_operator'
    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        material_glass = bpy.data.materials.get("Glass Hack")
        if material_glass:
            ShowMessageBox(message_text, "Glass Hack")
            print(f"Glass Hack already exists")
            bpy.context.object.active_material = material_glass
            return {'FINISHED'}
        else:
            #CreateShader
            material_glass = bpy.data.materials.new(name = "Glass Hack")
            material_glass.use_nodes = True
            material_glass.diffuse_color = (0.737911, 0.737911, 1, 1)

            #materialoutput
            material_output = material_glass.node_tree.nodes.get('Material Output')
            material_output.location = (0,0)

            #princibledbsdf
            BSDF = material_glass.node_tree.nodes.get('Principled BSDF')
            material_glass.node_tree.nodes.remove(BSDF)

            #mixshader
            m_mix = material_glass.node_tree.nodes.new('ShaderNodeMixShader')
            m_mix.location = (-200,0)

            #mathadd
            m_add = material_glass.node_tree.nodes.new('ShaderNodeMath')
            m_add.operation = 'ADD'
            m_add.location = (-400,0)

            #mixshader2
            m_mix2 = material_glass.node_tree.nodes.new('ShaderNodeMixShader')
            m_mix2.location = (-400,-200)

            #mathadd2
            m_add2 = material_glass.node_tree.nodes.new('ShaderNodeMath')
            m_add2.operation = 'ADD'
            m_add2.location = (-600,100)

            #fresnel
            m_fresnel = material_glass.node_tree.nodes.new('ShaderNodeFresnel')
            m_fresnel.location = (-600,-200)
            m_fresnel.inputs[0].default_value = 40

            #glossyshader
            m_glossy = material_glass.node_tree.nodes.new('ShaderNodeBsdfGlossy')
            m_glossy.location = (-600,-320)

            #transparentshader
            m_transparent = material_glass.node_tree.nodes.new('ShaderNodeBsdfTransparent')
            m_transparent.location = (-600,-500)
            m_transparent.inputs[0].default_value = (0.737911, 0.737911, 1, 1)

            #lightpath
            m_light_path = material_glass.node_tree.nodes.new('ShaderNodeLightPath')
            m_light_path.location = (-800,0)

            material_glass.node_tree.links.new(m_transparent.outputs[0], m_mix2.inputs[2])
            material_glass.node_tree.links.new(m_glossy.outputs[0], m_mix2.inputs[1])
            material_glass.node_tree.links.new(m_fresnel.outputs[0], m_mix2.inputs[0])
            material_glass.node_tree.links.new(m_light_path.outputs[2], m_add2.inputs[1])
            material_glass.node_tree.links.new(m_light_path.outputs[1], m_add2.inputs[0])
            material_glass.node_tree.links.new(m_light_path.outputs[3], m_add.inputs[1])
            material_glass.node_tree.links.new(m_add2.outputs[0], m_add.inputs[0])
            material_glass.node_tree.links.new(m_transparent.outputs[0], m_mix.inputs[2])
            material_glass.node_tree.links.new(m_mix2.outputs[0], m_mix.inputs[1])
            material_glass.node_tree.links.new(m_add.outputs[0], m_mix.inputs[0])
            material_glass.node_tree.links.new(m_mix.outputs[0], material_output.inputs[0])

            bpy.context.object.active_material = material_glass

            return {'FINISHED'}
