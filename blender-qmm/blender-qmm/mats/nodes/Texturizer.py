import bpy

class TexturizerGroup(bpy.types.Operator):
    """Add/Get Texturizer Group Node"""
    bl_label  = "Texturizer Node Group"
    bl_idname = 'node.texturizer_group_operator'

    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        ng_texturizer = bpy.data.node_groups.get("Texturizer")

        if not ng_texturizer:
            self.make_group()
        return {'FINISHED'}

    def make_node(self, group, arg1, arg2, arg3):
        result = group.nodes.new(arg1)
        result.location = arg2, arg3
        return result

    def make_separate_rgb(self, group, x, y):
        n = self.make_node(group, "ShaderNodeSeparateColor", x, y)
        n.mode = 'RGB'
        return n

    def make_group(self):
        # newnodegroup
        texturizer_group = bpy.data.node_groups.new('Texturizer', 'ShaderNodeTree')

        # groupinput
        group_in = self.make_node(texturizer_group, 'NodeGroupInput', -1300, 0)
        texturizer_group.interface.new_socket(name="Color", in_out='INPUT', socket_type='NodeSocketColor')

        scale_socket = texturizer_group.interface.new_socket(name="Scale", in_out='INPUT', socket_type='NodeSocketFloat')
        scale_socket.default_value = 512.0
        scale_socket.min_value = 0
        scale_socket.max_value = 4096.0

        roughness_socket = texturizer_group.interface.new_socket(name="Roughness", in_out='INPUT', socket_type='NodeSocketFloat')
        roughness_socket.default_value = 0.565
        roughness_socket.min_value = 0
        roughness_socket.max_value = 1

        saturation_socket = texturizer_group.interface.new_socket(name="Saturation", in_out='INPUT', socket_type='NodeSocketFloat')
        saturation_socket.default_value = 0.5
        saturation_socket.min_value = 0
        saturation_socket.max_value = 2

        mix_socket = texturizer_group.interface.new_socket(name="Mix", in_out='INPUT', socket_type='NodeSocketFloat')
        mix_socket.default_value = 0.5
        mix_socket.min_value = 0
        mix_socket.max_value = 1

        bump_socket = texturizer_group.interface.new_socket(name="Bump", in_out='INPUT', socket_type='NodeSocketFloat')
        bump_socket.default_value = 0.1
        bump_socket.min_value = 0
        bump_socket.max_value = 1

        vector_socket = texturizer_group.interface.new_socket(name="Vector", in_out='INPUT', socket_type='NodeSocketVector')
        vector_socket.hide_value = True

        # groupoutput
        group_out = self.make_node(texturizer_group, 'NodeGroupOutput', 0, 0)
        texturizer_group.interface.new_socket(name="Color", in_out='OUTPUT', socket_type='NodeSocketColor')
        texturizer_group.interface.new_socket(name="Rough Ceiling", in_out='OUTPUT', socket_type='NodeSocketFloat')
        texturizer_group.interface.new_socket(name="Roughness", in_out='OUTPUT', socket_type='NodeSocketFloat')
        texturizer_group.interface.new_socket(name="Rough Floor", in_out='OUTPUT', socket_type='NodeSocketFloat')
        texturizer_group.interface.new_socket(name="Height", in_out='OUTPUT', socket_type='NodeSocketFloat')
        texturizer_group.interface.new_socket(name="Normal", in_out='OUTPUT', socket_type='NodeSocketVector')

        # mixrgb-multiply
        n_mix_rgb = self.make_node(texturizer_group, 'ShaderNodeMix', -300, 600)
        n_mix_rgb.data_type = 'RGBA'
        n_mix_rgb.blend_type = 'MULTIPLY'
        n_mix_rgb.inputs[0].default_value = 0.5

        # maprange-roughceiling
        n_mr_rc = self.make_node(texturizer_group, 'ShaderNodeMapRange', -300, 300)
        n_mr_rc.label = "Rough Ceiling"
        n_mr_rc.inputs[1].default_value = 0.4
        n_mr_rc.inputs[2].default_value = 0.6

        # mixrgb-roughness
        n_mix_rough = self.make_node(texturizer_group, 'ShaderNodeMix', -300, 00)
        n_mix_rough.data_type = 'RGBA'
        n_mix_rough.blend_type = 'OVERLAY'
        n_mix_rough.inputs[0].default_value = 1.0

        # maprange-roughfloor
        n_mr_rf = self.make_node(texturizer_group, 'ShaderNodeMapRange', -300, -200)
        n_mr_rf.label = "Rough Floor"
        n_mr_rf.inputs[1].default_value = 0.6
        n_mr_rf.inputs[2].default_value = 0.8

        # bump
        n_bump = self.make_node(texturizer_group, 'ShaderNodeBump', -300, -500)
        n_bump.inputs['Strength'].default_value = 0.1

        # hsl
        n_hsl = self.make_node(
            texturizer_group, 'ShaderNodeHueSaturation', -500, 500)
        n_hsl.inputs['Saturation'].default_value = 0.5

        # mathsub
        n_msub = self.make_node(texturizer_group, 'ShaderNodeMath', -500, 300)
        n_msub.operation = 'SUBTRACT'
        n_msub.inputs[1].default_value = 0.1

        # mathadd
        n_madd = self.make_node(texturizer_group, 'ShaderNodeMath', -500, -200)
        n_madd.operation = 'ADD'
        n_madd.inputs[1].default_value = 0.1

        # maprange
        n_mr = self.make_node(texturizer_group, 'ShaderNodeMapRange', -500, -500)
        n_mr.inputs[1].default_value = 0.5
        n_mr.inputs[2].default_value = 0.6

        n_rr11 = self.make_node(texturizer_group, 'NodeReroute', -600, 100)
        n_rr12 = self.make_node(texturizer_group, 'NodeReroute', -600, -200)
        n_rr13 = self.make_node(texturizer_group, 'NodeReroute', -600, -400)

        n_rr21 = self.make_node(texturizer_group, 'NodeReroute', -700, 200)
        n_rr22 = self.make_node(texturizer_group, 'NodeReroute', -700, -100)
        n_rr23 = self.make_node(texturizer_group, 'NodeReroute', -700, -300)

        # seperatergb
        n_sep_rgb = self.make_separate_rgb(
            texturizer_group, -900, 0
        )

        # noisetexture
        n_tex = self.make_node(texturizer_group, 'ShaderNodeTexNoise', -1100, 0)
        n_tex.inputs['Scale'].default_value = 256
        n_tex.inputs['Detail'].default_value = 2.0
        n_tex.inputs['Roughness'].default_value = 0.5

        links = texturizer_group.links.new

        links(group_in.outputs['Scale'], n_tex.inputs['Scale'])
        links(group_in.outputs['Roughness'], n_rr12.inputs['Input'])
        links(group_in.outputs['Saturation'], n_hsl.inputs['Saturation'])
        links(group_in.outputs['Mix'], n_mix_rgb.inputs[0])
        links(group_in.outputs['Bump'], n_bump.inputs['Strength'])
        # links(group_in.outputs['Vector'], n_tex.inputs['Vector'])
        links(n_tex.outputs['Color'], n_hsl.inputs['Color'])
        links(n_tex.outputs['Color'], n_sep_rgb.inputs['Color'])
        links(n_sep_rgb.outputs['Green'], n_rr22.inputs['Input'])
        links(n_sep_rgb.outputs['Blue'], n_mr.inputs['Value'])
        links(n_rr22.outputs['Output'], n_rr21.inputs['Input'])
        links(n_rr22.outputs['Output'], n_rr23.inputs['Input'])
        links(n_rr21.outputs['Output'], n_mr_rc.inputs['Value'])
        links(n_rr23.outputs['Output'], n_mr_rf.inputs['Value'])
        links(n_msub.outputs['Value'], n_mr_rc.inputs[3])
        links(n_madd.outputs['Value'], n_mr_rf.inputs[4])
        links(n_mr.outputs['Result'], group_out.inputs['Height'])
        links(n_mr.outputs['Result'], n_bump.inputs['Height'])
        links(n_rr11.outputs['Output'], n_msub.inputs[0])
        links(n_rr11.outputs['Output'], n_mr_rc.inputs[4])
        links(n_rr12.outputs['Output'], n_rr11.inputs['Input'])
        links(n_rr12.outputs['Output'], n_rr13.inputs['Input'])
        links(n_rr13.outputs['Output'], n_madd.inputs[0])
        links(n_rr13.outputs['Output'], n_mr_rf.inputs[3])
        links(n_mr_rc.outputs['Result'], group_out.inputs['Rough Ceiling'])
        links(n_mr_rf.outputs['Result'], group_out.inputs['Rough Floor'])
        links(n_bump.outputs['Normal'], group_out.inputs['Normal'])

        links(group_in.outputs['Color'], n_mix_rgb.inputs[6])
        links(n_rr22.outputs['Output'], n_mix_rough.inputs[6])
        links(n_hsl.outputs['Color'], n_mix_rgb.inputs[7])
        links(n_rr12.outputs['Output'], n_mix_rough.inputs[7])
        links(n_mix_rgb.outputs[2], group_out.inputs['Color'])
        links(n_mix_rough.outputs[2], group_out.inputs['Roughness'])
