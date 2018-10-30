from pyglet.gl import GL_STATIC_DRAW, glBufferData, glBindBuffer, glGenBuffers
from pyglet.gl import GLuint, GLfloat, glGenVertexArrays


class VBO:
    def __init__(self, buffer_type, data):
        self.type = buffer_type
        self.handle = GLuint()
        glGenBuffers(1, self.handle)

    def bind(self):
        glBindBuffer(self.type, self.handle)

    def upload(self, usage=GL_STATIC_DRAW):
        size = sizeof(self.data)
        data_gl = (GLfloat * len(self.data))(*self.data)
        glBufferData(self.type, size, data_gl, usage)


class VAO:
    def __init__(self, *args, **kwargs):
        self.handle = GLuint()
        glGenVertexArrays(1, self.handle)

    def bind(self):
        glBindVertexArray(self.handle)

    def draw(self):
        pass
