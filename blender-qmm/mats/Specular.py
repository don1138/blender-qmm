import bpy

class SpecularGroup(bpy.types.Operator):
    """Add/Get Specular Group Node"""
    bl_label  = "Specular Node Group"
    bl_idname = 'node.specular_group_operator'

    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        ng_specular = bpy.data.node_groups.get("Specular")

        if not ng_specular:
            self.make_group()
        return {'FINISHED'}

    def make_node(self, specular_group, arg1, arg2, arg3):
        result = specular_group.nodes.new('ShaderNodeMath')
        result.operation = arg1
        result.location = arg2, arg3
        return result

    def make_group(self):
        # newnodegroup
        specular_group = bpy.data.node_groups.new('Specular', 'ShaderNodeTree')

        # groupinput
        group_in = specular_group.nodes.new('NodeGroupInput')
        group_in.location = (-1000, 0)
        specular_group.inputs.new('NodeSocketFloat', 'IOR')

        # groupoutput
        group_out = specular_group.nodes.new('NodeGroupOutput')
        group_out.location = (0, 0)
        specular_group.outputs.new('NodeSocketFloat', 'Specular')
        specular_group.outputs.new('NodeSocketFloat', 'IOR')

        # IOR TO SPECULAR
        # mathdivide
        m_divide = self.make_node(
            specular_group, 'DIVIDE', -200, 200
        )
        m_divide.inputs[1].default_value = 0.08

        # mathpower
        m_power = self.make_node(
            specular_group, 'POWER', -400, 200
        )
        m_power.inputs[1].default_value = 2

        # mathdivide2
        m_divide2 = self.make_node(
            specular_group, 'DIVIDE', -600, 200
        )

        # mathsubtract
        m_subtract = self.make_node(
            specular_group, 'SUBTRACT', -800, 200
        )
        m_subtract.inputs[1].default_value = 1

        # mathadd
        m_add = self.make_node(specular_group, 'ADD', -800, -100)
        m_add.inputs[1].default_value = 1

        links = specular_group.links.new

        links(group_in.outputs[0], m_subtract.inputs[0])
        links(group_in.outputs[0], m_add.inputs[0])
        links(m_add.outputs[0], m_divide2.inputs[1])
        links(m_subtract.outputs[0], m_divide2.inputs[0])
        links(m_divide2.outputs[0], m_power.inputs[0])
        links(m_power.outputs[0], m_divide.inputs[0])
        links(m_divide.outputs[0], group_out.inputs[0])
        links(group_in.outputs[0], group_out.inputs[1])
