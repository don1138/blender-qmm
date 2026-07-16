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
            #ShowMessageBox(message_text, "QMM Car Paint")
            bpy.context.object.active_material = m_car_paint
            diffuse_bool = bpy.context.scene.diffuse_bool.diffuse_more
            m_car_paint.diffuse_color = (0.527115, 0.564712, 0.577580, 1) if diffuse_bool else (0.8, 0.8, 0.8, 1)
            m_car_paint.metallic = 1 if diffuse_bool else 0
            m_car_paint.roughness = 0.24 if diffuse_bool else 0.4
            return {'FINISHED'}
        else:
            self.make_shader()
        return {'FINISHED'}

    def make_shader(self):
        start = time.time()

        # CreateShader
        m_car_paint = bpy.data.materials.new(name="QMM Car Paint")
        m_car_paint.use_nodes = True
        diffuse_bool = bpy.context.scene.diffuse_bool.diffuse_more
        if diffuse_bool:
            m_car_paint.diffuse_color = (0.527115, 0.564712, 0.577580, 1)
            m_car_paint.metallic = 1
            m_car_paint.roughness = 0.25

        nodes = m_car_paint.node_tree.nodes

        # materialoutput
        material_output = next((n for n in nodes if n.bl_idname == 'ShaderNodeOutputMaterial'), None)
        if material_output:
            material_output.location = (0, 0)

        # principledbsdf
        BSDF = next((n for n in nodes if n.bl_idname == 'ShaderNodeBsdfPrincipled'), None)
        if BSDF:
            BSDF.distribution = 'MULTI_GGX'
            BSDF.location = (-300, 0)
            BSDF.inputs["Base Color"].default_value = (0.527115, 0.564712, 0.577580, 1)
            BSDF.inputs["Metallic"].default_value = 1
            BSDF.inputs["Roughness"].default_value = 0.25
            BSDF.inputs["Coat Weight"].default_value = 1

        # Pearlescent Pigment Group
        bpy.ops.node.pearlescent_pigment_group_operator()
        pp_group = nodes.new("ShaderNodeGroup")
        pp_group.name = "Pearlescent Pigment"
        pp_group.node_tree = bpy.data.node_groups['Pearlescent Pigment']
        pp_group.location = (-600, 100)
        pp_group.width = 240

        # Metal Flake Group
        bpy.ops.node.metal_flake_group_operator()
        mf_group = nodes.new("ShaderNodeGroup")
        mf_group.name = "Metal Flake"
        mf_group.node_tree = bpy.data.node_groups['Metal Flake']
        mf_group.location = (-800, -100)
        mf_group.width = 240
        mf_group.inputs[0].default_value = 4096
        mf_group.inputs[1].default_value = 0.25

        n_maprange = nodes.new("ShaderNodeMapRange")
        n_maprange.location = (-500, -100)
        n_maprange.inputs[3].default_value = 0.4
        n_maprange.inputs[4].default_value = 0.2

        # Links
        links = m_car_paint.node_tree.links.new

        links(BSDF.outputs["BSDF"], material_output.inputs["Surface"])
        links(mf_group.outputs[1], n_maprange.inputs["Value"])
        links(mf_group.outputs[0], BSDF.inputs["Normal"])
        links(n_maprange.outputs["Result"], BSDF.inputs["Roughness"])

        # LOAD THE MATERIAL
        bpy.context.object.active_material = m_car_paint

        end = time.time()
        print(f"QMM Car Paint: {end - start} seconds")
