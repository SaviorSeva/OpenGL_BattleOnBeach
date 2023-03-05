# Python built-in modules
from itertools import cycle         # allows easy circular choice list

# External, non built-in modules
import OpenGL.GL as GL              # standard Python OpenGL wrapper
import glfw                         # lean window system wrapper for OpenGL
import numpy as np                  # all matrix manipulations & OpenGL args

from camera import Camera
from core import Node
from musketeerOnBeach import MusketeerOnBeach
from transform import identity, perspective
# our transform functions
from transform import identity

# ------------  Viewer class & window management ------------------------------
class Viewer(Node):
    """ GLFW viewer window, with classic initialization & graphics loop """

    def __init__(self, width=640, height=480):
        super().__init__()
        self.lastFrame = 0.0

        # version hints: create GL window with >= OpenGL 3.3 and core profile
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.RESIZABLE, True)
        self.win = glfw.create_window(width, height, 'Viewer', None, None)

        # make win's OpenGL context current; no OpenGL calls can happen before
        glfw.make_context_current(self.win)

        # Init camera
        camera_pos = np.array((-80.0, 15.0, 0.0))
        world_up = np.array((0.0, 1.0, 0.0))
        self.camera = Camera(camera_pos, world_up, pitch=-15.0)

        # register event handlers
        glfw.set_key_callback(self.win, self.on_key)
        glfw.set_window_size_callback(self.win, self.on_size)

        # useful message to check OpenGL renderer characteristics
        print('OpenGL', GL.glGetString(GL.GL_VERSION).decode() + ', GLSL',
              GL.glGetString(GL.GL_SHADING_LANGUAGE_VERSION).decode() +
              ', Renderer', GL.glGetString(GL.GL_RENDERER).decode())

        # initialize GL by setting viewport and default render characteristics
        GL.glClearColor(0.1, 0.1, 0.1, 0.1)
        GL.glEnable(GL.GL_CULL_FACE)   # backface culling enabled (TP2)
        GL.glEnable(GL.GL_DEPTH_TEST)  # depth test now enabled (TP2)

        # cyclic iterator to easily toggle polygon rendering modes
        self.fill_modes = cycle([GL.GL_LINE, GL.GL_POINT, GL.GL_FILL])

    def run(self):
        """ Main render loop for this OpenGL window """
        while not glfw.window_should_close(self.win):
            
            # Set frame time
            self.currentFrame = glfw.get_time()
            deltaTime = self.currentFrame - self.lastFrame
            self.lastFrame = self.currentFrame

            # clear draw buffer and depth buffer (<-TP2)
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

            win_size = glfw.get_window_size(self.win)

            # Add key listenser for camera movement
            self.camera.camera_key_handler(window=self.win, deltaTime=deltaTime)

            # draw our scene objects
            cam_pos = np.linalg.inv(self.camera.get_view_matrix())[:, 3]
            self.draw(view=self.camera.get_view_matrix(),
                      projection=perspective(fovy=45.0, aspect=(win_size[0]/win_size[1]), near=0.1, far=1000.0),
                      model=identity(),
                      w_camera_position=cam_pos)

            # flush render commands, and swap draw buffers
            glfw.swap_buffers(self.win)

            # Poll for and process events
            glfw.poll_events()

    def on_key(self, _win, key, _scancode, action, _mods):
        """ 'Escape' quits """
        if action == glfw.PRESS or action == glfw.REPEAT:
            if key == glfw.KEY_ESCAPE :
                glfw.set_window_should_close(self.win, True)
            if key == glfw.KEY_P:
                GL.glPolygonMode(GL.GL_FRONT_AND_BACK, next(self.fill_modes))
            if key == glfw.KEY_SPACE:
                glfw.set_time(0.0)

            # call Node.key_handler which calls key_handlers for all drawables
            self.key_handler(key)

    def on_key_musk(self, _win, key, _scancode, action, _mods):
        """ 'Escape' quits """
        if action == glfw.PRESS or action == glfw.REPEAT:
            if key == glfw.KEY_ESCAPE :
                glfw.set_window_should_close(self.win, True)
            if key == glfw.KEY_P:
                GL.glPolygonMode(GL.GL_FRONT_AND_BACK, next(self.fill_modes))
            if key == glfw.KEY_SPACE:
                glfw.set_time(0.0)

            # call Node.key_handler which calls key_handlers for all drawables
            self.key_handler(key)

        self.musk.musketeer_key_handler(key, action)

    def on_size(self, _win, _width, _height):
        """ window size update => update viewport to new framebuffer size """
        GL.glViewport(0, 0, *glfw.get_framebuffer_size(self.win))

    def constructMuskOnBeach(self, shader, light_dir, hmap_file):
        self.musk = MusketeerOnBeach(shader=shader, light_dir=light_dir, hmap_file=hmap_file)
        self.add(self.musk)
        glfw.set_key_callback(self.win, self.on_key_musk)