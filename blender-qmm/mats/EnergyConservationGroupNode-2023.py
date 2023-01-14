# TODO: Replace Specular Sine Mapping with Specular Exponential Mapping

import bpy

bv = bpy.app.version

class EnergyConservationGroup(bpy.types.Operator):
    """Add/Get Energy Conservation Group Node"""
    bl_label  = "Energy Conservation Node Group"
    bl_idname = 'node.ec_group_operator'

    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        ng_spec = bpy.data.node_groups.get("% Specular")
        ng_smap = bpy.data.node_groups.get("% Specular Mapping")
        ng_sine = bpy.data.node_groups.get("% Specular Sine Mapping")
        ng_ec = bpy.data.node_groups.get("Energy Conservation")

        if not ng_spec:
            self.make_spec_group()

        if not ng_smap:
            self.make_sm_group()

        if not ng_sine:
            self.make_sine_group()

        if not ng_ec:
            self.make_ec_group()

        return {'FINISHED'}

    def make_spec_group(self):
        # spec_group
        spec_group = bpy.data.node_groups.new('% Specular', 'ShaderNodeTree')

        # groupinput
        group_in = self.make_node(spec_group, 'NodeGroupInput', -1000, 0)
        spec_group.inputs.new('NodeSocketFloat', 'IOR')
        spec_group.inputs[0].default_value = 1.52
        spec_group.inputs[0].min_value = 0
        spec_group.inputs[0].max_value = 10

        # groupoutput
        group_out = self.make_node(spec_group, 'NodeGroupOutput', 0, 0)
        spec_group.outputs.new('NodeSocketFloat', 'IOR')

        # mathdivide
        m_divide = self.make_math_node(spec_group, 'DIVIDE', -200, 100)
        m_divide.inputs[1].default_value = 0.08

        # mathpower
        m_power = self.make_math_node(spec_group, 'POWER', -400, 100)
        m_power.inputs[1].default_value = 2

        # mathdivide2
        m_divide2 = self.make_math_node(spec_group, 'DIVIDE', -600, 100)

        # mathsubtract
        m_subtract = self.make_math_node(spec_group, 'SUBTRACT', -800, 100)
        m_subtract.inputs[1].default_value = 1

        # mathadd
        m_add = self.make_math_node(spec_group, 'ADD', -800, -100)
        m_add.inputs[1].default_value = 1

        slinks = spec_group.links.new

        # connect spec group
        slinks(group_in.outputs[0], m_subtract.inputs[0])
        slinks(group_in.outputs[0], m_add.inputs[0])
        slinks(m_add.outputs[0], m_divide2.inputs[1])
        slinks(m_subtract.outputs[0], m_divide2.inputs[0])
        slinks(m_divide2.outputs[0], m_power.inputs[0])
        slinks(m_power.outputs[0], m_divide.inputs[0])
        slinks(m_divide.outputs[0], group_out.inputs[1])

    def make_sm_group(self):
        # specular_sine_mapping_group
        sm_group = bpy.data.node_groups.new('% Specular Mapping', 'ShaderNodeTree')

        # groupinput
        group_in = self.make_node(sm_group, 'NodeGroupInput', -1000, 0)
        sm_group.inputs.new('NodeSocketFloat', 'Value')

        # groupoutput
        group_out = self.make_node(sm_group, 'NodeGroupOutput', 0, 0)
        sm_group.outputs.new('NodeSocketFloat', 'Value')

        # mathsubtract
        m_subtract = self.make_math_node(sm_group, 'SUBTRACT', -200, 0)
        m_subtract.inputs[0].default_value = 1

        # mathmultiply
        m_multiply = self.make_math_node(sm_group, 'MULTIPLY', -400, 0)

        # mathsubtract2
        m_subtract2 = self.make_math_node(sm_group, 'SUBTRACT', -600, 100)
        m_subtract2.inputs[0].default_value = 1

        # mathsine
        m_sine = self.make_math_node(sm_group, 'SINE', -600, -100)

        # mathdivide
        m_divide = self.make_math_node(sm_group, 'DIVIDE', -800, -100)
        m_divide.inputs[0].default_value = 3.14159
        m_divide.inputs[1].default_value = 2

        smlinks = sm_group.links.new

        # connect sm group
        smlinks(group_in.outputs[0], m_subtract2.inputs[1])
        smlinks(m_divide.outputs[0], m_sine.inputs[0])
        smlinks(m_subtract2.outputs[0], m_multiply.inputs[0])
        smlinks(m_sine.outputs[0], m_multiply.inputs[1])
        smlinks(m_multiply.outputs[0], m_subtract.inputs[1])
        smlinks(m_subtract.outputs[0], group_out.inputs[0])

    def make_sine_group(self):
        # sine_mapping_group
        sine_group = bpy.data.node_groups.new('% Specular Sine Mapping', 'ShaderNodeTree')

        # groupinput
        group_in = self.make_node(sine_group, 'NodeGroupInput', -800, 0)
        sine_group.inputs.new('NodeSocketColor', 'Color')

        # groupoutput
        group_out = self.make_node(sine_group, 'NodeGroupOutput', 0, 0)
        sine_group.outputs.new('NodeSocketColor', 'Color')

        # combineecolor
        combine_color = self.make_node(sine_group, 'ShaderNodeCombineColor', 200, 0)

        # % specular mapping
        sm_group_r = self.make_node_group(sine_group, "% Specular Mapping", '% Specular Mapping')
        sm_group_r.location = (-400, 200)

        sm_group_g = self.make_node_group(sine_group, "% Specular Mapping", '% Specular Mapping')
        sm_group_g.location = (-400, 0)

        sm_group_b = self.make_node_group(sine_group, "% Specular Mapping", '% Specular Mapping')
        sm_group_b.location = (-400, -200)

        # separatecolor
        separate_color = self.make_node(sine_group, 'ShaderNodeSeparateColor', -600, 0)

        snlinks = sine_group.links.new

        # connect sine group
        snlinks(group_in.outputs[0], separate_color.inputs[0])
        snlinks(separate_color.outputs[0], sm_group_r.inputs[0])
        snlinks(separate_color.outputs[1], sm_group_g.inputs[0])
        snlinks(separate_color.outputs[2], sm_group_b.inputs[0])
        snlinks(sm_group_r.outputs[0], combine_color.inputs[0])
        snlinks(sm_group_g.outputs[0], combine_color.inputs[1])
        snlinks(sm_group_b.outputs[0], combine_color.inputs[2])
        snlinks(combine_color.outputs[0], group_out.inputs[0])

    def make_ec_group(self):
        # ec_group
        ec_group = bpy.data.node_groups.new('Energy Conservation', 'ShaderNodeTree')

        # groupinput
        group_in = self.make_node(ec_group, 'NodeGroupInput', -600, -100)
        ec_group.inputs.new('NodeSocketFloat', 'IOR')               #0
        ec_group.inputs.new('NodeSocketColor', 'Diffuse (Base)')    #1
        ec_group.inputs.new('NodeSocketString', '- Specular -')     #2
        ec_group.inputs.new('NodeSocketColor', 'Specular Custom')   #3
        ec_group.inputs.new('NodeSocketFloat', 'Auto/Custom')       #4
        ec_group.inputs[0].default_value = 1.52
        ec_group.inputs[0].min_value = 0
        ec_group.inputs[0].max_value = 10
        ec_group.inputs[1].default_value = (0.428690, 0.527115, 0.590619, 1)
        ec_group.inputs[2].hide_value = True
        ec_group.inputs[3].default_value = (0.01, 0.01, 0.01, 1)
        ec_group.inputs[4].default_value = 0
        ec_group.inputs[4].min_value = 0
        ec_group.inputs[4].max_value = 1

        # groupoutput
        group_out = self.make_node(ec_group, 'NodeGroupOutput', 0, 0)
        ec_group.outputs.new('NodeSocketColor', 'Color')
        ec_group.outputs.new('NodeSocketFloat', 'Specular')
        ec_group.outputs.new('NodeSocketFloat', 'Clearcoat')
        ec_group.outputs.new('NodeSocketFloat', 'IOR')

        # IOR TO SPECULAR
        spec_group = self.make_node_group(ec_group, "% Specular", '% Specular')
        spec_group.location = (-400, -100)

        # CLEARCOAT
        # mathmultiply
        m_multiply = self.make_math_node(ec_group, 'MULTIPLY', -200, 100)
        m_multiply.inputs[1].default_value = 10
        m_multiply.label = "Clearcoat"

        # colormix
        if bv < (3, 4, 0):
            m_colormix = self.make_node(ec_group, 'ShaderNodeMixRGB', -400, 300)
        else:
            m_colormix = self.make_node(ec_group, 'ShaderNodeMix', -400, 200)
            m_colormix.data_type = 'RGBA'

        # FRESNEL COLOR
        # fresnel
        m_fresnel = self.make_node(ec_group, 'ShaderNodeFresnel', -600, 200)

        # groupinput2
        group_in2 = self.make_node(ec_group, 'NodeGroupInput', -800, 200)

        # colormix2
        if bv < (3, 4, 0):
            m_colormix2 = self.make_node(ec_group, 'ShaderNodeMixRGB', -1000, 200)
        else:
            m_colormix2 = self.make_node(ec_group, 'ShaderNodeMix', -1000, 200)
            m_colormix2.data_type = 'RGBA'

        # Specular Sine Mapping
        sine_group = self.make_node_group(ec_group, "% Specular Sine Mapping", '% Specular Sine Mapping')
        sine_group.location = (-1200, 200)

        # mathgreaterthan
        m_greaterthan = self.make_math_node(ec_group, 'GREATER_THAN', -1200, 0)
        m_greaterthan.inputs[1].default_value = 0.5

        # groupinput3
        group_in3 = self.make_node(ec_group, 'NodeGroupInput', -1400, 200)

        links = ec_group.links.new

        # connect ior calc
        links(group_in.outputs[0], spec_group.inputs[0])
        links(spec_group.outputs[0], group_out.inputs[1])

        # connect clearcoat
        links(spec_group.outputs[0], m_multiply.inputs[0])
        links(m_multiply.outputs[0], group_out.inputs[2])

        links(group_in2.outputs[0], m_fresnel.inputs[0])

        # connect color mix
        links(m_fresnel.outputs[0], m_colormix.inputs[0])
        links(m_greaterthan.outputs[0], m_colormix2.inputs[0])
        if bv < (3, 4, 0):
            links(group_in2.outputs[1], m_colormix.inputs[1])
            links(m_colormix2.outputs[0], m_colormix.inputs[2])
            links(m_colormix.outputs[0], group_out.inputs[0])
            links(sine_group.outputs[0], m_colormix2.inputs[1])
            links(group_in3.outputs[3], m_colormix2.inputs[2])
        else:
            links(group_in2.outputs[1], m_colormix.inputs[6])
            links(m_colormix2.outputs[2], m_colormix.inputs[7])
            links(m_colormix.outputs[2], group_out.inputs[0])
            links(sine_group.outputs[0], m_colormix2.inputs[6])
            links(group_in3.outputs[3], m_colormix2.inputs[7])

        links(group_in3.outputs[1], sine_group.inputs[0])
        links(group_in3.outputs[4], m_greaterthan.inputs[0])

    def make_node(self, group, arg1, arg2, arg3):
        result = group.nodes.new(arg1)
        result.location = arg2, arg3
        return result

    def make_node_group(self, group, arg1, arg2):
        result = group.nodes.new("ShaderNodeGroup")
        result.name = arg1
        result.node_tree = bpy.data.node_groups[arg2]
        return result

    def make_math_node(self, group, arg1, arg2, arg3):
        result = self.make_node(group, 'ShaderNodeMath', arg2, arg3)
        result.operation = arg1
        return result
