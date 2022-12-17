import bpy


class CanisotrophyGroup(bpy.types.Operator):
    """Add/Get Canisotrophy Group Node"""
    bl_label = "Canisotrophy Node Group"
    bl_idname = 'node.canisotrophy_group_operator'

    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        ng_canisotrophy = bpy.data.node_groups.get("Canisotrophy")

        if not ng_canisotrophy:
            self.make_group()
        return {'FINISHED'}

    def make_group(self):
        # newnodegroup
        canisotrophy_group = bpy.data.node_groups.new(
            'Canisotrophy', 'ShaderNodeTree')

        # groupinputs
        group_in = canisotrophy_group.nodes.new('NodeGroupInput')
        group_in_a = canisotrophy_group.nodes.new('NodeGroupInput')
        group_in_b = canisotrophy_group.nodes.new('NodeGroupInput')
        group_in.location = (-1600, -300)
        group_in_a.location = (-800, 100)
        group_in_b.location = (-800, -300)

        canisotrophy_group.inputs.new('NodeSocketFloat', 'Master Scale')
        canisotrophy_group.inputs.new('NodeSocketFloat', 'Noise Scale')
        canisotrophy_group.inputs.new('NodeSocketFloat', 'XY Scale')
        canisotrophy_group.inputs.new('NodeSocketFloat', 'Z Scale')
        canisotrophy_group.inputs.new('NodeSocketFloat', 'XY Min Value')
        canisotrophy_group.inputs.new('NodeSocketFloat', 'XY Max Value')
        canisotrophy_group.inputs.new('NodeSocketFloat', 'Z Min Value')
        canisotrophy_group.inputs.new('NodeSocketFloat', 'Z Max Value')

        canisotrophy_group.inputs[0].default_value = 1
        canisotrophy_group.inputs[1].default_value = 16
        canisotrophy_group.inputs[2].default_value = 0.5
        canisotrophy_group.inputs[3].default_value = 24
        canisotrophy_group.inputs[4].default_value = 0.1
        canisotrophy_group.inputs[5].default_value = 0.3
        canisotrophy_group.inputs[6].default_value = 0.1
        canisotrophy_group.inputs[7].default_value = 0.3

        canisotrophy_group.inputs[0].min_value = 0
        canisotrophy_group.inputs[0].max_value = 10
        canisotrophy_group.inputs[1].min_value = 0
        canisotrophy_group.inputs[2].max_value = 0
        canisotrophy_group.inputs[3].min_value = 0
        canisotrophy_group.inputs[4].min_value = 0
        canisotrophy_group.inputs[4].max_value = 1
        canisotrophy_group.inputs[5].min_value = 0
        canisotrophy_group.inputs[5].max_value = 1
        canisotrophy_group.inputs[6].min_value = 0
        canisotrophy_group.inputs[6].max_value = 1
        canisotrophy_group.inputs[7].min_value = 0
        canisotrophy_group.inputs[7].max_value = 1

        # groupoutput
        group_out = self.make_node(canisotrophy_group, 'NodeGroupOutput', 0, 0)
        canisotrophy_group.outputs.new(
            'NodeSocketFloat', '- To Roughness & Bump -')
        canisotrophy_group.outputs[0].hide_value = True
        canisotrophy_group.outputs.new('NodeSocketFloat', 'XYZ')
        canisotrophy_group.outputs.new('NodeSocketFloat', 'XY Only')

        # mixrbg
        m_mixrgb = self.make_node(
            canisotrophy_group, 'ShaderNodeMixRGB', -200, 0)

        # maprange
        m_maprange = self.make_node(
            canisotrophy_group, 'ShaderNodeMapRange', -400, 200)
        m_maprange.inputs[3].default_value = 0.1
        m_maprange.inputs[4].default_value = 0.3

        # noise
        m_noise = self.make_node(
            canisotrophy_group, 'ShaderNodeTexNoise', -600, 200)
        m_noise.inputs[3].default_value = 16

        # voronoi
        # m_voronoi = canisotrophy_group.nodes.new('ShaderNodeTexVoronoi')
        # m_voronoi.location = (-600,200)
        # m_voronoi.inputs[2].default_value = 20

        # mapping
        m_mapping = self.make_node(
            canisotrophy_group, 'ShaderNodeMapping', -1000, 200)
        m_mapping.width = 140

        # separatexyz
        m_separatexyz = self.make_node(
            canisotrophy_group, 'ShaderNodeSeparateXYZ', -600, -40)

        # texturecoordinates
        m_texcoords = self.make_node(
            canisotrophy_group, 'ShaderNodeTexCoord', -1600, 0)

        # maprange2
        m_maprange2 = self.make_node(
            canisotrophy_group, 'ShaderNodeMapRange', -400, -200)
        m_maprange2.inputs[3].default_value = 0.1
        m_maprange2.inputs[4].default_value = 0.3

        # noise2
        m_noise2 = self.make_node(
            canisotrophy_group, 'ShaderNodeTexNoise', -600, -200)
        m_noise2.inputs[3].default_value = 16

        # mapping2
        m_mapping2 = self.make_node(
            canisotrophy_group, 'ShaderNodeMapping', -1000, -200)
        m_mapping2.width = 140

        # vectormath
        m_vectormath = self.make_node(
            canisotrophy_group, 'ShaderNodeVectorMath', -1200, -200)
        m_vectormath.operation = 'DISTANCE'

        # vectormath2
        m_vectormath2 = self.make_node(
            canisotrophy_group, 'ShaderNodeVectorMath', -1400, -100)
        m_vectormath2.operation = 'SCALE'

        # combinexyz
        m_combinexyz = self.make_node(
            canisotrophy_group, 'ShaderNodeCombineXYZ', -1400, -300)
        m_combinexyz.inputs[0].default_value = 0.5
        m_combinexyz.inputs[1].default_value = 0.5
        m_combinexyz.inputs[2].default_value = 24

        links = canisotrophy_group.links.new

        links(group_in.outputs[0], m_vectormath2.inputs[3])
        links(group_in_a.outputs[1], m_noise.inputs[2])
        links(group_in_b.outputs[1], m_noise2.inputs[2])
        links(group_in.outputs[2], m_combinexyz.inputs[0])
        links(group_in.outputs[2], m_combinexyz.inputs[1])
        links(group_in.outputs[3], m_combinexyz.inputs[2])
        links(group_in_a.outputs[4], m_maprange.inputs[3])
        links(group_in_a.outputs[5], m_maprange.inputs[4])
        links(group_in_b.outputs[6], m_maprange2.inputs[3])
        links(group_in_b.outputs[7], m_maprange2.inputs[4])
        links(m_vectormath2.outputs[0], m_mapping.inputs[0])
        links(m_vectormath2.outputs[0], m_vectormath.inputs[0])
        links(m_texcoords.outputs[3], m_vectormath2.inputs[0])
        links(m_texcoords.outputs[1], m_separatexyz.inputs[0])
        links(m_combinexyz.outputs[0], m_mapping.inputs[3])
        links(m_combinexyz.outputs[0], m_mapping2.inputs[3])
        links(m_separatexyz.outputs[2], m_mixrgb.inputs[0])
        links(m_vectormath.outputs[1], m_mapping2.inputs[0])
        links(m_mapping.outputs[0], m_noise.inputs[0])
        links(m_mapping2.outputs[0], m_noise2.inputs[0])
        links(m_noise.outputs[0], m_maprange.inputs[0])
        links(m_noise2.outputs[0], m_maprange2.inputs[0])
        links(m_maprange.outputs[0], m_mixrgb.inputs[1])
        links(m_maprange2.outputs[0], m_mixrgb.inputs[2])
        links(m_mixrgb.outputs[0], group_out.inputs[1])
        links(m_maprange.outputs[0], group_out.inputs[2])

    def make_node(self, group, arg1, arg2, arg3):
        result = group.nodes.new(arg1)
        result.location = arg2, arg3
        return result
