#version 330 core

// Variable d'entrée, ici la position
layout (location = 0) in vec3 position;

uniform vec4 translation;

//Un Vertex Shader minimaliste
void main (void)
{
  //Coordonnees du sommet
  gl_Position = vec4(position.xy, position.z, 1.0);
  gl_Position += translation;
  // gl_Position.x += 0.2; on a décalé la position du sommet de 0.2
}
