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
    bl_label  = "Gold Colors Node Group"
    bl_idname = 'node.gold_cg_operator'

    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        ng_gcg = bpy.data.node_groups.get("Gold Colors")

        if not ng_gcg:
            self.make_group()
        return {'FINISHED'}

    def make_color(self, group, arg1, arg2, arg3, arg4):
        result = group.nodes.new('ShaderNodeRGB')
        result.location = arg2, arg3
        result.label = arg1
        result.outputs[0].default_value = hex_to_rgb(arg4)

        return result

    def make_group(self):
        # newnodegroup
        gold_cg = bpy.data.node_groups.new(
            'Gold Colors', 'ShaderNodeTree')

        # groupinput
        # group_in = gold_cg.nodes.new('NodeGroupInput')
        # group_in.location(-400, 0)

        # groupoutput
        group_out = gold_cg.nodes.new('NodeGroupOutput')
        group_out.location = (0, 0)
        gold_cg.outputs.new('NodeSocketColor', 'Gold')
        gold_cg.outputs.new('NodeSocketColor', 'PBM Gold')
        gold_cg.outputs.new('NodeSocketColor', 'White Gold')
        gold_cg.outputs.new('NodeSocketColor', 'Chaos Gold')
        gold_cg.outputs.new('NodeSocketColor', 'Crayola Gold')
        gold_cg.outputs.new('NodeSocketColor', 'Vegas Gold')
        gold_cg.outputs.new('NodeSocketColor', 'Old Gold')
        gold_cg.outputs.new('NodeSocketColor', 'Satin Sheen Gold')
        gold_cg.outputs.new('NodeSocketColor', 'Pirate Gold')
        gold_cg.outputs.new('NodeSocketColor', 'Golden Yellow')
        gold_cg.outputs.new('NodeSocketColor', 'Golden Gold')
        gold_cg.outputs.new('NodeSocketColor', 'Golden Poppy')
        gold_cg.outputs.new('NodeSocketColor', 'Harvest Gold')

        # makecolors
        gc_g = self.make_color(gold_cg, "Gold", -400, 600, 0xD4AF37)
        gc_pbmg = self.make_color(gold_cg, "PBM Gold", -600, 600, 0xF9E4A4)
        gc_wg = self.make_color(gold_cg, "White Gold", -800, 600, 0xFFE39D)
        gc_chg = self.make_color(gold_cg, "Chaos Gold", -1000, 600, 0xF3C968)
        gc_cg = self.make_color(gold_cg, "Crayola Gold", -1200, 400, 0xE6BE8A)
        gc_vg = self.make_color(gold_cg, "Vegas Gold", -1000, 200, 0xC5B358)
        gc_og = self.make_color(gold_cg, "Old Gold", -1200, 0, 0xCFB53B)
        gc_ssg = self.make_color(gold_cg, "Satin Sheen Gold", -1000, -200, 0xCBA135)
        gc_prtg = self.make_color(gold_cg, "Pirate Gold", -1200, -400, 0xAE8403)
        gc_gy = self.make_color(gold_cg, "Golden Yellow", -1000, -600, 0xFFDF00)
        gc_gg = self.make_color(gold_cg, "Golden Gold", -800, -600, 0xFFD700)
        gc_gp = self.make_color(gold_cg, "Golden Poppy", -600, -600, 0xFCC200)
        gc_hg = self.make_color(gold_cg, "Harvest Gold", -400, -600, 0xDA9100)

        links = gold_cg.links.new

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
