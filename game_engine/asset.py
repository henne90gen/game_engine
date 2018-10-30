from typing import List
from game_engine.vertex_objects import VBO, VertexAttribute, Uniform

import cv2


class Texture:
    def __init__(self, image):
        self.image = image
        self.width = image.cols
        self.height = image.rows


def load_image(file_name: str):
    img = cv2.imread(file_name)
    return Texture(img)


class Mesh:
    def __init__(self, vbos: List[VBO], vertex_attributes: List[VertexAttribute], uniforms: List[Uniform]):
        self.vbos = vbos
        self.vertex_attributes = vertex_attributes
        self.uniforms = uniforms
