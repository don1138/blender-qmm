import bpy

# MESSAGE BOX
message_text = "This material already exists"
def ShowMessageBox(message = "", title = "", icon = 'INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

#IronShaderOperator
class QMMIron(bpy.types.Operator):
    """Add/Apply Iron Material to Selected Object (or Scene)"""
    bl_label = "QMM Iron Shader"
    bl_idname = 'shader.qmm_iron_operator'
    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        if m_iron := bpy.data.materials.get("QMM Iron"):
            ShowMessageBox(message_text, "QMM Iron")
            # print(f"QMM Iron already exists")
            bpy.context.object.active_material = m_iron
            return {'FINISHED'}
        else:
            self.make_shader()
        return {'FINISHED'}

    # TODO Rename this here and in `execute`
    def make_shader(self):
        #CreateShader
        m_iron = bpy.data.materials.new(name = "QMM Iron")
        m_iron.use_nodes = True
        m_iron.diffuse_color = (0.531, 0.512, 0.496, 1)
        m_iron.metallic = 1
        m_iron.roughness = 0.3

        nodes = m_iron.node_tree.nodes

        #materialoutput
        material_output = nodes.get('Material Output')
        material_output.location = (0,0)

        #principledbsdf
        BSDF = nodes.get('Principled BSDF')
        BSDF.location = (-300,0)
        BSDF.inputs[0].default_value = (0.531, 0.512, 0.496, 1)
        BSDF.inputs[6].default_value = 1
        BSDF.inputs[9].default_value = 0.3
        BSDF.inputs[16].default_value = 2.950

        #EnergyConservationGroup
        bpy.ops.node.ec_group_operator()
        ec_group = nodes.new("ShaderNodeGroup")
        ec_group.name = "Energy Conservation"
        ec_group.node_tree = bpy.data.node_groups['Energy Conservation']
        ec_group.location = (-500, -200)
        ec_group.inputs[0].default_value = 2.95
        ec_group.inputs[1].default_value = (0.531, 0.512, 0.496, 1)
        ec_group.inputs[2].default_value = (0.571, 0.540, 0.586, 1)

        links = m_iron.node_tree.links.new

        links(ec_group.outputs[0], BSDF.inputs[0])
        links(ec_group.outputs[1], BSDF.inputs[7])
        links(ec_group.outputs[3], BSDF.inputs[16])

        #LOAD THE MATERIAL
        bpy.context.object.active_material = m_iron
