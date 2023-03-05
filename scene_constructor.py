

import random
import numpy as np                 # all matrix manipulations & OpenGL args
import math
from animation import KeyFrameControlNode

from core import load, Node
from transform import vec, translate, rotate, scale, quaternion, quaternion_from_euler
from PIL import Image


def construct_boat(shader, light_dir):
    boat_nodeList = load(file="./models/ship1/pirate_baot.obj", 
                         shader=shader,
                         tex_file="./models/ship1/boat.001.png",
                         light_dir=light_dir,
                         k_a = np.array((0.05, 0.05, 0.05)),
                         k_d = np.array((0.8, 0.8, 0.8)),
                         k_s = np.array((0.2, 0.2, 0.2)),
                         s=64)
    boat = Node(children=boat_nodeList, transform=translate(0, -1, 0))
    return boat

def construct_flagship(shader, light_dir):
    flagship_nodeList =load(file="./models/Boats/Galleon_Flying.FBX",
                            shader=shader, 
                            tex_file="./textures/Ships 1.tga",
                            light_dir=light_dir,
                            k_a = np.array((0.05, 0.05, 0.05)),
                            k_d = np.array((0.6, 0.6, 0.6)),
                            k_s = np.array((0.1, 0.1, 0.1)),
                            s=64)
    flagship = Node(children=flagship_nodeList, transform=translate(0, 0, 0) @ rotate((0.0, 1.0, 0.0), -90.0) @ scale(0.8, 0.8, 0.8))
    return flagship

def construct_galleon(shader, light_dir):
    galleon_nodeList =load(file="./models/Boats/Galleon.FBX",
                            shader=shader, 
                            tex_file="./textures/Ships 1.tga",
                            light_dir=light_dir,
                            k_a = np.array((0.05, 0.05, 0.05)),
                            k_d = np.array((0.6, 0.6, 0.6)),
                            k_s = np.array((0.1, 0.1, 0.1)),
                            s=20)
    galleon = Node(children=galleon_nodeList, transform=translate(0, 0, 0) @ rotate((0.0, 1.0, 0.0), -90.0) @ scale(0.5, 0.5, 0.5))
    return galleon

def construct_random_tree(shader, light_dir, hmap_file):
    treeTotalNode = Node(transform=translate(0, 0, 0))
    hmap = np.asarray(Image.open(hmap_file).convert('RGB'))
    tree_nodeList = load("./models/tree/Lowpoly_tree_sample.obj", 
                            shader,
                            light_dir=light_dir)
    for i in range(0, 10):
        xpos = random.randint(0, 255)
        zpos = random.randint(160, 255)
        ypos = get_height(hmap, xpos, zpos)
        tree = Node(transform=translate(xpos, ypos, zpos))
        for node in tree_nodeList:
            tree.add(node)
        treeTotalNode.add(tree)
        
    return treeTotalNode

def construct_rocks(shader, light_dir):
    rock_rootNode = Node(transform=translate(0, 0, 0))
    rock_nodeList =load(file="./models/Free rock/Rock_1.fbx",
                            shader=shader, 
                            light_dir=light_dir,
                            k_a = np.array((0.05, 0.05, 0.005)),
                            k_d = np.array((0.7, 0.7, 0.7)),
                            k_s = np.array((0.07, 0.07, 0.07)),
                            s=20)
    for i in range(0, 20):
        xpos = random.randint(0, 255)
        zpos = random.randint(128, 160)
        angle = random.randint(0, 360)
        rock_node = Node(transform=translate(xpos, 0, zpos) @ rotate((1.0, 0.0, 0.0), angle) @ scale(0.0025, 0.0025, 0.0025))
        for node in rock_nodeList:
            rock_node.add(node)
        rock_rootNode.add(rock_node)
    return rock_rootNode

def construct_musketeer_onboat(shader, light_dir):
    musketeer_nodeList =load(file="./models/Musketeer/Musketeer_idle.fbx",
                            shader=shader, 
                            tex_file="./models/Musketeer/texture/texture.png",
                            light_dir=light_dir,
                            k_a = np.array((0.3, 0.3, 0.3)),
                            k_d = np.array((0.6, 0.6, 0.6)),
                            k_s = np.array((0.2, 0.2, 0.2)),
                            s=32)
    musketeer = Node(children=musketeer_nodeList, transform=translate(13.0, 15.5, 34.5) @ rotate((1.0, 0.0, 0.0), -5.0) @ scale(0.25, 0.25, 0.25))
    return musketeer

def construct_golem(shader, light_dir):
    golem_nodeList =load(file="./models/Golem/Golem_idle.fbx",
                         shader=shader, 
                         tex_file="./models/Golem/Texture/Golem.psd",
                         light_dir=light_dir,
                         k_a = np.array((0.3, 0.3, 0.3)),
                         k_d = np.array((0.6, 0.6, 0.6)),
                         k_s = np.array((0.2, 0.2, 0.2)),
                         s=32)
    golem = Node(children=golem_nodeList, transform=translate(128, 0, 190) @ rotate((0.0, 1.0, 0.0), 180.0) @ scale(0.25, 0.25, 0.25))
    return golem

def construct_seagulls_formation(shader, light_dir, center, radius, seagull_count_each_side):
    seagull_formation_node = Node(transform=translate(0, 0, 0))
    seagull_nodeList = load(file="./models/seagull/seagul.FBX",
                            shader=shader, 
                            tex_file="./models/seagull/gull.png",
                            light_dir=light_dir)
    heightList = []
    for i in range(0, 33):
        heightList.append(random.randint(-5, 5))
    for i in range(1-seagull_count_each_side, seagull_count_each_side):
        seagull_formation_node.add(construct_seagull(shader, light_dir, center, radius, i, seagull_nodeList, heightList))
    return seagull_formation_node

# Load a seagull. 
# relative_position : The position in the formation of seagull. -3 means it's the 3rd seagull on the left of the leading seagull.
def construct_seagull(shader, light_dir, center, radius, relative_position, seagull_nodeList, heightList):
    seagull_node = Node(children=seagull_nodeList, transform=translate(0, 0, 0) @ rotate((0.0, 1.0, 0.0), -90.0) @ scale(0.25, 0.25, 0.25))
    translate_keys = {}
    for time in range(0, 33):
        translate_keys[time] = vec(center[0]+(radius+15*relative_position)*math.sin(((time % 32) * math.pi / 8)), 
                                   center[1]-3*abs(relative_position)+heightList[time], 
                                   center[2]+(radius+15*relative_position)*math.cos((time%32* math.pi / 8)))
    # print("Trans_Keys : ", translate_keys)
    rotate_keys = {0: quaternion(),
                   8: quaternion_from_euler(0, 180, 0),
                   16: quaternion_from_euler(0, 360, 0),
                   16.001: quaternion_from_euler(0, 0, 0),
                   24: quaternion_from_euler(0, 180, 0),
                   32: quaternion_from_euler(0, 360, 0)
                  }
    scale_keys = {0: 1}
    keynode = KeyFrameControlNode(translate_keys, rotate_keys, scale_keys)
    keynode.add(seagull_node)
    return keynode

def construct_seagulls_and_animation(shader, light_dir, center, radius):
    seagull_final_animation_node = Node(transform=translate(0, 0, 0))
    seagullL = Node(transform=translate(0, 0, 0) @ rotate((0.0, 1.0, 0.0), -90.0) @ scale(0.25, 0.25, 0.25))
    seagullC = Node(transform=translate(0, 0, 0) @ rotate((0.0, 1.0, 0.0), -90.0) @ scale(0.25, 0.25, 0.25))
    seagullR = Node(transform=translate(0, 0, 0) @ rotate((0.0, 1.0, 0.0), -90.0) @ scale(0.25, 0.25, 0.25))
    seagull_nodeList =load(file="./models/seagull/seagul.FBX",
                            shader=shader, 
                            tex_file="./models/seagull/gull.png",
                            light_dir=light_dir)
    for node in seagull_nodeList:        
        seagullL.add(node)
        seagullC.add(node)
        seagullR.add(node)

    translate_keysL = {}
    translate_keysR = {}
    translate_keysC = {}

    for time in range(0, 33):
        height_offset = random.randint(-5, 5)
        translate_keysL[time] = vec(center[0]+(radius-15)*math.sin((time%32* math.pi / 8)), center[1]+height_offset, center[2]+(radius-15)*math.cos((time%32* math.pi / 8)))
        translate_keysR[time] = vec(center[0]+(radius+15)*math.sin((time%32* math.pi / 8)), center[1]+height_offset, center[2]+(radius+15)*math.cos((time%32* math.pi / 8)))
        translate_keysC[time] = vec(center[0]+radius*math.sin(((time+0.5)%32* math.pi / 8)), center[1]+height_offset+2.5, center[2]+radius*math.cos(((time+0.5)%32* math.pi / 8)))
    rotate_keys = {0: quaternion(),
                   8: quaternion_from_euler(0, 180, 0),
                   16: quaternion_from_euler(0, 360, 0),
                   16.001: quaternion_from_euler(0, 0, 0),
                   24: quaternion_from_euler(0, 180, 0),
                   32: quaternion_from_euler(0, 360, 0)
                  }
    scale_keys = {0: 1}
    keynodeL = KeyFrameControlNode(translate_keysL, rotate_keys, scale_keys)
    keynodeL.add(seagullL)
    keynodeR = KeyFrameControlNode(translate_keysR, rotate_keys, scale_keys)
    keynodeR.add(seagullR)
    keynodeC = KeyFrameControlNode(translate_keysC, rotate_keys, scale_keys)
    keynodeC.add(seagullC)
    seagull_final_animation_node.add(keynodeL, keynodeR, keynodeC)
    return seagull_final_animation_node

def construct_ship_animation(x, z, offset, yrange):
    translate_keys = {}
    for time in range(0, 33):
        translate_keys[time] = vec(x, yrange * math.sin(((time+offset) % 16) * math.pi / 8), z)
    rotate_keys = {0: quaternion()}
    scale_keys = {0: 1}
    keynode = KeyFrameControlNode(translate_keys, rotate_keys, scale_keys)
    return keynode

def get_height(hmap, x, z):
    # Get the height from the input heightmap
    height = hmap[int(x), int(z), 0]
    height = height * 25 / 256    # 25 is the max height of the ground
    return height