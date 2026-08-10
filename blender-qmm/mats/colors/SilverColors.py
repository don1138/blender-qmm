import bpy

# https://en.wikipedia.org/wiki/Silver_(color)

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


class SilverColorsGroup(bpy.types.Operator):
    """Add/Get Silver Colors Group Node"""
    bl_label  = "Silver Colors Node Group"
    bl_idname = 'node.silver_cg_operator'

    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        ng_scg = bpy.data.node_groups.get("Silver Colors")

        if not ng_scg:
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
        silver_cg = bpy.data.node_groups.new('Silver Colors', 'ShaderNodeTree')

        # groupoutput
        group_out = silver_cg.nodes.new('NodeGroupOutput')
        group_out.location = (0, 0)
        silver_cg.interface.new_socket(name="Silver", in_out='OUTPUT', socket_type='NodeSocketColor')
        silver_cg.interface.new_socket(name="Pale Silver", in_out='OUTPUT', socket_type='NodeSocketColor')
        silver_cg.interface.new_socket(name="PBM Silver", in_out='OUTPUT', socket_type='NodeSocketColor')
        silver_cg.interface.new_socket(name="Crayola Silver", in_out='OUTPUT', socket_type='NodeSocketColor')
        silver_cg.interface.new_socket(name="Silver Pink", in_out='OUTPUT', socket_type='NodeSocketColor')
        silver_cg.interface.new_socket(name="Basic Silver", in_out='OUTPUT', socket_type='NodeSocketColor')
        silver_cg.interface.new_socket(name="Silver Sand", in_out='OUTPUT', socket_type='NodeSocketColor')
        silver_cg.interface.new_socket(name="Silver Chalice", in_out='OUTPUT', socket_type='NodeSocketColor')
        silver_cg.interface.new_socket(name="Old Silver", in_out='OUTPUT', socket_type='NodeSocketColor')
        silver_cg.interface.new_socket(name="Roman Silver", in_out='OUTPUT', socket_type='NodeSocketColor')
        silver_cg.interface.new_socket(name="Sonic Silver", in_out='OUTPUT', socket_type='NodeSocketColor')

        # makecolors
        sc_s = self.make_color(silver_cg, "Silver", -400, 400, 0xAAA9AD)
        sc_ps = self.make_color(silver_cg, "Pale Silver", -600, 400, 0xFCFAF5)
        sc_pbms = self.make_color(silver_cg, "PBM Silver", -800, 400, 0XFBF9F6)
        sc_cs = self.make_color(silver_cg, "Crayola Silver", -1000, 400, 0xC9C0BB)
        sc_sp = self.make_color(silver_cg, "Silver Pink", -1200, 200, 0xC4AEAD)
        sc_bs = self.make_color(silver_cg, "Basic Silver", -1000, 0, 0xC0C0C0)
        sc_ss = self.make_color(silver_cg, "Silver Sand", -1200, -200, 0xBFC1C2)
        sc_sc = self.make_color(silver_cg, "Silver Chalice", -1000, -400, 0xACACAC)
        sc_os = self.make_color(silver_cg, "Old Silver", -800, -400, 0x848482)
        sc_rs = self.make_color(silver_cg, "Roman Silver", -600, -400, 0x838996)
        sc_sos = self.make_color(silver_cg, "Sonic Silver", -400, -400, 0x757575)

        links = silver_cg.links.new

        links(sc_s.outputs['Color'], group_out.inputs['Silver'])
        links(sc_ps.outputs['Color'], group_out.inputs['Pale Silver'])
        links(sc_pbms.outputs['Color'], group_out.inputs['PBM Silver'])
        links(sc_cs.outputs['Color'], group_out.inputs['Crayola Silver'])
        links(sc_sp.outputs['Color'], group_out.inputs['Silver Pink'])
        links(sc_bs.outputs['Color'], group_out.inputs['Basic Silver'])
        links(sc_ss.outputs['Color'], group_out.inputs['Silver Sand'])
        links(sc_sc.outputs['Color'], group_out.inputs['Silver Chalice'])
        links(sc_os.outputs['Color'], group_out.inputs['Old Silver'])
        links(sc_rs.outputs['Color'], group_out.inputs['Roman Silver'])
        links(sc_sos.outputs['Color'], group_out.inputs['Sonic Silver'])
