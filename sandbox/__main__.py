from pyglet.gl import GL_ARRAY_BUFFER

import game_engine.window
import game_engine.game
from game_engine.camera import Camera
from game_engine.shader import Shader
from game_engine.vertex_objects import VAO, array_buffer, VertexAttribute, Uniform
from game_engine.asset import Mesh, load_image
from game_engine.renderer import draw
from game_engine.math import vec3, identity, scale, translate, rotate
import logging
LOG = logging.getLogger()


class Game(game_engine.game.BaseGame):
    def __init__(self):
        super().__init__()
        self.texture = load_image("sandbox/kitten.jpg")

    def update(self, data: game_engine.game.BaseData):
        LOG.info("Updating", data)
        data.camera.update(data)

    def render(self, data: game_engine.game.BaseData):
        LOG.info("Rendering", data)
        triangles = [
            Mesh([array_buffer([10, 10, 0, -10, -10, 0, 10, -10, 0])],
                  [VertexAttribute('a_Position', 3, 0)],
                  [Uniform("u_Color", vec3(1.0, 0.0, 0.0)), Uniform("u_Model", identity())]),
            Mesh([array_buffer([10, 10, 0, -10, 10, 0, -10, -10, 0])],
                  [VertexAttribute('a_Position', 3, 0)],
                  [Uniform("u_Color", vec3(0.0, 1.0, 0.0)), Uniform("u_Model", identity())]),
            Mesh([array_buffer([10, 10, 0, -10, 20, -5, -10, 10, 0])],
                  [VertexAttribute('a_Position', 3, 0)],
                  [Uniform("u_Color", vec3(0.0, 0.0, 1.0)), Uniform("u_Model", identity())]),
            Mesh([array_buffer([-10, -10, 0, -10, 10, 0, -10, 20, -5])],
                  [VertexAttribute('a_Position', 3, 0)],
                  [Uniform("u_Color", vec3(1.0, 0.0, 1.0)), Uniform("u_Model", identity())]),
        ]

        vao = VAO()
        shader = Shader("sandbox/shader.vert", "sandbox/shader.frag")
        projection = Uniform("u_Projection", data.projection_matrix)
        view = Uniform("u_View", data.camera.get_view_matrix())

        for triangle in triangles:
            uniforms = [projection, view] + triangle.uniforms
            draw(vao, triangle.vbos[0],
                 triangle.vertex_attributes, uniforms, shader, self.texture)


class Data(game_engine.game.BaseData):
    def __init__(self):
        super().__init__()
        self.camera = Camera(vec3(0, 0, 15), vec3(0, 0, 0))


if __name__ == "__main__":
    game_engine.window.run_game("Hello", Game(), Data())
