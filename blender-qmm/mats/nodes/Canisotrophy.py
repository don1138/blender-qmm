import bpy

class CanisotrophyGroup(bpy.types.Operator):
    """Add/Get Canisotrophy Group Node"""
    bl_label  = "Canisotrophy Node Group"
    bl_idname = 'node.canisotrophy_group_operator'

    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        ng_canisotrophy = bpy.data.node_groups.get("Canisotrophy")

        if not ng_canisotrophy:
            self.make_group()
        return {'FINISHED'}

    def make_node(self, group, arg1, arg2, arg3):
        result = group.nodes.new(arg1)
        result.location = arg2, arg3
        return result

    def make_group(self):
        # newnodegroup
        canisotrophy_group = bpy.data.node_groups.new('Canisotrophy', 'ShaderNodeTree')

        # groupinputs
        group_in   = canisotrophy_group.nodes.new('NodeGroupInput')
        group_in_a = canisotrophy_group.nodes.new('NodeGroupInput')
        group_in_b = canisotrophy_group.nodes.new('NodeGroupInput')
        group_in.location   = (-1600, -300)
        group_in_a.location = (-800, 100)
        group_in_b.location = (-800, -300)

        master_scale = canisotrophy_group.interface.new_socket(name="Master Scale", in_out='INPUT', socket_type='NodeSocketFloat')
        master_scale.default_value = 1
        master_scale.min_value = 0
        master_scale.max_value = 10

        noise_scale = canisotrophy_group.interface.new_socket(name="Noise Scale", in_out='INPUT', socket_type='NodeSocketFloat')
        noise_scale.default_value = 16
        noise_scale.min_value = 0

        xy_scale = canisotrophy_group.interface.new_socket(name="XY Scale", in_out='INPUT', socket_type='NodeSocketFloat')
        xy_scale.default_value = 0.5
        xy_scale.min_value = 0

        z_scale = canisotrophy_group.interface.new_socket(name="Z Scale", in_out='INPUT', socket_type='NodeSocketFloat')
        z_scale.default_value = 24
        z_scale.min_value = 0

        xy_min = canisotrophy_group.interface.new_socket(name="XY Min Value", in_out='INPUT', socket_type='NodeSocketFloat')
        xy_min.default_value = 0.1
        xy_min.min_value = 0
        xy_min.max_value = 1

        xy_max = canisotrophy_group.interface.new_socket(name="XY Max Value", in_out='INPUT', socket_type='NodeSocketFloat')
        xy_max.default_value = 0.3
        xy_max.min_value = 0
        xy_max.max_value = 1

        z_min = canisotrophy_group.interface.new_socket(name="Z Min Value", in_out='INPUT', socket_type='NodeSocketFloat')
        z_min.default_value = 0.1
        z_min.min_value = 0
        z_min.max_value = 1

        z_max = canisotrophy_group.interface.new_socket(name="Z Max Value", in_out='INPUT', socket_type='NodeSocketFloat')
        z_max.default_value = 0.3
        z_max.min_value = 0
        z_max.max_value = 1

        # groupoutput
        group_out = self.make_node(canisotrophy_group, 'NodeGroupOutput', 0, 0)
        canisotrophy_group.interface.new_socket(name="( For Both Roughness & Bump )", in_out='OUTPUT', socket_type='NodeSocketFloat').hide_value = True
        canisotrophy_group.interface.new_socket(name="XYZ", in_out='OUTPUT', socket_type='NodeSocketFloat')
        canisotrophy_group.interface.new_socket(name="XY Only", in_out='OUTPUT', socket_type='NodeSocketFloat')

        # mixrbg
        m_mixrgb = self.make_node(canisotrophy_group, 'ShaderNodeMix', -200, 0)
        m_mixrgb.data_type = 'RGBA'

        # maprange
        m_maprange = self.make_node(canisotrophy_group, 'ShaderNodeMapRange', -400, 200)
        m_maprange.inputs[3].default_value = 0.1
        m_maprange.inputs[4].default_value = 0.3

        # noise
        m_noise = self.make_node(canisotrophy_group, 'ShaderNodeTexNoise', -600, 200)
        m_noise.inputs['Detail'].default_value = 16

        # mapping
        m_mapping = self.make_node(canisotrophy_group, 'ShaderNodeMapping', -1000, 200)
        m_mapping.width = 140

        # separatexyz
        m_separatexyz = self.make_node(canisotrophy_group, 'ShaderNodeSeparateXYZ', -600, -40)

        # texturecoordinates
        m_texcoords = self.make_node(canisotrophy_group, 'ShaderNodeTexCoord', -1600, 0)

        # maprange2
        m_maprange2 = self.make_node(canisotrophy_group, 'ShaderNodeMapRange', -400, -200)
        m_maprange2.inputs[3].default_value = 0.1
        m_maprange2.inputs[4].default_value = 0.3

        # noise2
        m_noise2 = self.make_node(canisotrophy_group, 'ShaderNodeTexNoise', -600, -200)
        m_noise2.inputs['Detail'].default_value = 16

        # mapping2
        m_mapping2 = self.make_node(canisotrophy_group, 'ShaderNodeMapping', -1000, -200)
        m_mapping2.width = 140

        # vectormath
        m_vectormath = self.make_node(canisotrophy_group, 'ShaderNodeVectorMath', -1200, -200)
        m_vectormath.operation = 'DISTANCE'

        # vectormath2
        m_vectormath2 = self.make_node(canisotrophy_group, 'ShaderNodeVectorMath', -1400, -100)
        m_vectormath2.operation = 'SCALE'

        # combinexyz
        m_combinexyz = self.make_node(canisotrophy_group, 'ShaderNodeCombineXYZ', -1400, -300)
        m_combinexyz.inputs['X'].default_value = 0.5
        m_combinexyz.inputs['Y'].default_value = 0.5
        m_combinexyz.inputs['Z'].default_value = 24

        links = canisotrophy_group.links.new

        links(group_in.outputs['Master Scale'], m_vectormath2.inputs['Scale'])
        links(group_in_a.outputs['Noise Scale'], m_noise.inputs['Scale'])
        links(group_in_b.outputs['Noise Scale'], m_noise2.inputs['Scale'])
        links(group_in.outputs['XY Scale'], m_combinexyz.inputs['X'])
        links(group_in.outputs['XY Scale'], m_combinexyz.inputs['Y'])
        links(group_in.outputs['Z Scale'], m_combinexyz.inputs['Z'])
        links(group_in_a.outputs['XY Min Value'], m_maprange.inputs[3])
        links(group_in_a.outputs['XY Max Value'], m_maprange.inputs[4])
        links(group_in_b.outputs['Z Min Value'], m_maprange2.inputs[3])
        links(group_in_b.outputs['Z Max Value'], m_maprange2.inputs[4])
        links(m_vectormath2.outputs['Vector'], m_mapping.inputs['Vector'])
        links(m_vectormath2.outputs['Vector'], m_vectormath.inputs[0])
        links(m_texcoords.outputs['Object'], m_vectormath2.inputs[0])
        links(m_texcoords.outputs['Normal'], m_separatexyz.inputs['Vector'])
        links(m_separatexyz.outputs['Z'], m_mixrgb.inputs[0])
        links(m_combinexyz.outputs['Vector'], m_mapping.inputs['Scale'])
        links(m_combinexyz.outputs['Vector'], m_mapping2.inputs['Scale'])
        links(m_vectormath.outputs['Value'], m_mapping2.inputs['Vector'])
        links(m_mapping.outputs['Vector'], m_noise.inputs['Vector'])
        links(m_mapping2.outputs['Vector'], m_noise2.inputs['Vector'])
        links(m_noise.outputs['Fac'], m_maprange.inputs['Value'])
        links(m_noise2.outputs['Fac'], m_maprange2.inputs['Value'])
        links(m_maprange.outputs['Result'], group_out.inputs['XY Only'])
        links(m_maprange.outputs['Result'], m_mixrgb.inputs[6])
        links(m_maprange2.outputs['Result'], m_mixrgb.inputs[7])
        links(m_mixrgb.outputs[2], group_out.inputs['XYZ'])
