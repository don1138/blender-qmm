import bpy

class AnisotrophyXGroup(bpy.types.Operator):
    """Add/Get Anisotrophy X Group Node"""
    bl_label  = "Anisotrophy X Node Group"
    bl_idname = 'node.anisotrophy_x_group_operator'

    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        anix_group = bpy.data.node_groups.get("Anisotrophy X")

        if not anix_group:
            self.make_anix_group()

        return {'FINISHED'}

    def make_anix_group(self):
        # anix_group
        anix_group = bpy.data.node_groups.new('Anisotrophy X', 'ShaderNodeTree')

        # groupinput 1
        group_in = self.make_node(anix_group, 'NodeGroupInput', -400, -200)
        group_in.label = "Group In 1"
        if bpy.app.version < (4, 0, 0):
            anix_group.inputs.new('NodeSocketFloat', 'Bands')             #0
            anix_group.inputs.new('NodeSocketFloat', 'Grain')             #1
            anix_group.inputs.new('NodeSocketFloat', 'Min Roughness')     #2
            anix_group.inputs[0].default_value = 200
            anix_group.inputs[1].default_value = 100
            anix_group.inputs[2].default_value = 0.2
        else:
            anix_group.interface.new_socket(name="Bands", in_out='INPUT', socket_type='NodeSocketFloat')
            anix_group.interface.new_socket(name="Grain", in_out='INPUT', socket_type='NodeSocketFloat')
            anix_group.interface.new_socket(name="Min Roughness", in_out='INPUT', socket_type='NodeSocketFloat')
            anix_group.interface.items_tree[0].default_value = 200
            anix_group.interface.items_tree[1].default_value = 100
            anix_group.interface.items_tree[2].default_value = 0.2

        # groupoutput
        group_out = self.make_node(anix_group, 'NodeGroupOutput', 0, 0)
        if bpy.app.version < (4, 0, 0):
            anix_group.outputs.new('NodeSocketFloat', 'To Roughness')     #0
            anix_group.outputs.new('NodeSocketFloat', 'To Bump')          #1
        else:
            anix_group.interface.new_socket(name="To Roughness", in_out='OUTPUT', socket_type='NodeSocketFloat')
            anix_group.interface.new_socket(name="To Bump", in_out='OUTPUT', socket_type='NodeSocketFloat')

        # map range
        m_map_range = self.make_node(anix_group, 'ShaderNodeMapRange', -200, 0)
        m_map_range.inputs[3].default_value = 0.3
        m_map_range.inputs[4].default_value = 0.2

        # reroute
        n_rr = self.make_node(anix_group, 'NodeReroute', -300, -100)

        # bool1
        m_greater = self.make_math_node(anix_group, 'GREATER_THAN', -500, 0)
        m_greater.inputs[1].default_value = 0.05
        m_greater.use_clamp = True

        # subtract
        m_subtract = self.make_math_node(anix_group, 'SUBTRACT', -700, 0)
        m_subtract.inputs[1].default_value = 5

        # noise1
        m_noise = self.make_node(anix_group, 'ShaderNodeTexNoise', -900, 0)
        m_noise.noise_dimensions = '1D'
        m_noise.inputs[1].default_value = 200
        m_noise.inputs[5].default_value = 2.0

        # noise2
        m_noise2 = self.make_node(anix_group, 'ShaderNodeTexNoise', -900, -300)
        m_noise2.noise_dimensions = '3D'
        m_noise2.inputs[1].default_value = 100

        # mapping
        m_map = self.make_node(anix_group, 'ShaderNodeMapping', -1100, 200)

        # groupinput 2
        group_in2 = self.make_node(anix_group, 'NodeGroupInput', -1100, -200)
        group_in2.label = "Group In 2"

        # separate xyz
        m_sep = self.make_node(anix_group, 'ShaderNodeSeparateXYZ', -1300, 200)

        # texture coordinate
        m_tex = self.make_node(anix_group, 'ShaderNodeTexCoord', -1500, 200)

        links = anix_group.links.new

        links(m_tex.outputs[2], m_sep.inputs[0])
        links(m_sep.outputs[0], m_map.inputs[0])
        links(m_map.outputs[0], m_noise.inputs[1])
        links(group_in2.outputs[0], m_noise.inputs[2])
        links(group_in2.outputs[1], m_noise2.inputs[2])
        links(m_noise.outputs[1], m_subtract.inputs[0])
        links(m_noise2.outputs[0], m_subtract.inputs[1])
        links(m_subtract.outputs[0], m_greater.inputs[0])
        links(m_greater.outputs[0], n_rr.inputs[0])
        links(n_rr.outputs[0], group_out.inputs[1])
        links(n_rr.outputs[0], m_map_range.inputs[0])
        links(group_in.outputs[2], m_map_range.inputs[4])
        links(m_map_range.outputs[0], group_out.inputs[0])

    def make_node(self, group, arg1, arg2, arg3):
        result = group.nodes.new(arg1)
        result.location = arg2, arg3
        return result

    def make_math_node(self, group, arg1, arg2, arg3):
        result = self.make_node(group, 'ShaderNodeMath', arg2, arg3)
        result.operation = arg1
        return result

