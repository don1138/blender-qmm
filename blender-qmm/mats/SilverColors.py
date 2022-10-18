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
        ng_ccg = bpy.data.node_groups.get("Silver Colors")

        if not ng_ccg:
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

            #Silver
            sc_s = silver_colors_group.nodes.new('ShaderNodeRGB')
            sc_s.label = "Silver"
            sc_s.location = (-800, 1000)
            sc_s.outputs[0].default_value = hex_to_rgb(0xAAA9AD)

            #Pale Silver
            sc_ps = silver_colors_group.nodes.new('ShaderNodeRGB')
            sc_ps.label = "Pale Silver"
            sc_ps.location = (-800, 800)
            sc_ps.outputs[0].default_value = hex_to_rgb(0xFCFAF5)

            #PBM Silver
            sc_pbms = silver_colors_group.nodes.new('ShaderNodeRGB')
            sc_pbms.label = "PBM Silver"
            sc_pbms.location = (-800, 600)
            sc_pbms.outputs[0].default_value = hex_to_rgb(0xFBF9F6)

            #Crayola Silver
            sc_cs = silver_colors_group.nodes.new('ShaderNodeRGB')
            sc_cs.label = "Crayola Silver"
            sc_cs.location = (-800, 400)
            sc_cs.outputs[0].default_value = hex_to_rgb(0xC9C0BB)

            #Silver Pink
            sc_sp = silver_colors_group.nodes.new('ShaderNodeRGB')
            sc_sp.label = "Silver Pink"
            sc_sp.location = (-800, 200)
            sc_sp.outputs[0].default_value = hex_to_rgb(0xC4AEAD)

            #Basic Silver
            sc_bs = silver_colors_group.nodes.new('ShaderNodeRGB')
            sc_bs.label = "Basic Silver"
            sc_bs.location = (-800, 0)
            sc_bs.outputs[0].default_value = hex_to_rgb(0xC0C0C0)

            #Silver Sand
            sc_ss = silver_colors_group.nodes.new('ShaderNodeRGB')
            sc_ss.label = "Silver Sand"
            sc_ss.location = (-800, -200)
            sc_ss.outputs[0].default_value = hex_to_rgb(0xBFC1C2)

            #Silver Chalice
            sc_sc = silver_colors_group.nodes.new('ShaderNodeRGB')
            sc_sc.label = "Silver Chalice"
            sc_sc.location = (-800, -400)
            sc_sc.outputs[0].default_value = hex_to_rgb(0xACACAC)

            #Old Silver
            sc_os = silver_colors_group.nodes.new('ShaderNodeRGB')
            sc_os.label = "Old Silver"
            sc_os.location = (-800, -600)
            sc_os.outputs[0].default_value = hex_to_rgb(0x848482)

            #Roman Silver
            sc_rs = silver_colors_group.nodes.new('ShaderNodeRGB')
            sc_rs.label = "Roman Silver"
            sc_rs.location = (-800, -800)
            sc_rs.outputs[0].default_value = hex_to_rgb(0x838996)

            #Sonic Silver
            sc_sos = silver_colors_group.nodes.new('ShaderNodeRGB')
            sc_sos.label = "Sonic Silver"
            sc_sos.location = (-800, -1000)
            sc_sos.outputs[0].default_value = hex_to_rgb(0x757575)


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

        return {'FINISHED'}
