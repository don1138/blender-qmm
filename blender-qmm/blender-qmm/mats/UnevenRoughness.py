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
        group_in_1 = self.make_node(uneven_roughness_group, 'NodeGroupInput', -400, -200)
        group_in_1.label = "Group Input 1"
        if bv < (4, 0, 0):
            uneven_roughness_group.inputs.new('NodeSocketFloat', 'Min')   # 2
            uneven_roughness_group.inputs.new('NodeSocketFloat', 'Max')   # 3
            uneven_roughness_group.inputs.new('NodeSocketFloat', 'Scale') # 1
            uneven_roughness_group.inputs.new('NodeSocketFloat', 'Contrast')   # 3
            uneven_roughness_group.inputs.new('NodeSocketFloat', 'Midpoint')   # 3
            uneven_roughness_group.inputs.new('NodeSocketFloat', 'Seed')  # 0
            uneven_roughness_group.inputs[0].default_value = 0
            uneven_roughness_group.inputs[0].min_value = 0.0
            uneven_roughness_group.inputs[0].max_value = 1.0
            uneven_roughness_group.inputs[1].default_value = 0.5
            uneven_roughness_group.inputs[1].min_value = 0.0
            uneven_roughness_group.inputs[1].max_value = 1.0
            uneven_roughness_group.inputs[2].default_value = 6
            uneven_roughness_group.inputs[2].min_value = 0.5
            uneven_roughness_group.inputs[2].max_value = 128
            uneven_roughness_group.inputs[3].default_value = 0.5
            uneven_roughness_group.inputs[3].min_value = 0.0
            uneven_roughness_group.inputs[3].max_value = 1.0
            uneven_roughness_group.inputs[4].default_value = 0.5
            uneven_roughness_group.inputs[4].min_value = 0.0
            uneven_roughness_group.inputs[4].max_value = 1.0
            uneven_roughness_group.inputs[5].default_value = 1618
            uneven_roughness_group.inputs[5].min_value = -1618
            uneven_roughness_group.inputs[5].max_value = 1618
        else:
            uneven_roughness_group.interface.new_socket(name="Min", in_out='INPUT', socket_type='NodeSocketFloat')
            uneven_roughness_group.interface.new_socket(name="Max", in_out='INPUT', socket_type='NodeSocketFloat')
            uneven_roughness_group.interface.new_socket(name="Scale", in_out='INPUT', socket_type='NodeSocketFloat')
            uneven_roughness_group.interface.new_socket(name="Contrast", in_out='INPUT', socket_type='NodeSocketFloat')
            uneven_roughness_group.interface.new_socket(name="Midpoint", in_out='INPUT', socket_type='NodeSocketFloat')
            uneven_roughness_group.interface.new_socket(name="Seed", in_out='INPUT', socket_type='NodeSocketFloat')
            uneven_roughness_group.interface.items_tree[0].default_value = 0
            uneven_roughness_group.interface.items_tree[0].min_value = 0.0
            uneven_roughness_group.interface.items_tree[0].max_value = 1.0
            uneven_roughness_group.interface.items_tree[1].default_value = 0.5
            uneven_roughness_group.interface.items_tree[1].min_value = 0.0
            uneven_roughness_group.interface.items_tree[1].max_value = 1.0
            uneven_roughness_group.interface.items_tree[2].default_value = 6
            uneven_roughness_group.interface.items_tree[2].min_value = 0.5
            uneven_roughness_group.interface.items_tree[2].max_value = 128
            uneven_roughness_group.interface.items_tree[3].default_value = 0.5
            uneven_roughness_group.interface.items_tree[3].min_value = 0.0
            uneven_roughness_group.interface.items_tree[3].max_value = 1.0
            uneven_roughness_group.interface.items_tree[4].default_value = 0.5
            uneven_roughness_group.interface.items_tree[4].min_value = 0.0
            uneven_roughness_group.interface.items_tree[4].max_value = 1.0
            uneven_roughness_group.interface.items_tree[5].default_value = 1618
            uneven_roughness_group.interface.items_tree[5].min_value = -1618
            uneven_roughness_group.interface.items_tree[5].max_value = 1618

        # groupoutput
        group_out = self.make_node(uneven_roughness_group, 'NodeGroupOutput', 0, 0)
        if bv < (4, 0, 0):
            uneven_roughness_group.outputs.new('NodeSocketFloat', 'Roughness') # 0
            uneven_roughness_group.outputs.new('NodeSocketFloat', 'Mask')      # 1
        else:
            uneven_roughness_group.interface.new_socket(name="Roughness", in_out='OUTPUT', socket_type='NodeSocketFloat')
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
        group_in_2.label = "Group Input 2"
        
        # Math Min
        n_math_min = self.make_node(uneven_roughness_group, 'ShaderNodeMath', -600, -300)
        n_math_min.label = "Max"
        n_math_min.operation = 'SUBTRACT'
        n_math_min.use_clamp = True

        # Math Max Bump
        n_math_max_bump = self.make_node(uneven_roughness_group, 'ShaderNodeMath', -400, -500)
        n_math_max_bump.label = "Max Bump"
        n_math_max_bump.operation = 'ADD'
        n_math_max_bump.use_clamp = True
        n_math_max_bump.inputs[1].default_value = 0.0001

        # Math Max
        n_math_max = self.make_node(uneven_roughness_group, 'ShaderNodeMath', -600, -500)
        n_math_max.label = "Max"
        n_math_max.operation = 'ADD'
        n_math_max.use_clamp = True

        # Math One-Tenth
        n_math_tenth = self.make_node(uneven_roughness_group, 'ShaderNodeMath', -800, -400)
        n_math_tenth.label = "1/10th"
        n_math_tenth.operation = 'MULTIPLY'
        n_math_tenth.use_clamp = True
        n_math_tenth.inputs[1].default_value = 0.1

        # Map Range 3
        n_map_3 = self.make_node(uneven_roughness_group, 'ShaderNodeMapRange', -1000, -300)
        n_map_3.label = "Map Range 3"
        n_map_3.inputs[3].default_value = 2
        n_map_3.inputs[4].default_value = 0

        # Map Range 4
        n_map_4 = self.make_node(uneven_roughness_group, 'ShaderNodeMapRange', -1000, -600)
        n_map_4.label = "Map Range 3"
        n_map_4.inputs[3].default_value = 0.4
        n_map_4.inputs[4].default_value = 0.6

        # groupinput 3
        group_in_3 = self.make_node(uneven_roughness_group, 'NodeGroupInput', -1200, -300)
        group_in_3.label = "Group Input 3"

        # LINKS
        links = uneven_roughness_group.links.new

        links(n_tex.outputs[3], n_noise.inputs[0])
        links(group_in_2.outputs[5], n_noise.inputs[1])
        links(group_in_2.outputs[2], n_noise.inputs[2])
        links(n_noise.outputs[0], n_map_1.inputs[0])
        links(n_noise.outputs[0], n_map_2.inputs[0])
        links(n_noise.outputs[0], n_map_2.inputs[0])
        links(group_in_1.outputs[0], n_map_1.inputs[3])
        links(group_in_1.outputs[1], n_map_1.inputs[4])
        links(n_map_1.outputs[0], group_out.inputs[0])
        links(n_map_2.outputs[0], group_out.inputs[1])

        links(n_math_min.outputs[0], n_map_1.inputs[1])
        links(n_math_min.outputs[0], n_map_2.inputs[1])
        links(n_math_max_bump.outputs[0], n_map_1.inputs[2])
        links(n_math_max_bump.outputs[0], n_map_2.inputs[2])
        links(n_math_max.outputs[0], n_math_max_bump.inputs[0])
        links(n_math_tenth.outputs[0], n_math_min.inputs[1])
        links(n_math_tenth.outputs[0], n_math_max.inputs[1])
        links(n_map_3.outputs[0], n_math_tenth.inputs[0])
        links(n_map_4.outputs[0], n_math_min.inputs[0])
        links(n_map_4.outputs[0], n_math_max.inputs[0])
        links(group_in_3.outputs[3], n_map_3.inputs[0])
        links(group_in_3.outputs[4], n_map_4.inputs[0])