import bpy

# MESSAGE BOX
message_text = "This material already exists"
def ShowMessageBox(message = "", title = "", icon = 'INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

#BronzeShaderOperator
class QMMBronze(bpy.types.Operator):
    """Add/Apply Bronze Material to Selected Object (or Scene)"""
    bl_label = "QMM Bronze Shader"
    bl_idname = 'shader.qmm_bronze_operator'
    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        m_bronze = bpy.data.materials.get("QMM Bronze")
        if m_bronze:
            ShowMessageBox(message_text, "QMM Bronze")
            # print(f"QMM Bronze already exists")
            bpy.context.object.active_material = m_bronze
            return {'FINISHED'}
        else:
            #CreateShader
            m_bronze = bpy.data.materials.new(name = "QMM Bronze")
            m_bronze.use_nodes = True
            m_bronze.diffuse_color = (0.434154, 0.266356, 0.0953075, 1)
            m_bronze.metallic = 1
            m_bronze.roughness = 0.25

            nodes = m_bronze.node_tree.nodes

            #materialoutput
            material_output = nodes.get('Material Output')
            material_output.location = (0,0)

            #princibledbsdf
            BSDF = nodes.get('Principled BSDF')
            BSDF.location = (-300,0)
            BSDF.inputs[0].default_value = (0.434154, 0.266356, 0.0953075, 1)
            BSDF.inputs[6].default_value = 1
            BSDF.inputs[9].default_value = 0.25
            # BSDF.inputs[16].default_value = 1.180

            #LOAD THE MATERIAL
            bpy.context.object.active_material = m_bronze

            #SpecularGroup
            bpy.ops.node.specular_group_operator()
            nodes = m_bronze.node_tree.nodes
            specular_group = nodes.new("ShaderNodeGroup")
            specular_group.node_tree = bpy.data.node_groups['Specular']
            specular_group.location = (-500, -300)
            specular_group.inputs[0].default_value = 1.180
            links = m_bronze.node_tree.links.new
            links(specular_group.outputs[0], BSDF.inputs[7])
            links(specular_group.outputs[1], BSDF.inputs[16])

            return {'FINISHED'}
