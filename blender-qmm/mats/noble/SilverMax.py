import bpy

# MESSAGE BOX
message_text = "This material already exists"
def ShowMessageBox(message = "", title = "", icon = 'INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

#SilverMaxShaderOperator
class QMMSilverMax(bpy.types.Operator):
    """Add/Apply Silver (Maximum) Material to Selected Object (or Scene)"""
    bl_label = "QMM Silver Max Shader"
    bl_idname = 'shader.qmm_silver_max_operator'
    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        m_silver_max = bpy.data.materials.get("QMM Silver Max")
        if m_silver_max:
            ShowMessageBox(message_text, "QMM Silver Max")
            # print(f"QMM Silver Max already exists")
            bpy.context.object.active_material = m_silver_max
            return {'FINISHED'}
        else:
            #CreateShader
            m_silver_max = bpy.data.materials.new(name = "QMM Silver Max")
            m_silver_max.use_nodes = True
            m_silver_max.diffuse_color = (0.401978, 0.396755, 0.417885, 1)
            m_silver_max.metallic = 1
            m_silver_max.roughness = 0.25

            nodes = m_silver_max.node_tree.nodes

            #materialoutput
            material_output = nodes.get('Material Output')
            material_output.location = (0,0)

            #princibledbsdf
            BSDF = nodes.get('Principled BSDF')
            BSDF.location = (-300,0)
            BSDF.inputs[0].default_value = (0.401978, 0.396755, 0.417885, 1)
            BSDF.inputs[6].default_value = 1
            BSDF.inputs[9].default_value = 0.25
            BSDF.inputs[16].default_value = 1.350

            #LOAD THE MATERIAL
            bpy.context.object.active_material = m_silver_max

            #SpecularGroup
            bpy.ops.node.specular_group_operator()
            nodes = m_silver_max.node_tree.nodes
            specular_group = nodes.new("ShaderNodeGroup")
            specular_group.node_tree = bpy.data.node_groups['Specular']
            specular_group.location = (-500, -300)
            specular_group.inputs[0].default_value = 1.350
            links = m_silver_max.node_tree.links.new
            links(specular_group.outputs[0], BSDF.inputs[7])
            links(specular_group.outputs[1], BSDF.inputs[16])

        return {'FINISHED'}
