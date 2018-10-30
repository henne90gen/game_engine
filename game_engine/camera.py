from pyglet.window import key

from game_engine.math import vec2, vec3, mat4, identity, translate, rotate
from game_engine.game import BaseData


class Camera:
    def __init__(self, position: vec3, rotation: vec3):
        self.position = position
        self.rotation = rotation

    def get_view_matrix(self) -> mat4:
        view_matrix = identity()
        translate(view_matrix, self.position * -1)
        rotate(view_matrix, self.rotation)
        return view_matrix

    def update(self, data: BaseData) -> None:
        move = vec2()
        if data.key_map[key.LEFT] and not data.key_map[key.RIGHT]:
            move.x = -1
        elif data.key_map[key.RIGHT] and not data.key_map[key.LEFT]:
            move.x = 1

        if data.key_map[key.DOWN] and not data.key_map[key.UP]:
            move.y = -1
        elif data.key_map[key.UP] and not data.key_map[key.DOWN]:
            move.y = 1

        speed = 0.5
        self.position.x += move.x * speed
        self.position.y += move.y * speed