import bpy

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


class TitaniumColorsGroup(bpy.types.Operator):
    """Add/Get Titanium Colors Group Node"""
    bl_label  = "Titanium Colors Node Group"
    bl_idname = 'node.titanium_cg_operator'

    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        ng_tcg = bpy.data.node_groups.get("Titanium Colors")

        if not ng_tcg:
            self.make_group()
        return {'FINISHED'}

    def make_color(self, group, label, locX, locY, hex):
        result = group.nodes.new('ShaderNodeRGB')
        result.location = locX, locY
        result.label = label
        result.outputs[0].default_value = hex_to_rgb(hex)
        return result

    def make_group(self):
        # newnodegroup
        titanium_cg = bpy.data.node_groups.new('Titanium Colors', 'ShaderNodeTree')

        # groupinput
        # group_in = titanium_cg.nodes.new('NodeGroupInput')
        # group_in.location = (-400, 0)

        # groupoutput
        group_out = titanium_cg.nodes.new('NodeGroupOutput')
        group_out.location = (0, 0)
        if bpy.app.version < (4, 0, 0):
            titanium_cg.outputs.new('NodeSocketColor', 'Titanium')
            titanium_cg.outputs[0].default_value = (0.533276, 0.491021, 0.439657, 1)
            titanium_cg.outputs.new('NodeSocketColor', 'Chaos Titanium')
            titanium_cg.outputs.new('NodeSocketColor', 'Titanium White')
            titanium_cg.outputs.new('NodeSocketColor', 'PBM Titanium')
            titanium_cg.outputs.new('NodeSocketColor', 'Titanium Frost')
            titanium_cg.outputs.new('NodeSocketColor', 'Titanium Warm')
            titanium_cg.outputs.new('NodeSocketColor', 'Titanium Dark')
            titanium_cg.outputs.new('NodeSocketColor', 'Titanium Metallic')
            titanium_cg.outputs.new('NodeSocketColor', 'Titanium Blue')
        else:
            titanium_cg.interface.new_socket(name="Titanium", in_out='OUTPUT', socket_type='NodeSocketColor')
            titanium_cg.interface.items_tree[0].default_value = (0.533276, 0.491021, 0.439657, 1)
            titanium_cg.interface.new_socket(name="Chaos Titanium", in_out='OUTPUT', socket_type='NodeSocketColor')
            titanium_cg.interface.new_socket(name="Titanium White", in_out='OUTPUT', socket_type='NodeSocketColor')
            titanium_cg.interface.new_socket(name="PBM Titanium", in_out='OUTPUT', socket_type='NodeSocketColor')
            titanium_cg.interface.new_socket(name="Titanium Frost", in_out='OUTPUT', socket_type='NodeSocketColor')
            titanium_cg.interface.new_socket(name="Titanium Warm", in_out='OUTPUT', socket_type='NodeSocketColor')
            titanium_cg.interface.new_socket(name="Titanium Dark", in_out='OUTPUT', socket_type='NodeSocketColor')
            titanium_cg.interface.new_socket(name="Titanium Metallic", in_out='OUTPUT', socket_type='NodeSocketColor')
            titanium_cg.interface.new_socket(name="Titanium Blue", in_out='OUTPUT', socket_type='NodeSocketColor')

        # makecolors
        tc_t   = self.make_color(titanium_cg, "Titanium", -400, 300, 0xC1BAB1)
        tc_ct  = self.make_color(titanium_cg, "Chaos Titanium", -600, 300, 0xFCF9EA)
        tc_tw  = self.make_color(titanium_cg, "Titanium White", -800, 300, 0xF3F4F7)
        tc_pbm  = self.make_color(titanium_cg, "PBM Titanium", -1000, 300, 0xCEC9C3)
        tc_tf  = self.make_color(titanium_cg, "Titanium Frost", -1000, 0, 0xB0AFA9)
        tc_twr = self.make_color(titanium_cg, "Titanium Warm", -1000, -300, 0x9D948A)
        tc_dt  = self.make_color(titanium_cg, "Titanium Dark", -800, -300, 0x878681)
        tc_mt  = self.make_color(titanium_cg, "Titanium Metallic", -600, -300, 0x7A7772)
        tc_tb  = self.make_color(titanium_cg, "Titanium Blue", -400, -300, 0x5B798E)

        links = titanium_cg.links.new

        links(tc_t.outputs[0], group_out.inputs[0])
        links(tc_ct.outputs[0], group_out.inputs[1])
        links(tc_tw.outputs[0], group_out.inputs[2])
        links(tc_pbm.outputs[0], group_out.inputs[3])
        links(tc_tf.outputs[0], group_out.inputs[4])
        links(tc_twr.outputs[0], group_out.inputs[5])
        links(tc_dt.outputs[0], group_out.inputs[6])
        links(tc_mt.outputs[0], group_out.inputs[7])
        links(tc_tb.outputs[0], group_out.inputs[8])
