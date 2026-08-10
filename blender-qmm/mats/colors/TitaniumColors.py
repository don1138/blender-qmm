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
        result.outputs['Color'].default_value = hex_to_rgb(hex)
        return result

    def make_group(self):
        # newnodegroup
        titanium_cg = bpy.data.node_groups.new('Titanium Colors', 'ShaderNodeTree')

        # groupoutput
        group_out = titanium_cg.nodes.new('NodeGroupOutput')
        group_out.location = (0, 0)
        titanium_socket = titanium_cg.interface.new_socket(name="Titanium", in_out='OUTPUT', socket_type='NodeSocketColor')
        titanium_socket.default_value = (0.533276, 0.491021, 0.439657, 1)
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

        links(tc_t.outputs['Color'], group_out.inputs['Titanium'])
        links(tc_ct.outputs['Color'], group_out.inputs['Chaos Titanium'])
        links(tc_tw.outputs['Color'], group_out.inputs['Titanium White'])
        links(tc_pbm.outputs['Color'], group_out.inputs['PBM Titanium'])
        links(tc_tf.outputs['Color'], group_out.inputs['Titanium Frost'])
        links(tc_twr.outputs['Color'], group_out.inputs['Titanium Warm'])
        links(tc_dt.outputs['Color'], group_out.inputs['Titanium Dark'])
        links(tc_mt.outputs['Color'], group_out.inputs['Titanium Metallic'])
        links(tc_tb.outputs['Color'], group_out.inputs['Titanium Blue'])
