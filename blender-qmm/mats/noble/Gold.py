import bpy
import time 

# MESSAGE BOX
message_text = "This material already exists"

def ShowMessageBox(message="", title="", icon='INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)

# GoldShaderOperator

class QMMGold(bpy.types.Operator):
    """Add/Apply Gold Material to Selected Object (or Scene)"""
    bl_label  = "QMM Gold Shader"
    bl_idname = 'shader.qmm_gold_m_operator'

    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        if m_gold_m := bpy.data.materials.get("QMM Gold"):
            ShowMessageBox(message_text, "QMM Gold")
            # print(f"QMM Gold already exists")
            bpy.context.object.active_material = m_gold_m
            return {'FINISHED'}
        else:
            self.make_shader()
        return {'FINISHED'}

    def make_shader(self):
        start = time.time()

        # CreateShader
        m_gold_m = bpy.data.materials.new(name="QMM Gold")
        m_gold_m.use_nodes = True
        m_gold_m.diffuse_color = (0.871367, 0.558340, 0.114436, 1)
        m_gold_m.metallic = 1
        m_gold_m.roughness = 0.075

        nodes = m_gold_m.node_tree.nodes

        # materialoutput
        material_output = nodes.get('Material Output')
        material_output.location = (0, 0)

        # principledbsdf
        BSDF = nodes.get('Principled BSDF')
        BSDF.distribution = 'MULTI_GGX'
        BSDF.location = (-300, 0)
        BSDF.inputs[0].default_value = (0.871367, 0.558340, 0.114436, 1)
        BSDF.inputs[6].default_value = 1
        BSDF.inputs[9].default_value = 0.075
        BSDF.inputs[16].default_value = 1.45

        links = m_gold_m.node_tree.links.new

        # EnergyConservationGroup
        bpy.ops.node.ec_group_operator()
        ec_group = self.make_node(nodes, "Energy Conservation v5", 'Energy Conservation v5')
        ec_group.inputs[0].default_value = (0.871367, 0.558340, 0.114436, 1)
        ec_group.inputs[1].default_value = 0.075
        ec_group.inputs[2].default_value = 1.45
        ec_group.inputs[4].default_value = (0.991101, 0.955973, 0.520996, 1)
        ec_group.location = (-500, -200)
        links(ec_group.outputs[0], BSDF.inputs[0])
        links(ec_group.outputs[1], BSDF.inputs[7])
        links(ec_group.outputs[2], BSDF.inputs[9])
        links(ec_group.outputs[4], BSDF.inputs[16])

        # GoldColorsGroup
        bpy.ops.node.gold_cg_operator()
        nodes = m_gold_m.node_tree.nodes
        gold_cg = self.make_node(nodes, "Gold Colors", 'Gold Colors')
        gold_cg.location = (-700, -300)
        links(gold_cg.outputs[1], ec_group.inputs[0])

        # LOAD THE MATERIAL
        bpy.context.object.active_material = m_gold_m

        end = time.time()
        print(f"QMM Gold: {end - start} seconds")

    def make_node(self, nodes, arg1, arg2):
        result = nodes.new("ShaderNodeGroup")
        result.name = arg1
        result.node_tree = bpy.data.node_groups[arg2]
        return result
