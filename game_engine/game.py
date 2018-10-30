from game_engine.math import vec2


class BaseGame:
    def update(delta: float):
        pass

    def render(delta: float):
        pass


class BaseData:
    def __init__(self):
        self.frame_time = 0
        self.mouse_position = vec2()
        self.mouse_movement = vec2()
        self.key_map = {}

    def __repr__(self):
        result = "[BaseData "
        for key, val in self.__dict__.items():
            result += f"{key}={val}, "
        result = result[:-2]
        result += "]"
        return result

    def __str__(self):
        return self.__repr__()
