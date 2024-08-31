import bpy

bv = bpy.app.version


class PearlescentPigmentGroup(bpy.types.Operator):
    """Add/Get Pearlescent Pigment Group Node"""
    bl_label = "Pearlescent Pigment Node Group"
    bl_idname = 'node.pearlescent_pigment_group_operator'

    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        ng_pearlescent_pigment = bpy.data.node_groups.get("Pearlescent Pigment")

        if not ng_pearlescent_pigment:
            self.make_group()
        return {'FINISHED'}

    def make_node(self, group, arg1, arg2, arg3):
        result = group.nodes.new(arg1)
        result.location = arg2, arg3
        return result

    def make_group(self):
        # newnodegroup
        pearlescent_pigment_group = bpy.data.node_groups.new('Pearlescent Pigment', 'ShaderNodeTree')

        # groupinput 1
        group_in = self.make_node(pearlescent_pigment_group, 'NodeGroupInput', -400, -200)
        if bv < (4, 0, 0):
            pearlescent_pigment_group.inputs.new('NodeSocketColor', 'Primary Color')    # 0
            pearlescent_pigment_group.inputs.new('NodeSocketColor', 'Secondary Color')  # 1
            pearlescent_pigment_group.inputs.new('NodeSocketFloat', 'Blend Factor')            # 2
            pearlescent_pigment_group.inputs[0].default_value = [0.102242, 0.104616, 0.346704, 1]
            pearlescent_pigment_group.inputs[2].default_value = [0.520996, 0.009721, 0.031896, 1.000000]
            pearlescent_pigment_group.inputs[2].min_value = 0.0
            pearlescent_pigment_group.inputs[2].max_value = 1.0
        else:
            pearlescent_pigment_group.interface.new_socket(name="Primary Color", in_out='INPUT', socket_type='NodeSocketColor')
            pearlescent_pigment_group.interface.new_socket(name="Secondary Color", in_out='INPUT', socket_type='NodeSocketColor')
            pearlescent_pigment_group.interface.new_socket(name="Blend Factor", in_out='INPUT', socket_type='NodeSocketFloat')
            pearlescent_pigment_group.interface.items_tree[0].default_value = [0.102242, 0.104616, 0.346704, 1]
            pearlescent_pigment_group.interface.items_tree[1].default_value = [0.520996, 0.009721, 0.031896, 1.000000]
            pearlescent_pigment_group.interface.items_tree[2].default_value = 0.22
            pearlescent_pigment_group.interface.items_tree[2].min_value = 0.0
            pearlescent_pigment_group.interface.items_tree[2].max_value = 1.0

        # groupinput 2
        group_in_2 = self.make_node(pearlescent_pigment_group, 'NodeGroupInput', -600, 0)

        # groupoutput
        group_out = self.make_node(pearlescent_pigment_group, 'NodeGroupOutput', 0, 0)
        if bv < (4, 0, 0):
            pearlescent_pigment_group.outputs.new('NodeSocketColor', 'Result')

        else:
            pearlescent_pigment_group.interface.new_socket(name="Result", in_out='OUTPUT', socket_type='NodeSocketColor')

        # Mix Node
        n_mix = self.make_node(pearlescent_pigment_group, 'ShaderNodeMix', -200, 0)
        n_mix.data_type = 'RGBA'

        # Layer Weight
        n_layer_weight = self.make_node(pearlescent_pigment_group, 'ShaderNodeLayerWeight', -400, 0)

        # LINKS
        links = pearlescent_pigment_group.links.new

        links(n_mix.outputs[2], group_out.inputs[0])
        links(n_layer_weight.outputs[1], n_mix.inputs[0])
        links(group_in_2.outputs[2], n_layer_weight.inputs[0])
        links(group_in.outputs[0], n_mix.inputs[6])
        links(group_in.outputs[1], n_mix.inputs[7])
