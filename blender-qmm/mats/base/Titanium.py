import bpy

# MESSAGE BOX
message_text = "This material already exists"
def ShowMessageBox(message = "", title = "", icon = 'INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

#TitaniumShaderOperator
class QMMTitanium(bpy.types.Operator):
    """Add/Apply Titanium Material to Selected Object (or Scene)"""
    bl_label = "QMM Titanium Shader"
    bl_idname = 'shader.qmm_titanium_operator'
    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        m_titanium = bpy.data.materials.get("QMM Titanium")
        if m_titanium:
            ShowMessageBox(message_text, "QMM Titanium")
            # print(f"QMM Titanium already exists")
            bpy.context.object.active_material = m_titanium
            return {'FINISHED'}
        else:
            #CreateShader
            m_titanium = bpy.data.materials.new(name = "QMM Titanium")
            m_titanium.use_nodes = True
            m_titanium.diffuse_color = (0.242281, 0.238398, 0.219526, 1)
            m_titanium.metallic = 1
            m_titanium.roughness = 0.25

            nodes = m_titanium.node_tree.nodes

            #materialoutput
            material_output = nodes.get('Material Output')
            material_output.location = (0,0)

            #princibledbsdf
            BSDF = nodes.get('Principled BSDF')
            BSDF.location = (-300,0)
            BSDF.inputs[0].default_value = (0.242281, 0.238398, 0.219526, 1)
            BSDF.inputs[6].default_value = 1
            BSDF.inputs[9].default_value = 0.25
            # BSDF.inputs[16].default_value = 0.25

            #LOAD THE MATERIAL
            bpy.context.object.active_material = m_titanium

            #SpecularGroup
            bpy.ops.node.specular_group_operator()
            nodes = m_titanium.node_tree.nodes
            specular_group = nodes.new("ShaderNodeGroup")
            specular_group.node_tree = bpy.data.node_groups['Specular']
            specular_group.location = (-500, -300)
            specular_group.inputs[0].default_value = 0.25
            links = m_titanium.node_tree.links.new
            links(specular_group.outputs[0], BSDF.inputs[7])
            links(specular_group.outputs[1], BSDF.inputs[16])

        return {'FINISHED'}
