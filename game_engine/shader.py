import logging
from builtins import bytes
from ctypes import (
    byref, c_char, c_char_p, c_int, c_float, cast, create_string_buffer, pointer,
    POINTER, addressof
)

from pyglet.gl import glCreateProgram, glDeleteProgram, GL_VERTEX_SHADER, GL_FRAGMENT_SHADER, glCreateShader
from pyglet.gl import glCompileShader, glGetShaderiv, glShaderSource, GL_COMPILE_STATUS, glGetShaderInfoLog
from pyglet.gl import glAttachShader, GL_INFO_LOG_LENGTH, glLinkProgram, glGetProgramiv, GL_LINK_STATUS
from pyglet.gl import glGetProgramInfoLog, glUseProgram, glGetUniformLocation, glUniform1f, glUniform2f
from pyglet.gl import glUniform3f, glUniform4f, glUniformMatrix4fv, glUniform1i, glUniform2i, glUniform3i
from pyglet.gl import glUniform4i

from game_engine.math import mat4, vec3, vec2


class Shader:
    def __init__(self, vertex_shader_name: str = "", fragment_shader_name: str = ""):
        self.log = logging.getLogger(__name__)
        self.log.setLevel(logging.INFO)

        self.handle = None
        self.linked = False
        self.vertex_shader_name = vertex_shader_name
        self.fragment_shader_name = fragment_shader_name

        self.compile()

    def compile(self):
        if self.handle is not None:
            glDeleteProgram(self.handle)
        self.handle = glCreateProgram()

        if len(self.vertex_shader_name) > 0:
            with open(self.vertex_shader_name) as f:
                vertex_source = f.readlines()
            self.create_shader(vertex_source, GL_VERTEX_SHADER)

        if len(self.fragment_shader_name) > 0:
            with open(self.fragment_shader_name) as f:
                fragment_source = f.readlines()
            self.create_shader(fragment_source, GL_FRAGMENT_SHADER)

        self.link()

    def create_shader(self, strings, t):
        count = len(strings)
        # if we have no source code, ignore this shader
        if count <= 0:
            self.log.info("Source string was empty. Not doing anything")
            return

        shader = glCreateShader(t)

        string_buffers = [
            create_string_buffer(bytes(s, "utf-8")) for s in strings]
        src = (c_char_p * count)(*map(addressof, string_buffers))
        glShaderSource(shader, count, cast(
            pointer(src), POINTER(POINTER(c_char))), None)

        glCompileShader(shader)

        if self.was_compile_successful(shader):
            glAttachShader(self.handle, shader)
        else:
            self.log.warn("Could not compile shader")

    def was_compile_successful(self, shader):
        status = c_int(0)
        glGetShaderiv(shader, GL_COMPILE_STATUS, byref(status))
        if not status:
            glGetShaderiv(shader, GL_INFO_LOG_LENGTH, byref(status))
            buffer = create_string_buffer(status.value)
            glGetShaderInfoLog(shader, status, None, buffer)
            self.log.error(f"{buffer.value}")
        return status

    def link(self):
        glLinkProgram(self.handle)

        if self.was_link_successful():
            self.linked = True
        else:
            self.log.warn("Could not link shader program")

    def was_link_successful(self):
        status = c_int(0)
        glGetProgramiv(self.handle, GL_LINK_STATUS, byref(status))
        if not status:
            glGetProgramiv(self.handle, GL_INFO_LOG_LENGTH, byref(status))
            buffer = create_string_buffer(status.value)
            glGetProgramInfoLog(self.handle, status, None, buffer)
            self.log.error(f"{buffer.value}")
        return status

    def bind(self):
        glUseProgram(self.handle)

    @staticmethod
    def unbind():
        glUseProgram(0)

    def uniform(self, name: str, data, index: int = -1):
        if index > -1:
            name = f"{name}[{index}]"

        self.log.debug(f"Binding {name} with data: {data}")

        data_type = type(data)
        if data_type == mat4:
            self.uniform_matrixf(name, data)

        elif data_type in [vec2, vec3]:
            self.uniformf(name, *data)

        elif data_type == float:
            self.uniformf(name, data)

        elif data_type == int:
            self.uniformi(name, data)

        elif data_type == list:
            for index, d in enumerate(data):
                self.uniform(name, d, index)

        elif data_type == dict:
            for key in data:
                self.uniform(f"{name}.{key}", data[key])

        else:
            self.log.error(f"Could not bind {name}")
            return
        self.log.debug(f"Bound {name} with data: {data}")

    def uniformf(self, name: str, *vals):
        # upload a floating point uniform
        # this program must be currently bound
        # check there are 1-4 values
        if len(vals) in range(1, 5):
            c_vals = list(map(c_float, vals))
            # location = glGetUniformLocation(
            #     self.handle, c_char_p(name.encode("utf-8")))
            location = glGetUniformLocation(
                self.handle, bytes(name, "utf-8"))
            # select the correct function
            uniform_functions = {
                1: glUniform1f,
                2: glUniform2f,
                3: glUniform3f,
                4: glUniform4f
            }
            uniform_functions[len(c_vals)](location, *c_vals)

    def uniformi(self, name: str, *vals):
        # upload an integer uniform
        # this program must be currently bound
        # check there are 1-4 values
        if len(vals) in range(1, 5):
            c_vals = list(map(c_int, vals))
            # select the correct function
            location = glGetUniformLocation(
                self.handle, c_char_p(name.encode("utf-8")))
            uniform_functions = {1: glUniform1i,
                                 2: glUniform2i, 3: glUniform3i, 4: glUniform4i}
            uniform_functions[len(c_vals)](location, *c_vals)

    def uniform_matrixf(self, name: str, mat: mat4):
        # upload a uniform matrix
        # works with matrices stored as lists,
        # as well as euclid matrices
        # obtain the uniform location
        location = glGetUniformLocation(
            self.handle, c_char_p(name.encode("utf-8")))
        # upload the 4x4 floating point matrix
        mat_values = mat.to_list()
        # noinspection PyCallingNonCallable, PyTypeChecker
        glUniformMatrix4fv(location, 1, True, (c_float * 16)(*mat_values))
