import bpy

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


class TitaniumColorsGroup(bpy.types.Operator):
    """Add/Get Titanium Colors Group Node"""
    bl_label = "Titanium Colors Node Group"
    bl_idname = 'node.titanium_colors_group_operator'
    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        ng_tcg = bpy.data.node_groups.get("Titanium Colors")

        if not ng_tcg:
            self.make_group()
        return {'FINISHED'}

    def make_group(self):
        #newnodegroup
        titanium_colors_group = bpy.data.node_groups.new('Titanium Colors', 'ShaderNodeTree')

        #groupinput
        # group_in = titanium_colors_group.nodes.new('NodeGroupInput')
        # group_in.location = (-400, 0)

        #groupoutput
        group_out = titanium_colors_group.nodes.new('NodeGroupOutput')
        group_out.location = (0, 0)
        titanium_colors_group.outputs.new('NodeSocketColor', 'Titanium')
        titanium_colors_group.outputs[0].default_value = (0.533276, 0.491021, 0.439657, 1)
        titanium_colors_group.outputs.new('NodeSocketColor', 'Chaos Titanium')
        titanium_colors_group.outputs.new('NodeSocketColor', 'Titanium White')
        titanium_colors_group.outputs.new('NodeSocketColor', 'Titanium Pale')
        titanium_colors_group.outputs.new('NodeSocketColor', 'Titanium Frost')
        titanium_colors_group.outputs.new('NodeSocketColor', 'PBM Titanium')
        titanium_colors_group.outputs.new('NodeSocketColor', 'Titanium Dark')
        titanium_colors_group.outputs.new('NodeSocketColor', 'Titanium Metallic')
        titanium_colors_group.outputs.new('NodeSocketColor', 'Titanium Blue')

        tc_t = self.define_color(
            titanium_colors_group, "Titanium", 800, 0xC1BAB1
        )
        tc_ct = self.define_color(
            titanium_colors_group, "Chaos Titanium", 600, 0xFCF9EA
        )
        tc_tw = self.define_color(
            titanium_colors_group, "Titanium White", 400, 0xF3F4F7
        )
        tc_pt = self.define_color(
            titanium_colors_group, "Titanium Pale", 200, 0xCEC8C2
        )
        tc_tf = self.define_color(
            titanium_colors_group, "Titanium Frost", 0, 0xB0AFA9
        )
        tc_pbm = self.define_color(
            titanium_colors_group, "PBM Titanium", -200, 0x9D948B
        )
        tc_dt = self.define_color(
            titanium_colors_group, "Titanium Dark", -400, 0x878681
        )
        tc_mt = self.define_color(
            titanium_colors_group, "Titanium Metallic", -600, 0x7A7772
        )
        tc_tb = self.define_color(
            titanium_colors_group, "Titanium Blue", -800, 0x5B798E
        )
        links = titanium_colors_group.links.new

        links(tc_t.outputs[0], group_out.inputs[0])
        links(tc_ct.outputs[0], group_out.inputs[1])
        links(tc_tw.outputs[0], group_out.inputs[2])
        links(tc_pt.outputs[0], group_out.inputs[3])
        links(tc_tf.outputs[0], group_out.inputs[4])
        links(tc_pbm.outputs[0], group_out.inputs[5])
        links(tc_dt.outputs[0], group_out.inputs[6])
        links(tc_mt.outputs[0], group_out.inputs[7])
        links(tc_tb.outputs[0], group_out.inputs[8])

    def define_color(self, titanium_colors_group, arg1, arg2, arg3):
        #Titanium
        result = titanium_colors_group.nodes.new('ShaderNodeRGB')
        result.label = arg1
        result.location = -800, arg2
        result.outputs[0].default_value = hex_to_rgb(arg3)

        return result
