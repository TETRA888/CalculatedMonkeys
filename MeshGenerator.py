# Include Python-Blender functionality
import bpy

# Include math libs
import math

# Include randomness for funr
import random

# Easier mesh manipulation and selection
import bmesh

def create_monkey():
    bpy.ops.mesh.primitive_monkey_add()
    monkey = bpy.context.active_object
    return monkey

def create_material():
    material_instance = bpy.data.materials.new(name = "Random_material")
    material_instance.use_nodes = True
    
    principled_bsdf_node = material_instance.node_tree.nodes["Principled BSDF"]
    
    Alpha = 1.0
    
    principled_bsdf_node.inputs["Base Color"].default_value = (random.random(), random.random(), random.random(), Alpha)

    # set metallic value
    principled_bsdf_node.inputs["Metallic"].default_value = random.randint(0,1)

    # set roughness value
    principled_bsdf_node.inputs["Roughness"].default_value = random.random()

    return material_instance

def assign_colors(monkey, CLOD):
    bpy.ops.object.mode_set(mode = 'EDIT')
    bmesh_data = bmesh.from_edit_mesh(monkey.data)
    
    for face in bmesh_data.faces:
        monkey.active_material_index = random.randint(0, CLOD - 1) # indices range from 0 - (color level of detail - 1)
        face.select = True
        bpy.ops.object.material_slot_assign()
        face.select = False
    bpy.ops.object.mode_set(mode = 'OBJECT')


def main():
    monkey = create_monkey()
    CLOD = 30
    for i in range(0,CLOD):
        material = create_material()
        monkey.data.materials.append(material)
    assign_colors(monkey, CLOD)

main()