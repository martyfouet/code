import OpenGL.GL as GL
import glfw
import numpy as np
import pyrr
from GLprogram import create_program_from_file
from ctypes import c_void_p, sizeof, c_float

class Game(object):
    def __init__(self):
        self.position = np.array([0.0, 0.0], dtype=np.float32)
        self.window = self.init_window()
        self.init_context()
        self.init_programs()
        self.init_data()
        self.rotation_matrix = pyrr.matrix44.create_identity(dtype=np.float32)
        self.projection = pyrr.matrix44.create_perspective_projection(
            fovy=50.0, aspect=1.0, near=0.5, far=10.0, dtype=np.float32
        )
        self.z = -3.0

    def init_window(self):
        glfw.init()
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.RESIZABLE, False)
        window = glfw.create_window(800, 800, 'OpenGL', None, None)
        glfw.set_key_callback(window, self.key_callback)
        return window

    def init_context(self):
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)
        GL.glEnable(GL.GL_DEPTH_TEST)

    def init_programs(self):
        self.program = create_program_from_file("shader.vert", "shader.frag")
        GL.glUseProgram(self.program)

    def init_data(self):
        sommets = np.array([
            0.0, 0.0, 0.0,  1.0, 0.0, 0.0,  # rouge
            1.0, 0.0, 0.0,  0.0, 1.0, 0.0,  # vert
            0.0, 1.0, 0.0,  0.0, 0.0, 1.0,  # bleu
            0.0, 0.0, 1.0,  1.0, 1.0, 0.0   # jaune
        ], dtype=np.float32)

        index = np.array([
            0, 1, 2,
            0, 1, 3
        ], dtype=np.uint32)

        self.vao = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.vao)

        self.vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, sommets.nbytes, sommets, GL.GL_STATIC_DRAW)

        self.ebo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, index.nbytes, index, GL.GL_STATIC_DRAW)

        GL.glEnableVertexAttribArray(0)
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, 6 * sizeof(c_float()), c_void_p(0))

        GL.glEnableVertexAttribArray(1)
        GL.glVertexAttribPointer(1, 3, GL.GL_FLOAT, GL.GL_FALSE, 6 * sizeof(c_float()), c_void_p(3 * sizeof(c_float())))

        GL.glBindVertexArray(0)

    def run(self):
        speed = 0.1
        projection_speed = 0.1
        last_time = glfw.get_time()

        while not glfw.window_should_close(self.window):
            current_time = glfw.get_time()
            delta_time = current_time - last_time
            last_time = current_time
            rotation_speed = 1.5 * delta_time

            GL.glClearColor(0.2, 0.2, 0.2, 1.0)
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

            if glfw.get_key(self.window, glfw.KEY_K) == glfw.PRESS:
                self.rotation_matrix = pyrr.matrix44.multiply(
                    pyrr.matrix44.create_from_x_rotation(rotation_speed), self.rotation_matrix
                )
            if glfw.get_key(self.window, glfw.KEY_I) == glfw.PRESS:
                self.rotation_matrix = pyrr.matrix44.multiply(
                    pyrr.matrix44.create_from_x_rotation(-rotation_speed), self.rotation_matrix
                )
            if glfw.get_key(self.window, glfw.KEY_L) == glfw.PRESS:
                self.rotation_matrix = pyrr.matrix44.multiply(
                    pyrr.matrix44.create_from_y_rotation(rotation_speed), self.rotation_matrix
                )
            if glfw.get_key(self.window, glfw.KEY_J) == glfw.PRESS:
                self.rotation_matrix = pyrr.matrix44.multiply(
                    pyrr.matrix44.create_from_y_rotation(-rotation_speed), self.rotation_matrix
                )

            if glfw.get_key(self.window, glfw.KEY_LEFT) == glfw.PRESS:
                self.position[0] -= speed
            if glfw.get_key(self.window, glfw.KEY_RIGHT) == glfw.PRESS:
                self.position[0] += speed
            if glfw.get_key(self.window, glfw.KEY_UP) == glfw.PRESS:
                self.position[1] += speed
            if glfw.get_key(self.window, glfw.KEY_DOWN) == glfw.PRESS:
                self.position[1] -= speed

            if glfw.get_key(self.window, glfw.KEY_Y) == glfw.PRESS:
                self.z += projection_speed
            if glfw.get_key(self.window, glfw.KEY_H) == glfw.PRESS:
                self.z -= projection_speed

            translation = pyrr.matrix44.create_from_translation(
                [self.position[0], self.position[1], self.z], dtype=np.float32
            )
            model = pyrr.matrix44.multiply(translation, self.rotation_matrix)

            view = pyrr.matrix44.create_look_at(
                eye=[0.0, 0.0, 3.0],
                target=[0.0, 0.0, 0.0],
                up=[0.0, 1.0, 0.0],
                dtype=np.float32
            )

            GL.glUseProgram(self.program)
            GL.glUniformMatrix4fv(GL.glGetUniformLocation(self.program, "model"), 1, GL.GL_FALSE, model)
            GL.glUniformMatrix4fv(GL.glGetUniformLocation(self.program, "view"), 1, GL.GL_FALSE, view)
            GL.glUniformMatrix4fv(GL.glGetUniformLocation(self.program, "projection"), 1, GL.GL_FALSE, self.projection)

            GL.glBindVertexArray(self.vao)
            GL.glDrawElements(GL.GL_TRIANGLES, 6, GL.GL_UNSIGNED_INT, None)
            GL.glBindVertexArray(0)

            glfw.swap_buffers(self.window)
            glfw.poll_events()

    def key_callback(self, win, key, scancode, action, mods):
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(win, glfw.TRUE)

def main():
    g = Game()
    g.run()
    glfw.terminate()

if __name__ == '__main__':
    main()
