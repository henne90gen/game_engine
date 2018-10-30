import math
from datetime import datetime

import pyglet
from pyglet.gl import glEnable, GL_DEPTH_TEST, GL_BLEND, glBlendFunc, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA
from pyglet.gl import glClearColor, glViewport

from game_engine.math import identity, mat4, vec2
from game_engine.game import BaseGame, BaseData


class Window(pyglet.window.Window):
    def __init__(self,  name: str, width: int, height: int, resizable: bool = False, game: BaseGame = None, data: BaseData = None):
        super(Window, self).__init__(width, height, resizable=resizable)

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glClearColor(0, 0, 0, 1)

        # glEnable(GL_CULL_FACE)

        self.name = name
        self.num_frames = 0
        self.start_time = datetime.now()
        self.frame_start_time = datetime.now()

        self.projection_matrix = identity()

        if game is None:
            game = BaseGame()
        self.game = game

        if data is None:
            data = BaseData()
        self.data = data

    def show_average_time(self):
        self.num_frames += 1
        end = datetime.now()
        diff = end - self.start_time
        average = diff.total_seconds() * 1000.0 / self.num_frames
        caption = f"{self.name} {'%.5f' % average}"
        self.set_caption(caption)

        if diff.total_seconds() > 1:
            self.start_time = end
            self.num_frames = 0

    def on_draw(self, *args):
        end = datetime.now()
        frame_time = (end - self.frame_start_time).total_seconds()
        self.frame_start_time = datetime.now()

        self.clear()

        self.data.frame_time = frame_time
        self.data.projection_matrix = self.projection_matrix
        self.game.update(self.data)
        self.game.render(self.data)

        self.show_average_time()

    def on_resize(self, width, height):
        glViewport(0, 0, width, height)

        # if self.game_data.show_overview:
        #     self.orthographic_projection(width, height)
        # else:
        self.perspective_projection(width, height)

    def orthographic_projection(self, width, height):
        z_near = 1
        z_far = 500
        temp1 = -2 / (z_far - z_near)
        temp2 = -1 * (z_far + z_near) / (z_far - z_near)
        self.projection_matrix = mat4([
            [2 / width, 0, 0, 0],
            [0, 2 / height, 0, 0],
            [0, 0, temp1, temp2],
            [0, 0, 0, 1],
        ])

    def perspective_projection(self, width, height):
        aspect_ratio = width / height
        fovy = 75
        z_near = 1
        z_far = 1000
        f = 1 / (math.tan(fovy * math.pi / 360))
        temp1 = (z_far + z_near) / (z_near - z_far)
        temp2 = (2 * z_far * z_near) / (z_near - z_far)
        self.projection_matrix = mat4([
            [f / aspect_ratio, 0, 0, 0],
            [0, f, 0, 0],
            [0, 0, temp1, temp2],
            [0, 0, -1, 0],
        ])

    def on_key_press(self, symbol, modifiers):
        self.data.key_map[symbol] = True

    def on_key_release(self, symbol, modifiers):
        self.data.key_map[symbol] = False

    def on_mouse_motion(self, x, y, dx, dy):
        self.data.mouse_movement = vec2(dx, dy)
        self.data.mouse_position = vec2(x, y)


def run_game(name: str, game: BaseGame, data: BaseData):
    window = Window(name=name, width=1280, height=720,
                    resizable=True, game=game, data=data)

    pyglet.clock.schedule_interval(window.on_draw, 1 / 120.0)
    pyglet.app.run()
