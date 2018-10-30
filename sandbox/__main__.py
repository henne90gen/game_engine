from pyglet.gl import GL_ARRAY_BUFFER

import game_engine.window
import game_engine.game
from game_engine.shader import Shader
from game_engine.vertex_objects import VAO, VBO
import logging
LOG = logging.getLogger()


class Game(game_engine.game.BaseGame):
    def update(self, data: game_engine.game.BaseData):
        LOG.info("Updating", data)

    def render(self, data: game_engine.game.BaseData):
        LOG.info("Rendering", data)
        vbo = VBO(GL_ARRAY_BUFFER, [1, 1, -1, -1, 1, -1])
        vao = VAO()
        shader = Shader("sandbox/shader.vert", "sandbox/shader.frag")
        shader.bind()
        vao.draw()
        shader.unbind()


class Data(game_engine.game.BaseData):
    def __init__(self):
        super().__init__()
        self.objs = {}


if __name__ == "__main__":
    game_engine.window.window("Hello", Game(), Data())