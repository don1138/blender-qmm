import bpy

# MESSAGE BOX
message_text = "This material already exists"
def ShowMessageBox(message = "", title = "", icon = 'INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

#BrassShaderOperator
class QMMBrass(bpy.types.Operator):
    """Add/Apply Brass Material to Selected Object (or Scene)"""
    bl_label = "QMM Brass Shader"
    bl_idname = 'shader.qmm_brass_operator'
    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        if m_brass := bpy.data.materials.get("QMM Brass"):
            ShowMessageBox(message_text, "QMM Brass")
            # print(f"QMM Brass already exists")
            bpy.context.object.active_material = m_brass
            return {'FINISHED'}
        else:
            self.make_shader()
        return {'FINISHED'}

    def make_shader(self):
        #CreateShader
        m_brass = bpy.data.materials.new(name = "QMM Brass")
        m_brass.use_nodes = True
        m_brass.diffuse_color = (0.760524, 0.584078, 0.158961, 1)
        m_brass.metallic = 1
        m_brass.roughness = 0.38

        nodes = m_brass.node_tree.nodes

        #materialoutput
        material_output = nodes.get('Material Output')
        material_output.location = (0,0)

        #princibledbsdf
        BSDF = nodes.get('Principled BSDF')
        BSDF.location = (-300,0)
        BSDF.inputs[0].default_value = (0.760524, 0.584078, 0.158961, 1)
        BSDF.inputs[6].default_value = 1
        BSDF.inputs[9].default_value = 0.38
        BSDF.inputs[16].default_value = 1.225

        #EnergyConservationGroup
        bpy.ops.node.ec_group_operator()
        ec_group = nodes.new("ShaderNodeGroup")
        ec_group.name = "Energy Conservation"
        ec_group.node_tree = bpy.data.node_groups['Energy Conservation']
        ec_group.location = (-500, -200)
        ec_group.inputs[0].default_value = 1.225
        ec_group.inputs[1].default_value = (0.760524, 0.584078, 0.158961, 1)
        ec_group.inputs[2].default_value = (0.973444, 0.947306, 0.679543, 1)

        links = m_brass.node_tree.links.new

        links(ec_group.outputs[0], BSDF.inputs[0])
        links(ec_group.outputs[1], BSDF.inputs[7])
        links(ec_group.outputs[3], BSDF.inputs[16])

        #LOAD THE MATERIAL
        bpy.context.object.active_material = m_brass
