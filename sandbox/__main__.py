import logging
import threading
from typing import List
import cv2
import numpy as np
from pyglet.gl import GL_ARRAY_BUFFER

import game_engine.window
import game_engine.game
from game_engine.camera import Camera
from game_engine.shader import Shader
from game_engine.vertex_objects import VAO, array_buffer, VertexAttribute, Uniform
from game_engine.asset import TextureMeshSurface, ColorMeshSurface, load_image_from_file, load_image_from_mat
from game_engine.math import vec3, vec2, identity, scale, translate, rotate

LOG = logging.getLogger()


def to_vec_arr(arr, vector_size):
    result = []
    for i in range(0, len(arr), vector_size):
        if vector_size == 2:
            new_vector = vec2(arr[i], arr[i+1])
        elif vector_size == 3:
            new_vector = vec3(arr[i], arr[i+1], arr[i+2])
        else:
            print("Unsupported vector size")
            return []
        result.append(new_vector)
    return result


def to_vec3_arr(arr):
    return to_vec_arr(arr, 3)


def to_vec2_arr(arr):
    return to_vec_arr(arr, 2)


class Image:
    def __init__(self, path):
        texture = load_image_from_file(path)
        width_half = texture.width / texture.height * 10.0 / 2.0
        height_half = 10.0 / 2.0
        points = to_vec3_arr([
            width_half, height_half, 0,
            -width_half, -height_half, 0,
            width_half, -height_half, 0,
            width_half, height_half, 0,
            -width_half, height_half, 0,
            -width_half, -height_half, 0,
        ])
        uvs = to_vec2_arr([
            1, 1,
            0, 0,
            1, 0,
            1, 1,
            0, 1,
            0, 0,
        ])
        self.surface = TextureMeshSurface(points, uvs, texture)
        self.model_matrix = identity()

    def draw(self, uniforms: List[Uniform]):
        uniforms.append(Uniform("u_Model", self.model_matrix))
        self.surface.draw(uniforms)


class Video:
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        ret, self.next_frame = self.video.read()
        self.next_frame = cv2.flip(self.next_frame, -1)
        self.next_frame = cv2.resize(self.next_frame, (0, 0), fx=0.5, fy=0.5)

        texture = load_image_from_mat(self.next_frame)
        width_half = texture.width / texture.height * 10.0 / 2.0
        height_half = 10.0 / 2.0
        points = to_vec3_arr([
            width_half, height_half, 0,
            -width_half, -height_half, 0,
            width_half, -height_half, 0,
            width_half, height_half, 0,
            -width_half, height_half, 0,
            -width_half, -height_half, 0,
        ])
        uvs = to_vec2_arr([
            1, 1,
            0, 0,
            1, 0,
            1, 1,
            0, 1,
            0, 0,
        ])
        self.surface = TextureMeshSurface(points, uvs, texture)

    def draw(self, uniforms: List[Uniform]):
        ret, self.next_frame = self.video.read()
        self.next_frame = cv2.flip(self.next_frame, -1)
        self.next_frame = cv2.resize(self.next_frame, (0, 0), fx=0.5, fy=0.5)

        self.surface.texture.image = self.next_frame
        self.model_matrix = identity()

        uniforms.append(Uniform("u_Model", self.model_matrix))
        self.surface.draw(uniforms)


class Game(game_engine.game.BaseGame):
    def init(self):
        self.image = Image("sandbox/cat.jpg")
        self.video = Video()

    def update(self, data: game_engine.game.BaseData):
        LOG.info("Updating", data)
        data.camera.update(data)

    def render(self, data: game_engine.game.BaseData):
        LOG.info("Rendering", data)

        projection = Uniform("u_Projection", data.projection_matrix)
        view = Uniform("u_View", data.camera.get_view_matrix())
        uniforms = [projection, view]

        self.image.model_matrix = identity()
        translate(self.image.model_matrix, vec3(0, 10, 0))

        self.image.draw(uniforms)
        self.video.draw(uniforms)


class Data(game_engine.game.BaseData):
    def __init__(self):
        super().__init__()
        self.camera = Camera(vec3(0, 0, 15), vec3(0, 0, 0))


if __name__ == "__main__":
    game_engine.window.run_game("Hello", Game(), Data())
