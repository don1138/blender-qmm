import bpy

# https://en.wikipedia.org/wiki/Copper_(color)

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


class CopperColorsGroup(bpy.types.Operator):
    """Add/Get Copper Colors Group Node"""
    bl_label = "Copper Colors Node Group"
    bl_idname = 'node.copper_colors_group_operator'
    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        ng_ccg = bpy.data.node_groups.get("Copper Colors")

        if not ng_ccg:
            #newnodegroup
            copper_colors_group = bpy.data.node_groups.new('Copper Colors', 'ShaderNodeTree')

            #groupinput
            # group_in = copper_colors_group.nodes.new('NodeGroupInput')
            # group_in.location = (-400, 0)

            #groupoutput
            group_out = copper_colors_group.nodes.new('NodeGroupOutput')
            group_out.location = (0, 0)
            copper_colors_group.outputs.new('NodeSocketColor', 'Copper')
            copper_colors_group.outputs.new('NodeSocketColor', 'PBM Copper')
            copper_colors_group.outputs.new('NodeSocketColor', 'Dontnod Copper')
            copper_colors_group.outputs.new('NodeSocketColor', 'Pale Copper')
            copper_colors_group.outputs.new('NodeSocketColor', 'Copper Red')
            copper_colors_group.outputs.new('NodeSocketColor', 'Copper Penny')
            copper_colors_group.outputs.new('NodeSocketColor', 'Copper Rose')

            #Copper
            cc_c = copper_colors_group.nodes.new('ShaderNodeRGB')
            cc_c.label = "Copper"
            cc_c.location = (-800, 600)
            cc_c.outputs[0].default_value = hex_to_rgb(0xB87333)

            #PBM Copper
            cc_pbmc = copper_colors_group.nodes.new('ShaderNodeRGB')
            cc_pbmc.label = "PBM Copper"
            cc_pbmc.location = (-800, 400)
            cc_pbmc.outputs[0].default_value = hex_to_rgb(0xF7DDBC)

            #Dontnod Copper
            cc_dc = copper_colors_group.nodes.new('ShaderNodeRGB')
            cc_dc.label = "Dontnod Copper"
            cc_dc.location = (-800, 200)
            cc_dc.outputs[0].default_value = hex_to_rgb(0xFAD0C0)

            #Pale Copper
            cc_pc = copper_colors_group.nodes.new('ShaderNodeRGB')
            cc_pc.label = "Pale Copper"
            cc_pc.location = (-800, 0)
            cc_pc.outputs[0].default_value = hex_to_rgb(0xDA8A67)

            #Copper Red
            cc_cr = copper_colors_group.nodes.new('ShaderNodeRGB')
            cc_cr.label = "Copper Red"
            cc_cr.location = (-800, -200)
            cc_cr.outputs[0].default_value = hex_to_rgb(0xCB6D51)

            #Copper Penny
            cc_cp = copper_colors_group.nodes.new('ShaderNodeRGB')
            cc_cp.label = "Copper Penny"
            cc_cp.location = (-800, -400)
            cc_cp.outputs[0].default_value = hex_to_rgb(0xAD6F69)

            #Copper Rose
            cc_cro = copper_colors_group.nodes.new('ShaderNodeRGB')
            cc_cro.label = "Copper Rose"
            cc_cro.location = (-800, -600)
            cc_cro.outputs[0].default_value = hex_to_rgb(0x996666)

            links = copper_colors_group.links.new

            links(cc_c.outputs[0], group_out.inputs[0])
            links(cc_pbmc.outputs[0], group_out.inputs[1])
            links(cc_dc.outputs[0], group_out.inputs[2])
            links(cc_pc.outputs[0], group_out.inputs[3])
            links(cc_cr.outputs[0], group_out.inputs[4])
            links(cc_cp.outputs[0], group_out.inputs[5])
            links(cc_cro.outputs[0], group_out.inputs[6])

        return {'FINISHED'}
