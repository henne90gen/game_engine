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
        if data.keyboard.keys[key.LEFT] and not data.keyboard.keys[key.RIGHT]:
            move.x = -1
        elif data.keyboard.keys[key.RIGHT] and not data.keyboard.keys[key.LEFT]:
            move.x = 1

        if data.keyboard.keys[key.DOWN] and not data.keyboard.keys[key.UP]:
            move.y = -1
        elif data.keyboard.keys[key.UP] and not data.keyboard.keys[key.DOWN]:
            move.y = 1

        move_speed = 0.5
        self.position.x += move.x * move_speed
        self.position.y += move.y * move_speed

        horizontal_rotation = 0
        if data.keyboard.keys[key.Q] and not data.keyboard.keys[key.E]:
            horizontal_rotation = -1
        elif data.keyboard.keys[key.E] and not data.keyboard.keys[key.Q]:
            horizontal_rotation = 1

        rotation_speed = 1
        self.rotation.y += horizontal_rotation * rotation_speed
