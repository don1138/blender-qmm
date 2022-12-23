import bpy

class TexturizerGroup(bpy.types.Operator):
    """Add/Get Texturizer Group Node"""
    bl_label = "Texturizer Node Group"
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

    def make_group(self):
        # newnodegroup
        texturizer_group = bpy.data.node_groups.new(
            'Texturizer', 'ShaderNodeTree')

        # groupinput
        group_in = self.make_node(texturizer_group, 'NodeGroupInput', -1300, 0)
        texturizer_group.inputs.new('NodeSocketColor', 'Color')      # 0
        texturizer_group.inputs.new('NodeSocketFloat', 'Roughness')  # 1
        texturizer_group.inputs.new('NodeSocketFloat', 'Saturation')  # 2
        texturizer_group.inputs.new('NodeSocketFloat', 'Mix')        # 3
        texturizer_group.inputs.new('NodeSocketFloat', 'Bump')       # 4
        texturizer_group.inputs.new('NodeSocketVector', 'Vector')    # 5
        texturizer_group.inputs[5].hide_value = True

        texturizer_group.inputs[1].default_value = 0.565
        texturizer_group.inputs[1].min_value = 0.0
        texturizer_group.inputs[1].max_value = 1.0
        texturizer_group.inputs[2].default_value = 0.5
        texturizer_group.inputs[2].min_value = 0.0
        texturizer_group.inputs[2].max_value = 2.0
        texturizer_group.inputs[3].default_value = 0.5
        texturizer_group.inputs[3].min_value = 0.0
        texturizer_group.inputs[3].max_value = 1.0
        texturizer_group.inputs[4].default_value = 0.1
        texturizer_group.inputs[4].min_value = 0.0
        texturizer_group.inputs[4].max_value = 1.0

        # groupoutput
        group_out = self.make_node(texturizer_group, 'NodeGroupOutput', 0, 0)
        texturizer_group.outputs.new('NodeSocketColor', 'Color')         # 0
        texturizer_group.outputs.new('NodeSocketFloat', 'Rough Ceiling')  # 1
        texturizer_group.outputs.new('NodeSocketFloat', 'Roughness')     # 2
        texturizer_group.outputs.new('NodeSocketFloat', 'Rough Floor')   # 3
        texturizer_group.outputs.new('NodeSocketColor', 'Height')        # 4
        texturizer_group.outputs.new('NodeSocketVector', 'Normal')       # 5

        # mixrgb-multiply
        n_mix_rgb = self.make_node(
            texturizer_group, 'ShaderNodeMixRGB', -300, 500)
        n_mix_rgb.blend_type = 'MULTIPLY'
        n_mix_rgb.inputs[0].default_value = 0.5

        # maprange-roughceiling
        n_mr_rc = self.make_node(
            texturizer_group, 'ShaderNodeMapRange', -300, 300)
        n_mr_rc.label = "Rough Ceiling"
        n_mr_rc.inputs[1].default_value = 0.4
        n_mr_rc.inputs[2].default_value = 0.6

        # mixrgb-roughness
        n_mix_rough = self.make_node(
            texturizer_group, 'ShaderNodeMixRGB', -300, 00)
        n_mix_rough.blend_type = 'OVERLAY'
        n_mix_rough.inputs[0].default_value = 1.0

        # maprange-roughfloor
        n_mr_rf = self.make_node(
            texturizer_group, 'ShaderNodeMapRange', -300, -200)
        n_mr_rf.label = "Rough Floor"
        n_mr_rf.inputs[1].default_value = 0.6
        n_mr_rf.inputs[2].default_value = 0.8

        # bump
        n_bump = self.make_node(texturizer_group, 'ShaderNodeBump', -300, -500)
        n_bump.inputs[0].default_value = 0.1

        # hsl
        n_hsl = self.make_node(
            texturizer_group, 'ShaderNodeHueSaturation', -500, 500)
        n_hsl.inputs[1].default_value = 0.5

        # mathsub
        n_msub = self.make_node(texturizer_group, 'ShaderNodeMath', -500, 300)
        n_msub.operation = 'SUBTRACT'
        n_msub.inputs[1].default_value = 0.1

        # mathadd
        n_madd = self.make_node(texturizer_group, 'ShaderNodeMath', -500, -200)
        n_madd.operation = 'ADD'
        n_madd.inputs[1].default_value = 0.1

        # maprange
        n_mr = self.make_node(
            texturizer_group, 'ShaderNodeMapRange', -500, -500)
        n_mr.inputs[1].default_value = 0.5
        n_mr.inputs[2].default_value = 0.6

        n_rr11 = self.make_node(texturizer_group, 'NodeReroute', -600, 100)
        n_rr12 = self.make_node(texturizer_group, 'NodeReroute', -600, -200)
        n_rr13 = self.make_node(texturizer_group, 'NodeReroute', -600, -400)

        n_rr21 = self.make_node(texturizer_group, 'NodeReroute', -700, 200)
        n_rr22 = self.make_node(texturizer_group, 'NodeReroute', -700, -100)
        n_rr23 = self.make_node(texturizer_group, 'NodeReroute', -700, -300)

        # seperatergb
        n_sep_rgb = self.make_node(
            texturizer_group, 'ShaderNodeSeparateRGB', -900, 0)

        # noisetexture
        n_tex = self.make_node(
            texturizer_group, 'ShaderNodeTexNoise', -1100, 0)
        n_tex.inputs[2].default_value = 256
        n_tex.inputs[3].default_value = 2.0
        n_tex.inputs[4].default_value = 0.5

        links = texturizer_group.links.new

        links(group_in.outputs[0], n_mix_rgb.inputs[1])
        links(group_in.outputs[1], n_rr12.inputs[0])
        links(group_in.outputs[2], n_hsl.inputs[1])
        links(group_in.outputs[3], n_mix_rgb.inputs[0])
        links(group_in.outputs[4], n_bump.inputs[0])
        links(group_in.outputs[5], n_tex.inputs[0])
        links(n_tex.outputs[1], n_hsl.inputs[4])
        links(n_tex.outputs[1], n_sep_rgb.inputs[0])
        links(n_sep_rgb.outputs[1], n_rr22.inputs[0])
        links(n_sep_rgb.outputs[2], n_mr.inputs[0])
        links(n_rr22.outputs[0], n_rr21.inputs[0])
        links(n_rr22.outputs[0], n_rr23.inputs[0])
        links(n_rr21.outputs[0], n_mr_rc.inputs[0])
        links(n_rr22.outputs[0], n_mix_rough.inputs[1])
        links(n_rr23.outputs[0], n_mr_rf.inputs[0])
        links(n_hsl.outputs[0], n_mix_rgb.inputs[2])
        links(n_msub.outputs[0], n_mr_rc.inputs[3])
        links(n_madd.outputs[0], n_mr_rf.inputs[4])
        links(n_mr.outputs[0], group_out.inputs[4])
        links(n_mr.outputs[0], n_bump.inputs[2])
        links(n_rr11.outputs[0], n_msub.inputs[1])
        links(n_rr11.outputs[0], n_mr_rc.inputs[4])
        links(n_rr12.outputs[0], n_rr11.inputs[0])
        links(n_rr12.outputs[0], n_mix_rough.inputs[2])
        links(n_rr12.outputs[0], n_rr13.inputs[0])
        links(n_rr13.outputs[0], n_madd.inputs[0])
        links(n_rr13.outputs[0], n_mr_rf.inputs[3])
        links(n_mix_rgb.outputs[0], group_out.inputs[0])
        links(n_mr_rc.outputs[0], group_out.inputs[1])
        links(n_mix_rough.outputs[0], group_out.inputs[2])
        links(n_mr_rf.outputs[0], group_out.inputs[3])
        links(n_bump.outputs[0], group_out.inputs[5])
