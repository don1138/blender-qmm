import bpy

# https://en.wikipedia.org/wiki/Silver_(color)

# HEX TO RGB CALCS

def srgb_to_linearrgb(c):
    if   c < 0:       return 0
    elif c < 0.04045: return c/12.92
    else:             return ((c+0.055)/1.055)**2.4

def hex_to_rgb(h,alpha=1):
    r = (h & 0xff0000) >> 16
    g = (h & 0x00ff00) >> 8
    b = (h & 0x0000ff)
    return tuple([srgb_to_linearrgb(c/0xff) for c in (r,g,b)] + [alpha])


class SilverColorsGroup(bpy.types.Operator):
    """Add/Get Silver Colors Group Node"""
    bl_label = "Silver Colors Node Group"
    bl_idname = 'node.silver_colors_group_operator'
    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        ng_scg = bpy.data.node_groups.get("Silver Colors")

        if not ng_scg:
            self.make_group()
        return {'FINISHED'}

    def make_group(self):
        #newnodegroup
        silver_colors_group = bpy.data.node_groups.new('Silver Colors', 'ShaderNodeTree')

        #groupinput
        # group_in = silver_colors_group.nodes.new('NodeGroupInput')
        # group_in.location = (-400, 0)

        #groupoutput
        group_out = silver_colors_group.nodes.new('NodeGroupOutput')
        group_out.location = (0, 0)
        silver_colors_group.outputs.new('NodeSocketColor', 'Silver')
        silver_colors_group.outputs.new('NodeSocketColor', 'Pale Silver')
        silver_colors_group.outputs.new('NodeSocketColor', 'PBM Silver')
        silver_colors_group.outputs.new('NodeSocketColor', 'Crayola Silver')
        silver_colors_group.outputs.new('NodeSocketColor', 'Silver Pink')
        silver_colors_group.outputs.new('NodeSocketColor', 'Basic Silver')
        silver_colors_group.outputs.new('NodeSocketColor', 'Silver Sand')
        silver_colors_group.outputs.new('NodeSocketColor', 'Silver Chalice')
        silver_colors_group.outputs.new('NodeSocketColor', 'Old Silver')
        silver_colors_group.outputs.new('NodeSocketColor', 'Roman Silver')
        silver_colors_group.outputs.new('NodeSocketColor', 'Sonic Silver')

        sc_s = self.define_colors(
            silver_colors_group, "Silver", 1000, 0xAAA9AD
        )
        sc_ps = self.define_colors(
            silver_colors_group, "Pale Silver", 800, 0xFCFAF5
        )
        sc_pbms = self.define_colors(
            silver_colors_group, "PBM Silver", 600, 0xFBF9F6
        )
        sc_cs = self.define_colors(
            silver_colors_group, "Crayola Silver", 400, 0xC9C0BB
        )
        sc_sp = self.define_colors(
            silver_colors_group, "Silver Pink", 200, 0xC4AEAD
        )
        sc_bs = self.define_colors(
            silver_colors_group, "Basic Silver", 0, 0xC0C0C0
        )
        sc_ss = self.define_colors(
            silver_colors_group, "Silver Sand", -200, 0xBFC1C2
        )
        sc_sc = self.define_colors(
            silver_colors_group, "Silver Chalice", -400, 0xACACAC
        )
        sc_os = self.define_colors(
            silver_colors_group, "Old Silver", -600, 0x848482
        )
        sc_rs = self.define_colors(
            silver_colors_group, "Roman Silver", -800, 0x838996
        )
        sc_sos = self.define_colors(
            silver_colors_group, "Sonic Silver", -1000, 0x757575
        )
        links = silver_colors_group.links.new

        links(sc_s.outputs[0], group_out.inputs[0])
        links(sc_ps.outputs[0], group_out.inputs[1])
        links(sc_pbms.outputs[0], group_out.inputs[2])
        links(sc_cs.outputs[0], group_out.inputs[3])
        links(sc_sp.outputs[0], group_out.inputs[4])
        links(sc_bs.outputs[0], group_out.inputs[5])
        links(sc_ss.outputs[0], group_out.inputs[6])
        links(sc_sc.outputs[0], group_out.inputs[7])
        links(sc_os.outputs[0], group_out.inputs[8])
        links(sc_rs.outputs[0], group_out.inputs[9])
        links(sc_sos.outputs[0], group_out.inputs[10])

    def define_colors(self, silver_colors_group, arg1, arg2, arg3):
        #Silver
        result = silver_colors_group.nodes.new('ShaderNodeRGB')
        result.label = arg1
        result.location = -800, arg2
        result.outputs[0].default_value = hex_to_rgb(arg3)

        return result
