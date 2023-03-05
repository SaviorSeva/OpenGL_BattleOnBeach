import random
import numpy as np
from core import Shader, Node
from ground import Ground
from scene_constructor import construct_boat, construct_flagship, construct_galleon, construct_golem, construct_musketeer_onboat, construct_random_tree, construct_rocks, construct_seagulls_and_animation, construct_seagulls_formation, construct_ship_animation
from transform import translate
from viewer import Viewer

# -------------- main program and scene setup --------------------------------
def main():
    """ create a window, add scene objects, then run rendering loop """
    viewer = Viewer(width=1600, height=900)

    global_light = np.array((0.6, -0.8, 0.1))

    texphong_shader = Shader("shaders/texphong.vert", "shaders/texphong.frag")
    ground_shader = Shader("shaders/ground.vert", "shaders/ground.frag")
    skinning_shader = Shader("shaders/skinning.vert", "shaders/skinning.frag")

    # Add the ground to the scene. It has 3 textures and terrains with different height.
    base = Node(transform=translate(-128, 0, -128))
    base.add(Ground(ground_shader, "mappings/ground_texmap_256.png", "mappings/ground_hmap_256.png", 256, light=global_light))

    # Add the a boat to the scene. It has an animation corresponding to the tide of water.
    boat = construct_boat(shader=texphong_shader, light_dir=global_light)
    boat_animation_node = construct_ship_animation(100, 84, offset=0, yrange=0.5)
    boat_animation_node.add(boat)
    base.add(boat_animation_node)

    # Add the flagship to the scene. It has a animation corresponding to the tide of water, but the animation is different to the boat one.
    flagship = construct_flagship(shader=texphong_shader, light_dir=global_light)
    flagship_animation_node = construct_ship_animation(128, 44, offset=8, yrange=1.0)
    flagship_animation_node.add(flagship)

    # Add galleon to the scene. Galleon share the same tide animation with flagship.
    galleon = construct_galleon(shader=texphong_shader, light_dir=global_light)
    flagship_animation_node.add(galleon)

    # Add the musketeer standing on the flagship
    musketeer = construct_musketeer_onboat(shader=skinning_shader, light_dir=global_light)
    flagship_animation_node.add(musketeer)

    # Add the seagulls in a V-shape formation into the scene.
    seagull_finalNode = construct_seagulls_and_animation(shader=skinning_shader, 
                                                         light_dir=global_light, 
                                                         center=[random.randint(64, 192), random.randint(45, 55), random.randint(64, 192)], 
                                                         radius=128.0)
    
    # Add the trees on the grass terrain into the scene.
    # The position of the tree depends on the height of the terrain.
    tree = construct_random_tree(shader=texphong_shader, light_dir=global_light, hmap_file="mappings/ground_hmap_256.png")

    # Add rocks on the beach
    rock = construct_rocks(shader=texphong_shader, light_dir=global_light)
    
    viewer.constructMuskOnBeach(shader=skinning_shader, light_dir=global_light, hmap_file="mappings/ground_hmap_256.png")

    # KeyFrameControlNode(self.translateKeys, self.rotateKeys, self.scaleKeys)

    # Add everything to the base node
    base.add(flagship_animation_node)
    base.add(seagull_finalNode)
    base.add(tree)
    base.add(rock)
    viewer.add(base) 

    # start rendering loop
    message = """
    Welcome to the fantasy world with 2 cute cat musketeers!
    Use WASD keys to move the camera around, the ARROW keys to change the camera viewing angle, and Q E to move camera up and down.
    Press 0 1 2 to move to some preset camera postion.
    Use IJKL keys to move the musketeer on the beach !
    Press U and O to trigger some animation on the musketeer.

    Press P key to pass through different polygon mode (Display the actual model, the edge of triangles or the vertice of model).
    Press SPACEBAR to reset all animations.
    
    And finally, press ESC or Q to exit the game.
    """
    print(message)

    viewer.run()


if __name__ == '__main__':
    main()                     # main function keeps variables locally scoped