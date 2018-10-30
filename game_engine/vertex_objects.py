from ctypes import sizeof
from typing import List

from pyglet.gl import GL_STATIC_DRAW, glBufferData, glBindBuffer, glGenBuffers
from pyglet.gl import GLuint, GLfloat, GL_FLOAT, glGenVertexArrays, glBindVertexArray
from pyglet.gl import GL_TRIANGLES, glDrawArrays, GL_FALSE
from pyglet.gl import glVertexAttribPointer, glEnableVertexAttribArray, glBindAttribLocation

from game_engine.shader import Shader


class VBO:
    def __init__(self, buffer_type, floats_per_vertex, data):
        self.type = buffer_type
        self.floats_per_vertex = floats_per_vertex
        self.uploaded = False
        self.data = data
        self.handle = GLuint()
        glGenBuffers(1, self.handle)

    def bind(self):
        glBindBuffer(self.type, self.handle)
        if not self.uploaded:
            self.upload()

    def unbind(self):
        glBindBuffer(self.type, 0)

    def upload(self, usage=GL_STATIC_DRAW):
        data_gl = (GLfloat * len(self.data))(*self.data)
        size = sizeof(data_gl)
        glBufferData(self.type, size, data_gl, usage)
        self.uploaded = True

    def __len__(self):
        return len(self.data) // self.floats_per_vertex


class VAO:
    def __init__(self):
        self.handle = GLuint()
        glGenVertexArrays(1, self.handle)

    def bind(self):
        glBindVertexArray(self.handle)

    @staticmethod
    def unbind():
        glBindVertexArray(0)


class VertexAttribute:
    def __init__(self, location, name, vertex_size, offset):
        self.location = location
        self.name = name
        self.vertex_size = vertex_size
        self.offset = offset

    def bind(self, shader: Shader):
        glEnableVertexAttribArray(self.location)
        stride = self.vertex_size * sizeof(GLfloat)
        glVertexAttribPointer(self.location, self.vertex_size,
                              GL_FLOAT, GL_FALSE, stride, 0)
        glBindAttribLocation(shader.handle, self.location,
                             bytes(self.name, "utf-8"))


class Uniform:
    def __init__(self, name, data):
        self.name = name
        self.data = data

    def bind(self, shader: Shader):
        shader.uniform(self.name, self.data)


def draw(vao: VAO, vbo: VBO, vertex_attributes: List[VertexAttribute], uniforms: List[Uniform], shader: Shader):
    shader.bind()
    vao.bind()
    vbo.bind()

    for uniform in uniforms:
        uniform.bind(shader)

    for attrib in vertex_attributes:
        attrib.bind(shader)

    glDrawArrays(GL_TRIANGLES, 0, len(vbo))

    vbo.unbind()
    vao.unbind()
    shader.unbind()
