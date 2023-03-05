#!/usr/bin/env python3
"""
Python OpenGL practical application.
"""

import glfw                        # lean window system wrapper for OpenGL
import numpy as np                 # all matrix manipulations & OpenGL args
import math

from transform import lookat, normalized

class Camera:
    def __init__(self, camera_pos, worldup, yaw=0.0, pitch=0.0, speed=20.0, sensitivity=45, zoom=45.0):
        # Set the camera position
        self.position = camera_pos
        self.world_up = worldup
        self.yaw = yaw
        self.pitch = pitch
        self.speed = speed
        self.sensitivity = sensitivity
        self.zoom = zoom
        self.updateCameraVectors()

    def updateCameraVectors(self):
        front = np.array((0.0, 0.0, 0.0))
        front[0] = math.cos(math.radians(self.yaw)) * math.cos(math.radians(self.pitch))
        front[1] = math.sin(math.radians(self.pitch))
        front[2] = math.sin(math.radians(self.yaw)) * math.cos(math.radians(self.pitch))
        self.front = normalized(front)
        self.right = normalized(np.cross(self.front, self.world_up))

    def get_view_matrix(self):
        return lookat(eye=self.position, target=self.position+self.front, up=self.world_up)

    def camera_key_handler(self, window, deltaTime):
        move_speed = self.speed * deltaTime
        rotate_speed = self.sensitivity * deltaTime
        if glfw.get_key(window, glfw.KEY_W):
            # W - Move forward according to which direction the camera is facing
            self.position += move_speed * self.front
        if glfw.get_key(window, glfw.KEY_S):
            # S - Move backward
            self.position -= move_speed * self.front
        if glfw.get_key(window, glfw.KEY_A):
            # A - Move Left
            self.position -= move_speed * self.right
        if glfw.get_key(window, glfw.KEY_D):
            # D - Move Right
            self.position += move_speed * self.right
        if glfw.get_key(window, glfw.KEY_Q):
            # Q - Move Up
            self.position += move_speed * self.world_up
        if glfw.get_key(window, glfw.KEY_E):
            # E - Move Down
            self.position -= move_speed * self.world_up
        if glfw.get_key(window, glfw.KEY_LEFT):
            # ArrowRLEFT - Turn left : yaw-
            self.yaw -= rotate_speed
            self.updateCameraVectors()
        if glfw.get_key(window, glfw.KEY_RIGHT):
            # ArrowRIGHT - Turn right : yaw+
            self.yaw += rotate_speed
            self.updateCameraVectors()
        if glfw.get_key(window, glfw.KEY_UP):
            # ArrowUP - Turn up : pitch++
            self.pitch += rotate_speed
            if self.pitch > 89.0 : 
                self.pitch = 89.0
            self.updateCameraVectors()
        if glfw.get_key(window, glfw.KEY_DOWN):
            # ArrowDOWN - Turn down : pitch--
            self.pitch -= rotate_speed
            if self.pitch < -89.0 : 
                self.pitch = -89.0
            self.updateCameraVectors()
        if glfw.get_key(window, glfw.KEY_1):
            # ArrowDOWN - Turn down : pitch--
            self.position = np.array((-16, 17.0, -103.0))
            self.yaw = 78
            self.pitch = -6.0
            self.updateCameraVectors()
        if glfw.get_key(window, glfw.KEY_2):
            # ArrowDOWN - Turn down : pitch--
            self.position = np.array((12, 19.0, -36.0))
            self.yaw = -84
            self.pitch = 0.0
            self.updateCameraVectors()
        if glfw.get_key(window, glfw.KEY_0):
            # ArrowDOWN - Turn down : pitch--
            self.position = np.array((-80, 15.0, 0.0))
            self.yaw = 0
            self.pitch = 0.0
            self.updateCameraVectors()
        # print("Position:", self.position, "yaw:", self.yaw, "pitch:", self.pitch)