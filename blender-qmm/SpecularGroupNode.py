import bpy

class SPECULAR_GROUP(bpy.types.Operator):
    """Add/Get Specular Group Node"""
    bl_label = "Specular Node Group"
    bl_idname = 'node.specular_group_operator'
    def execute(self, context):
        # DOES THE MATERIAL ALREADY EXIST?
        ng_specular = bpy.data.node_groups.get("Specular")

        if ng_specular:
            node_tree = bpy.context.object.active_material.node_tree
            nodes = node_tree.nodes
            specular_group = nodes.new("ShaderNodeGroup")
            specular_group.node_tree = bpy.data.node_groups['Specular']

            return {'FINISHED'}
        else:
            #newnodegroup
            specular_group = bpy.data.node_groups.new('Specular', 'ShaderNodeTree')

            #groupinput
            group_in = specular_group.nodes.new('NodeGroupInput')
            group_in.location = (-1000, 0)
            specular_group.inputs.new('NodeSocketFloat', 'IOR')

            #groupoutput
            group_out = specular_group.nodes.new('NodeGroupOutput')
            group_out.location = (0, 0)
            specular_group.outputs.new('NodeSocketFloat', 'Specular')
            specular_group.outputs.new('NodeSocketFloat', 'IOR')

            #mathdivide
            m_divide = specular_group.nodes.new('ShaderNodeMath')
            m_divide.operation = 'DIVIDE'
            m_divide.location = (-200,200)
            m_divide.inputs[1].default_value = 0.08

            #mathpower
            m_power = specular_group.nodes.new('ShaderNodeMath')
            m_power.operation = 'POWER'
            m_power.location = (-400,200)
            m_power.inputs[1].default_value = 2

            #mathdivide2
            m_divide2 = specular_group.nodes.new('ShaderNodeMath')
            m_divide2.operation = 'DIVIDE'
            m_divide2.location = (-600,200)

            #mathsubtract
            m_subtract = specular_group.nodes.new('ShaderNodeMath')
            m_subtract.operation = 'SUBTRACT'
            m_subtract.location = (-800,200)
            m_subtract.inputs[1].default_value = 1

            #mathadd
            m_add = specular_group.nodes.new('ShaderNodeMath')
            m_add.operation = 'ADD'
            m_add.location = (-800,-100)
            m_add.inputs[1].default_value = 1

            link = specular_group.links.new

            link(group_in.outputs[0], m_add.inputs[0])
            link(group_in.outputs[0], m_subtract.inputs[0])
            link(group_in.outputs[0], group_out.inputs[1])
            link(m_add.outputs[0], m_divide2.inputs[1])
            link(m_subtract.outputs[0], m_divide2.inputs[0])
            link(m_divide2.outputs[0], m_power.inputs[0])
            link(m_power.outputs[0], m_divide.inputs[0])
            link(m_divide.outputs[0], group_out.inputs[0])

            return {'FINISHED'}
