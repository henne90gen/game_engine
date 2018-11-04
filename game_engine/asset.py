import logging
from typing import List

import cv2
import numpy as np
from pyglet.gl import glGenTextures, glBindTexture, glTexParameterf, glTexImage2D, GLuint, GL_BGR, GL_RGB, GL_UNSIGNED_BYTE, GL_BYTE
from pyglet.gl import GL_RGBA, GL_RGB8, glFlush
from pyglet.gl import GL_TEXTURE_2D, glActiveTexture, GL_TEXTURE0, GL_TEXTURE_MAG_FILTER, GL_TEXTURE_MIN_FILTER, GL_LINEAR, GLubyte

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
        glBindTexture(GL_TEXTURE_2D, self.handle)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

        texture_data = bytes(self.image.flat)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.width,
                     self.height, 0, self.format, self.type, texture_data)
        glFlush()
        self.uploaded = True

    def bind(self):
        if not self.uploaded:
            self.upload()
        else:
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, self.handle)

    def unbind(self):
        glBindTexture(GL_TEXTURE_2D, 0)


def load_image(file_name: str):
    img = cv2.imread(file_name, cv2.IMREAD_COLOR)
    if img is None:
        LOG.error(f"Could not load image {file_name}")
        return None
    img = cv2.flip(img, 0)
    return Texture(img, GL_BGR, GL_UNSIGNED_BYTE)


class Mesh:
    def __init__(self, vbos: List[VBO], vertex_attributes: List[VertexAttribute], uniforms: List[Uniform]):
        self.vbos = vbos
        self.vertex_attributes = vertex_attributes
        self.uniforms = uniforms
