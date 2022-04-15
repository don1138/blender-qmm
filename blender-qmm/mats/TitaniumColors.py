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
            #newnodegroup
            titanium_colors_group = bpy.data.node_groups.new('Titanium Colors', 'ShaderNodeTree')

            #groupinput
            group_in = titanium_colors_group.nodes.new('NodeGroupInput')
            group_in.location = (-400, 0)

            #groupoutput
            group_out = titanium_colors_group.nodes.new('NodeGroupOutput')
            group_out.location = (0, 0)
            titanium_colors_group.outputs.new('NodeSocketColor', 'Titanium')
            titanium_colors_group.outputs.new('NodeSocketColor', 'Pale Titanium')
            titanium_colors_group.outputs.new('NodeSocketColor', 'Dark Titanium')
            titanium_colors_group.outputs.new('NodeSocketColor', 'Metallic Titanium')
            titanium_colors_group.outputs.new('NodeSocketColor', 'Titanium White')
            titanium_colors_group.outputs.new('NodeSocketColor', 'Titanium Frost')
            titanium_colors_group.outputs.new('NodeSocketColor', 'Titanium Blue')

            #Titanium
            tc_t = titanium_colors_group.nodes.new('ShaderNodeRGB')
            tc_t.label = "Titanium"
            tc_t.location = (-200, 600)
            tc_t.outputs[0].default_value = hex_to_rgb(0xC1BAB1)

            #Pale Titanium
            tc_pt = titanium_colors_group.nodes.new('ShaderNodeRGB')
            tc_pt.label = "Pale Titanium"
            tc_pt.location = (-200, 400)
            tc_pt.outputs[0].default_value = hex_to_rgb(0xCEC8C2)

            #Dark Titanium
            tc_dt = titanium_colors_group.nodes.new('ShaderNodeRGB')
            tc_dt.label = "Dark Titanium"
            tc_dt.location = (-200, 200)
            tc_dt.outputs[0].default_value = hex_to_rgb(0x878681)

            #Metallic Titanium
            tc_mt = titanium_colors_group.nodes.new('ShaderNodeRGB')
            tc_mt.label = "Metallic Titanium"
            tc_mt.location = (-200, 0)
            tc_mt.outputs[0].default_value = hex_to_rgb(0x7A7772)

            #Titanium White
            tc_tw = titanium_colors_group.nodes.new('ShaderNodeRGB')
            tc_tw.label = "Titanium White"
            tc_tw.location = (-200, -200)
            tc_tw.outputs[0].default_value = hex_to_rgb(0xF3F4F7)

            #Titanium Frost
            tc_tf = titanium_colors_group.nodes.new('ShaderNodeRGB')
            tc_tf.label = "Titanium Frost"
            tc_tf.location = (-200, -400)
            tc_tf.outputs[0].default_value = hex_to_rgb(0xB0AFA9)

            #Titanium Blue
            tc_tb = titanium_colors_group.nodes.new('ShaderNodeRGB')
            tc_tb.label = "Titanium Blue"
            tc_tb.location = (-200, -600)
            tc_tb.outputs[0].default_value = hex_to_rgb(0x5B798E)

            links = titanium_colors_group.links.new

            links(tc_t.outputs[0], group_out.inputs[0])
            links(tc_pt.outputs[0], group_out.inputs[1])
            links(tc_dt.outputs[0], group_out.inputs[2])
            links(tc_mt.outputs[0], group_out.inputs[3])
            links(tc_tw.outputs[0], group_out.inputs[4])
            links(tc_tf.outputs[0], group_out.inputs[5])
            links(tc_tb.outputs[0], group_out.inputs[6])

        return {'FINISHED'}

