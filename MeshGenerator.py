# Include Python-Blender functionality
import bpy

# Include math libs
import math

# Include randomness for fun
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
    """ This creates a primitve base mesh for the VR headset """
    bpy.ops.mesh.primitive_cube_add(enter_editmode = True, location=(0, 0, 0), scale=(1, 0.25, 0.5))
    bpy.ops.mesh.bevel(offset=0.1, offset_pct=0, segments=2, affect='EDGES')
    bpy.ops.object.mode_set(mode='OBJECT')
    base_piece = bpy.context.active_object
    
    return base_piece # Returns the reference to the VR headset base mesh object
    

def create_vr_headset_side_pieces():
    """ This creates the side pieces of the VR headset.
        In this instance I chose to create two seperate pieces 
        instead of using an array modifier or object instantiation 
        so that there is finer control on both of the pieces
    """
    # Piece one
    bpy.ops.mesh.primitive_cube_add(enter_editmode = True, location=(-1.05741, 0.549105, 0.140719), scale=(0.1, 0.625, 0.1))
    bpy.ops.mesh.bevel(offset=0.04, offset_pct=0, segments=2, affect='EDGES')
    bpy.ops.object.mode_set(mode='OBJECT')
    
    piece_one = bpy.context.active_object
    
    # Piece Two
    bpy.ops.mesh.primitive_cube_add(enter_editmode = True, location=(1.05741, 0.549105, 0.140719), scale=(0.1, 0.625, 0.1))
    bpy.ops.mesh.bevel(offset=0.04, offset_pct=0, segments=2, affect='EDGES')
    bpy.ops.object.mode_set(mode='OBJECT')
    
    piece_two = bpy.context.active_object
    
    return piece_one, piece_two # Returns the reference to the VR headset side pieces of the mesh objects
    
def create_vr_headset():
    """ This simply calls both of the functions to build the entire VR headset
        and it also appends the same color to all of the seperate objects that make up the VR headset
    """
    base_piece = create_vr_headset_base()
    piece_one, piece_two = create_vr_headset_side_pieces()
    headset_material = bpy.data.materials.new(name = "Grey")
    headset_material.diffuse_color = (0.08, 0.08, 0.08, 1)
    base_piece.data.materials.append(headset_material)
    piece_one.data.materials.append(headset_material)
    piece_two.data.materials.append(headset_material)
    
    bpy.ops.object.select_all(action='DESELECT')
    
    piece_one.select_set(True)
    piece_two.select_set(True)
    base_piece.select_set(True)
    
    bpy.ops.object.join()
    
    vr_headset = bpy.context.active_object
    
    return vr_headset
    # Returns joined pieces for easier referencing

def create_monkey():
    """ Creates the iconic Blender Suzanne monkey """
    bpy.ops.mesh.primitive_monkey_add(location = (0, 0.9, 0))
    monkey = bpy.context.active_object
    
    return monkey # returns reference to th monkey mesh object

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

def create_vr_monkey():
    monkey = create_monkey()
    CLOD = 5
    
    for i in range(0,CLOD):
        material = create_material()
        monkey.data.materials.append(material)
    assign_colors(monkey, CLOD)
    vr_headset = create_vr_headset()
    
    bpy.ops.object.select_all(action='DESELECT')
    monkey.select_set(True)
    vr_headset.select_set(True)
    bpy.ops.object.join()
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
    bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)

    
    return bpy.context.active_object

steps = 8
radius = 5

angle_increment = math.tau/steps
current_angle = 0

for i in range(0,steps):
    current_monkey = create_vr_monkey()
    current_angle = angle_increment*i
    current_monkey.location = (math.cos(current_angle)*radius, math.sin(current_angle)*radius, 0)
    current_monkey.rotation_euler = (0, 0, current_angle + math.pi/2)
