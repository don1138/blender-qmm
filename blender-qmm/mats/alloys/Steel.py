import bpy

# MESSAGE BOX
message_text = "This material already exists"
def ShowMessageBox(message = "", title = "", icon = 'INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

#SteelShaderOperator
class QMMSteel(bpy.types.Operator):
    """Add/Apply Steel Material to Selected Object (or Scene)"""
    bl_label = "QMM Steel Shader"
    bl_idname = 'shader.qmm_steel_operator'
    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        if m_steel := bpy.data.materials.get("QMM Steel"):
            ShowMessageBox(message_text, "QMM Steel")
            # print(f"QMM Steel already exists")
            bpy.context.object.active_material = m_steel
            return {'FINISHED'}
        else:
            self.make_shader()
        return {'FINISHED'}

    # TODO Rename this here and in `execute`
    def make_shader(self):
        #CreateShader
        m_steel = bpy.data.materials.new(name = "QMM Steel")
        m_steel.use_nodes = True
        m_steel.diffuse_color = (0.42869, 0.527115, 0.590619, 1)
        m_steel.metallic = 1
        m_steel.roughness = 0.3

        nodes = m_steel.node_tree.nodes

        #materialoutput
        material_output = nodes.get('Material Output')
        material_output.location = (0,0)

        #princibledbsdf
        BSDF = nodes.get('Principled BSDF')
        BSDF.location = (-300,0)
        BSDF.inputs[0].default_value = (0.42869, 0.527115, 0.590619, 1)
        BSDF.inputs[6].default_value = 1
        BSDF.inputs[9].default_value = 0.3
        BSDF.inputs[16].default_value = 2.5

        #EnergyConservationGroup
        bpy.ops.node.ec_group_operator()
        ec_group = nodes.new("ShaderNodeGroup")
        ec_group.name = "Energy Conservation"
        ec_group.node_tree = bpy.data.node_groups['Energy Conservation']
        ec_group.location = (-500, -200)
        ec_group.inputs[0].default_value = 2.5
        ec_group.inputs[1].default_value = (0.42869, 0.527115, 0.590619, 1)
        ec_group.inputs[2].default_value = (0.99, 0.99, 0.99, 1)

        links = m_steel.node_tree.links.new

        links(ec_group.outputs[0], BSDF.inputs[0])
        links(ec_group.outputs[1], BSDF.inputs[7])
        links(ec_group.outputs[3], BSDF.inputs[16])

        #LOAD THE MATERIAL
        bpy.context.object.active_material = m_steel
