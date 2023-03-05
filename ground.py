#!/usr/bin/env python3
import OpenGL.GL as GL              # standard Python OpenGL wrapper
import numpy as np                  # all matrix manipulations & OpenGL args
from core import Mesh
from texture import Texture
from PIL import Image

from transform import normalized

class Ground(Mesh):
    """ Simple first textured object """
    def __init__(self, shader, texmap_file, hmap_file, size, light):
        # prepare texture modes cycling variables for interactive toggling
        # self.wraps = cycle([GL.GL_REPEAT, GL.GL_MIRRORED_REPEAT,
        #                     GL.GL_CLAMP_TO_BORDER, GL.GL_CLAMP_TO_EDGE])
        # self.filters = cycle([(GL.GL_NEAREST, GL.GL_NEAREST),
        #                       (GL.GL_LINEAR, GL.GL_LINEAR),
        #                       (GL.GL_LINEAR, GL.GL_LINEAR_MIPMAP_LINEAR)])
        # self.wrap, self.filter = next(self.wraps), next(self.filters)
        self.wrap = GL.GL_REPEAT
        self.filter = (GL.GL_LINEAR, GL.GL_LINEAR_MIPMAP_LINEAR)
        self.texmap_file = texmap_file
        self.size = size
        self.hmap_file = hmap_file
        self.light = light

        # Get height map for ground generation
        self.hmap = np.asarray(Image.open(hmap_file).convert('RGB'))
        texmap_image = Image.open(texmap_file).convert('RGB')
        water_image, beach_image, grass_image = texmap_image.split()

        self.tex_water_map = np.asarray(water_image)
        self.tex_beach_map = np.asarray(beach_image)
        self.tex_grass_map = np.asarray(grass_image)

        # setup plane mesh to be textured
        # base_coords = ((-1, 0, -1), (1, 0, -1), (1, 0, 1), (-1, 0, 1))
        # scaled = 100 * np.array(base_coords, np.float32)
        # indices = np.array((0, 2, 1, 0, 3, 2), np.uint32)

        self.init_ground()
        
        mesh = Mesh(shader, 
                    attributes=dict(position=self.vertice_array, 
                                    normal=self.normal_array, 
                                    tex_coords=self.tex_coords_array
                                    ), 
                    index=self.indices)
        self.drawable = mesh

        # setup & upload texture to GPU, bind it to shader name 'diffuse_map'
        water_tex = Texture("textures/water2.jpg", self.wrap, *self.filter)
        beach_tex = Texture("textures/beach.jpg", self.wrap, *self.filter)
        grass_tex = Texture("textures/grass.png", self.wrap, *self.filter)
        texmap_tex = Texture(self.texmap_file, self.wrap, *self.filter)
        self.textures = dict(water_tex=water_tex, 
                             beach_tex=beach_tex, 
                             grass_tex=grass_tex, 
                             texmap=texmap_tex
                             )

        super().__init__(shader, 
                         attributes=dict(position=self.vertice_array, 
                                         normal=self.normal_array, 
                                         tex_coords=self.tex_coords_array
                                         ), 
                         index=self.indices
                         )

    def init_ground(self):
        vertices = []
        normals = []
        tex_coords = []
        indices = []

        for currentZ in range(0, self.size):
            for currentX in range(0, self.size):
                vertex_coord = [currentX,
                                self.get_height(self.hmap, currentX, currentZ),
                                currentZ]
                vertices.append(vertex_coord)
                normals.append(self.calc_normal(self.hmap, currentX, currentZ))
                tex_coords.append([currentX, currentZ])
                # print("Vcoord : ", vertex_coord)
        
        indices = []
        for currentZ in range(0, self.size - 1):
            for currentX in range(0, self.size - 1):
                top_left = (currentZ * self.size) + currentX
                top_right = top_left + 1
                bottom_left = ((currentZ + 1) * self.size) + currentX
                bottom_right = bottom_left + 1
                indices.append([top_left, bottom_left, top_right, top_right, bottom_left, bottom_right])

        self.indices = np.array(indices)

        self.vertice_array = np.array(vertices)
        self.normal_array = np.array(normals)
        self.tex_coords_array = np.array(tex_coords)

    def get_height(self, hmap, x, z):
        # Get the height from the input heightmap
        height = hmap[x, z, 0]
        height = height * 25 / 256    # 25 is the max height of the ground
        return height

    def calc_normal(self, hmap, x, z):
        # if vertex on border then set normal as (0, 1, 0)
        if x==0 or x==self.size-1 or z==0 or z==self.size-1 :
            return np.array([0.0, 1.0, 0.0])
        else:
            # Calculate the normal of a vertex from its top / bottom / left / right neighbour vertex coords
            top_neighbour_height = self.get_height(hmap, x, z-1)
            bot_neighbour_height = self.get_height(hmap, x, z+1)
            # The actual vector on z axis should be half the difference, hence the "/ 2"
            # The actual vector is actually (0, 0, vecZ) so we leave only vecZ here
            vecZ = (top_neighbour_height - bot_neighbour_height) / 2

            left_neighbour_height = self.get_height(hmap, x-1, z)
            right_neighbour_height = self.get_height(hmap, x+1, z)
            vecX = (left_neighbour_height - right_neighbour_height) / 2

            # Combine the vectors together to get the final vector (normal)
            final_vec = normalized(np.array([vecX, 1.0, vecZ]))
            return final_vec

    def draw(self, primitives=GL.GL_TRIANGLES, **uniforms):
        GL.glUseProgram(self.shader.glid)
        
        light_location = GL.glGetUniformLocation(self.shader.glid, 'light_dir')
        kd_loc = GL.glGetUniformLocation(self.shader.glid, 'k_d')
        s_loc = GL.glGetUniformLocation(self.shader.glid, 's')

        GL.glUniform3fv(light_location, 1, self.light)

        GL.glUniform3fv(kd_loc, 1, [0.9, 0.9, 0.9])
        GL.glUniform1f(s_loc, 100.0)

        for index, (name, texture) in enumerate(self.textures.items()):
            GL.glActiveTexture(GL.GL_TEXTURE0 + index)
            GL.glBindTexture(texture.type, texture.glid)
            uniforms[name] = index
        self.drawable.draw(primitives=primitives, **uniforms)

