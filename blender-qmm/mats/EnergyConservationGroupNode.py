import bpy

class EnergyConservationGroup(bpy.types.Operator):
    """Add/Get Energy Conservation Group Node"""
    bl_label = "Energy Conservation Node Group"
    bl_idname = 'node.ec_group_operator'
    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        ng_ec = bpy.data.node_groups.get("Energy Conservation")

        if not ng_ec:
            self.make_group()
        return {'FINISHED'}

    def make_group(self):
        #newnodegroup
        ec_group = bpy.data.node_groups.new('Energy Conservation', 'ShaderNodeTree')

        #groupinput
        group_in = ec_group.nodes.new('NodeGroupInput')
        group_in.location = (-1400, 0)
        ec_group.inputs.new('NodeSocketFloat', 'IOR')
        ec_group.inputs.new('NodeSocketColor', 'Diffuse (Base)')
        ec_group.inputs.new('NodeSocketColor', 'Specular')
        ec_group.inputs[0].default_value = 1.52
        ec_group.inputs[1].default_value = (0.428690, 0.527115, 0.590619, 1)
        ec_group.inputs[2].default_value = (0.01, 0.01, 0.01, 1)

        #groupoutput
        group_out = ec_group.nodes.new('NodeGroupOutput')
        group_out.location = (0, 0)
        ec_group.outputs.new('NodeSocketColor', 'Color')
        ec_group.outputs.new('NodeSocketFloat', 'Specular')
        ec_group.outputs.new('NodeSocketFloat', 'Clearcoat')
        ec_group.outputs.new('NodeSocketFloat', 'IOR')

        m_divide = self.make_node(ec_group, 'DIVIDE', -400, 0)
        m_divide.inputs[1].default_value = 0.08

        m_power = self.make_node(ec_group, 'POWER', -600, 0)
        m_power.inputs[1].default_value = 2

        m_divide2 = self.make_node(ec_group, 'DIVIDE', -800, 0)
        m_subtract = self.make_node(ec_group, 'SUBTRACT', -1000, 0)
        m_subtract.inputs[1].default_value = 1

        m_add = self.make_node(ec_group, 'ADD', -1000, -300)
        m_add.inputs[1].default_value = 1

        m_multiply = self.make_node(ec_group, 'MULTIPLY', -200, 200)
        m_multiply.inputs[1].default_value = 10

        m_multiply.label = "Clearcoat"

        # FRESNEL COLOR
        #fresnel
        m_fresnel = ec_group.nodes.new('ShaderNodeFresnel')
        m_fresnel.location = (-1000,300)

        #colormix
        m_colormix = ec_group.nodes.new('ShaderNodeMixRGB')
        m_colormix.location = (-800,300)

        links = ec_group.links.new

        links(group_in.outputs[0], m_subtract.inputs[0])
        links(group_in.outputs[0], m_add.inputs[0])
        links(m_add.outputs[0], m_divide2.inputs[1])
        links(m_subtract.outputs[0], m_divide2.inputs[0])
        links(m_divide2.outputs[0], m_power.inputs[0])
        links(m_power.outputs[0], m_divide.inputs[0])
        links(m_divide.outputs[0], group_out.inputs[1])
        links(group_in.outputs[0], group_out.inputs[3])

        links(m_divide.outputs[0], m_multiply.inputs[0])
        links(m_multiply.outputs[0], group_out.inputs[2])

        links(group_in.outputs[0], m_fresnel.inputs[0])
        links(m_fresnel.outputs[0], m_colormix.inputs[0])
        links(group_in.outputs[1], m_colormix.inputs[1])
        links(group_in.outputs[2], m_colormix.inputs[2])
        links(m_colormix.outputs[0], group_out.inputs[0])

    def make_node(self, ec_group, arg1, arg2, arg3):
        # IOR TO SPECULAR
        #mathdivide
        result = ec_group.nodes.new('ShaderNodeMath')
        result.operation = arg1
        result.location = arg2, arg3
        return result
