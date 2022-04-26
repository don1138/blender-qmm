import bpy

class TexturizerGroup(bpy.types.Operator):
    """Add/Get Texturizer Group Node"""
    bl_label = "Texturizer Node Group"
    bl_idname = 'node.texturizer_group_operator'
    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        ng_texturizer = bpy.data.node_groups.get("Texturizer")

        if not ng_texturizer:
            #newnodegroup
            texturizer_group = bpy.data.node_groups.new('Texturizer', 'ShaderNodeTree')

            #groupinput
            group_in = texturizer_group.nodes.new('NodeGroupInput')
            group_in.location = (-800, 0)
            texturizer_group.inputs.new('NodeSocketColor', 'Color')
            texturizer_group.inputs.new('NodeSocketFloat', 'Saturation')
            texturizer_group.inputs.new('NodeSocketFloat', 'Mix')
            texturizer_group.inputs.new('NodeSocketFloat', 'Bump')
            texturizer_group.inputs.new('NodeSocketVector', 'Vector')
            texturizer_group.inputs[4].hide_value = True

            texturizer_group.inputs[1].default_value = 0.5
            texturizer_group.inputs[2].default_value = 0.5
            texturizer_group.inputs[3].default_value = 0.1

            #groupoutput
            group_out = texturizer_group.nodes.new('NodeGroupOutput')
            group_out.location = (0, 0)
            texturizer_group.outputs.new('NodeSocketColor', 'Color')
            texturizer_group.outputs.new('NodeSocketVector', 'Vector')

            #mixrgb-overlay
            n_mix_rgb = texturizer_group.nodes.new('ShaderNodeMixRGB')
            n_mix_rgb.location = (-200,100)
            n_mix_rgb.blend_type = 'OVERLAY'
            n_mix_rgb.inputs[0].default_value = 0.5

            #bump
            n_bump = texturizer_group.nodes.new('ShaderNodeBump')
            n_bump.location = (-200,-100)
            n_bump.inputs[0].default_value = 0.1

            #hsl
            n_hsl = texturizer_group.nodes.new('ShaderNodeHueSaturation')
            n_hsl.location = (-400,0)
            n_hsl.inputs[1].default_value = 0.5

            #maprange
            n_mr = texturizer_group.nodes.new('ShaderNodeMapRange')
            n_mr.location = (-400,-200)
            n_mr.inputs[1].default_value = 0.5
            n_mr.inputs[2].default_value = 0.6

            #noisetexture
            n_tex = texturizer_group.nodes.new('ShaderNodeTexNoise')
            n_tex.location = (-600,-100)
            n_tex.inputs[2].default_value = 256
            n_tex.inputs[3].default_value = 2.0
            n_tex.inputs[4].default_value = 0.5

            links = texturizer_group.links.new

            links(group_in.outputs[0], n_mix_rgb.inputs[1])
            links(group_in.outputs[1], n_hsl.inputs[1])
            links(group_in.outputs[2], n_mix_rgb.inputs[0])
            links(group_in.outputs[3], n_bump.inputs[0])
            links(group_in.outputs[4], n_tex.inputs[0])
            links(n_tex.outputs[0], n_mr.inputs[0])
            links(n_tex.outputs[1], n_hsl.inputs[4])
            links(n_hsl.outputs[0], n_mix_rgb.inputs[2])
            links(n_mr.outputs[0], n_bump.inputs[2])
            links(n_mix_rgb.outputs[0], group_out.inputs[0])
            links(n_bump.outputs[0], group_out.inputs[1])

        return {'FINISHED'}
