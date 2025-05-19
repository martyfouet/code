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

def create_program(vertex_source, fragment_source):
    # creation d'un programme GPU ´
    vs_id = compile_shader(vertex_source, GL.GL_VERTEX_SHADER)
    fs_id = compile_shader(fragment_source, GL.GL_FRAGMENT_SHADER)
    if vs_id and fs_id:
        program_id = GL.glCreateProgram()
        GL.glAttachShader(program_id, vs_id)
        GL.glAttachShader(program_id, fs_id)
        GL.glLinkProgram(program_id)
        success = GL.glGetProgramiv(program_id, GL.GL_LINK_STATUS)
        if not success:
            log = GL.glGetProgramInfoLog(program_id).decode('ascii')
            print(f'{25*"-"}\nError linking program:\n{log}\n{25*"-"}')
        GL.glDeleteShader(vs_id)
        GL.glDeleteShader(fs_id)
    return program_id

def create_program_from_file(vs_file, fs_file):
    # creation d'un programme GPU ´ a partir de fichiers `
    vs_content = open(vs_file, 'r').read() if os.path.exists(vs_file)\
        else print(f'{25*"-"}\nError reading file:\n{vs_file}\n{25*"-"}')
    fs_content = open(fs_file, 'r').read() if os.path.exists(fs_file)\
        else print(f'{25*"-"}\nError reading file:\n{fs_file}\n{25*"-"}')
    return create_program(vs_content, fs_content)