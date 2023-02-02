import bpy
import time 

# MESSAGE BOX
message_text = "This material already exists"


def ShowMessageBox(message="", title="", icon='INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)

# TinShaderOperator


class QMMTin(bpy.types.Operator):
    """Add/Apply Tin Material to Selected Object (or Scene)"""
    bl_label  = "QMM Tin Shader"
    bl_idname = 'shader.qmm_tin_operator'

    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        if m_tin := bpy.data.materials.get("QMM Tin"):
            ShowMessageBox(message_text, "QMM Tin")
            # print(f"QMM Tin already exists")
            bpy.context.object.active_material = m_tin
            return {'FINISHED'}
        else:
            self.make_shader()
        return {'FINISHED'}

    def make_shader(self):
        start = time.time()

        # CreateShader
        m_tin = bpy.data.materials.new(name="QMM Tin")
        m_tin.use_nodes = True
        m_tin.diffuse_color = (0.8, 0.8, 0.8, 1)
        m_tin.metallic = 1
        m_tin.roughness = 0.35

        nodes = m_tin.node_tree.nodes

        # materialoutput
        material_output = nodes.get('Material Output')
        material_output.location = (0, 0)

        # princibledbsdf
        BSDF = nodes.get('Principled BSDF')
        BSDF.distribution = 'MULTI_GGX'
        BSDF.location = (-300, 0)
        BSDF.inputs[0].default_value = (0.8, 0.8, 0.8, 1)
        BSDF.inputs[6].default_value = 1
        BSDF.inputs[9].default_value = 0.35
        BSDF.inputs[16].default_value = 2.9

        # EnergyConservationGroup
        bpy.ops.node.ec_group_operator()
        ec_group = nodes.new("ShaderNodeGroup")
        ec_group.name = "Energy Conservation v5"
        ec_group.node_tree = bpy.data.node_groups['Energy Conservation v5']
        ec_group.location = (-500, -200)
        ec_group.inputs[0].default_value = (0.8, 0.8, 0.8, 1)
        ec_group.inputs[1].default_value = 0.35
        ec_group.inputs[2].default_value = 2.9
        ec_group.inputs[4].default_value = (0.99, 0.99, 0.99, 1)

        # CanisotrophyGroup
        bpy.ops.node.canisotrophy_group_operator()
        canisotrophy_group = nodes.new("ShaderNodeGroup")
        canisotrophy_group.name = "Canisotrophy"
        canisotrophy_group.node_tree = bpy.data.node_groups['Canisotrophy']
        canisotrophy_group.location = (-800, -500)
        canisotrophy_group.width = 240

        # Bump
        bpy.ops.node.canisotrophy_group_operator()
        m_bump = nodes.new("ShaderNodeBump")
        m_bump.location = -500, -600
        m_bump.inputs[0].default_value = 0.02

        links = m_tin.node_tree.links.new

        links(ec_group.outputs[0], BSDF.inputs[0])
        links(ec_group.outputs[1], BSDF.inputs[7])
        links(ec_group.outputs[2], BSDF.inputs[9])
        links(ec_group.outputs[4], BSDF.inputs[16])
        links(canisotrophy_group.outputs[1], m_bump.inputs[2])

        # LOAD THE MATERIAL
        bpy.context.object.active_material = m_tin

        end = time.time()
        print(f"QMM Tin: {end - start} seconds")

    def make_node(self, nodes, arg1, arg2, arg3):
        result = nodes.new(arg1)
        result.location = -500, arg2
        result.inputs[0].default_value = arg3
        return result
