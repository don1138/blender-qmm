import bpy

# MESSAGE BOX
message_text = "This material already exists"
def ShowMessageBox(message = "", title = "", icon = 'INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

#PlatinumShaderOperator
class QMMPlatinum(bpy.types.Operator):
    """Add/Apply Platinum Material to Selected Object (or Scene)"""
    bl_label = "QMM Platinum Shader"
    bl_idname = 'shader.qmm_platinum_m_operator'
    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        m_platinum_m = bpy.data.materials.get("QMM Platinum")
        if m_platinum_m:
            ShowMessageBox(message_text, "QMM Platinum")
            # print(f"QMM Platinum already exists")
            bpy.context.object.active_material = m_platinum_m
            return {'FINISHED'}
        else:
            #CreateShader
            m_platinum_m = bpy.data.materials.new(name = "QMM Platinum")
            m_platinum_m.use_nodes = True
            m_platinum_m.diffuse_color = (0.665387, 0.630757, 0.577580, 1)
            m_platinum_m.metallic = 1
            m_platinum_m.roughness = 0.2

            nodes = m_platinum_m.node_tree.nodes

            #materialoutput
            material_output = nodes.get('Material Output')
            material_output.location = (0,0)

            #princibledbsdf
            BSDF = nodes.get('Principled BSDF')
            BSDF.location = (-300,0)
            BSDF.inputs[0].default_value = (0.665387, 0.630757, 0.577580, 1)
            BSDF.inputs[6].default_value = 1
            BSDF.inputs[9].default_value = 0.2
            # BSDF.inputs[16].default_value = 2.084700

            #SpecularGroup
            bpy.ops.node.specular_group_operator()
            nodes = m_platinum_m.node_tree.nodes
            specular_group = nodes.new("ShaderNodeGroup")
            specular_group.node_tree = bpy.data.node_groups['Specular']
            specular_group.location = (-500, -300)
            specular_group.inputs[0].default_value = 2.084700
            links = m_platinum_m.node_tree.links.new
            links(specular_group.outputs[0], BSDF.inputs[7])
            links(specular_group.outputs[1], BSDF.inputs[16])

            #LOAD THE MATERIAL
            bpy.context.object.active_material = m_platinum_m

        return {'FINISHED'}