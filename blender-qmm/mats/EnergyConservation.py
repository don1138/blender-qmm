# Energy Conservation v5 Group v.5
import bpy

bv = bpy.app.version

class EnergyConservationGroup(bpy.types.Operator):
    """Add/Get Energy Conservation v5 Group Node"""
    bl_label  = "Energy Conservation v5 Node Group"
    bl_idname = 'node.ec_group_operator'

    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        ng_spec = bpy.data.node_groups.get("Specular")
        ng_fres = bpy.data.node_groups.get("Fresnel CCP")
        ng_ec   = bpy.data.node_groups.get("Energy Conservation v5")

        if not ng_spec:
            self.make_spec_group()

        if not ng_fres:
            self.make_fres_group()

        if not ng_ec:
            self.make_ec_group()

        return {'FINISHED'}

    def make_spec_group(self):
        # spec_group
        spec_group = bpy.data.node_groups.new('Specular', 'ShaderNodeTree')

        # groupinput
        group_in = self.make_node(spec_group, 'NodeGroupInput', -1000, 0)
        spec_group.inputs.new('NodeSocketFloat', 'IOR')
        spec_group.inputs[0].default_value = 1.52
        spec_group.inputs[0].min_value = 0
        spec_group.inputs[0].max_value = 10

        # groupoutput
        group_out = self.make_node(spec_group, 'NodeGroupOutput', 0, 0)
        spec_group.outputs.new('NodeSocketFloat', 'Specular')
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

        # connect spec group
        links = spec_group.links.new
        links(group_in.outputs[0], m_subtract.inputs[0])
        links(group_in.outputs[0], m_add.inputs[0])
        links(group_in.outputs[0], group_out.inputs[1])
        links(m_add.outputs[0], m_divide2.inputs[1])
        links(m_subtract.outputs[0], m_divide2.inputs[0])
        links(m_divide2.outputs[0], m_power.inputs[0])
        links(m_power.outputs[0], m_divide.inputs[0])
        links(m_divide.outputs[0], group_out.inputs[0])

    def make_fres_group(self):
        # fresnel group - cynicalcatpro version
        fres_group = bpy.data.node_groups.new('Fresnel CCP', 'ShaderNodeTree')
        
        # groupinput
        group_in = self.make_node(fres_group, 'NodeGroupInput', -1000, 0)
        fres_group.inputs.new('NodeSocketFloat', 'Roughness')
        fres_group.inputs.new('NodeSocketFloat', 'IOR')
        fres_group.inputs.new('NodeSocketVector', 'Normal')
        fres_group.inputs[0].default_value = 0.2
        fres_group.inputs[0].min_value = 0
        fres_group.inputs[0].max_value = 1
        fres_group.inputs[1].default_value = 1.45
        fres_group.inputs[1].min_value = 0
        fres_group.inputs[1].max_value = 3

        # groupoutput
        group_out = self.make_node(fres_group, 'NodeGroupOutput', 0, 0)
        fres_group.outputs.new('NodeSocketFloat', 'Fresnel')
        fres_group.outputs.new('NodeSocketFloat', 'Fresnel Metal')

        # fresnel
        m_fresnel = self.make_node(fres_group, 'ShaderNodeFresnel', -400, 0)

        # layer weight
        m_layer_weight = self.make_node(fres_group, 'ShaderNodeLayerWeight', -400, -200)

        # power
        m_power = self.make_math_node(fres_group, 'POWER', -200, -100)
        m_power.inputs[1].default_value = 5
        
        # colormix
        if bv < (3, 4, 0):
            m_colormix = self.make_node(fres_group, 'ShaderNodeMixRGB', -600, -100)
        else:
            m_colormix = self.make_node(fres_group, 'ShaderNodeMix', -600, -100)
            m_colormix.data_type = 'RGBA'

        # bump
        m_bump = self.make_node(fres_group, 'ShaderNodeBump', -800, -100)
        m_bump.inputs[0].default_value = 0
        m_bump.inputs[1].default_value = 0.1
        
        # geometry
        m_geometry = self.make_node(fres_group, 'ShaderNodeNewGeometry', -800, -300)

        # connect fres_group
        links = fres_group.links.new
        links(group_in.outputs[0], m_colormix.inputs[0])
        links(group_in.outputs[1], m_fresnel.inputs[0])
        links(group_in.outputs[2], m_bump.inputs[3])
        if bv < (3, 4, 0):
            links(m_bump.outputs[0], m_colormix.inputs[1])
            links(m_geometry.outputs[4], m_colormix.inputs[2])
            links(m_colormix.outputs[0], m_fresnel.inputs[1])
            links(m_colormix.outputs[0], m_layer_weight.inputs[1])
        else:
            links(m_bump.outputs[0], m_colormix.inputs[6])
            links(m_geometry.outputs[4], m_colormix.inputs[7])
            links(m_colormix.outputs[2], m_fresnel.inputs[1])
            links(m_colormix.outputs[2], m_layer_weight.inputs[1])
        links(m_fresnel.outputs[0], group_out.inputs[0])
        links(m_layer_weight.outputs[1], m_power.inputs[0])
        links(m_power.outputs[0], group_out.inputs[1])

    def make_ec_group(self):
        # ec_group
        ec_group = bpy.data.node_groups.new('Energy Conservation v5', 'ShaderNodeTree')

        # groupinput
        group_in = self.make_node(ec_group, 'NodeGroupInput', -200, 0)
        group_in.label = "Group In 1"
        ec_group.inputs.new('NodeSocketColor', 'Reflectivity')      #0
        ec_group.inputs.new('NodeSocketFloat', 'Roughness')         #1
        ec_group.inputs.new('NodeSocketFloat', 'IOR')               #2
        ec_group.inputs.new('NodeSocketVector', 'Normal')           #3
        ec_group.inputs.new('NodeSocketColor', 'Edge Tint')         #4
        ec_group.inputs.new('NodeSocketFloat', 'Custom/Auto')       #5
        ec_group.inputs.new('NodeSocketFloat', 'Metal/Dielectric')  #6
        ec_group.inputs[0].default_value = (0.215860, 0.215860, 0.215861, 1)
        ec_group.inputs[1].default_value = 0.2
        ec_group.inputs[1].min_value = 0
        ec_group.inputs[1].max_value = 1
        ec_group.inputs[2].default_value = 1.45
        ec_group.inputs[2].min_value = 0
        ec_group.inputs[2].max_value = 3
        ec_group.inputs[3].hide_value = True
        ec_group.inputs[4].default_value = (0.01, 0.01, 0.01, 1)
        ec_group.inputs[5].default_value = 0
        ec_group.inputs[5].min_value = 0
        ec_group.inputs[5].max_value = 1
        ec_group.inputs[6].default_value = 0
        ec_group.inputs[6].min_value = 0
        ec_group.inputs[6].max_value = 1

        # groupoutput
        group_out = self.make_node(ec_group, 'NodeGroupOutput', 0, 0)
        ec_group.outputs.new('NodeSocketColor', 'Color')      #0
        ec_group.outputs.new('NodeSocketFloat', 'Specular')   #1
        ec_group.outputs.new('NodeSocketFloat', 'Roughness')  #2
        ec_group.outputs.new('NodeSocketFloat', 'Clearcoat')  #3
        ec_group.outputs.new('NodeSocketFloat', 'IOR')        #4

        # CLEARCOAT
        m_clearcoat = self.make_math_node(ec_group, 'MULTIPLY', -200, -300)
        m_clearcoat.label = "Clearcoat"
        m_clearcoat.inputs[1].default_value = 10
        m_clearcoat.label = "Clearcoat"

        # colormix1
        if bv < (3, 4, 0):
            m_colormix = self.make_node(ec_group, 'ShaderNodeMixRGB', -400, 300)
        else:
            m_colormix = self.make_node(ec_group, 'ShaderNodeMix', -400, 300)
            m_colormix.data_type = 'RGBA'
        m_colormix.label = "Color Mix 1"

        # IOR TO SPECULAR
        spec_group = self.make_node_group(ec_group, "Specular", 'Specular', -400, -300)
        spec_group.label = "Specular"

        # colormix2
        if bv < (3, 4, 0):
            m_colormix2 = self.make_node(ec_group, 'ShaderNodeMixRGB', -600, 400)
        else:
            m_colormix2 = self.make_node(ec_group, 'ShaderNodeMix', -600, 400)
            m_colormix2.data_type = 'RGBA'
        m_colormix2.label = "Color Mix 2"

        # colormix3
        if bv < (3, 4, 0):
            m_colormix3 = self.make_node(ec_group, 'ShaderNodeMixRGB', -600, 0)
        else:
            m_colormix3 = self.make_node(ec_group, 'ShaderNodeMix', -600, 0)
            m_colormix3.data_type = 'RGBA'
        m_colormix3.label = "Color Mix 3"

        # groupinput2
        group_in2 = self.make_node(ec_group, 'NodeGroupInput', -600, -300)
        group_in2.label = "Group In 2"

        # bool1
        m_greaterthan = self.make_math_node(ec_group, 'GREATER_THAN', -800, 200)
        m_greaterthan.inputs[1].default_value = 0.5
        m_greaterthan.label = "Bool 1"

        # bool2
        m_greaterthan2 = self.make_math_node(ec_group, 'GREATER_THAN', -800, -100)
        m_greaterthan2.inputs[1].default_value = 0.5
        m_greaterthan2.label = "Bool 2"

        # colormix4
        if bv < (3, 4, 0):
            m_colormix4 = self.make_node(ec_group, 'ShaderNodeMixRGB', -800, -300)
            m_colormix4.inputs[1].default_value = (0.99, 0.99, 0.99, 1)
        else:
            m_colormix4 = self.make_node(ec_group, 'ShaderNodeMix', -800, -300)
            m_colormix4.data_type = 'RGBA'
            m_colormix4.inputs[6].default_value = (0.99, 0.99, 0.99, 1)
        m_colormix4.label = "Color Mix 4"

        # FRESNEL GROUP
        fres_group = self.make_node_group(ec_group, "Fresnel CCP", 'Fresnel CCP', -1000, 300)
        fres_group.label = "Fresnel CCP"

        # groupinput4
        group_in4 = self.make_node(ec_group, 'NodeGroupInput', -1000, 0)
        group_in4.label = "Group In 4"

        # HSV
        m_hsv = self.make_node(ec_group, 'ShaderNodeHueSaturation', -1000, -300)
        m_hsv.inputs[2].default_value = 0.01
        m_hsv.label = "HSV"

        # bool 3
        m_greaterthan3 = self.make_math_node(ec_group, 'GREATER_THAN', -1000, -500)
        m_greaterthan3.inputs[1].default_value = 0.5
        m_greaterthan3.label = "Bool 3"

        # groupinput3
        group_in3 = self.make_node(ec_group, 'NodeGroupInput', -1200, 300)
        group_in3.label = "Group In 3"

        # groupinput5
        group_in5 = self.make_node(ec_group, 'NodeGroupInput', -1200, -400)
        group_in5.label = "Group In 5"

        links = ec_group.links.new

        # connect group in 1
        links(group_in.outputs[1], group_out.inputs[2])
        links(group_in.outputs[2], group_out.inputs[4])
        
        # connect clearcoat
        links(m_clearcoat.outputs[0], group_out.inputs[3])

        # connect color mix 1
        if bv < (3, 4, 0):
            links(group_in3.outputs[0], m_colormix.inputs[1])
            links(m_colormix.outputs[0], m_colormix.inputs[2])
            links(m_colormix.outputs[0], group_out.inputs[0])
        else:
            links(group_in3.outputs[0], m_colormix.inputs[6])
            links(m_colormix3.outputs[2], m_colormix.inputs[7])
            links(m_colormix.outputs[2], group_out.inputs[0])

        # connect specular group
        links(spec_group.outputs[0], group_out.inputs[1])
        links(spec_group.outputs[0], m_clearcoat.inputs[0])

        # connect color mix 2
        links(m_greaterthan.outputs[0], m_colormix2.inputs[0])
        if bv < (3, 4, 0):
            links(fres_group.outputs[0], m_colormix2.inputs[2])
            links(fres_group.outputs[1], m_colormix2.inputs[1])
            links(m_colormix2.outputs[0], m_colormix.inputs[0])
        else:
            links(fres_group.outputs[0], m_colormix2.inputs[7])
            links(fres_group.outputs[1], m_colormix2.inputs[6])
            links(m_colormix2.outputs[2], m_colormix.inputs[0])

        # connect fresnel group

        # connect bool 2 to color mix 3
        links(m_greaterthan2.outputs[0], m_colormix3.inputs[0])
        if bv < (3, 4, 0):
            links(group_in4.outputs[4], m_colormix3.inputs[1])
            links(m_colormix4.outputs[0], m_colormix3.inputs[2])
        else:
            links(group_in4.outputs[4], m_colormix3.inputs[6])
            links(m_colormix4.outputs[2], m_colormix3.inputs[7])

        # connect group in 2
        links(group_in2.outputs[2], spec_group.inputs[0])

        # connect group in 3
        links(group_in3.outputs[1], fres_group.inputs[0])
        links(group_in3.outputs[2], fres_group.inputs[1])
        links(group_in3.outputs[3], fres_group.inputs[2])
        links(group_in3.outputs[6], m_greaterthan.inputs[0])

        # connect color mix 3
        links(m_greaterthan3.outputs[0], m_colormix4.inputs[0])
        if bv < (3, 4, 0):
            links(m_hsv.outputs[0], m_colormix4.inputs[2])
        else:
            links(m_hsv.outputs[0], m_colormix4.inputs[7])

        # connect group in 4
        links(group_in4.outputs[5], m_greaterthan2.inputs[0])

        # connect group in 5
        links(group_in5.outputs[0], m_hsv.inputs[4])
        links(group_in5.outputs[6], m_greaterthan3.inputs[0])
        
    def make_node(self, group, arg1, arg2, arg3):
        result = group.nodes.new(arg1)
        result.location = arg2, arg3
        return result

    def make_node_group(self, group, arg1, arg2, locX, locY):
        result = group.nodes.new("ShaderNodeGroup")
        result.name = arg1
        result.node_tree = bpy.data.node_groups[arg2]
        result.location = locX, locY
        return result

    def make_math_node(self, group, arg1, arg2, arg3):
        result = self.make_node(group, 'ShaderNodeMath', arg2, arg3)
        result.operation = arg1
        return result

    def make_math_multiply_node(self, group, locY):
        result = self.make_math_node(group, 'MULTIPLY', -400, locY)
        result.inputs[0].default_value = 2
        result.use_clamp = True
        return result
