import bpy
import time 

bv = bpy.app.version

# MESSAGE BOX
message_text = "This material already exists"


def ShowMessageBox(message="", title="", icon='INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)

def make_node(nodes, shader, locX, locY):
    result = nodes.new(shader)
    result.location = (locX, locY)
    return result

# MithrylShaderOperator

class QMMMithryl(bpy.types.Operator):
    """Add/Apply Tinted Mithryl Material to Selected Object (or Scene)"""
    bl_label  = "QMM Mithryl Shader"
    bl_idname = 'shader.qmm_mithryl_operator'

    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        if m_mithryl := bpy.data.materials.get("QMM Mithryl"):
            #ShowMessageBox(message_text, "QMM Mithryl")
            # print(f"QMM Mithryl already exists")
            bpy.context.object.active_material = m_mithryl
            diffuse_bool = bpy.context.scene.diffuse_bool.diffuse_more
            m_mithryl.diffuse_color = (0.666667, 1, 1, 1) if diffuse_bool else (0.8, 0.8, 0.8, 1)
            m_mithryl.metallic = 1 if diffuse_bool else 0
            m_mithryl.roughness = 0.075 if diffuse_bool else 0.4
            return {'FINISHED'}
        else:
            self.make_shader()
        return {'FINISHED'}

    def make_shader(self):
        start = time.time()

        # CreateShader
        m_mithryl = bpy.data.materials.new(name="QMM Mithryl")
        m_mithryl.use_nodes = True
        diffuse_bool = bpy.context.scene.diffuse_bool.diffuse_more
        if diffuse_bool == True:
            m_mithryl.diffuse_color = (0.666667, 1, 1, 1)
            m_mithryl.metallic = 1
            m_mithryl.roughness = 0.075

        nodes = m_mithryl.node_tree.nodes

        # materialoutput
        material_output = nodes.get('Material Output')
        material_output.location = (0, 0)

        # principledbsdf
        BSDF = nodes.get('Principled BSDF')
        BSDF.distribution = 'MULTI_GGX'
        BSDF.location = (-300, 0)
        BSDF.inputs[0].default_value = (0.590619, 0.625682, 0.679542, 1)
        if bpy.app.version < (4, 0, 0):
            BSDF.inputs[6].default_value = 1                           #Metallic
            BSDF.inputs[9].default_value = 0.075                       #Roughness
            BSDF.inputs[16].default_value = 0.18                       #IOR
            BSDF.inputs[19].default_value = (0.332452, 1, 0.617207, 1) #Emission
        elif bpy.app.version < (4, 3, 0):
            BSDF.inputs[1].default_value = 1                           #Metallic
            BSDF.inputs[2].default_value = 0.075                       #Roughness
            BSDF.inputs[3].default_value = 0.18                        #IOR
            BSDF.inputs[26].default_value = (0.332452, 1, 0.617207, 1) #Emission
        else:
            BSDF.inputs[1].default_value = 1                           #Metallic
            BSDF.inputs[2].default_value = 0.075                       #Roughness
            BSDF.inputs[3].default_value = 0.18                        #IOR
            BSDF.inputs[27].default_value = (0.332452, 1, 0.617207, 1) #Emission
        # BSDF.select = True

        # mixshader
        m_mixshader = make_node(nodes, 'ShaderNodeMix', -500, 0)
        m_mixshader.data_type = 'RGBA'
        m_mixshader.blend_type = 'COLOR'
        m_mixshader.inputs[0].default_value = 0.6
        m_mixshader.inputs[7].default_value = (0.590619, 0.625682, 0.679542, 1)

        # maprange
        m_maprange = make_node(nodes, 'ShaderNodeMapRange', -500, -300)
        m_maprange.width = 140
        m_maprange.inputs[1].default_value = 0.866666
        m_maprange.inputs[4].default_value = 0.133333

        # colorramp
        m_colorramp = make_node(nodes, 'ShaderNodeValToRGB', -800, -100)
        m_colorramp.color_ramp.interpolation = 'B_SPLINE'
        # Ensure there are enough elements in the color ramp
        while len(m_colorramp.color_ramp.elements) < 5:
            m_colorramp.color_ramp.elements.new(0.0)
        m_colorramp.color_ramp.elements[0].color = (0.973445, 0.955973, 0.913099, 1)
        m_colorramp.color_ramp.elements[0].position = 0.12
        m_colorramp.color_ramp.elements[1].color = (0.16, 0.8, 0.43136, 1)
        m_colorramp.color_ramp.elements[1].position = 0.17
        m_colorramp.color_ramp.elements[2].color = (0.332452, 1, 0.617207, 1)
        m_colorramp.color_ramp.elements[2].position = 0.2
        m_colorramp.color_ramp.elements[3].color = (0.590619, 0.625682, 0.679542, 1)
        m_colorramp.color_ramp.elements[3].position = 0.22
        m_colorramp.color_ramp.elements[4].color = (0.973445, 0.955973, 0.913099, 1)
        m_colorramp.color_ramp.elements[4].position = 0.25

        # layerweight
        m_layerweight = make_node(nodes, 'ShaderNodeLayerWeight', -1000, -300)
        m_layerweight.inputs[0].default_value = 0.5

        # Uneven Roughness Group
        bpy.ops.node.uneven_roughness_group_operator()
        ur_group = nodes.new("ShaderNodeGroup")
        ur_group.name = "Uneven Roughness"
        ur_group.node_tree = bpy.data.node_groups['Uneven Roughness']
        ur_group.location = (-1000, 0)
        ur_group.width = 140
        ur_group.inputs[0].default_value = 0.075
        ur_group.inputs[1].default_value = 0.225
        ur_group.inputs[2].default_value = 2
        ur_group.inputs[3].default_value = 0.8

        links = m_mithryl.node_tree.links.new

        links(m_mixshader.outputs[2], BSDF.inputs[0])
        links(m_colorramp.outputs[0], m_mixshader.inputs[6])
        links(m_layerweight.outputs[0], m_colorramp.inputs[0])
        links(m_layerweight.outputs[1], m_maprange.inputs[0])
        if bpy.app.version < (4, 0, 0):
            links(m_maprange.outputs[0], BSDF.inputs[19])
            links(ur_group.outputs[0], BSDF.inputs[9])
        elif bpy.app.version < (4, 3, 0):
            links(m_maprange.outputs[0], BSDF.inputs[27])
            links(ur_group.outputs[0], BSDF.inputs[2])
        else:
            links(m_maprange.outputs[0], BSDF.inputs[28])
            links(ur_group.outputs[0], BSDF.inputs[2])

        bpy.context.object.active_material = m_mithryl

        end = time.time()
        print(f"QMM Mithryl: {end - start} seconds")
