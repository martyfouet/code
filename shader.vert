#version 330 core

// Variable d'entrée, ici la position
layout (location = 0) in vec3 aPos;

uniform vec2 translation;
uniform mat4 rotation;

//Un Vertex Shader minimaliste
void main ()
{
  //Coordonnees du sommet
  gl_Position = vec4(aPos.xy + translation, 0.0, 1.0);
  vec4 pos = vec4(aPos.xy + translation, 0.0, 1.0);
  gl_Position = rotation * pos;
}
