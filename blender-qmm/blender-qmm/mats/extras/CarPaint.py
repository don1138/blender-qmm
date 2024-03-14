import bpy
import time

# MESSAGE BOX
message_text = "This material already exists"


def ShowMessageBox(message="", title="", icon='INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)


# CarPaintShaderOperator
class QMMCarPaint(bpy.types.Operator):
    """Add/Apply Car Paint Material to Selected Object (or Scene)"""
    bl_label = "QMM Car Paint Shader"
    bl_idname = 'shader.qmm_car_paint_operator'

    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        if m_car_paint := bpy.data.materials.get("QMM Car Paint"):
            ShowMessageBox(message_text, "QMM Car Paint")
            bpy.context.object.active_material = m_car_paint
            return {'FINISHED'}
        else:
            self.make_shader()
        return {'FINISHED'}

    def make_shader(self):
        start = time.time()

        # CreateShader
        m_car_paint = bpy.data.materials.new(name="QMM Car Paint")
        m_car_paint.use_nodes = True
        m_car_paint.diffuse_color = (0.527115, 0.564712, 0.577580, 1)
        m_car_paint.metallic = 1
        m_car_paint.roughness = 0.25

        nodes = m_car_paint.node_tree.nodes

        # materialoutput
        material_output = nodes.get('Material Output')
        material_output.location = (0, 0)

        # princibledbsdf
        BSDF = nodes.get('Principled BSDF')
        BSDF.distribution = 'MULTI_GGX'
        BSDF.location = (-300, 0)
        BSDF.inputs[0].default_value = (0.527115, 0.564712, 0.577580, 1)
        if bpy.app.version < (4, 0, 0):
            BSDF.inputs[6].default_value = 1        #Metallic
            BSDF.inputs[9].default_value = 0.25    #Roughness
            BSDF.inputs[14].default_value = 0.25    #Clearcoat
        else:
            BSDF.inputs[1].default_value = 1        #Metallic
            BSDF.inputs[2].default_value = 0.25    #Roughness
            BSDF.inputs[18].default_value = 0.25    #Coat Weight

        # Metal Flake Group
        bpy.ops.node.metal_flake_group_operator()
        mf_group = nodes.new("ShaderNodeGroup")
        mf_group.name = "Metal Flake"
        mf_group.node_tree = bpy.data.node_groups['Metal Flake']
        mf_group.location = (-600, -100)
        mf_group.width = 240
        mf_group.inputs[0].default_value = 4000
        mf_group.inputs[1].default_value = 0.25

        # Uneven Roughness Group
        bpy.ops.node.uneven_roughness_group_operator()
        ur_group = nodes.new("ShaderNodeGroup")
        ur_group.name = "Uneven Roughness"
        ur_group.node_tree = bpy.data.node_groups['Uneven Roughness']
        ur_group.location = (-600, -300)
        ur_group.width = 240
        ur_group.inputs[0].default_value = 0.2
        ur_group.inputs[1].default_value = 0.3

        # Links
        links = m_car_paint.node_tree.links.new

        links(BSDF.outputs[0], material_output.inputs[0])
        if bpy.app.version < (4, 0, 0):
            links(mf_group.outputs[0], BSDF.inputs[22])     #Normal
            links(ur_group.outputs[0], BSDF.inputs[14])    #Clearcoat
        else:
            links(mf_group.outputs[0], BSDF.inputs[5])     #Normal
            links(ur_group.outputs[0], BSDF.inputs[18])    #Clearcoat

        # LOAD THE MATERIAL
        bpy.context.object.active_material = m_car_paint

        end = time.time()
        print(f"QMM Car Paint: {end - start} seconds")
