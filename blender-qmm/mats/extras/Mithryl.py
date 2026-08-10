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
        if diffuse_bool:
            m_mithryl.diffuse_color = (0.666667, 1, 1, 1)
            m_mithryl.metallic = 1
            m_mithryl.roughness = 0.075

        nodes = m_mithryl.node_tree.nodes

        # materialoutput
        material_output = next((n for n in nodes if n.bl_idname == 'ShaderNodeOutputMaterial'), None)
        if material_output:
            material_output.location = (0, 0)

        # principledbsdf
        BSDF = next((n for n in nodes if n.bl_idname == 'ShaderNodeBsdfPrincipled'), None)
        if BSDF:
            BSDF.distribution = 'MULTI_GGX'
            BSDF.location = (-300, 0)
            BSDF.inputs["Base Color"].default_value = (0.590619, 0.625682, 0.679542, 1)
            BSDF.inputs["Metallic"].default_value = 1
            BSDF.inputs["Roughness"].default_value = 0.075
            BSDF.inputs["IOR"].default_value = 0.18
            BSDF.inputs["Emission Color"].default_value = (0.332452, 1, 0.617207, 1)
            # BSDF.select = True

        # mix
        m_mixshader = make_node(nodes, 'ShaderNodeMix', -500, 0)
        m_mixshader.data_type = 'RGBA'
        m_mixshader.blend_type = 'COLOR'
        m_mixshader.inputs[0].default_value = 0.6
        m_mixshader.inputs[7].default_value = (0.590619, 0.625682, 0.679542, 1)

        # map range
        m_maprange = make_node(nodes, 'ShaderNodeMapRange', -500, -300)
        m_maprange.width = 140
        m_maprange.inputs[1].default_value = 0.866666
        m_maprange.inputs[4].default_value = 0.133333

        # color ramp
        m_colorramp = make_node(nodes, 'ShaderNodeValToRGB', -800, -100)
        m_colorramp.color_ramp.interpolation = 'B_SPLINE'

        ramp = m_colorramp.color_ramp
        color_0 = ramp.elements[0]
        color_4 = ramp.elements[1]
        color_1 = ramp.elements.new(0.17)
        color_2 = ramp.elements.new(0.20)
        color_3 = ramp.elements.new(0.22)

        color_0.position = 0.12
        color_0.color = (0.973445, 0.955973, 0.913099, 1)

        color_1.color = (0.16, 0.8, 0.43136, 1)
        color_2.color = (0.332452, 1, 0.617207, 1)
        color_3.color = (0.590619, 0.625682, 0.679542, 1)

        color_4.position = 0.25
        color_4.color = (0.973445, 0.955973, 0.913099, 1)

        # layerweight
        m_layerweight = make_node(nodes, 'ShaderNodeLayerWeight', -1000, -300)
        m_layerweight.inputs["Blend"].default_value = 0.5

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

        links(m_mixshader.outputs[2], BSDF.inputs["Base Color"])
        links(m_colorramp.outputs["Color"], m_mixshader.inputs[6])
        links(m_layerweight.outputs["Fresnel"], m_colorramp.inputs["Fac"])
        links(m_layerweight.outputs["Facing"], m_maprange.inputs["Value"])
        links(m_maprange.outputs["Result"], BSDF.inputs["Emission Strength"])
        links(ur_group.outputs[0], BSDF.inputs["Roughness"])

        bpy.context.object.active_material = m_mithryl

        end = time.time()
        print(f"QMM Mithryl: {end - start} seconds")
