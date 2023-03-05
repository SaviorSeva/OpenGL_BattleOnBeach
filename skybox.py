#!/usr/bin/env python3

from ctypes import sizeof
import OpenGL.GL as GL
import numpy as np
from PIL import Image
from core import Node

class Skybox(Node):
    def __init__(self, shader_skybox, path):
        super().__init__()
        self.skybox_vertices = np.array((
            # positions          
            (-1.0,  1.0, -1.0),
            (-1.0, -1.0, -1.0),
            (1.0, -1.0, -1.0),
            (1.0, -1.0, -1.0),
            (1.0,  1.0, -1.0),
            (-1.0,  1.0, -1.0),

            (-1.0, -1.0,  1.0),
            (-1.0, -1.0, -1.0),
            (-1.0,  1.0, -1.0),
            (-1.0,  1.0, -1.0),
            (-1.0,  1.0,  1.0),
            (-1.0, -1.0,  1.0),

            (1.0, -1.0, -1.0),
            (1.0, -1.0,  1.0),
            (1.0,  1.0,  1.0),
            (1.0,  1.0,  1.0),
            (1.0,  1.0, -1.0),
            (1.0, -1.0, -1.0),

            (-1.0, -1.0,  1.0),
            (-1.0,  1.0,  1.0),
            (1.0,  1.0,  1.0),
            (1.0,  1.0,  1.0),
            (1.0, -1.0,  1.0),
            (-1.0, -1.0,  1.0),

            (-1.0,  1.0, -1.0),
            (1.0,  1.0, -1.0),
            (1.0,  1.0,  1.0),
            (1.0,  1.0,  1.0),
            (-1.0,  1.0,  1.0),
            (-1.0,  1.0, -1.0),

            (-1.0, -1.0, -1.0),
            (-1.0, -1.0,  1.0),
            (1.0, -1.0, -1.0),
            (1.0, -1.0, -1.0),
            (-1.0, -1.0,  1.0),
            (1.0, -1.0,  1.0)
        ), 'f')

        self.faces = ["right.jpg",
            "left.jpg",
            "top.jpg",
            "bottom.jpg",
            "back.jpg",
            "front.jpg"]

        self.shader = shader_skybox
        self.set_skybox_vao()
        self.path = path
        self.skybox_texture = self.load_cubemap(path=self.path)
    
    def set_skybox_vao(self):
        self.skybox_vao = GL.glGenVertexArrays(1)
        self.skybox_vbo = GL.glGenBuffers(1)
        GL.glBindVertexArray(self.skybox_vao)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.skybox_vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, self.skybox_vertices, GL.GL_STATIC_DRAW)
        GL.glEnableVertexAttribArray(0)
        GL.glVertexAttribPointer( 0, 3, GL.GL_FLOAT, GL.GL_FALSE, 3 * sizeof(GL.GLfloat), 0)
        GL.glBindVertexArray(0)
    
    def load_cubemap(self, path):
        # Generate texture with textureID
        texture_ID = GL.glGenTextures(1)
        
        # Load texture for each face
        faces_path = []
        for filename in self.faces:
            faces_path.append(path + filename)

        GL.glBindTexture(GL.GL_TEXTURE_CUBE_MAP, texture_ID)

        for index, faces_path in enumerate(faces_path):
            tex_image = Image.open(faces_path)
            tex_data = np.array(tex_image)
            width, height = tex_image.size
            GL.glTexImage2D(GL.GL_TEXTURE_CUBE_MAP_POSITIVE_X + index, 
                            0, GL.GL_RGB, width, height, 0,
                            GL.GL_RGB, GL.GL_UNSIGNED_BYTE, tex_data)
            print("Loaded", faces_path, width, height)

        # Specify wrapping and filtering methods
        GL.glTexParameteri(GL.GL_TEXTURE_CUBE_MAP, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
        GL.glTexParameteri(GL.GL_TEXTURE_CUBE_MAP, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
        GL.glTexParameteri(GL.GL_TEXTURE_CUBE_MAP, GL.GL_TEXTURE_WRAP_S, GL.GL_CLAMP_TO_EDGE)
        GL.glTexParameteri(GL.GL_TEXTURE_CUBE_MAP, GL.GL_TEXTURE_WRAP_T, GL.GL_CLAMP_TO_EDGE)
        GL.glTexParameteri(GL.GL_TEXTURE_CUBE_MAP, GL.GL_TEXTURE_WRAP_R, GL.GL_CLAMP_TO_EDGE)
        GL.glBindTexture(GL.GL_TEXTURE_CUBE_MAP, 0)

        return texture_ID

    def draw(self, model, view, projection):
        GL.glUseProgram(self.shader.glid)
        GL.glDepthFunc(GL.GL_LEQUAL)
        
        self.model_loc = GL.glGetUniformLocation(self.shader.glid, 'model')
        self.view_loc = GL.glGetUniformLocation(self.shader.glid, 'view')
        self.projection_loc = GL.glGetUniformLocation(self.shader.glid, "projection")
        self.skybox_loc = GL.glGetUniformLocation(self.shader.glid, "skybox")

        GL.glUniformMatrix4fv(self.model_loc, 1, True, model)
        GL.glUniformMatrix4fv(self.view_loc, 1, True, view)
        GL.glUniformMatrix4fv(self.projection_loc, 1, True, projection)
        GL.glUniform1i(self.skybox_loc, 0)
        
        GL.glBindVertexArray(self.skybox_vao)
        GL.glBindTexture(GL.GL_TEXTURE_CUBE_MAP, self.skybox_texture)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 36)
        GL.glBindVertexArray(0)
        GL.glDepthMask(GL.GL_FALSE)