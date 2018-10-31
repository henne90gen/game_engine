import logging
from typing import List

import cv2
from pyglet.gl import glGenTextures, glBindTexture, glTexParameterf, glTexImage2D, GLuint, GL_RGB, GL_UNSIGNED_BYTE
from pyglet.gl import GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_TEXTURE_MIN_FILTER, GL_LINEAR, GLubyte

from game_engine.vertex_objects import VBO, VertexAttribute, Uniform


LOG = logging.getLogger()


class Texture:
    def __init__(self, image, f, t):
        self.image = image
        self.width = image.shape[1]
        self.height = image.shape[0]
        self.format = f
        self.type = t
        self.uploaded = False
        self.handle = GLuint()
        glGenTextures(1, self.handle)

    def upload(self):
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        texture_data = (GLubyte * len(self.image.flat))(*self.image.flatten())
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.width,
                     self.height, 0, self.format, self.type, texture_data)
        self.uploaded = True

    def bind(self):
        glBindTexture(GL_TEXTURE_2D, self.handle)
        if not self.uploaded:
            self.upload()

    def unbind(self):
        glBindTexture(GL_TEXTURE_2D, 0)


def load_image(file_name: str):
    img = cv2.imread(file_name)
    if img is None:
        LOG.error(f"Could not load image {file_name}")
        return None
    return Texture(img, GL_RGB, GL_UNSIGNED_BYTE)


class Mesh:
    def __init__(self, vbos: List[VBO], vertex_attributes: List[VertexAttribute], uniforms: List[Uniform]):
        self.vbos = vbos
        self.vertex_attributes = vertex_attributes
        self.uniforms = uniforms
