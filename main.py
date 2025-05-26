import OpenGL.GL as GL
import glfw
import numpy as np
import pyrr
import ctypes
import os
from PIL import Image
from GLprogram import create_program_from_file

class Game(object):
    def __init__(self):
        self.position = np.array([0.0, 0.0], dtype=np.float32)
        self.window = self.init_window()
        self.init_context()
        self.init_programs()
        self.init_data()
        self.rotation_matrix = pyrr.matrix44.create_identity(dtype=np.float32)
        self.projection = pyrr.matrix44.create_perspective_projection(50.0, 1.0, 0.5, 10.0, dtype=np.float32)
        self.z = -3.0

    def init_window(self):
        glfw.init()
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.RESIZABLE, False)
        window = glfw.create_window(800, 800, 'OpenGL', None, None)
        glfw.set_input_mode(window, glfw.STICKY_KEYS, glfw.TRUE)
        glfw.set_key_callback(window, self.key_callback)
        return window

    def init_context(self):
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)
        GL.glEnable(GL.GL_DEPTH_TEST)

    def init_programs(self):
        self.program = create_program_from_file("shaders/shader.vert", "shaders/shader.frag")
        GL.glUseProgram(self.program)

    def load_texture(self, filename):
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Texture not found: {filename}")
        im = Image.open(filename).transpose(Image.Transpose.FLIP_TOP_BOTTOM).convert('RGBA')
        texture_id = GL.glGenTextures(1)
        GL.glBindTexture(GL.GL_TEXTURE_2D, texture_id)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_REPEAT)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_REPEAT)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
        GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA, im.width, im.height, 0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, im.tobytes())
        return texture_id

    def init_data(self):
        data = np.array([
            0.0, 0.0, 0.0, 0, 0, 1,    1, 0, 0,     0, 0,
            1.0, 0.0, 0.0, 0, 0, 1,    0, 1, 0,     1, 0,
            0.0, 1.0, 0.0, 0, 0, 1,    0, 0, 1,     0, 1,
            0.0, 0.0, 1.0, 0, 0, 1,    1, 1, 0,     1, 1
        ], dtype=np.float32)

        indices = np.array([0, 1, 2, 0, 1, 3], dtype=np.uint32)

        self.vao = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.vao)

        self.vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, data.nbytes, data, GL.GL_STATIC_DRAW)

        self.ebo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL.GL_STATIC_DRAW)

        stride = 11 * ctypes.sizeof(ctypes.c_float)
        offset = 0
        GL.glEnableVertexAttribArray(0)
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, stride, ctypes.c_void_p(offset))

        offset += 3 * ctypes.sizeof(ctypes.c_float)
        GL.glEnableVertexAttribArray(1)
        GL.glVertexAttribPointer(1, 3, GL.GL_FLOAT, GL.GL_FALSE, stride, ctypes.c_void_p(offset))

        offset += 3 * ctypes.sizeof(ctypes.c_float)
        GL.glEnableVertexAttribArray(2)
        GL.glVertexAttribPointer(2, 3, GL.GL_FLOAT, GL.GL_FALSE, stride, ctypes.c_void_p(offset))

        offset += 3 * ctypes.sizeof(ctypes.c_float)
        GL.glEnableVertexAttribArray(3)
        GL.glVertexAttribPointer(3, 2, GL.GL_FLOAT, GL.GL_FALSE, stride, ctypes.c_void_p(offset))

        self.texture = self.load_texture("textures/brique.png")
        GL.glUseProgram(self.program)
        GL.glUniform1i(GL.glGetUniformLocation(self.program, "texture"), 0)

        GL.glBindVertexArray(0)

    def run(self):
        last_time = glfw.get_time()
        while not glfw.window_should_close(self.window):
            current_time = glfw.get_time()
            delta = current_time - last_time
            last_time = current_time

            # Contrôles clavier
            if glfw.get_key(self.window, glfw.KEY_LEFT) == glfw.PRESS:
                self.position[0] -= 1.0 * delta
            if glfw.get_key(self.window, glfw.KEY_RIGHT) == glfw.PRESS:
                self.position[0] += 1.0 * delta
            if glfw.get_key(self.window, glfw.KEY_UP) == glfw.PRESS:
                self.position[1] += 1.0 * delta
            if glfw.get_key(self.window, glfw.KEY_DOWN) == glfw.PRESS:
                self.position[1] -= 1.0 * delta
            if glfw.get_key(self.window, glfw.KEY_Y) == glfw.PRESS:
                self.z += 1.0 * delta
            if glfw.get_key(self.window, glfw.KEY_H) == glfw.PRESS:
                self.z -= 1.0 * delta
            if glfw.get_key(self.window, glfw.KEY_K) == glfw.PRESS:
                rot_x = pyrr.matrix44.create_from_x_rotation(2 * delta)
                self.rotation_matrix = pyrr.matrix44.multiply(rot_x, self.rotation_matrix)
            if glfw.get_key(self.window, glfw.KEY_I) == glfw.PRESS:
                rot_x = pyrr.matrix44.create_from_x_rotation(-2 * delta)
                self.rotation_matrix = pyrr.matrix44.multiply(rot_x, self.rotation_matrix)
            if glfw.get_key(self.window, glfw.KEY_L) == glfw.PRESS:
                rot_y = pyrr.matrix44.create_from_y_rotation(2 * delta)
                self.rotation_matrix = pyrr.matrix44.multiply(rot_y, self.rotation_matrix)
            if glfw.get_key(self.window, glfw.KEY_J) == glfw.PRESS:
                rot_y = pyrr.matrix44.create_from_y_rotation(-2 * delta)
                self.rotation_matrix = pyrr.matrix44.multiply(rot_y, self.rotation_matrix)

            GL.glClearColor(0.1, 0.1, 0.1, 1.0)
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

            translation = pyrr.matrix44.create_from_translation([*self.position, self.z], dtype=np.float32)
            model = pyrr.matrix44.multiply(translation, self.rotation_matrix)

            view = pyrr.matrix44.create_look_at([0, 0, 3], [0, 0, 0], [0, 1, 0], dtype=np.float32)

            GL.glUseProgram(self.program)
            GL.glUniformMatrix4fv(GL.glGetUniformLocation(self.program, "model"), 1, GL.GL_FALSE, model)
            GL.glUniformMatrix4fv(GL.glGetUniformLocation(self.program, "view"), 1, GL.GL_FALSE, view)
            GL.glUniformMatrix4fv(GL.glGetUniformLocation(self.program, "projection"), 1, GL.GL_FALSE, self.projection)

            GL.glActiveTexture(GL.GL_TEXTURE0)
            GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture)

            GL.glBindVertexArray(self.vao)
            GL.glDrawElements(GL.GL_TRIANGLES, 6, GL.GL_UNSIGNED_INT, None)
            GL.glBindVertexArray(0)

            glfw.swap_buffers(self.window)
            glfw.poll_events()

    def key_callback(self, win, key, scancode, action, mods):
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(win, glfw.TRUE)

def main():
    game = Game()
    game.run()
    glfw.terminate()

if __name__ == '__main__':
    main()


#cd C:\Users\dmonn\Downloads\code_tutoriel\code
#python main.py
