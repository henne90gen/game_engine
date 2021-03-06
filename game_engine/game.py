from collections import defaultdict

from game_engine.math import vec2, identity


class Mouse:
    def __init__(self, *args, **kwargs):
        self.position = vec2()
        self.movement = vec2()


class Keyboard:
    def __init__(self, *args, **kwargs):
        self.keys = defaultdict(lambda: False)


class WindowData:
    def __init__(self, *args, **kwargs):
        self.width = 0
        self.height = 0


class BaseGame:
    def init(self):
        pass

    def update(self, delta: float):
        pass

    def render(self, delta: float):
        pass


class BaseData:
    def __init__(self):
        self.frame_time = 0
        self.mouse = Mouse()
        self.keyboard = Keyboard()
        self.window = WindowData()
        self.projection_matrix = identity()

    def __repr__(self):
        result = "[BaseData "
        for key, val in self.__dict__.items():
            result += f"{key}={val}, "
        result = result[:-2]
        result += "]"
        return result

    def __str__(self):
        return self.__repr__()
