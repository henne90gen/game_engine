from typing import List

from pyglet.gl import glDrawArrays, GL_TRIANGLES

from game_engine.vertex_objects import VAO, VBO, VertexAttribute, Uniform
from game_engine.shader import Shader
from game_engine.asset import Texture


def draw(vao: VAO, vbo: VBO, vertex_attributes: List[VertexAttribute], uniforms: List[Uniform], shader: Shader, texture: Texture):
    shader.bind()
    vao.bind()
    vbo.bind()
    texture.bind()

    for uniform in uniforms:
        uniform.bind(shader)

    for index, attrib in enumerate(vertex_attributes):
        attrib.bind(index, shader)

    glDrawArrays(GL_TRIANGLES, 0, len(vbo))

    texture.unbind()
    vbo.unbind()
    vao.unbind()
    shader.unbind()
