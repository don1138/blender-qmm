import bpy


class OsmiumCrystallineSurfaceGroup(bpy.types.Operator):
    """Add/Get Osmium Crystalline Surface Group Node"""
    bl_label = "Osmium Crystalline Surface Node Group"
    bl_idname = 'node.osmium_crystalline_surface_group_operator'

    def execute(self, context):
        if not bpy.data.node_groups.get("Osmium Crystalline Surface"):
            self.make_group()
        return {'FINISHED'}

    @staticmethod
    def make_node(group, node_type, x_pos, y_pos):
        node = group.nodes.new(node_type)
        node.location = (x_pos, y_pos)
        return node

    def make_group(self):
        group = bpy.data.node_groups.new(
            "Osmium Crystalline Surface", 'ShaderNodeTree')

        crystal_scale = group.interface.new_socket(
            name="Crystal Scale", in_out='INPUT', socket_type='NodeSocketFloat')
        crystal_scale.default_value = 256.0
        crystal_scale.min_value = 0.0
        crystal_scale.max_value = 10000.0

        facet_strength = group.interface.new_socket(
            name="Facet Strength", in_out='INPUT', socket_type='NodeSocketFloat')
        facet_strength.default_value = 2.0
        facet_strength.min_value = 0.0
        facet_strength.max_value = 10.0

        growth_scale = group.interface.new_socket(
            name="Growth Scale", in_out='INPUT', socket_type='NodeSocketFloat')
        growth_scale.default_value = 8.0
        growth_scale.min_value = 0.0
        growth_scale.max_value = 1000.0

        growth_strength = group.interface.new_socket(
            name="Growth Strength", in_out='INPUT', socket_type='NodeSocketFloat')
        growth_strength.default_value = 0.4
        growth_strength.min_value = 0.0
        growth_strength.max_value = 1.0

        growth_distance = group.interface.new_socket(
            name="Growth Distance", in_out='INPUT', socket_type='NodeSocketFloat')
        growth_distance.default_value = 0.1
        growth_distance.min_value = 0.0
        growth_distance.max_value = 1.0

        group.interface.new_socket(
            name="Normal", in_out='OUTPUT', socket_type='NodeSocketVector')

        group_in = self.make_node(group, 'NodeGroupInput', -600, 0)
        group_in_vor = self.make_node(group, 'NodeGroupInput', -1400, -500)
        group_out = self.make_node(group, 'NodeGroupOutput', 0, 0)

        texture_coordinates = self.make_node(
            group, 'ShaderNodeTexCoord', -1400, -200)

        voronoi = self.make_node(
            group, 'ShaderNodeTexVoronoi', -1200, -200)
        voronoi.voronoi_dimensions = '3D'
        voronoi.feature = 'F1'
        voronoi.distance = 'EUCLIDEAN'
        voronoi.inputs['Detail'].default_value = 0.0
        voronoi.inputs['Roughness'].default_value = 0.5
        voronoi.inputs['Lacunarity'].default_value = 2.0
        voronoi.inputs['Randomness'].default_value = 1.0

        separate_color = self.make_node(
            group, 'ShaderNodeSeparateColor', -1000, -200)
        separate_color.mode = 'RGB'

        map_red = self.make_node(group, 'ShaderNodeMapRange', -800, 0)
        map_red.clamp = True
        map_red.inputs['From Min'].default_value = 0.0
        map_red.inputs['From Max'].default_value = 1.0
        map_red.inputs['To Min'].default_value = 0.1
        map_red.inputs['To Max'].default_value = 0.9

        map_green = self.make_node(group, 'ShaderNodeMapRange', -800, -300)
        map_green.clamp = True
        map_green.inputs['From Min'].default_value = 0.0
        map_green.inputs['From Max'].default_value = 1.0
        map_green.inputs['To Min'].default_value = 0.1
        map_green.inputs['To Max'].default_value = 0.9

        combine_color = self.make_node(
            group, 'ShaderNodeCombineColor', -600, -200)
        combine_color.mode = 'RGB'
        combine_color.inputs['Blue'].default_value = 1.0

        normal_map = self.make_node(
            group, 'ShaderNodeNormalMap', -400, -200)
        normal_map.label = "Glitter Normal Map"
        normal_map.space = 'TANGENT'

        noise = self.make_node(group, 'ShaderNodeTexNoise', -400, 100)
        noise.noise_dimensions = '3D'
        noise.inputs['Detail'].default_value = 2.0
        noise.inputs['Roughness'].default_value = 0.6
        noise.inputs['Lacunarity'].default_value = 2.0
        noise.inputs['Distortion'].default_value = 0.0
        if hasattr(noise, "normalize"):
            noise.normalize = True

        bump = self.make_node(group, 'ShaderNodeBump', -200, 0)
        bump.label = "Coarse Bump"
        bump.inputs['Filter Width'].default_value = 0.1

        links = group.links.new
        links(texture_coordinates.outputs['Object'], voronoi.inputs['Vector'])
        links(texture_coordinates.outputs['Object'], noise.inputs['Vector'])
        links(group_in_vor.outputs['Crystal Scale'], voronoi.inputs['Scale'])
        links(group_in.outputs['Facet Strength'], normal_map.inputs['Strength'])
        links(group_in.outputs['Growth Scale'], noise.inputs['Scale'])
        links(group_in.outputs['Growth Strength'], bump.inputs['Strength'])
        links(group_in.outputs['Growth Distance'], bump.inputs['Distance'])
        links(voronoi.outputs['Color'], separate_color.inputs['Color'])
        links(separate_color.outputs['Red'], map_red.inputs['Value'])
        links(separate_color.outputs['Green'], map_green.inputs['Value'])
        links(map_red.outputs['Result'], combine_color.inputs['Red'])
        links(map_green.outputs['Result'], combine_color.inputs['Green'])
        links(combine_color.outputs['Color'], normal_map.inputs['Color'])
        links(normal_map.outputs['Normal'], bump.inputs['Normal'])
        links(noise.outputs['Fac'], bump.inputs['Height'])
        links(bump.outputs['Normal'], group_out.inputs['Normal'])
