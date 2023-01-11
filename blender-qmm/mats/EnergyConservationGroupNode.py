import bpy

bv = bpy.app.version

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
        # newnodegroup
        ec_group = bpy.data.node_groups.new(
            'Energy Conservation', 'ShaderNodeTree')

        # groupinput
        group_in = self.make_node(ec_group, 'NodeGroupInput', -1200, -200)
        ec_group.inputs.new('NodeSocketFloat', 'IOR')               #0
        ec_group.inputs.new('NodeSocketColor', 'Diffuse (Base)')    #1
        ec_group.inputs.new('NodeSocketString', '- Specular -')     #2
        ec_group.inputs.new('NodeSocketColor', 'Specular Custom')   #3
        ec_group.inputs.new('NodeSocketFloat', 'Custom/Auto')       #4
        ec_group.inputs.new('NodeSocketFloat', 'Metal/Dialectric')  #5
        ec_group.inputs.new('NodeSocketFloat', 'Saturation')        #6
        ec_group.inputs[0].default_value = 1.52
        ec_group.inputs[0].min_value = 0
        ec_group.inputs[0].max_value = 10
        ec_group.inputs[1].default_value = (0.428690, 0.527115, 0.590619, 1)
        ec_group.inputs[2].hide_value = True
        ec_group.inputs[3].default_value = (0.01, 0.01, 0.01, 1)
        ec_group.inputs[4].default_value = 0
        ec_group.inputs[4].min_value = 0
        ec_group.inputs[4].max_value = 1
        ec_group.inputs[5].default_value = 0
        ec_group.inputs[5].min_value = 0
        ec_group.inputs[5].max_value = 1
        ec_group.inputs[6].default_value = 0.25
        ec_group.inputs[6].min_value = 0
        ec_group.inputs[6].max_value = 1


        # groupoutput
        group_out = self.make_node(ec_group, 'NodeGroupOutput', 0, 0)
        ec_group.outputs.new('NodeSocketColor', 'Color')
        ec_group.outputs.new('NodeSocketFloat', 'Specular')
        ec_group.outputs.new('NodeSocketFloat', 'Clearcoat')
        ec_group.outputs.new('NodeSocketFloat', 'IOR')

        # IOR TO SPECULAR
        # mathdivide
        m_divide = self.make_math_node(ec_group, 'DIVIDE', -400, 0)
        m_divide.inputs[1].default_value = 0.08

        # mathpower
        m_power = self.make_math_node(ec_group, 'POWER', -600, 0)
        m_power.inputs[1].default_value = 2

        # mathdivide2
        m_divide2 = self.make_math_node(ec_group, 'DIVIDE', -800, 0)

        # mathsubtract
        m_subtract = self.make_math_node(ec_group, 'SUBTRACT', -1000, 0)
        m_subtract.inputs[1].default_value = 1

        # mathadd
        m_add = self.make_math_node(ec_group, 'ADD', -1000, -300)
        m_add.inputs[1].default_value = 1

        # CLEARCOAT
        # mathmultiply
        m_multiply = self.make_math_node(ec_group, 'MULTIPLY', -200, 200)
        m_multiply.inputs[1].default_value = 10
        m_multiply.label = "Clearcoat"

        # colormix
        if bv < (3, 4, 0):
            m_colormix = self.make_node(ec_group, 'ShaderNodeMixRGB', -600, 300)
        else:
            m_colormix = self.make_node(ec_group, 'ShaderNodeMix', -600, 300)
            m_colormix.data_type = 'RGBA'

        # FRESNEL COLOR
        # fresnel
        m_fresnel = self.make_node(ec_group, 'ShaderNodeFresnel', -800, 300)

        # groupinput2
        group_in2 = self.make_node(ec_group, 'NodeGroupInput', -1000, 300)

        # colormix2
        if bv < (3, 4, 0):
            m_colormix2 = self.make_node(ec_group, 'ShaderNodeMixRGB', -1200, 200)
        else:
            m_colormix2 = self.make_node(ec_group, 'ShaderNodeMix', -1200, 200)
            m_colormix2.data_type = 'RGBA'

        # mathgreaterthan
        m_greaterthan = self.make_math_node(ec_group, 'GREATER_THAN', -1400, 200)
        m_greaterthan.inputs[1].default_value = 0.5

        # combinehsv
        m_combinehsv = self.make_node(ec_group, 'ShaderNodeCombineColor', -1400, 0)
        m_combinehsv.mode = 'HSV'
        m_combinehsv.inputs[1].default_value = 0.25
        m_combinehsv.inputs[2].default_value = 0.99

        # groupinput3
        group_in3 = self.make_node(ec_group, 'NodeGroupInput', -1600, 300)

        # separatehsv
        m_separatehsv = self.make_node(ec_group, 'ShaderNodeSeparateColor', -1800, 0)
        m_separatehsv.mode = 'HSV'

        # valuemix
        m_valuemix = self.make_node(ec_group, 'ShaderNodeMix', -1600, -200)
        m_valuemix.data_type = 'FLOAT'
        m_valuemix.inputs[2].default_value = 0.99
        m_valuemix.inputs[3].default_value = 0.01

        # mathgreaterthan2
        m_greaterthan2 = self.make_math_node(ec_group, 'GREATER_THAN', -1800, -300)
        m_greaterthan2.inputs[1].default_value = 0.5

        # groupinput4
        group_in4 = self.make_node(ec_group, 'NodeGroupInput', -2000, -100)

        links = ec_group.links.new

        # connect ior calc
        links(group_in.outputs[0], m_subtract.inputs[0])
        links(group_in.outputs[0], m_add.inputs[0])
        links(m_add.outputs[0], m_divide2.inputs[1])
        links(m_subtract.outputs[0], m_divide2.inputs[0])
        links(m_divide2.outputs[0], m_power.inputs[0])
        links(m_power.outputs[0], m_divide.inputs[0])
        links(m_divide.outputs[0], group_out.inputs[1])
        links(group_in.outputs[0], group_out.inputs[3])

        # connect clearcoat
        links(m_divide.outputs[0], m_multiply.inputs[0])
        links(m_multiply.outputs[0], group_out.inputs[2])

        # connect color mix
        links(group_in2.outputs[0], m_fresnel.inputs[0])
        links(m_fresnel.outputs[0], m_colormix.inputs[0])
        links(m_greaterthan.outputs[0], m_colormix2.inputs[0])
        links(group_in3.outputs[4], m_greaterthan.inputs[0])
        if bv < (3, 4, 0):
            links(group_in2.outputs[1], m_colormix.inputs[1])
            links(m_colormix2.outputs[0], m_colormix.inputs[2])
            links(m_colormix.outputs[0], group_out.inputs[0])
            links(group_in3.outputs[3], m_colormix2.inputs[1])
            links(group_in3.outputs[4], m_greaterthan.inputs[0])
            links(m_combinehsv.outputs[0], m_colormix2.inputs[2])
        else:
            links(group_in2.outputs[1], m_colormix.inputs[6])
            links(m_colormix2.outputs[2], m_colormix.inputs[7])
            links(m_colormix.outputs[2], group_out.inputs[0])
            links(group_in3.outputs[3], m_colormix2.inputs[6])
            links(m_combinehsv.outputs[0], m_colormix2.inputs[7])

        links(m_separatehsv.outputs[0], m_combinehsv.inputs[0])
        links(group_in4.outputs[6], m_combinehsv.inputs[1])
        links(m_valuemix.outputs[0], m_combinehsv.inputs[2])

        links(group_in4.outputs[1], m_separatehsv.inputs[0])

        links(m_greaterthan2.outputs[0], m_valuemix.inputs[0])

        links(group_in4.outputs[5], m_greaterthan2.inputs[0])


    def make_node(self, group, arg1, arg2, arg3):
        result = group.nodes.new(arg1)
        result.location = arg2, arg3
        return result

    def make_math_node(self, group, arg1, arg2, arg3):
        result = self.make_node(group, 'ShaderNodeMath', arg2, arg3)
        result.operation = arg1
        return result
