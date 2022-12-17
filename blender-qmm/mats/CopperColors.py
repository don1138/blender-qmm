import bpy

# https://en.wikipedia.org/wiki/Copper_(color)

# HEX TO RGB CALCS


def srgb_to_linearrgb(c):
    if c < 0:
        return 0
    elif c < 0.04045:
        return c/12.92
    else:
        return ((c+0.055)/1.055)**2.4


def hex_to_rgb(h, alpha=1):
    r = (h & 0xff0000) >> 16
    g = (h & 0x00ff00) >> 8
    b = (h & 0x0000ff)
    return tuple([srgb_to_linearrgb(c/0xff) for c in (r, g, b)] + [alpha])


class CopperColorsGroup(bpy.types.Operator):
    """Add/Get Copper Colors Group Node"""
    bl_label = "Copper Colors Node Group"
    bl_idname = 'node.copper_colors_group_operator'

    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        ng_ccg = bpy.data.node_groups.get("Copper Colors")

        if not ng_ccg:
            self.make_group()
        return {'FINISHED'}

    def make_group(self):
        # newnodegroup
        copper_colors_group = bpy.data.node_groups.new(
            'Copper Colors', 'ShaderNodeTree')

        # groupinput
        # group_in = copper_colors_group.nodes.new('NodeGroupInput')
        # group_in.location = (-400, 0)

        # groupoutput
        group_out = copper_colors_group.nodes.new('NodeGroupOutput')
        group_out.location = (0, 0)
        copper_colors_group.outputs.new('NodeSocketColor', 'Copper')
        copper_colors_group.outputs.new('NodeSocketColor', 'PBM Copper')
        copper_colors_group.outputs.new('NodeSocketColor', 'Dontnod Copper')
        copper_colors_group.outputs.new('NodeSocketColor', 'Pale Copper')
        copper_colors_group.outputs.new('NodeSocketColor', 'Copper Red')
        copper_colors_group.outputs.new('NodeSocketColor', 'Copper Penny')
        copper_colors_group.outputs.new('NodeSocketColor', 'Copper Rose')

        cc_c = self.define_color(
            copper_colors_group, "Copper", 600, 0xB87333
        )
        cc_pbmc = self.define_color(
            copper_colors_group, "PBM Copper", 400, 0xF7DDBC
        )
        cc_dc = self.define_color(
            copper_colors_group, "Dontnod Copper", 200, 0xFAD0C0
        )
        cc_pc = self.define_color(
            copper_colors_group, "Pale Copper", 0, 0xDA8A67
        )
        cc_cr = self.define_color(
            copper_colors_group, "Copper Red", -200, 0xCB6D51
        )
        cc_cp = self.define_color(
            copper_colors_group, "Copper Penny", -400, 0xAD6F69
        )
        cc_cro = self.define_color(
            copper_colors_group, "Copper Rose", -600, 0x996666
        )
        links = copper_colors_group.links.new

        links(cc_c.outputs[0], group_out.inputs[0])
        links(cc_pbmc.outputs[0], group_out.inputs[1])
        links(cc_dc.outputs[0], group_out.inputs[2])
        links(cc_pc.outputs[0], group_out.inputs[3])
        links(cc_cr.outputs[0], group_out.inputs[4])
        links(cc_cp.outputs[0], group_out.inputs[5])
        links(cc_cro.outputs[0], group_out.inputs[6])

    def define_color(self, copper_colors_group, arg1, arg2, arg3):
        # Copper
        result = copper_colors_group.nodes.new('ShaderNodeRGB')
        result.label = arg1
        result.location = -800, arg2
        result.outputs[0].default_value = hex_to_rgb(arg3)

        return result
