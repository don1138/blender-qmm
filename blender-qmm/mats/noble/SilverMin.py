import bpy

# MESSAGE BOX
message_text = "This material already exists"
def ShowMessageBox(message = "", title = "", icon = 'INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

#SilverMinShaderOperator
class QMMSilverMin(bpy.types.Operator):
    """Add/Apply Silver (Minimum) Material to Selected Object (or Scene)"""
    bl_label = "QMM Silver Min Shader"
    bl_idname = 'shader.qmm_silver_min_operator'
    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        m_silver_min = bpy.data.materials.get("QMM Silver Min")
        if m_silver_min:
            ShowMessageBox(message_text, "QMM Silver Min")
            # print(f"QMM Silver Min already exists")
            bpy.context.object.active_material = m_silver_min
            return {'FINISHED'}
        else:
            #CreateShader
            m_silver_min = bpy.data.materials.new(name = "QMM Silver Min")
            m_silver_min.use_nodes = True
            m_silver_min.diffuse_color = (0.401978, 0.396755, 0.417885, 1)
            m_silver_min.metallic = 1
            m_silver_min.roughness = 0.25

            nodes = m_silver_min.node_tree.nodes

            #materialoutput
            material_output = nodes.get('Material Output')
            material_output.location = (0,0)

            #princibledbsdf
            BSDF = nodes.get('Principled BSDF')
            BSDF.location = (-300,0)
            BSDF.inputs[0].default_value = (0.401978, 0.396755, 0.417885, 1)
            BSDF.inputs[6].default_value = 1
            BSDF.inputs[9].default_value = 0.25
            BSDF.inputs[16].default_value = 0.180

            #LOAD THE MATERIAL
            bpy.context.object.active_material = m_silver_min

            #SpecularGroup
            bpy.ops.node.specular_group_operator()
            nodes = m_silver_min.node_tree.nodes
            specular_group = nodes.new("ShaderNodeGroup")
            specular_group.node_tree = bpy.data.node_groups['Specular']
            specular_group.location = (-500, -300)
            specular_group.inputs[0].default_value = 0.180
            links = m_silver_min.node_tree.links.new
            links(specular_group.outputs[0], BSDF.inputs[7])
            links(specular_group.outputs[1], BSDF.inputs[16])

            return {'FINISHED'}
