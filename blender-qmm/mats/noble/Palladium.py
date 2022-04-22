import bpy

# MESSAGE BOX
message_text = "This material already exists"
def ShowMessageBox(message = "", title = "", icon = 'INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

#PalladiumShaderOperator
class QMMPalladium(bpy.types.Operator):
    """Add/Apply Palladium Material to Selected Object (or Scene)"""
    bl_label = "QMM Palladium Shader"
    bl_idname = 'shader.qmm_palladium_m_operator'
    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        m_palladium_m = bpy.data.materials.get("QMM Palladium")
        if m_palladium_m:
            ShowMessageBox(message_text, "QMM Palladium")
            # print(f"QMM Palladium already exists")
            bpy.context.object.active_material = m_palladium_m
            return {'FINISHED'}
        else:
            #CreateShader
            m_palladium_m = bpy.data.materials.new(name = "QMM Palladium")
            m_palladium_m.use_nodes = True
            m_palladium_m.diffuse_color = (0.783537, 0.775822, 0.760524, 1)
            m_palladium_m.metallic = 1
            m_palladium_m.roughness = 0.2

            nodes = m_palladium_m.node_tree.nodes

            #materialoutput
            material_output = nodes.get('Material Output')
            material_output.location = (0,0)

            #princibledbsdf
            BSDF = nodes.get('Principled BSDF')
            BSDF.location = (-300,0)
            BSDF.inputs[0].default_value = (0.783537, 0.775822, 0.760524, 1)
            BSDF.inputs[6].default_value = 1
            BSDF.inputs[9].default_value = 0.2
            # BSDF.inputs[16].default_value = 1.6381

            #SpecularGroup
            bpy.ops.node.specular_group_operator()
            nodes = m_palladium_m.node_tree.nodes
            specular_group = nodes.new("ShaderNodeGroup")
            specular_group.node_tree = bpy.data.node_groups['Specular']
            specular_group.location = (-500, -300)
            specular_group.inputs[0].default_value = 1.6381
            links = m_palladium_m.node_tree.links.new
            links(specular_group.outputs[0], BSDF.inputs[7])
            links(specular_group.outputs[1], BSDF.inputs[16])

            #LOAD THE MATERIAL
            bpy.context.object.active_material = m_palladium_m

        return {'FINISHED'}
