import logging
import os
import inspect
from typing import List

import cv2
import numpy as np
from pyglet.gl import glGenTextures, glBindTexture, glTexParameterf, glTexImage2D, GLuint, GL_BGR, GL_RGB, GL_UNSIGNED_BYTE, GL_BYTE
from pyglet.gl import GL_RGBA, GL_RGB8, glFlush, glDrawArrays, GL_TRIANGLES
from pyglet.gl import GL_TEXTURE_2D, glActiveTexture, GL_TEXTURE0, GL_TEXTURE_MAG_FILTER, GL_TEXTURE_MIN_FILTER, GL_LINEAR, GLubyte

from game_engine.shader import Shader
from game_engine.vertex_objects import VBO, VAO, VertexAttribute, Uniform, array_buffer
from game_engine.math import vec3, vec2, identity

LOG = logging.getLogger()


class Texture:
    def __init__(self, image, f, t):
        self.image = image
        self.format = f
        self.type = t
        self.uploaded = False
        self.handle = GLuint()
        glGenTextures(1, self.handle)

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        self._image = value
        self.width = value.shape[1]
        self.height = value.shape[0]
        self.uploaded = False

    def upload(self):
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.handle)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

        texture_data = bytes(self.image.flat)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.width,
                     self.height, 0, self.format, self.type, texture_data)
        glFlush()
        self.uploaded = True

    def bind(self):
        if not self.uploaded:
            self.upload()
        else:
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, self.handle)

    def unbind(self):
        glBindTexture(GL_TEXTURE_2D, 0)


def load_image_from_mat(mat):
    img = cv2.flip(mat, 0)
    return Texture(img, GL_BGR, GL_UNSIGNED_BYTE)


def load_image_from_file(file_name: str):
    img = cv2.imread(file_name, cv2.IMREAD_COLOR)
    if img is None:
        LOG.error(f"Could not load image {file_name}")
        return None
    return load_image_from_mat(img)


def get_current_directory():
    return os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


TEXTURE_MESH_SHADER = None
COLOR_MESH_SHADER = None


class MeshSurface:
    def __init__(self, vertex_attributes: List[VertexAttribute], uniforms: List[Uniform]):
        self.vertex_attributes = vertex_attributes
        self.uniforms = uniforms
        self.vao = VAO()
        self.is_setup = False

    def setup(self):
        self.shader.bind()
        self.vao.bind()
        self.vertex_buffer.bind()

        for index, attrib in enumerate(self.vertex_attributes):
            attrib.bind(index, self.shader)
        self.is_setup = True

    def draw(self, uniforms: List[Uniform]):
        if not self.is_setup:
            self.setup()

        self.shader.bind()
        self.vao.bind()

        for uniform in self.uniforms + uniforms:
            uniform.bind(self.shader)

        glDrawArrays(GL_TRIANGLES, 0, len(self.vertex_buffer))

        self.vao.unbind()
        self.shader.unbind()


class ColorMeshSurface(MeshSurface):
    def __init__(self, points: List[vec3], colors: List[vec3]):
        attributes = [VertexAttribute('a_Position', 3, 6, 0),
                      VertexAttribute('a_Color', 3, 6, 3)]
        uniforms = [Uniform("u_Model", identity())]
        super().__init__(attributes, uniforms)
        data = []
        for point, color in zip(points, colors):
            data += point.to_list()
            data += color.to_list()
        self.vertex_buffer = array_buffer(data, 6)

        global COLOR_MESH_SHADER
        if COLOR_MESH_SHADER is None:
            dir_name = get_current_directory()
            COLOR_MESH_SHADER = Shader(
                f"{dir_name}/color.vert", f"{dir_name}/color.frag")
            LOG.info("Loaded color mesh shader")
        self.shader = COLOR_MESH_SHADER


class TextureMeshSurface(MeshSurface):
    def __init__(self, points: List[vec3], uvs: List[vec2], texture: Texture):
        attributes = [VertexAttribute('a_Position', 3, 5, 0),
                      VertexAttribute('a_UV', 2, 5, 3)]
        uniforms = [Uniform("u_TextureSampler", 0)]
        super().__init__(attributes, uniforms)
        data = []
        for point, uv in zip(points, uvs):
            data += point.to_list()
            data += uv.to_list()
        self.vertex_buffer = array_buffer(data, 5)
        self.texture = texture

        global TEXTURE_MESH_SHADER
        if TEXTURE_MESH_SHADER is None:
            dir_name = get_current_directory()
            TEXTURE_MESH_SHADER = Shader(
                f"{dir_name}/texture.vert", f"{dir_name}/texture.frag")
            LOG.info("Loaded texture mesh shader")
        self.shader = TEXTURE_MESH_SHADER

    def draw(self, additional_uniforms):
        self.texture.bind()
        found_model = list(
            filter(lambda u: u.name == "u_Model", additional_uniforms))
        if not found_model:
            additional_uniforms.append(Uniform("u_Model", identity()))
        super().draw(additional_uniforms)
        self.texture.unbind()
