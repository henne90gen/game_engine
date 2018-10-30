from typing import List
from game_engine.vertex_objects import VBO, VertexAttribute, Uniform


class Mesh:
    def __init__(self, vbos: List[VBO], vertex_attributes: List[VertexAttribute], uniforms: List[Uniform]):
        self.vbos = vbos
        self.vertex_attributes = vertex_attributes
        self.uniforms = uniforms
