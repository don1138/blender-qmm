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
    bl_label  = "Copper Colors Node Group"
    bl_idname = 'node.copper_cg_operator'

    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        ng_ccg = bpy.data.node_groups.get("Copper Colors")

        if not ng_ccg:
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
        copper_cg = bpy.data.node_groups.new('Copper Colors', 'ShaderNodeTree')

        # groupoutput
        group_out = copper_cg.nodes.new('NodeGroupOutput')
        group_out.location = (0, 0)
        copper_cg.interface.new_socket(name="Copper", in_out='OUTPUT', socket_type='NodeSocketColor')
        copper_cg.interface.new_socket(name="PBM Copper", in_out='OUTPUT', socket_type='NodeSocketColor')
        copper_cg.interface.new_socket(name="Dontnod Copper", in_out='OUTPUT', socket_type='NodeSocketColor')
        copper_cg.interface.new_socket(name="Pale Copper", in_out='OUTPUT', socket_type='NodeSocketColor')
        copper_cg.interface.new_socket(name="Copper Red", in_out='OUTPUT', socket_type='NodeSocketColor')
        copper_cg.interface.new_socket(name="Copper Penny", in_out='OUTPUT', socket_type='NodeSocketColor')
        copper_cg.interface.new_socket(name="Copper Rose", in_out='OUTPUT', socket_type='NodeSocketColor')

        # makecolors
        cc_c = self.make_color(copper_cg, "Copper", -400, 300, 0xB87333)
        cc_pbmc = self.make_color(copper_cg, "PBM Copper", -600, 300, 0XF7DDBC)
        cc_dc = self.make_color(copper_cg, "Dontnod Copper", -800, 300, 0xFAD0C0)
        cc_pc = self.make_color(copper_cg, "Pale Copper", -800, 0, 0xDA8A67)
        cc_cr = self.make_color(copper_cg, "Copper Red", -800, -300, 0xCB6D51)
        cc_cp = self.make_color(copper_cg, "Copper Penny", -600, -300, 0xAD6F69)
        cc_cro = self.make_color(copper_cg, "Copper Rose", -400, -300, 0x996666)

        links = copper_cg.links.new

        links(cc_c.outputs['Color'], group_out.inputs['Copper'])
        links(cc_pbmc.outputs['Color'], group_out.inputs['PBM Copper'])
        links(cc_dc.outputs['Color'], group_out.inputs['Dontnod Copper'])
        links(cc_pc.outputs['Color'], group_out.inputs['Pale Copper'])
        links(cc_cr.outputs['Color'], group_out.inputs['Copper Red'])
        links(cc_cp.outputs['Color'], group_out.inputs['Copper Penny'])
        links(cc_cro.outputs['Color'], group_out.inputs['Copper Rose'])
