# Energy Conservation v5 Group v.5
import bpy

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
        ior_socket = spec_group.interface.new_socket(name="IOR", in_out='INPUT', socket_type='NodeSocketFloat')
        ior_socket.default_value = 1.52
        ior_socket.min_value = 0
        ior_socket.max_value = 10

        # groupoutput
        group_out = self.make_node(spec_group, 'NodeGroupOutput', 0, 0)
        spec_group.interface.new_socket(name="Specular", in_out='OUTPUT', socket_type='NodeSocketFloat')
        spec_group.interface.new_socket(name="IOR", in_out='OUTPUT', socket_type='NodeSocketFloat')

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
        links(group_in.outputs['IOR'], m_subtract.inputs[0])
        links(group_in.outputs['IOR'], m_add.inputs[0])
        links(group_in.outputs['IOR'], group_out.inputs['IOR'])
        links(m_add.outputs['Value'], m_divide2.inputs[1])
        links(m_subtract.outputs['Value'], m_divide2.inputs[0])
        links(m_divide2.outputs['Value'], m_power.inputs[0])
        links(m_power.outputs['Value'], m_divide.inputs[0])
        links(m_divide.outputs['Value'], group_out.inputs['Specular'])

    def make_fres_group(self):
        # fresnel group - cynicalcatpro version
        fres_group = bpy.data.node_groups.new('Fresnel CCP', 'ShaderNodeTree')
        
        # groupinput
        group_in = self.make_node(fres_group, 'NodeGroupInput', -1000, 0)
        roughness_socket = fres_group.interface.new_socket(name="Roughness", in_out='INPUT', socket_type='NodeSocketFloat')
        roughness_socket.default_value = 0.2
        roughness_socket.min_value = 0
        roughness_socket.max_value = 1

        ior_socket = fres_group.interface.new_socket(name="IOR", in_out='INPUT', socket_type='NodeSocketFloat')
        ior_socket.default_value = 1.45
        ior_socket.min_value = 0
        ior_socket.max_value = 3

        fres_group.interface.new_socket(name="Normal", in_out='INPUT', socket_type='NodeSocketVector')

        # groupoutput
        group_out = self.make_node(fres_group, 'NodeGroupOutput', 0, 0)
        fres_group.interface.new_socket(name="Fresnel", in_out='OUTPUT', socket_type='NodeSocketFloat')
        fres_group.interface.new_socket(name="Fresnel Metal", in_out='OUTPUT', socket_type='NodeSocketFloat')

        # fresnel
        m_fresnel = self.make_node(fres_group, 'ShaderNodeFresnel', -400, 0)

        # layer weight
        m_layer_weight = self.make_node(fres_group, 'ShaderNodeLayerWeight', -400, -200)

        # power
        m_power = self.make_math_node(fres_group, 'POWER', -200, -100)
        m_power.inputs[1].default_value = 5
        
        # colormix
        m_colormix = self.make_node(fres_group, 'ShaderNodeMix', -600, -100)
        m_colormix.data_type = 'RGBA'

        # bump
        m_bump = self.make_node(fres_group, 'ShaderNodeBump', -800, -100)
        m_bump.inputs['Strength'].default_value = 0
        m_bump.inputs['Distance'].default_value = 0.1
        
        # geometry
        m_geometry = self.make_node(fres_group, 'ShaderNodeNewGeometry', -800, -300)

        # connect fres_group
        links = fres_group.links.new
        links(group_in.outputs['Roughness'], m_colormix.inputs[0])
        links(group_in.outputs['IOR'], m_fresnel.inputs['IOR'])
        links(group_in.outputs['Normal'], m_bump.inputs['Normal'])
        links(m_bump.outputs['Normal'], m_colormix.inputs[6])
        links(m_geometry.outputs['Incoming'], m_colormix.inputs[7])
        links(m_colormix.outputs[2], m_fresnel.inputs['Normal'])
        links(m_colormix.outputs[2], m_layer_weight.inputs['Normal'])
        links(m_fresnel.outputs['Fac'], group_out.inputs['Fresnel'])
        links(m_layer_weight.outputs['Facing'], m_power.inputs[0])
        links(m_power.outputs['Value'], group_out.inputs['Fresnel Metal'])

    def make_ec_group(self):
        # ec_group
        ec_group = bpy.data.node_groups.new('Energy Conservation v5', 'ShaderNodeTree')

        # groupinput
        group_in = self.make_node(ec_group, 'NodeGroupInput', -200, 0)
        group_in.label = "Group In 1"
        reflectivity_socket = ec_group.interface.new_socket(name="Reflectivity", in_out='INPUT', socket_type='NodeSocketColor')
        reflectivity_socket.default_value = (0.215860, 0.215860, 0.215861, 1)

        roughness_socket = ec_group.interface.new_socket(name="Roughness", in_out='INPUT', socket_type='NodeSocketFloat')
        roughness_socket.default_value = 0.2
        roughness_socket.min_value = 0
        roughness_socket.max_value = 1

        ior_socket = ec_group.interface.new_socket(name="IOR", in_out='INPUT', socket_type='NodeSocketFloat')
        ior_socket.default_value = 1.45
        ior_socket.min_value = 0
        ior_socket.max_value = 3

        normal_socket = ec_group.interface.new_socket(name="Normal", in_out='INPUT', socket_type='NodeSocketVector')
        normal_socket.hide_value = True

        edge_tint_socket = ec_group.interface.new_socket(name="Edge Tint", in_out='INPUT', socket_type='NodeSocketColor')
        edge_tint_socket.default_value = (0.01, 0.01, 0.01, 1)

        custom_auto_socket = ec_group.interface.new_socket(name="Custom/Auto", in_out='INPUT', socket_type='NodeSocketFloat')
        custom_auto_socket.default_value = 0
        custom_auto_socket.min_value = 0
        custom_auto_socket.max_value = 1

        metal_dielectric_socket = ec_group.interface.new_socket(name="Metal/Dielectric", in_out='INPUT', socket_type='NodeSocketFloat')
        metal_dielectric_socket.default_value = 0
        metal_dielectric_socket.min_value = 0
        metal_dielectric_socket.max_value = 1

        # groupoutput
        group_out = self.make_node(ec_group, 'NodeGroupOutput', 0, 0)
        ec_group.interface.new_socket(name="Color", in_out='OUTPUT', socket_type='NodeSocketColor')
        ec_group.interface.new_socket(name="Specular", in_out='OUTPUT', socket_type='NodeSocketFloat')
        ec_group.interface.new_socket(name="Roughness", in_out='OUTPUT', socket_type='NodeSocketFloat')
        ec_group.interface.new_socket(name="Clearcoat", in_out='OUTPUT', socket_type='NodeSocketFloat')
        ec_group.interface.new_socket(name="IOR", in_out='OUTPUT', socket_type='NodeSocketFloat')

        # CLEARCOAT
        m_clearcoat = self.make_math_node(ec_group, 'MULTIPLY', -200, -300)
        m_clearcoat.label = "Clearcoat"
        m_clearcoat.inputs[1].default_value = 10
        m_clearcoat.label = "Clearcoat"

        # colormix1
        m_colormix = self.make_node(ec_group, 'ShaderNodeMix', -400, 300)
        m_colormix.data_type = 'RGBA'
        m_colormix.label = "Color Mix 1"

        # IOR TO SPECULAR
        spec_group = self.make_node_group(ec_group, "Specular", 'Specular', -400, -300)
        spec_group.label = "Specular"

        # colormix2
        m_colormix2 = self.make_node(ec_group, 'ShaderNodeMix', -600, 400)
        m_colormix2.data_type = 'RGBA'
        m_colormix2.label = "Color Mix 2"

        # colormix3
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
        m_hsv.inputs['Value'].default_value = 0.01
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
        links(group_in.outputs['Roughness'], group_out.inputs['Roughness'])
        links(group_in.outputs['IOR'], group_out.inputs['IOR'])

        # connect clearcoat
        links(m_clearcoat.outputs['Value'], group_out.inputs['Clearcoat'])

        # connect color mix 1
        links(group_in3.outputs['Reflectivity'], m_colormix.inputs[6])
        links(m_colormix3.outputs[2], m_colormix.inputs[7])
        links(m_colormix.outputs[2], group_out.inputs['Color'])

        # connect specular group
        links(spec_group.outputs['Specular'], group_out.inputs['Specular'])
        links(spec_group.outputs['Specular'], m_clearcoat.inputs[0])

        # connect color mix 2
        links(m_greaterthan.outputs['Value'], m_colormix2.inputs[0])
        links(fres_group.outputs['Fresnel'], m_colormix2.inputs[7])
        links(fres_group.outputs['Fresnel Metal'], m_colormix2.inputs[6])
        links(m_colormix2.outputs[2], m_colormix.inputs[0])

        # connect fresnel group

        # connect bool 2 to color mix 3
        links(m_greaterthan2.outputs['Value'], m_colormix3.inputs[0])
        links(group_in4.outputs['Edge Tint'], m_colormix3.inputs[6])
        links(m_colormix4.outputs[2], m_colormix3.inputs[7])

        # connect group in 2
        links(group_in2.outputs['IOR'], spec_group.inputs['IOR'])

        # connect group in 3
        links(group_in3.outputs['Roughness'], fres_group.inputs['Roughness'])
        links(group_in3.outputs['IOR'], fres_group.inputs['IOR'])
        links(group_in3.outputs['Normal'], fres_group.inputs['Normal'])
        links(group_in3.outputs['Metal/Dielectric'], m_greaterthan.inputs[0])

        # connect color mix 3
        links(m_greaterthan3.outputs['Value'], m_colormix4.inputs[0])
        links(m_hsv.outputs['Color'], m_colormix4.inputs[7])

        # connect group in 4
        links(group_in4.outputs['Custom/Auto'], m_greaterthan2.inputs[0])

        # connect group in 5
        links(group_in5.outputs['Reflectivity'], m_hsv.inputs['Color'])
        links(group_in5.outputs['Metal/Dielectric'], m_greaterthan3.inputs[0])
        
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
