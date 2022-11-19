import bpy

# MESSAGE BOX
message_text = "This material already exists"
def ShowMessageBox(message = "", title = "", icon = 'INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

#Titanium PolishedShaderOperator
class QMMTitaniumPolished(bpy.types.Operator):
    """Add/Apply Titanium Polished Material to Selected Object (or Scene)"""
    bl_label = "QMM Titanium Polished Shader"
    bl_idname = 'shader.qmm_titanium_p_operator'
    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        if m_titanium_p := bpy.data.materials.get("QMM Titanium Polished"):
            ShowMessageBox(message_text, "QMM Titanium Polished")
            # print(f"QMM Titanium Polished already exists")
            bpy.context.object.active_material = m_titanium_p
            return {'FINISHED'}
        else:
            #CreateShader
            m_titanium_p = bpy.data.materials.new(name = "QMM Titanium Polished")
            m_titanium_p.use_nodes = True
            m_titanium_p.diffuse_color = (0.337163, 0.296138, 0.258183, 1)
            m_titanium_p.metallic = 1
            m_titanium_p.roughness = 0.35

            nodes = m_titanium_p.node_tree.nodes

            #materialoutput
            material_output = nodes.get('Material Output')
            material_output.location = (0,0)

            #princibledbsdf
            BSDF = nodes.get('Principled BSDF')
            BSDF.location = (-300,0)
            BSDF.inputs[0].default_value = (0.337163, 0.296138, 0.258183, 1)
            BSDF.inputs[6].default_value = 1
            BSDF.inputs[9].default_value = 0.35
            BSDF.inputs[16].default_value = 2.16

            #EnergyConservationGroup
            bpy.ops.node.ec_group_operator()
            ec_group = nodes.new("ShaderNodeGroup")
            ec_group.name = "Energy Conservation"
            ec_group.node_tree = bpy.data.node_groups['Energy Conservation']
            ec_group.location = (-500, -200)
            ec_group.inputs[0].default_value = 2.16
            ec_group.inputs[1].default_value = (0.337163, 0.296138, 0.258183, 1)
            ec_group.inputs[2].default_value = (0.434153, 0.423267, 0.434154, 1)

            links = m_titanium_p.node_tree.links.new

            links(ec_group.outputs[0], BSDF.inputs[0])
            links(ec_group.outputs[1], BSDF.inputs[7])
            links(ec_group.outputs[3], BSDF.inputs[16])

            #LOAD THE MATERIAL
            bpy.context.object.active_material = m_titanium_p

        return {'FINISHED'}
