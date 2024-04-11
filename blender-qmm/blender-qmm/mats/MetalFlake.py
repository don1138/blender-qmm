import bpy

bv = bpy.app.version

class MetalFlakeGroup(bpy.types.Operator):
    """Add/Get Metal Flake Group Node"""
    bl_label  = "Metal Flake Node Group"
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
        group_in = self.make_node(metal_flake_group, 'NodeGroupInput', -1200, 0)
        if bv < (4, 0, 0):
            metal_flake_group.inputs.new('NodeSocketFloat', 'Scale') # 0
            metal_flake_group.inputs.new('NodeSocketFloat', 'Strength')  # 1
            metal_flake_group.inputs[0].default_value = 4096
            metal_flake_group.inputs[0].min_value = 0.0
            metal_flake_group.inputs[0].max_value = 10000.0
            metal_flake_group.inputs[1].default_value = 0.25
            metal_flake_group.inputs[1].min_value = 0.0
            metal_flake_group.inputs[1].max_value = 1.0
        else:
            metal_flake_group.interface.new_socket(name="Scale", in_out='INPUT', socket_type='NodeSocketFloat')
            metal_flake_group.interface.new_socket(name="Strength", in_out='INPUT', socket_type='NodeSocketFloat')
            metal_flake_group.interface.items_tree[0].default_value = 4096
            metal_flake_group.interface.items_tree[0].min_value = 0.0
            metal_flake_group.interface.items_tree[0].max_value = 10000.0
            metal_flake_group.interface.items_tree[1].default_value = 0.25
            metal_flake_group.interface.items_tree[1].min_value = 0.0
            metal_flake_group.interface.items_tree[1].max_value = 1.0

        # groupoutput
        group_out = self.make_node(metal_flake_group, 'NodeGroupOutput', 0, 0)
        if bv < (4, 0, 0):
            metal_flake_group.outputs.new('NodeSocketVector', 'Normal') # 0
            metal_flake_group.outputs.new('NodeSocketColor', 'Blue Mask') # 1

        else:
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

        links(n_map.outputs[0], group_out.inputs[0])
        links(n_combine_color.outputs[0], n_map.inputs[1])
        links(n_separate_color.outputs[0], n_combine_color.inputs[0])
        links(n_separate_color.outputs[1], n_combine_color.inputs[1])
        links(n_separate_color.outputs[2], group_out.inputs[1])
        links(n_voronoi.outputs[1], n_separate_color.inputs[0])
        links(n_tex.outputs[3], n_voronoi.inputs[0])
        links(group_in.outputs[0], n_voronoi.inputs[2])
        links(group_in.outputs[1], n_map.inputs[0])
