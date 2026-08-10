import bpy
import time

# MESSAGE BOX
message_text = "This material already exists"


def ShowMessageBox(message="", title="", icon='INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)


def make_node(nodes, shader, locX, locY):
    result = nodes.new(shader)
    result.location = (locX, locY + 100)
    return result

# PlasterShaderOperator


class QMMPlaster(bpy.types.Operator):
    """Add/Apply Tinted Plaster Material to Selected Object (or Scene)"""
    bl_label = "QMM Plaster Shader"
    bl_idname = 'shader.qmm_plaster_operator'

    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        if m_plaster := bpy.data.materials.get("QMM Plaster"):
            # ShowMessageBox(message_text, "QMM Plaster")
            # print(f"QMM Plaster already exists")
            bpy.context.object.active_material = m_plaster
            diffuse_bool = bpy.context.scene.diffuse_bool.diffuse_more
            m_plaster.diffuse_color = (0.9, 0.7, 0.9, 1) if diffuse_bool else (0.8, 0.8, 0.8, 1)
            m_plaster.roughness = 0.86 if diffuse_bool else 0.4
            return {'FINISHED'}
        else:
            self.make_shader()
        return {'FINISHED'}

    def make_shader(self):
        start = time.time()

        # CreateShader
        m_plaster = bpy.data.materials.new(name="QMM Plaster")
        m_plaster.use_nodes = True
        diffuse_bool = bpy.context.scene.diffuse_bool.diffuse_more
        if diffuse_bool:
            m_plaster.diffuse_color = (0.9, 0.7, 0.9, 1)
            m_plaster.roughness = 0.86

        nodes = m_plaster.node_tree.nodes

        # materialoutput
        material_output = next((n for n in nodes if n.bl_idname == 'ShaderNodeOutputMaterial'), None)
        if material_output:
            material_output.location = (0, 0)

        # Principled BSDF
        BSDF = next((n for n in nodes if n.bl_idname == 'ShaderNodeBsdfPrincipled'), None)
        if BSDF:
            BSDF.distribution = 'MULTI_GGX'
            BSDF.location = (-300, 0)

            BSDF.inputs["Base Color"].default_value = (0.708857, 0.392564, 0.708857, 1)
            BSDF.inputs["Roughness"].default_value = 0.86
            BSDF.inputs["IOR"].default_value = 1.3
            BSDF.inputs["Subsurface Radius"].default_value = (0.708857, 0.392564, 0.708857)

        # Tint
        m_tint = make_node(nodes, 'ShaderNodeMix', -500, -100)
        m_tint.data_type = 'RGBA'
        m_tint.blend_type = 'COLOR'
        m_tint.inputs[0].default_value = 0.2
        m_tint.inputs[7].default_value = (0.708857, 0.392564, 0.708857, 1)

        # colorramp
        m_colorramp = make_node(nodes, 'ShaderNodeValToRGB', -800, -100)
        m_colorramp.color_ramp.elements[0].position = 0.2
        m_colorramp.color_ramp.elements[1].position = 0.775
        m_colorramp.color_ramp.elements[0].color = (0.5, 0.5, 0.5, 1)
        m_colorramp.color_ramp.elements[1].color = (0.4, 0.4, 0.4, 1)
        m_colorramp.width = 240

        # mix
        m_mix = make_node(nodes, 'ShaderNodeMix', -1000, -100)
        m_mix.data_type = 'RGBA'
        m_mix.blend_type = 'COLOR'
        m_mix.inputs[7].default_value = (0.708857, 0.392564, 0.708857, 1)

        # voronoi
        m_voronoi = make_node(nodes, 'ShaderNodeTexVoronoi', -1200, -100)
        m_voronoi.distance = 'MANHATTAN'
        m_voronoi.inputs["Scale"].default_value = 30.0

        # noise
        m_noise = make_node(nodes, 'ShaderNodeTexNoise', -1400, -400)
        m_noise.inputs["Scale"].default_value = 50.0
        m_noise.inputs["Detail"].default_value = 5.0

        # mapping
        m_mapping = make_node(nodes, 'ShaderNodeMapping', -1600, -400)
        m_mapping.width = 140

        # texture coordinates
        m_texcoords = make_node(nodes, 'ShaderNodeTexCoord', -1800, -400)

        # bump
        m_bump = make_node(nodes, 'ShaderNodeBump', -500, -400)
        m_bump.inputs["Strength"].default_value = 0.25

        # EnergyConservationGroup
        bpy.ops.node.ec_group_operator()
        ec_group = nodes.new("ShaderNodeGroup")
        ec_group.name = "Energy Conservation v5"
        ec_group.node_tree = bpy.data.node_groups['Energy Conservation v5']
        ec_group.location = (0, -200)
        ec_group.inputs[0].default_value = (0.708857, 0.392564, 0.708857, 1)
        ec_group.inputs[1].default_value = 0.86
        ec_group.inputs[2].default_value = 1.52
        ec_group.inputs[4].default_value = (0.01, 0.01, 0.01, 1)

        links = m_plaster.node_tree.links.new

        links(m_texcoords.outputs["Object"], m_mapping.inputs["Vector"])
        links(m_mapping.outputs["Vector"], m_noise.inputs["Vector"])
        links(m_noise.outputs["Fac"], m_voronoi.inputs["Vector"])
        links(m_noise.outputs["Fac"], m_bump.inputs["Height"])
        links(m_voronoi.outputs["Distance"], m_mix.inputs[6])
        links(m_noise.outputs["Fac"], m_mix.inputs[7])
        links(m_mix.outputs[2], m_colorramp.inputs["Fac"])
        links(m_colorramp.outputs["Color"], m_tint.inputs[6])
        links(m_tint.outputs[2], BSDF.inputs["Base Color"])
        links(m_bump.outputs["Normal"], BSDF.inputs["Normal"])

        bpy.context.object.active_material = m_plaster

        end = time.time()
        print(f"QMM Plaster: {end - start} seconds")
