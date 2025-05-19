#!/usr/bin/env python3

import OpenGL.GL as GL
import glfw
import numpy as np
from GLprogram import compile_shader, create_program, create_program_from_file

class Game(object):
    """ fenêtre GLFW avec openGL """

    def __init__(self):
        self.position = np.array([0.0, 0.0], dtype=np.float32)
        self.window = self.init_window()
        self.init_context()
        self.init_programs()
        self.init_data()
        self.color = np.array([0.0, 0.0, 0.0], dtype=np.float32)

    def init_window(self):
        # initialisation de la librairie glfw et du context opengl associé
        glfw.init()
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        # création et parametrage de la fenêtre
        glfw.window_hint(glfw.RESIZABLE, False)
        window = glfw.create_window(800, 800, 'OpenGL', None, None)
        # parametrage de la fonction de gestion des évènements
        glfw.set_key_callback(window, self.key_callback)
        return window

    def init_context(self):
        # activation du context OpenGL pour la fenêtre
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)
        # activation de la gestion de la profondeur
        GL.glEnable(GL.GL_DEPTH_TEST)

    def init_programs(self):
        # Création du programme GPU à partir des fichiers shader.vert et shader.frag
        prog = create_program_from_file("shader.vert", "shader.frag")
        GL.glUseProgram(prog)
        
    def init_data(self):
        # création d'un tableau de sommets
        sommets = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0]], dtype=np.float32)

        # attribution d'une liste d'état (1 indique la création d'une seule liste)
        vao = GL.glGenVertexArrays(1)
        # affectation de la liste d'état courante
        GL.glBindVertexArray(vao)
        # attribution d’un buffer de données (1 indique la création d’un seul buffer)
        vbo = GL.glGenBuffers(1)
        # affectation du buffer courant
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo)

        # copie des donnees des sommets sur la carte graphique
        GL.glBufferData(GL.GL_ARRAY_BUFFER, sommets, GL.GL_STATIC_DRAW)

        # Les deux commandes suivantes sont stockées dans l'état du vao courant
        # Active l'utilisation des données de positions
        # (le 0 correspond à la location dans le vertex shader)
        GL.glEnableVertexAttribArray(0)
        # Indique comment le buffer courant (dernier vbo "bindé")
        # est utilisé pour les positions des sommets
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, 0, None)

    def run(self):
        # boucle d'affichage
        while not glfw.window_should_close(self.window):
            # choix de la couleur de fond
            GL.glClearColor(np.cos(glfw.get_time()), np.sin(glfw.get_time()), 0.1, 1.0)
            # nettoyage de la fenêtre : fond et profondeur
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)   
            self.send_color()
            # self.send_position()
            
            speed = 0.01
            
            if glfw.get_key(self.window, glfw.KEY_LEFT) == glfw.PRESS:
                self.position[0] -= speed
            if glfw.get_key(self.window, glfw.KEY_RIGHT) == glfw.PRESS:
                self.position[0] += speed
            if glfw.get_key(self.window, glfw.KEY_UP) == glfw.PRESS:
                self.position[1] += speed
            if glfw.get_key(self.window, glfw.KEY_DOWN) == glfw.PRESS:
                self.position[1] -= speed
            
            # dessin du triangle
            GL.glDrawArrays(GL.GL_TRIANGLES, 0, 3)
            
            # changement de buffer d'affichage pour éviter un effet de scintillement
            glfw.swap_buffers(self.window)
            # gestion des évènements
            glfw.poll_events()
            # print(glfw.get_time()) On a environ 56 FPS donc en gros c'est 60 FPS.
    
    def key_callback(self, win, key, scancode, action, mods):
        # sortie du programme si appui sur la touche 'echap'
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(win, glfw.TRUE)
        elif action == glfw.PRESS:
            if key == glfw.KEY_R:
                self.color = np.array([1.0, 0.0, 0.0], dtype=np.float32)
            elif key == glfw.KEY_G:
                self.color = np.array([0.0, 1.0, 0.0], dtype=np.float32)
            elif key == glfw.KEY_B:
                self.color = np.array([0.0, 0.0, 1.0], dtype=np.float32)
                
    def send_color(self):
        # Recup ´ ere l'identifiant du programme courant `
        prog = GL.glGetIntegerv(GL.GL_CURRENT_PROGRAM)
        # Recup ´ ere l'identifiant de la variable translation dans le programme courant `
        loc = GL.glGetUniformLocation(prog, "triangleColor")
        # Verifie que la variable existe ´
        if loc == -1 :
            print("Pas de variable uniforme : translation")
        # Modifie la variable pour le programme courant
        GL.glUniform3f(loc, *self.color)
        
    def send_position(self):
        loc = GL.glGetUniformLocation(self.program, "translation")
        GL.glUniform2f(loc, self.position[0], self.position[1])
        
def main():
    g = Game()
    g.run()
    glfw.terminate()

if __name__ == '__main__':
    main()
    
# Q25 : la fonction viewport (GL.glViewport)
# Q28 : le triangle reste dans l'écran pour les valeurs de x/y comprises entre -1 et 1 ; l'objet n'est pas modifié selon z car z gère la profondeur
# Q29 : les donn´ees du triangle envoy´ees au GPU sont mise `a jour instantanément car on voit le triangle se déplacer.
# Q30 : dans le repère monde, on repère notre triangle avec les coordonnées x,y,z et dans le repère écran, on le repère avec une projection des coordonnées x,y,z sur l'écran.
