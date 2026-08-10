import bpy


class MetalFlakeGroup(bpy.types.Operator):
    """Add/Get Metal Flake Group Node"""
    bl_label = "Metal Flake Node Group"
    bl_idname = 'node.metal_flake_group_operator'

    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        ng_metal_flake = bpy.data.node_groups.get("Metal Flake")

        if not ng_metal_flake:
            self.make_group()
        return {'FINISHED'}

    def make_node(self, group, arg1, arg2, arg3):
        result = group.nodes.new(arg1)
        result.location = arg2, arg3
        return result

    def make_group(self):
        # newnodegroup
        metal_flake_group = bpy.data.node_groups.new('Metal Flake', 'ShaderNodeTree')

        # groupinput 1
        scale_socket = metal_flake_group.interface.new_socket(name="Scale", in_out='INPUT', socket_type='NodeSocketFloat')
        scale_socket.default_value = 4096
        scale_socket.min_value = 0.0
        scale_socket.max_value = 10000.0

        strength_socket = metal_flake_group.interface.new_socket(name="Strength", in_out='INPUT', socket_type='NodeSocketFloat')
        strength_socket.default_value = 0.25
        strength_socket.min_value = 0.0
        strength_socket.max_value = 1.0

        group_in = self.make_node(metal_flake_group, 'NodeGroupInput', -1000, 100)

        # groupoutput
        group_out = self.make_node(metal_flake_group, 'NodeGroupOutput', 0, 0)
        metal_flake_group.interface.new_socket(name="Normal", in_out='OUTPUT', socket_type='NodeSocketVector')
        metal_flake_group.interface.new_socket(name="Blue Mask", in_out='OUTPUT', socket_type='NodeSocketColor')

        # Normal Map
        n_map = self.make_node(metal_flake_group, 'ShaderNodeNormalMap', -200, 0)
        n_map.space = 'OBJECT'

        # Combine Color
        n_combine_color = self.make_node(metal_flake_group, 'ShaderNodeCombineColor', -400, 0)

        # Separate Color
        n_separate_color = self.make_node(metal_flake_group, 'ShaderNodeSeparateColor', -600, 0)

        # Voronoi Texture
        n_voronoi = self.make_node(metal_flake_group, 'ShaderNodeTexVoronoi', -800, 0)

        # Texture Coordinates
        n_tex = self.make_node(metal_flake_group, 'ShaderNodeTexCoord', -1000, -100)

        # LINKS
        links = metal_flake_group.links.new

        links(n_map.outputs['Normal'], group_out.inputs['Normal'])
        links(n_combine_color.outputs['Color'], n_map.inputs['Color'])
        links(n_separate_color.outputs['Red'], n_combine_color.inputs['Red'])
        links(n_separate_color.outputs['Green'], n_combine_color.inputs['Green'])
        links(n_separate_color.outputs['Blue'], group_out.inputs['Blue Mask'])
        links(n_voronoi.outputs['Color'], n_separate_color.inputs['Color'])
        links(n_tex.outputs['Object'], n_voronoi.inputs['Vector'])
        links(group_in.outputs['Scale'], n_voronoi.inputs['Scale'])
        links(group_in.outputs['Strength'], n_map.inputs['Strength'])
