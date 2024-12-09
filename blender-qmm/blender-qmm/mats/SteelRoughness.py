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
            sr_group.outputs.new('NodeSocketFloat', '0.05 - Maraging, Weathering Steel')      #0
            sr_group.outputs.new('NodeSocketFloat', '0.1 - Free-Machining Steel')            #1
            sr_group.outputs.new('NodeSocketFloat', '0.2 - Spring, Stainless, HSLA Steel')   #2
            sr_group.outputs.new('NodeSocketFloat', '0.3 - Structural, Tool Steel')          #3
            sr_group.outputs.new('NodeSocketFloat', '0.4 - Alloy Steel')                     #4
            sr_group.outputs.new('NodeSocketFloat', '0.5 - Carbon Steel')                    #5
        else:
            sr_group.interface.new_socket(name="0.05 - Maraging, Weathering Steel", in_out='OUTPUT', socket_type='NodeSocketFloat')
            sr_group.interface.new_socket(name="0.1 - Free-Machining Steel", in_out='OUTPUT', socket_type='NodeSocketFloat')
            sr_group.interface.new_socket(name="0.2 - Spring, Stainless, HSLA Steel", in_out='OUTPUT', socket_type='NodeSocketFloat')
            sr_group.interface.new_socket(name="0.3 - Structural, Tool Steel", in_out='OUTPUT', socket_type='NodeSocketFloat')
            sr_group.interface.new_socket(name="0.4 - Alloy Steel", in_out='OUTPUT', socket_type='NodeSocketFloat')
            sr_group.interface.new_socket(name="0.5 - Carbon Steel", in_out='OUTPUT', socket_type='NodeSocketFloat')

        #set values
        group_out.inputs[0].default_value = 0.05
        group_out.inputs[1].default_value = 0.1
        group_out.inputs[2].default_value = 0.2
        group_out.inputs[3].default_value = 0.3
        group_out.inputs[4].default_value = 0.4
        group_out.inputs[5].default_value = 0.5

    def make_node(self, group, arg1, arg2, arg3):
        result = group.nodes.new(arg1)
        result.location = arg2, arg3
        return result
