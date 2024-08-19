# Include Python-Blender functionality
import bpy

# Include math libs
import math

# Include randomness for funr
import random

# Easier mesh manipulation and selection
import bmesh

"""
 ________      ___    ___      ________  ________  ________  ________          _____ ______          
|\   __  \    |\  \  /  /|    |\   __  \|\   ____\|\   __  \|\   ___ \        |\   _ \  _   \        
\ \  \|\ /_   \ \  \/  / /    \ \  \|\  \ \  \___|\ \  \|\  \ \  \_|\ \       \ \  \\\__\ \  \       
 \ \   __  \   \ \    / /      \ \   __  \ \_____  \ \   __  \ \  \ \\ \       \ \  \\|__| \  \      
  \ \  \|\  \   \/  /  /        \ \  \ \  \|____|\  \ \  \ \  \ \  \_\\ \       \ \  \    \ \  \ ___ 
   \ \_______\__/  / /           \ \__\ \__\____\_\  \ \__\ \__\ \_______\       \ \__\    \ \__\\__\
    \|_______|\___/ /             \|__|\|__|\_________\|__|\|__|\|_______|        \|__|     \|__\|__|
             \|___|/                       \|_________|                                              
                                                                                                                                                                                                                                                                                                                                                  
"""                                                                                                                

def create_vr_headset_base():
    """"""
    bpy.ops.mesh.primitive_cube_add(enter_editmode = True, location=(0, 0, 0), scale=(1, 0.25, 0.5))

    bpy.ops.mesh.bevel(offset=0.1, offset_pct=0, segments=2, affect='EDGES')

    bpy.ops.object.mode_set(mode='OBJECT')
    
    base_piece = bpy.context.active_object
    
    return base_piece
    

def create_vr_headset_side_pieces():
    bpy.ops.mesh.primitive_cube_add(enter_editmode = True, location=(-1.05741, 0.549105, 0.140719), scale=(0.1, 0.625, 0.1))
    bpy.ops.mesh.bevel(offset=0.04, offset_pct=0, segments=2, affect='EDGES')
    bpy.ops.object.mode_set(mode='OBJECT')
    
    piece_one = bpy.context.active_object
    
    bpy.ops.mesh.primitive_cube_add(enter_editmode = True, location=(1.05741, 0.549105, 0.140719), scale=(0.1, 0.625, 0.1))
    bpy.ops.mesh.bevel(offset=0.04, offset_pct=0, segments=2, affect='EDGES')
    bpy.ops.object.mode_set(mode='OBJECT')
    
    piece_two = bpy.context.active_object
    
    return piece_one, piece_two
    
def create_vr_headset():
    base_piece = create_vr_headset_base()
    piece_one, piece_two = create_vr_headset_side_pieces()
    headset_material = bpy.data.materials.new(name = "Grey")
    headset_material.diffuse_color = (0.08, 0.08, 0.08, 1)
    base_piece.data.materials.append(headset_material)
    piece_one.data.materials.append(headset_material)
    piece_two.data.materials.append(headset_material)
    
    

def create_monkey():
    bpy.ops.mesh.primitive_monkey_add(location = (0, 0.9, 0))
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

    """Create multiple shader nodes and then connect them via code"""
    node_location_x_step = 300
    current_node_location_x = -node_location_x_step
    
    # create color ramp node
    color_ramp_node = material_instance.node_tree.nodes.new(type = "ShaderNodeValToRGB")
    color_ramp_node.color_ramp.elements[0].position = random.random()
    color_ramp_node.color_ramp.elements[1].position = random.random()
    color_ramp_node.location.x = current_node_location_x
    current_node_location_x -= node_location_x_step
    
    # create a Noise Texture node
    noise_texture_node = material_instance.node_tree.nodes.new(type = "ShaderNodeTexNoise")
    noise_texture_node.inputs[2].default_value = random.uniform(0,20)
    noise_texture_node.location.x = current_node_location_x
    current_node_location_x -= node_location_x_step
    
    # create a Mapping node
    mapping_node = material_instance.node_tree.nodes.new(type = "ShaderNodeMapping")
    mapping_node.inputs[2].default_value[0] = random.uniform(0,math.radians(360))
    mapping_node.inputs[2].default_value[1] = random.uniform(0,math.radians(360))
    mapping_node.inputs[2].default_value[2] = random.uniform(0,math.radians(360))
    mapping_node.location.x = current_node_location_x
    current_node_location_x -= node_location_x_step 

    # create a texture coordinate node
    texture_coordinate_node = material_instance.node_tree.nodes.new(type = "ShaderNodeTexCoord")
    texture_coordinate_node.location.x = current_node_location_x
    
    material_instance.node_tree.links.new(noise_texture_node.outputs["Color"],
                                color_ramp_node.inputs["Fac"])
                                
    material_instance.node_tree.links.new(mapping_node.outputs["Vector"],
                                noise_texture_node.inputs["Vector"])
                                
    material_instance.node_tree.links.new(texture_coordinate_node.outputs["Generated"],
                                mapping_node.inputs["Vector"])
    
    material_instance.node_tree.links.new(color_ramp_node.outputs["Color"],
                                principled_bsdf_node.inputs["Roughness"])

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
    CLOD = 5
    for i in range(0,CLOD):
        material = create_material()
        monkey.data.materials.append(material)
    assign_colors(monkey, CLOD)
    create_vr_headset()
    
main()
