import bpy

# MESSAGE BOX
message_text = "This material already exists"
def ShowMessageBox(message = "", title = "", icon = 'INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

#SilverMaxShaderOperator
class QMMPaleSilverMax(bpy.types.Operator):
    """Add/Apply Pale Silver Material to Selected Object (or Scene)"""
    bl_label = "QMM Pale Silver Shader"
    bl_idname = 'shader.qmm_pale_silver_m_operator'
    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        m_pale_silver_m = bpy.data.materials.get("QMM Pale Silver")
        if m_pale_silver_m:
            ShowMessageBox(message_text, "QMM Pale Silver")
            # print(f"QMM Pale Silver already exists")
            bpy.context.object.active_material = m_pale_silver_m
            return {'FINISHED'}
        else:
            #CreateShader
            m_pale_silver_m = bpy.data.materials.new(name = "QMM Pale Silver")
            m_pale_silver_m.use_nodes = True
            m_pale_silver_m.diffuse_color = (0.972, 0.96, 0.915, 1)
            m_pale_silver_m.metallic = 1
            m_pale_silver_m.roughness = 0.25

            nodes = m_pale_silver_m.node_tree.nodes

            #materialoutput
            material_output = nodes.get('Material Output')
            material_output.location = (0,0)

            #princibledbsdf
            BSDF = nodes.get('Principled BSDF')
            BSDF.location = (-300,0)
            BSDF.inputs[0].default_value = (0.972, 0.96, 0.915, 1)
            BSDF.inputs[6].default_value = 1
            BSDF.inputs[9].default_value = 0.25
            # BSDF.inputs[16].default_value = 0.585

            #LOAD THE MATERIAL
            bpy.context.object.active_material = m_pale_silver_m

            #SpecularGroup
            bpy.ops.node.specular_group_operator()
            nodes = m_pale_silver_m.node_tree.nodes
            specular_group = nodes.new("ShaderNodeGroup")
            specular_group.node_tree = bpy.data.node_groups['Specular']
            specular_group.location = (-500, -300)
            specular_group.inputs[0].default_value = 0.585
            links = m_pale_silver_m.node_tree.links.new
            links(specular_group.outputs[0], BSDF.inputs[7])
            links(specular_group.outputs[1], BSDF.inputs[16])

            return {'FINISHED'}
