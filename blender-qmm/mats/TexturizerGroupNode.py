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

    def make_group(self):
        #newnodegroup
        texturizer_group = bpy.data.node_groups.new('Texturizer', 'ShaderNodeTree')

        #groupinput
        group_in = texturizer_group.nodes.new('NodeGroupInput')
        group_in.location = (-1300, 0)
        texturizer_group.inputs.new('NodeSocketColor', 'Color')      # 0
        texturizer_group.inputs.new('NodeSocketFloat', 'Roughness')  # 1
        texturizer_group.inputs.new('NodeSocketFloat', 'Saturation') # 2
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

        #groupoutput
        group_out = texturizer_group.nodes.new('NodeGroupOutput')
        group_out.location = (0, 0)
        texturizer_group.outputs.new('NodeSocketColor', 'Color')         # 0
        texturizer_group.outputs.new('NodeSocketFloat', 'Rough Ceiling') # 1
        texturizer_group.outputs.new('NodeSocketFloat', 'Roughness')     # 2
        texturizer_group.outputs.new('NodeSocketFloat', 'Rough Floor')   # 3
        texturizer_group.outputs.new('NodeSocketColor', 'Height')        # 4
        texturizer_group.outputs.new('NodeSocketVector', 'Normal')       # 5

        #mixrgb-multiply
        n_mix_rgb = texturizer_group.nodes.new('ShaderNodeMixRGB')
        n_mix_rgb.location = (-300,500)
        n_mix_rgb.blend_type = 'MULTIPLY'
        n_mix_rgb.inputs[0].default_value = 0.5

        #maprange-roughceiling
        n_mr_rc = texturizer_group.nodes.new('ShaderNodeMapRange')
        n_mr_rc.label = "Rough Ceiling"
        n_mr_rc.location = (-300,300)
        n_mr_rc.inputs[1].default_value = 0.4
        n_mr_rc.inputs[2].default_value = 0.6

        #mixrgb-roughness
        n_mix_rough = texturizer_group.nodes.new('ShaderNodeMixRGB')
        n_mix_rough.location = (-300,00)
        n_mix_rough.blend_type = 'OVERLAY'
        n_mix_rough.inputs[0].default_value = 1.0

        #maprange-roughfloor
        n_mr_rf = texturizer_group.nodes.new('ShaderNodeMapRange')
        n_mr_rf.label = "Rough Floor"
        n_mr_rf.location = (-300,-200)
        n_mr_rf.inputs[1].default_value = 0.6
        n_mr_rf.inputs[2].default_value = 0.8

        #bump
        n_bump = texturizer_group.nodes.new('ShaderNodeBump')
        n_bump.location = (-300,-500)
        n_bump.inputs[0].default_value = 0.1

        #hsl
        n_hsl = texturizer_group.nodes.new('ShaderNodeHueSaturation')
        n_hsl.location = (-500,500)
        n_hsl.inputs[1].default_value = 0.5

        #mathsub
        n_msub = texturizer_group.nodes.new('ShaderNodeMath')
        n_msub.location = (-500,300)
        n_msub.operation = 'SUBTRACT'
        n_msub.inputs[1].default_value = 0.1

        #mathadd
        n_madd = texturizer_group.nodes.new('ShaderNodeMath')
        n_madd.location = (-500,-200)
        n_madd.operation = 'ADD'
        n_madd.inputs[1].default_value = 0.1

        #maprange
        n_mr = texturizer_group.nodes.new('ShaderNodeMapRange')
        n_mr.location = (-500,-500)
        n_mr.inputs[1].default_value = 0.5
        n_mr.inputs[2].default_value = 0.6

        n_rr11 = texturizer_group.nodes.new('NodeReroute')
        n_rr11.location = (-600,100)
        n_rr12 = texturizer_group.nodes.new('NodeReroute')
        n_rr12.location = (-600,-200)
        n_rr13 = texturizer_group.nodes.new('NodeReroute')
        n_rr13.location = (-600,-400)

        n_rr21 = texturizer_group.nodes.new('NodeReroute')
        n_rr21.location = (-700,200)
        n_rr22 = texturizer_group.nodes.new('NodeReroute')
        n_rr22.location = (-700,-100)
        n_rr23 = texturizer_group.nodes.new('NodeReroute')
        n_rr23.location = (-700,-300)

        #seperatergb
        n_sep_rgb = texturizer_group.nodes.new('ShaderNodeSeparateRGB')
        n_sep_rgb.location = (-900,0)

        #noisetexture
        n_tex = texturizer_group.nodes.new('ShaderNodeTexNoise')
        n_tex.location = (-1100,0)
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
