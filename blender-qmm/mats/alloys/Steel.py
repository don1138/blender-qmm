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
        m_steel = bpy.data.materials.get("QMM Steel")
        if m_steel:
            ShowMessageBox(message_text, "QMM Steel")
            # print(f"QMM Steel already exists")
            bpy.context.object.active_material = m_steel
            return {'FINISHED'}
        else:
            #CreateShader
            m_steel = bpy.data.materials.new(name = "QMM Steel")
            m_steel.use_nodes = True
            m_steel.diffuse_color = (0.42869, 0.527115, 0.590619, 1)
            m_steel.metallic = 1
            m_steel.roughness = 0.25

            nodes = m_steel.node_tree.nodes

            #materialoutput
            material_output = nodes.get('Material Output')
            material_output.location = (0,0)

            #princibledbsdf
            BSDF = nodes.get('Principled BSDF')
            BSDF.location = (-300,0)
            BSDF.inputs[0].default_value = (0.42869, 0.527115, 0.590619, 1)
            BSDF.inputs[6].default_value = 1
            BSDF.inputs[9].default_value = 0.25
            # BSDF.inputs[16].default_value = 2.5

            #LOAD THE MATERIAL
            bpy.context.object.active_material = m_steel

            #SpecularGroup
            bpy.ops.node.specular_group_operator()
            nodes = m_steel.node_tree.nodes
            specular_group = nodes.new("ShaderNodeGroup")
            specular_group.node_tree = bpy.data.node_groups['Specular']
            specular_group.location = (-500, -300)
            specular_group.inputs[0].default_value = 2.5
            links = m_steel.node_tree.links.new
            links(specular_group.outputs[0], BSDF.inputs[7])
            links(specular_group.outputs[1], BSDF.inputs[16])

            return {'FINISHED'}
