from pyglet.gl import GL_ARRAY_BUFFER

import game_engine.window
import game_engine.game
from game_engine.camera import Camera
from game_engine.shader import Shader
from game_engine.vertex_objects import VAO, VBO, VertexAttribute, Uniform
from game_engine.renderer import draw
from game_engine.math import vec3, identity, scale, translate, rotate
import logging
LOG = logging.getLogger()


class Game(game_engine.game.BaseGame):
    def update(self, data: game_engine.game.BaseData):
        LOG.info("Updating", data)
        data.camera.update(data)

    def render(self, data: game_engine.game.BaseData):
        LOG.info("Rendering", data)
        triangles = [
            (VBO(GL_ARRAY_BUFFER, 2, [10, 10, 0, -10, -10, 0, 10, -10, 0]),
             VertexAttribute(0, 'a_Position', 3, 0),
             Uniform("u_Color", vec3(1.0, 0.0, 0.0))),
            (VBO(GL_ARRAY_BUFFER, 2, [10, 10, 0, -10, 10, 0, -10, -10, 0]),
             VertexAttribute(0, 'a_Position', 3, 0),
             Uniform("u_Color", vec3(0.0, 1.0, 0.0))),
            (VBO(GL_ARRAY_BUFFER, 2, [10, 10, 0, -10, 20, -5, -10, 10, 0]),
             VertexAttribute(0, 'a_Position', 3, 0),
             Uniform("u_Color", vec3(0.0, 0.0, 1.0))),
            (VBO(GL_ARRAY_BUFFER, 2, [-10, -10, 0, -10, 10, 0, -10, 20, -5]),
             VertexAttribute(0, 'a_Position', 3, 0),
             Uniform("u_Color", vec3(1.0, 0.0, 1.0))),
        ]
        vao = VAO()
        shader = Shader("sandbox/shader.vert", "sandbox/shader.frag")
        projection = Uniform("u_Projection", data.projection_matrix)
        view = Uniform("u_View", data.camera.get_view_matrix())
        model = Uniform("u_Model", identity())

        for vbo, attrib, color in triangles:
            uniforms = [color, projection, view, model]
            draw(vao, vbo, [attrib], uniforms, shader)


class Data(game_engine.game.BaseData):
    def __init__(self):
        super().__init__()
        self.camera = Camera(vec3(0, 0, 15), vec3(0, 0, 0))


if __name__ == "__main__":
    game_engine.window.run_game("Hello", Game(), Data())
