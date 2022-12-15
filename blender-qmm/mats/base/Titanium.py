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
    bl_label = "QMM Titanium Textured Shader"
    bl_idname = 'shader.qmm_titanium_operator'
    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        if m_titanium := bpy.data.materials.get("QMM Titanium Textured"):
            ShowMessageBox(message_text, "QMM Titanium Textured")
            # print(f"QMM Titanium Textured already exists")
            bpy.context.object.active_material = m_titanium
            return {'FINISHED'}
        else:
            #CreateShader
            m_titanium = bpy.data.materials.new(name = "QMM Titanium Textured")
            m_titanium.use_nodes = True
            m_titanium.diffuse_color = (0.616, 0.582, 0.544, 1)
            m_titanium.metallic = 1
            m_titanium.roughness = 0.55

            nodes = m_titanium.node_tree.nodes

            #materialoutput
            material_output = nodes.get('Material Output')
            material_output.location = (0,0)

            #princibledbsdf
            BSDF = nodes.get('Principled BSDF')
            BSDF.location = (-300,0)
            BSDF.inputs[0].default_value = (0.533276, 0.491020, 0.439657, 1)
            BSDF.inputs[6].default_value = 1
            BSDF.inputs[9].default_value = 0.55
            BSDF.inputs[16].default_value = 2.16

            #EnergyConservationGroup
            bpy.ops.node.ec_group_operator()
            ec_group = nodes.new("ShaderNodeGroup")
            ec_group.name = "Energy Conservation"
            ec_group.node_tree = bpy.data.node_groups['Energy Conservation']
            ec_group.location = (-500, -200)
            ec_group.inputs[0].default_value = 2.16
            ec_group.inputs[1].default_value = (0.533276, 0.491020, 0.439657, 1)
            ec_group.inputs[2].default_value = (0.689, 0.683, 0.689, 1)

            #TexturizerGroup
            bpy.ops.node.texturizer_group_operator()
            texturizer_group = nodes.new("ShaderNodeGroup")
            texturizer_group.name = "Texturizer"
            texturizer_group.node_tree = bpy.data.node_groups['Texturizer']
            texturizer_group.location = (-700, -300)
            texturizer_group.inputs[0].default_value = (0.533276, 0.491020, 0.439657, 1)
            texturizer_group.inputs[1].default_value = 0.55

            #TitaniumColorsGroup
            bpy.ops.node.titanium_colors_group_operator()
            titanium_colors_group = nodes.new("ShaderNodeGroup")
            titanium_colors_group.name = "Titanium Colors"
            titanium_colors_group.node_tree = bpy.data.node_groups['Titanium Colors']
            titanium_colors_group.location = (-900, -400)

            links = m_titanium.node_tree.links.new

            links(titanium_colors_group.outputs[0], texturizer_group.inputs[0])
            links(texturizer_group.outputs[0], ec_group.inputs[1])
            links(texturizer_group.outputs[2], BSDF.inputs[9])
            links(texturizer_group.outputs[5], BSDF.inputs[22])
            links(ec_group.outputs[0], BSDF.inputs[0])
            links(ec_group.outputs[1], BSDF.inputs[7])
            links(ec_group.outputs[3], BSDF.inputs[16])

            #LOAD THE MATERIAL
            bpy.context.object.active_material = m_titanium

        return {'FINISHED'}
