import bpy

class SteelRoughnessGroup(bpy.types.Operator):
    """Add/Get Steel Roughness Group Node"""
    bl_label  = "Steel Roughness Node Group"
    bl_idname = 'node.sr_group_operator'

    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        ng_sr = bpy.data.node_groups.get("Steel Roughness")

        if not ng_sr:
            self.make_sr_group()

        return {'FINISHED'}

    def make_sr_group(self):
        # sr_group
        sr_group = bpy.data.node_groups.new('Steel Roughness', 'ShaderNodeTree')

        # groupoutput
        group_out = self.make_node(sr_group, 'NodeGroupOutput', 0, 0)

        # create outputs
        if bpy.app.version < (4, 0, 0):
            sr_group.outputs.new('NodeSocketFloat', 'Carbon Steel')                    #0
            sr_group.outputs.new('NodeSocketFloat', 'Stainless Steel')                 #1
            sr_group.outputs.new('NodeSocketFloat', 'Alloy Steel')                     #2
            sr_group.outputs.new('NodeSocketFloat', 'Tool Steel')                      #3
            sr_group.outputs.new('NodeSocketFloat', 'Spring Steel')                    #4
            sr_group.outputs.new('NodeSocketFloat', 'Structural Steel')                #5
            sr_group.outputs.new('NodeSocketFloat', 'High-Strength, Low-Alloy Steel')  #6
            sr_group.outputs.new('NodeSocketFloat', 'Maraging Steel')                  #7
            sr_group.outputs.new('NodeSocketFloat', 'Weathering Steel')                #8
            sr_group.outputs.new('NodeSocketFloat', 'Free-machining Steel')            #9
        else:
            sr_group.interface.new_socket(name="Carbon Steel", in_out='OUTPUT', socket_type='NodeSocketFloat')
            sr_group.interface.new_socket(name="Stainless Steel", in_out='OUTPUT', socket_type='NodeSocketFloat')
            sr_group.interface.new_socket(name="Alloy Steel", in_out='OUTPUT', socket_type='NodeSocketFloat')
            sr_group.interface.new_socket(name="Tool Steel", in_out='OUTPUT', socket_type='NodeSocketFloat')
            sr_group.interface.new_socket(name="Spring Steel", in_out='OUTPUT', socket_type='NodeSocketFloat')
            sr_group.interface.new_socket(name="Structural Steel", in_out='OUTPUT', socket_type='NodeSocketFloat')
            sr_group.interface.new_socket(name="High-Strength, Low-Alloy Steel", in_out='OUTPUT', socket_type='NodeSocketFloat')
            sr_group.interface.new_socket(name="Maraging Steel", in_out='OUTPUT', socket_type='NodeSocketFloat')
            sr_group.interface.new_socket(name="Weathering Steel", in_out='OUTPUT', socket_type='NodeSocketFloat')
            sr_group.interface.new_socket(name="Free-machining Steel", in_out='OUTPUT', socket_type='NodeSocketFloat')

        #set values
        group_out.inputs[0].default_value = 0.5
        group_out.inputs[1].default_value = 0.2
        group_out.inputs[2].default_value = 0.4
        group_out.inputs[3].default_value = 0.3
        group_out.inputs[4].default_value = 0.2
        group_out.inputs[5].default_value = 0.3
        group_out.inputs[6].default_value = 0.2
        group_out.inputs[7].default_value = 0.05
        group_out.inputs[8].default_value = 0.05
        group_out.inputs[9].default_value = 0.1

    def make_node(self, group, arg1, arg2, arg3):
        result = group.nodes.new(arg1)
        result.location = arg2, arg3
        return result
