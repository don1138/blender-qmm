import bpy

class EnergyConservationGroup(bpy.types.Operator):
    """Add/Get Energy Conservation Group Node"""
    bl_label = "Energy Conservation Node Group"
    bl_idname = 'node.ec_group_operator'
    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        ng_ec = bpy.data.node_groups.get("Energy Conservation")

        if not ng_ec:
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

# IOR TO SPECULAR
            #mathdivide
            m_divide = ec_group.nodes.new('ShaderNodeMath')
            m_divide.operation = 'DIVIDE'
            m_divide.location = (-400,0)
            m_divide.inputs[1].default_value = 0.08

            #mathpower
            m_power = ec_group.nodes.new('ShaderNodeMath')
            m_power.operation = 'POWER'
            m_power.location = (-600,0)
            m_power.inputs[1].default_value = 2

            #mathdivide2
            m_divide2 = ec_group.nodes.new('ShaderNodeMath')
            m_divide2.operation = 'DIVIDE'
            m_divide2.location = (-800,0)

            #mathsubtract
            m_subtract = ec_group.nodes.new('ShaderNodeMath')
            m_subtract.operation = 'SUBTRACT'
            m_subtract.location = (-1000,0)
            m_subtract.inputs[1].default_value = 1

            #mathadd
            m_add = ec_group.nodes.new('ShaderNodeMath')
            m_add.operation = 'ADD'
            m_add.location = (-1000,-300)
            m_add.inputs[1].default_value = 1

# CLEARCOAT
            #mathmultiply
            m_multiply = ec_group.nodes.new('ShaderNodeMath')
            m_multiply.label = "Clearcoat"
            m_multiply.operation = 'MULTIPLY'
            m_multiply.location = (-200,200)
            m_multiply.inputs[1].default_value = 10

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

        return {'FINISHED'}
