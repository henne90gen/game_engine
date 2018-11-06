from ctypes import sizeof
from typing import List
import logging

from pyglet.gl import GL_STATIC_DRAW, glBufferData, glBindBuffer, glGenBuffers
from pyglet.gl import GLuint, GLfloat, GLint, GL_FLOAT, glGenVertexArrays, glBindVertexArray
from pyglet.gl import GL_TRIANGLES, glDrawArrays, GL_FALSE, GL_ARRAY_BUFFER
from pyglet.gl import glVertexAttribPointer, glEnableVertexAttribArray, glBindAttribLocation

from game_engine.shader import Shader

LOG = logging.getLogger()


class VBO:
    def __init__(self, buffer_type, nums_per_vertex, data, data_type):
        self.type = buffer_type
        self.nums_per_vertex = nums_per_vertex
        self.uploaded = False
        self.data = data
        self.data_type = data_type
        self.handle = GLuint()
        glGenBuffers(1, self.handle)

    def bind(self):
        glBindBuffer(self.type, self.handle)
        if not self.uploaded:
            self.upload()

    def unbind(self):
        glBindBuffer(self.type, 0)

    def upload(self, usage=GL_STATIC_DRAW):
        data_gl = (self.data_type * len(self.data))(*self.data)
        size = sizeof(data_gl)
        glBufferData(self.type, size, data_gl, usage)
        self.uploaded = True

    def __len__(self):
        return len(self.data) // self.nums_per_vertex


def array_buffer(vertices: list, nums_per_vertex=3):
    return VBO(GL_ARRAY_BUFFER, nums_per_vertex, vertices, GLfloat)


def index_buffer(indices: list):
    return VBO(GL_ELEMENT_ARRAY_BUFFER, 2, indices, GLint)


class VAO:
    def __init__(self):
        self.handle = GLuint()
        glGenVertexArrays(1, self.handle)

    def bind(self):
        glBindVertexArray(self.handle)

    @staticmethod
    def unbind():
        glBindVertexArray(0)

    def __repr__(self):
        return f"VAO({self.handle})"

    def __str__(self):
        return self.__repr__()


class VertexAttribute:
    def __init__(self, name, vertex_size, stride, offset):
        self.name = name
        self.vertex_size = vertex_size
        self.stride = stride
        self.offset = offset

    def bind(self, location: int, shader: Shader):
        stride = self.stride * sizeof(GLfloat)
        offset = self.offset * sizeof(GLfloat)
        glVertexAttribPointer(location, self.vertex_size,
                              GL_FLOAT, GL_FALSE, stride, offset)
        glBindAttribLocation(shader.handle, location,
                             bytes(self.name, "utf-8"))
        glEnableVertexAttribArray(location)


class Uniform:
    def __init__(self, name, data):
        self.name = name
        self.data = data

    def bind(self, shader: Shader):
        shader.uniform(self.name, self.data)
