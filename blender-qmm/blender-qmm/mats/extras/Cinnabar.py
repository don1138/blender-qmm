import bpy
import time

bv = bpy.app.version

# MESSAGE BOX
message_text = "This material already exists"


def ShowMessageBox(message="", title="", icon='INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)

# CinnabarShaderOperator

class QMMCinnabar(bpy.types.Operator):
    """Add/Apply Cinnabar Lacquer Material to Selected Object (or Scene)"""
    bl_label  = "QMM Cinnabar Lacquer Shader"
    bl_idname = 'shader.qmm_cinnabar_operator'

    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        if m_cinnabar := bpy.data.materials.get("QMM Cinnabar Lacquer"):
            #ShowMessageBox(message_text, "QMM Cinnabar Lacquer")
            # print(f"QMM Cinnabar already exists")
            bpy.context.object.active_material = m_cinnabar
            diffuse_bool = bpy.context.scene.diffuse_bool.diffuse_more
            m_cinnabar.diffuse_color = (0.768151, 0.054480, 0.034340, 1) if diffuse_bool else (0.8, 0.8, 0.8, 1)
            m_cinnabar.roughness = 0.5 if diffuse_bool else 0.4
            return {'FINISHED'}
        else:
            self.make_shader()
        return {'FINISHED'}

    def make_shader(self):
        start = time.time()

        # CreateShader
        m_cinnabar = bpy.data.materials.new(name="QMM Cinnabar Lacquer")
        m_cinnabar.use_nodes = True
        diffuse_bool = bpy.context.scene.diffuse_bool.diffuse_more
        if diffuse_bool == True:
            m_cinnabar.diffuse_color = (0.768151, 0.054480, 0.034340, 1)
            m_cinnabar.roughness = 0.5

        nodes = m_cinnabar.node_tree.nodes

        # materialoutput
        material_output = nodes.get('Material Output')
        material_output.location = (0, 0)

        # princibledbsdf
        BSDF = nodes.get('Principled BSDF')
        BSDF.distribution = 'MULTI_GGX'
        BSDF.location = (-300, 0)
        BSDF.inputs[0].default_value = (0.768151, 0.054480, 0.034340, 1)      # Base Color
        if bv < (4, 0, 0):
            BSDF.inputs[1].default_value =  0.2                               # Subsurface
            BSDF.inputs[2].default_value = (0.651516, 0.028425, 0.028424)     # Subsurface Radius
            BSDF.inputs[3].default_value = (0.010000, 0.000709, 0.000447, 1)  # Subsurface Color
            BSDF.inputs[9].default_value =  0.5                               # Roughness
            BSDF.inputs[12].default_value =  0.2                              # Sheen
            BSDF.inputs[14].default_value = 1.2                               # Clearcoat
            BSDF.inputs[15].default_value = 0.075                             # Clearcoat Roughness
            BSDF.inputs[16].default_value = 3.02                              # IOR
        elif bv < (4, 3, 0):
            BSDF.inputs[2].default_value =  0.5                               # Roughness
            BSDF.inputs[3].default_value =  3.02                              # IOR
            BSDF.inputs[7].default_value =  0.2                               # Subsurface Weight
            BSDF.inputs[8].default_value = (0.651516, 0.028425, 0.028424)     # Subsurface Radius
            BSDF.inputs[13].default_value = (0.010000, 0.000709, 0.000447, 1) # Specular Tint
            BSDF.inputs[18].default_value = 0.2                               # Coat Weight
            BSDF.inputs[19].default_value = 0.075                             # Coat Roughness
            BSDF.inputs[20].default_value = 3.2                               # Coat IOR
            BSDF.inputs[21].default_value = (0.010000, 0.000709, 0.000447, 1) # Coat Tint
            BSDF.inputs[23].default_value = 0.2                               # Sheen Weight
            BSDF.inputs[24].default_value = 0.2                               # Sheen Roughness
            BSDF.inputs[25].default_value = (0.010000, 0.000709, 0.000447, 1) # Sheen Tint
        else:
            BSDF.inputs[2].default_value =  0.5                               # Roughness
            BSDF.inputs[3].default_value =  3.02                              # IOR
            BSDF.inputs[8].default_value =  0.2                               # Subsurface Weight
            BSDF.inputs[9].default_value = (0.651516, 0.028425, 0.028424)     # Subsurface Radius
            BSDF.inputs[14].default_value = (0.010000, 0.000709, 0.000447, 1) # Specular Tint
            BSDF.inputs[19].default_value = 0.2                               # Coat Weight
            BSDF.inputs[20].default_value = 0.075                             # Coat Roughness
            BSDF.inputs[21].default_value = 3.2                               # Coat IOR
            BSDF.inputs[22].default_value = (0.010000, 0.000709, 0.000447, 1) # Coat Tint
            BSDF.inputs[24].default_value = 0.2                               # Sheen Weight
            BSDF.inputs[25].default_value = 0.2                               # Sheen Roughness
            BSDF.inputs[26].default_value = (0.010000, 0.000709, 0.000447, 1) # Sheen Tint

        # colorramp
        m_colorramp = nodes.new('ShaderNodeValToRGB')
        m_colorramp.label = "Cinnabar"
        m_colorramp.location = (-600, 0)
        m_colorramp.color_ramp.interpolation = 'B_SPLINE'
        # Ensure there are enough elements in the color ramp
        while len(m_colorramp.color_ramp.elements) < 4:
            m_colorramp.color_ramp.elements.new(0.0)
        m_colorramp.color_ramp.elements[0].color = (0.768151, 0.054480, 0.034340, 1)
        m_colorramp.color_ramp.elements[1].color = (0.291820, 0.019381, 0.012982, 1)
        m_colorramp.color_ramp.elements[2].color = (0.291820, 0.019381, 0.012982, 1)
        m_colorramp.color_ramp.elements[3].color = (0.768151, 0.054480, 0.034340, 1)
        m_colorramp.color_ramp.elements[0].position = 0
        m_colorramp.color_ramp.elements[1].position = 0.2
        m_colorramp.color_ramp.elements[2].position = 0.8
        m_colorramp.color_ramp.elements[3].position = 1

        # Layer Weight
        m_layerweight = nodes.new('ShaderNodeLayerWeight')
        m_layerweight.location = (-800, -100)
        m_layerweight.inputs[0].default_value = 0.3

        nodes = m_cinnabar.node_tree.nodes

        # UnevenRoughnessGroup
        bpy.ops.node.uneven_roughness_group_operator()
        uneven_roughness_group = nodes.new("ShaderNodeGroup")
        uneven_roughness_group.node_tree = bpy.data.node_groups['Uneven Roughness']
        uneven_roughness_group.location = (-500, -300)
        uneven_roughness_group.width = 140
        uneven_roughness_group.inputs[0].default_value = 0.075
        uneven_roughness_group.inputs[1].default_value = 0.375
        uneven_roughness_group.inputs[2].default_value = 1

        # LINKS
        links = m_cinnabar.node_tree.links.new

        links(m_colorramp.outputs[0], BSDF.inputs[0])
        links(m_layerweight.outputs[0], m_colorramp.inputs[0])
        if bpy.app.version < (4, 0, 0):
            links(uneven_roughness_group.outputs[0], BSDF.inputs[15])
        else:
            links(uneven_roughness_group.outputs[0], BSDF.inputs[19])

        # LOAD THE MATERIAL
        bpy.context.object.active_material = m_cinnabar

        end = time.time()
        print(f"QMM Cinnabar Lacquer: {end - start} seconds")
