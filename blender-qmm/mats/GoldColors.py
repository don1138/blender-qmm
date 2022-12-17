import bpy

# https://en.wikipedia.org/wiki/Gold_(color)

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


class GoldColorsGroup(bpy.types.Operator):
    """Add/Get Gold Colors Group Node"""
    bl_label = "Gold Colors Node Group"
    bl_idname = 'node.gold_colors_group_operator'

    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        ng_gcg = bpy.data.node_groups.get("Gold Colors")

        if not ng_gcg:
            self.make_group()
        return {'FINISHED'}

    def make_group(self):
        # newnodegroup
        gold_colors_group = bpy.data.node_groups.new(
            'Gold Colors', 'ShaderNodeTree')

        # groupinput
        # group_in = gold_colors_group.nodes.new('NodeGroupInput')
        # group_in.location(-400, 0)

        # groupoutput
        group_out = gold_colors_group.nodes.new('NodeGroupOutput')
        group_out.location = (0, 0)
        gold_colors_group.outputs.new('NodeSocketColor', 'Gold')
        gold_colors_group.outputs.new('NodeSocketColor', 'PBM Gold')
        gold_colors_group.outputs.new('NodeSocketColor', 'White Gold')
        gold_colors_group.outputs.new('NodeSocketColor', 'Chaos Gold')
        gold_colors_group.outputs.new('NodeSocketColor', 'Crayola Gold')
        gold_colors_group.outputs.new('NodeSocketColor', 'Vegas Gold')
        gold_colors_group.outputs.new('NodeSocketColor', 'Old Gold')
        gold_colors_group.outputs.new('NodeSocketColor', 'Satin Sheen Gold')
        gold_colors_group.outputs.new('NodeSocketColor', 'Pirate Gold')
        gold_colors_group.outputs.new('NodeSocketColor', 'Golden Yellow')
        gold_colors_group.outputs.new('NodeSocketColor', 'Golden Gold')
        gold_colors_group.outputs.new('NodeSocketColor', 'Golden Poppy')
        gold_colors_group.outputs.new('NodeSocketColor', 'Harvest Gold')

        # Gold
        gc_g = self.define_colors(
            gold_colors_group, "Gold", -600, 200, 0xD4AF37
        )

        # PBM Gold
        gc_pbmg = self.define_colors(
            gold_colors_group, "PBM Gold", -400, 200, 0xF9E4A4
        )

        # White Gold
        gc_wg = self.define_colors(
            gold_colors_group, "White Gold", -200, 200, 0xFFE39D
        )

        # Chaos Gold
        gc_chg = self.define_colors(
            gold_colors_group, "Chaos Gold", -600, 0, 0xF3C968
        )

        # Crayola Gold
        gc_cg = self.define_colors(
            gold_colors_group, "Crayola Gold", -400, 0, 0xE6BE8A
        )

        # Vegas Gold
        gc_vg = self.define_colors(
            gold_colors_group, "Vegas Gold", -200, 0, 0xC5B358
        )

        # Old Gold
        gc_og = self.define_colors(
            gold_colors_group, "Old Gold", -600, -200, 0xCFB53B
        )

        # Satin Sheen Gold
        gc_ssg = self.define_colors(
            gold_colors_group, "Satin Sheen Gold", -400, -200, 0xCBA135
        )

        # Pirate Gold
        gc_prtg = self.define_colors(
            gold_colors_group, "Pirate Gold", -200, -200, 0xAE8403
        )

        # Golden Yellow
        gc_gy = self.define_colors(
            gold_colors_group, "Golden Yellow", -600, -400, 0xFFDF00
        )

        # Golden Gold
        gc_gg = self.define_colors(
            gold_colors_group, "Golden Gold", -400, -400, 0xFFD700
        )

        # Golden Poppy
        gc_gp = self.define_colors(
            gold_colors_group, "Golden Poppy", -200, -400, 0xFCC200
        )

        # Harvest Gold
        gc_hg = self.define_colors(
            gold_colors_group, "Harvest Gold", -600, -600, 0xDA9100
        )

        links = gold_colors_group.links.new

        links(gc_g.outputs[0], group_out.inputs[0])
        links(gc_pbmg.outputs[0], group_out.inputs[1])
        links(gc_wg.outputs[0], group_out.inputs[2])
        links(gc_chg.outputs[0], group_out.inputs[3])
        links(gc_cg.outputs[0], group_out.inputs[4])
        links(gc_vg.outputs[0], group_out.inputs[5])
        links(gc_og.outputs[0], group_out.inputs[6])
        links(gc_ssg.outputs[0], group_out.inputs[7])
        links(gc_prtg.outputs[0], group_out.inputs[8])
        links(gc_gy.outputs[0], group_out.inputs[9])
        links(gc_gg.outputs[0], group_out.inputs[10])
        links(gc_gp.outputs[0], group_out.inputs[11])
        links(gc_hg.outputs[0], group_out.inputs[12])

    def define_colors(self, gold_colors_group, arg1, arg2, arg3, arg4):
        # Gold
        result = gold_colors_group.nodes.new('ShaderNodeRGB')
        result.label = arg1
        result.location = arg2, arg3
        result.outputs[0].default_value = hex_to_rgb(arg4)

        return result
