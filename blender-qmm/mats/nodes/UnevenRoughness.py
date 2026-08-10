import bpy

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
        min_socket = uneven_roughness_group.interface.new_socket(name="Min", in_out='INPUT', socket_type='NodeSocketFloat')
        min_socket.default_value = 0
        min_socket.min_value = 0.0
        min_socket.max_value = 1.0

        max_socket = uneven_roughness_group.interface.new_socket(name="Max", in_out='INPUT', socket_type='NodeSocketFloat')
        max_socket.default_value = 0.5
        max_socket.min_value = 0.0
        max_socket.max_value = 1.0

        scale_socket = uneven_roughness_group.interface.new_socket(name="Scale", in_out='INPUT', socket_type='NodeSocketFloat')
        scale_socket.default_value = 6
        scale_socket.min_value = 0.5
        scale_socket.max_value = 128

        contrast_socket = uneven_roughness_group.interface.new_socket(name="Contrast", in_out='INPUT', socket_type='NodeSocketFloat')
        contrast_socket.default_value = 0.5
        contrast_socket.min_value = 0.0
        contrast_socket.max_value = 1.0

        midpoint_socket = uneven_roughness_group.interface.new_socket(name="Midpoint", in_out='INPUT', socket_type='NodeSocketFloat')
        midpoint_socket.default_value = 0.5
        midpoint_socket.min_value = 0.0
        midpoint_socket.max_value = 1.0

        seed_socket = uneven_roughness_group.interface.new_socket(name="Seed", in_out='INPUT', socket_type='NodeSocketFloat')
        seed_socket.default_value = 1618
        seed_socket.min_value = -1618
        seed_socket.max_value = 1618

        # groupoutput
        group_out = self.make_node(uneven_roughness_group, 'NodeGroupOutput', 0, 0)
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
        n_noise.inputs['Detail'].default_value = 8
        n_noise.inputs['Roughness'].default_value = 1

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

        links(n_tex.outputs['Object'], n_noise.inputs['Vector'])
        links(group_in_2.outputs['Seed'], n_noise.inputs['W'])
        links(group_in_2.outputs['Scale'], n_noise.inputs['Scale'])
        links(n_noise.outputs['Fac'], n_map_1.inputs['Value'])
        links(n_noise.outputs['Fac'], n_map_2.inputs['Value'])
        links(group_in_1.outputs['Min'], n_map_1.inputs[3])
        links(group_in_1.outputs['Max'], n_map_1.inputs[4])
        links(n_map_1.outputs['Result'], group_out.inputs['Roughness'])
        links(n_map_2.outputs['Result'], group_out.inputs['Mask'])

        links(n_math_min.outputs['Value'], n_map_1.inputs[1])
        links(n_math_min.outputs['Value'], n_map_2.inputs[1])
        links(n_math_max_bump.outputs['Value'], n_map_1.inputs[2])
        links(n_math_max_bump.outputs['Value'], n_map_2.inputs[2])
        links(n_math_max.outputs['Value'], n_math_max_bump.inputs[0])
        links(n_math_tenth.outputs['Value'], n_math_min.inputs[1])
        links(n_math_tenth.outputs['Value'], n_math_max.inputs[1])
        links(n_map_3.outputs['Result'], n_math_tenth.inputs[0])
        links(n_map_4.outputs['Result'], n_math_min.inputs[0])
        links(n_map_4.outputs['Result'], n_math_max.inputs[0])
        links(group_in_3.outputs['Contrast'], n_map_3.inputs['Value'])
        links(group_in_3.outputs['Midpoint'], n_map_4.inputs['Value'])
