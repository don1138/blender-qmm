import bpy

bv = bpy.app.version

class UnevenRoughnessGroup(bpy.types.Operator):
    """Add/Get Uneven Roughness Group Node"""
    bl_label  = "Uneven Roughness Node Group"
    bl_idname = 'node.uneven_roughness_group_operator'

    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        ng_uneven_roughness = bpy.data.node_groups.get("Uneven Roughness")

        if not ng_uneven_roughness:
            self.make_group()
        return {'FINISHED'}

    def make_node(self, group, arg1, arg2, arg3):
        result = group.nodes.new(arg1)
        result.location = arg2, arg3
        return result

    def make_group(self):
        # newnodegroup
        uneven_roughness_group = bpy.data.node_groups.new('Uneven Roughness', 'ShaderNodeTree')

        # groupinput 1
        group_in_1 = self.make_node(uneven_roughness_group, 'NodeGroupInput', -400, -100)
        if bv < (4, 0, 0):
            uneven_roughness_group.inputs.new('NodeSocketFloat', 'Seed')  # 0
            uneven_roughness_group.inputs.new('NodeSocketFloat', 'Scale') # 1
            uneven_roughness_group.inputs.new('NodeSocketFloat', 'Min')   # 2
            uneven_roughness_group.inputs.new('NodeSocketFloat', 'Max')   # 3
            uneven_roughness_group.inputs[0].default_value = 1618
            uneven_roughness_group.inputs[0].min_value = -1618
            uneven_roughness_group.inputs[0].max_value = 1618
            uneven_roughness_group.inputs[1].default_value = 6
            uneven_roughness_group.inputs[1].min_value = 0.5
            uneven_roughness_group.inputs[1].max_value = 128
            uneven_roughness_group.inputs[2].default_value = 0
            uneven_roughness_group.inputs[2].min_value = 0.0
            uneven_roughness_group.inputs[2].max_value = 1.0
            uneven_roughness_group.inputs[3].default_value = 0.5
            uneven_roughness_group.inputs[3].min_value = 0.0
            uneven_roughness_group.inputs[3].max_value = 1.0
        else:
            uneven_roughness_group.interface.new_socket(name="Seed", in_out='INPUT', socket_type='NodeSocketFloat')
            uneven_roughness_group.interface.new_socket(name="Scale", in_out='INPUT', socket_type='NodeSocketFloat')
            uneven_roughness_group.interface.new_socket(name="Min", in_out='INPUT', socket_type='NodeSocketFloat')
            uneven_roughness_group.interface.new_socket(name="Max", in_out='INPUT', socket_type='NodeSocketFloat')
            uneven_roughness_group.interface.items_tree[0].default_value = 1618
            uneven_roughness_group.interface.items_tree[0].min_value = -1618
            uneven_roughness_group.interface.items_tree[0].max_value = 1618
            uneven_roughness_group.interface.items_tree[1].default_value = 6
            uneven_roughness_group.interface.items_tree[1].min_value = 0.5
            uneven_roughness_group.interface.items_tree[1].max_value = 128
            uneven_roughness_group.interface.items_tree[2].default_value = 0
            uneven_roughness_group.interface.items_tree[2].min_value = 0.0
            uneven_roughness_group.interface.items_tree[2].max_value = 1.0
            uneven_roughness_group.interface.items_tree[3].default_value = 0.5
            uneven_roughness_group.interface.items_tree[3].min_value = 0.0
            uneven_roughness_group.interface.items_tree[3].max_value = 1.0

        # groupoutput
        group_out = self.make_node(uneven_roughness_group, 'NodeGroupOutput', 0, 0)
        if bv < (4, 0, 0):
            uneven_roughness_group.outputs.new('NodeSocketFloat', 'Result') # 0
            uneven_roughness_group.outputs.new('NodeSocketFloat', 'Mask')   # 1
        else:
            uneven_roughness_group.interface.new_socket(name="Result", in_out='OUTPUT', socket_type='NodeSocketFloat')
            uneven_roughness_group.interface.new_socket(name="Mask", in_out='OUTPUT', socket_type='NodeSocketFloat')

        # Map Range 1
        n_map_1 = self.make_node(uneven_roughness_group, 'ShaderNodeMapRange', -200, 0)
        n_map_1.label = "Map Range 1"
        n_map_1.inputs[1].default_value = 0.49
        n_map_1.inputs[2].default_value = 0.51
        n_map_1.inputs[3].default_value = 0
        n_map_1.inputs[4].default_value = 0.5

        # Map Range 2
        n_map_2 = self.make_node(uneven_roughness_group, 'ShaderNodeMapRange', -200, -300)
        n_map_2.label = "Map Range 2"
        n_map_2.inputs[1].default_value = 0.49
        n_map_2.inputs[2].default_value = 0.51
        n_map_2.inputs[3].default_value = 0
        n_map_2.inputs[4].default_value = 1

        # Noise Texture
        n_noise = self.make_node(uneven_roughness_group, 'ShaderNodeTexNoise', -600, 0)
        n_noise.noise_dimensions = '4D'
        n_noise.inputs[3].default_value = 8
        n_noise.inputs[4].default_value = 1

        # Texture Coordinates
        n_tex = self.make_node(uneven_roughness_group, 'ShaderNodeTexCoord', -800, 0)

        # groupinput 2
        group_in_2 = self.make_node(uneven_roughness_group, 'NodeGroupInput', -1000, -100)

        # LINKS
        links = uneven_roughness_group.links.new

        links(n_tex.outputs[4], n_noise.inputs[0])
        links(group_in_2.outputs[0], n_noise.inputs[1])
        links(group_in_2.outputs[1], n_noise.inputs[2])
        links(n_noise.outputs[0], n_map_1.inputs[0])
        links(n_noise.outputs[0], n_map_2.inputs[0])
        links(n_noise.outputs[0], n_map_2.inputs[0])
        links(group_in_1.outputs[2], n_map_1.inputs[3])
        links(group_in_1.outputs[3], n_map_1.inputs[4])
        links(n_map_1.outputs[0], group_out.inputs[0])
        links(n_map_2.outputs[0], group_out.inputs[1])
