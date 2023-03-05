import numpy as np

from PIL import Image
from scene_constructor import get_height
from core import load, Node
from transform import  translate, rotate, scale, identity
import glfw                         # lean window system wrapper for OpenGL

class MusketeerOnBeach(Node):
    def __init__(self, shader, light_dir, hmap_file):
        super().__init__(transform=translate(0, 0, 0))
        self.xOffset = 12
        self.zOffset = 12
        self.direction = np.array((1.0, 0.0, 0.0))
        self.moveSpeed = 0.5
        self.musk_angle = 0.0
        self.hmap_file = hmap_file
        self.musketeer_mode = 'idle'
        musketeer_idleNodes=load(file="./models/Musketeer/Musketeer_idle.fbx",
                                      shader=shader, 
                                      tex_file="./models/Musketeer/texture/texture.png",
                                      light_dir=light_dir,
                                      k_a = np.array((0.3, 0.3, 0.3)),
                                      k_d = np.array((0.6, 0.6, 0.6)),
                                      k_s = np.array((0.2, 0.2, 0.2)),
                                      s=32)
        musketeer_runNodes=load(file="./models/Musketeer/Musketeer_run.fbx",
                                      shader=shader, 
                                      tex_file="./models/Musketeer/texture/texture.png",
                                      light_dir=light_dir,
                                      k_a = np.array((0.3, 0.3, 0.3)),
                                      k_d = np.array((0.6, 0.6, 0.6)),
                                      k_s = np.array((0.2, 0.2, 0.2)),
                                      s=32)
        musketeer_jumpNodes=load(file="./models/Musketeer/Musketeer_jump.fbx",
                                      shader=shader, 
                                      tex_file="./models/Musketeer/texture/texture.png",
                                      light_dir=light_dir,
                                      k_a = np.array((0.3, 0.3, 0.3)),
                                      k_d = np.array((0.6, 0.6, 0.6)),
                                      k_s = np.array((0.2, 0.2, 0.2)),
                                      s=32)
        musketeer_victoryNodes=load(file="./models/Musketeer/Musketeer_victory.fbx",
                                      shader=shader, 
                                      tex_file="./models/Musketeer/texture/texture.png",
                                      light_dir=light_dir,
                                      k_a = np.array((0.3, 0.3, 0.3)),
                                      k_d = np.array((0.6, 0.6, 0.6)),
                                      k_s = np.array((0.2, 0.2, 0.2)),
                                      s=32)
        self.musketeerIdleNode = Node(children=musketeer_idleNodes, transform=translate(12, 0, 12) @ scale(0.25, 0.25, 0.25))
        self.musketeerRunNode = Node(children=musketeer_runNodes, transform=translate(12, 0, 12) @ scale(0.25, 0.25, 0.25))
        self.musketeerJumpNode = Node(children=musketeer_jumpNodes, transform=translate(12, 0, 12) @ scale(0.25, 0.25, 0.25))
        self.musketeerVicNode = Node(children=musketeer_victoryNodes, transform=translate(12, 0, 12) @ scale(0.25, 0.25, 0.25))

        self.add(self.musketeerIdleNode)
        self.add(self.musketeerRunNode)

    def musketeer_reset(self):
        self.musketeer_mode = 'idle'

    def musketeer_key_handler(self, key, action):
        if(action == glfw.RELEASE):
            self.musketeer_mode = 'idle'
        elif key == glfw.KEY_I:
            self.musketeer_mode = 'run'
            self.direction = np.array((1.0, 0.0, 0.0))
            self.musk_angle = 90.0
            self.move()
        elif key == glfw.KEY_J:
            self.musketeer_mode = 'run'
            self.direction = np.array((0.0, 0.0, -1.0))
            self.musk_angle = 180.0
            self.move()
        elif key == glfw.KEY_K:
            self.musketeer_mode = 'run'
            self.direction = np.array((-1.0, 0.0, 0.0))
            self.musk_angle = 270.0
            self.move()
        elif key == glfw.KEY_L:
            self.musketeer_mode = 'run'
            self.direction = np.array((0.0, 0.0, 1.0))
            self.musk_angle = 0.0
            self.move()
            
        elif key == glfw.KEY_U:
            self.musketeer_mode = 'jump'
        elif key == glfw.KEY_O:
            self.musketeer_mode = 'victory'
            print("L Pressed")

    def move(self):
        self.xOffset += self.moveSpeed * self.direction[0]
        self.zOffset += self.moveSpeed * self.direction[2]

        if(self.xOffset > 126) : self.xOffset = 126
        elif(self.xOffset < -126) :  self.xOffset = -126
        if(self.zOffset > 126) : self.zOffset = 126
        elif(self.zOffset < -126) :  self.zOffset = -126

        yPos = self.get_relative_height(128+self.xOffset, 128+self.zOffset)

        self.musketeerIdleNode.transform=translate(self.xOffset, yPos, self.zOffset) @ rotate((0.0, 1.0, 0.0), self.musk_angle) @ scale(0.25, 0.25, 0.25)
        self.musketeerRunNode.transform=translate(self.xOffset, yPos, self.zOffset) @ rotate((0.0, 1.0, 0.0), self.musk_angle) @ scale(0.25, 0.25, 0.25)
        self.musketeerJumpNode.transform=translate(self.xOffset, yPos, self.zOffset) @ rotate((0.0, 1.0, 0.0), self.musk_angle) @ scale(0.25, 0.25, 0.25)
        self.musketeerVicNode.transform=translate(self.xOffset, yPos, self.zOffset) @ rotate((0.0, 1.0, 0.0), self.musk_angle) @ scale(0.25, 0.25, 0.25)

    def draw(self, model=identity(), **other_uniforms):
        """ Recursive draw, passing down updated model matrix. """
        self.world_transform = model @ self.transform
        if self.musketeer_mode == 'idle':
            self.musketeerIdleNode.draw(**other_uniforms)
        elif self.musketeer_mode == 'run':
            self.musketeerRunNode.draw(**other_uniforms)
        elif self.musketeer_mode == 'jump':
            self.musketeerJumpNode.draw(**other_uniforms)
        elif self.musketeer_mode == 'victory':
            self.musketeerVicNode.draw(**other_uniforms)

    def get_relative_height(self, x, z):
        # Get the height from the input heightmap
        hmap = np.asarray(Image.open(self.hmap_file).convert('RGB'))
        height = get_height(hmap, x, z)
        print("x = ", x, "; z = ", z)
        if(z < 128): 
            in_water_height = 0.5 * (128 - z)
            if in_water_height > 5 : in_water_height = 5
            height = height - in_water_height
        return height