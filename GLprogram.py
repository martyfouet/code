import OpenGL.GL as GL
import glfw
import numpy as np
import os

def compile_shader(shader_content, shader_type):
    # compilation d'un shader donne selon son type ´
    shader_id = GL.glCreateShader(shader_type)
    GL.glShaderSource(shader_id, shader_content)
    GL.glCompileShader(shader_id)
    success = GL.glGetShaderiv(shader_id, GL.GL_COMPILE_STATUS)
    if not success:
        log = GL.glGetShaderInfoLog(shader_id).decode('ascii')
        print(f'{25*"-"}\nError compiling shader: \n\
        {shader_content}\n{5*"-"}\n{log}\n{25*"-"}')
    return shader_id

def create_program(vertex_src, fragment_src):
    program = GL.glCreateProgram()
    
    vertex_shader = compile_shader(vertex_src, GL.GL_VERTEX_SHADER)
    fragment_shader = compile_shader(fragment_src, GL.GL_FRAGMENT_SHADER)
    
    GL.glAttachShader(program, vertex_shader)
    GL.glAttachShader(program, fragment_shader)
    GL.glLinkProgram(program)

    # Vérifie le lien
    link_status = GL.glGetProgramiv(program, GL.GL_LINK_STATUS)
    if not link_status:
        log = GL.glGetProgramInfoLog(program)
        raise RuntimeError(f"Erreur de linkage du programme:\n{log.decode()}")
    
    return program

def create_program_from_file(vertex_path, fragment_path):
    with open(vertex_path) as f:
        vertex_src = f.read()
    with open(fragment_path) as f:
        fragment_src = f.read()
    
    return create_program(vertex_src, fragment_src)