import bpy
import time 

# MESSAGE BOX
message_text = "This material already exists"

def ShowMessageBox(message="", title="", icon='INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)

# CopperShaderOperator

class QMMCopper(bpy.types.Operator):
    """Add/Apply Pale Copper (Minimum) Material to Selected Object (or Scene)"""
    bl_label  = "QMM Copper Shader"
    bl_idname = 'shader.qmm_copper_m_operator'

    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        if m_copper_m := bpy.data.materials.get("QMM Copper"):
            ShowMessageBox(message_text, "QMM Copper")
            # print(f"QMM Copper already exists")
            bpy.context.object.active_material = m_copper_m
            return {'FINISHED'}
        else:
            self.make_shader()
        return {'FINISHED'}

    def make_group(self, nodes, arg1, arg2, arg3):
        result = nodes.new("ShaderNodeGroup")
        result.node_tree = bpy.data.node_groups[arg1]
        result.location = arg2, arg3
        return result

    def make_shader(self):
        start = time.time()

        # CreateShader
        m_copper_m = bpy.data.materials.new(name="QMM Copper")
        m_copper_m.use_nodes = True
        m_copper_m.diffuse_color = (0.838799, 0.473531, 0.215861, 1)
        m_copper_m.metallic = 1
        m_copper_m.roughness = 0.35

        nodes = m_copper_m.node_tree.nodes

        # materialoutput
        material_output = nodes.get('Material Output')
        material_output.location = (0, 0)

        # princibledbsdf
        BSDF = nodes.get('Principled BSDF')
        BSDF.distribution = 'MULTI_GGX'
        BSDF.location = (-300, 0)
        BSDF.inputs[0].default_value = (0.838799, 0.473531, 0.215861, 1)
        BSDF.inputs[6].default_value = 1
        BSDF.inputs[9].default_value = 0.35
        # BSDF.inputs[16].default_value = 1.43

        # EnergyConservationGroup
        bpy.ops.node.ec_group_operator()
        ec_group = self.make_group(nodes, 'Energy Conservation v5', -500, -200)
        ec_group.inputs[0].default_value = (0.838799, 0.473531, 0.215861, 1)
        ec_group.inputs[1].default_value = 0.35
        # ec_group.inputs[2].default_value = 1.43
        ec_group.inputs[4].default_value = (0.982250, 0.904660, 0.637597, 1)
        ec_group.name = "Energy Conservation v5"

        # CopperColorsGroup
        bpy.ops.node.copper_cg_operator()
        copper_cg = self.make_group(nodes, 'Copper Colors', -700, -300)
        copper_cg.name = "Copper Colors"

        links = m_copper_m.node_tree.links.new
        links(copper_cg.outputs[1], ec_group.inputs[0])
        links(ec_group.outputs[0], BSDF.inputs[0])
        links(ec_group.outputs[1], BSDF.inputs[7])
        links(ec_group.outputs[2], BSDF.inputs[9])
        links(ec_group.outputs[4], BSDF.inputs[16])

        # LOAD THE MATERIAL
        bpy.context.object.active_material = m_copper_m

        end = time.time()
        print(f"QMM Copper: {end - start} seconds")
