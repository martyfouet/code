#version 330 core

uniform vec3 triangleColor;
// Variable de sortie (sera utilisé comme couleur)
out vec4 color;

//Un Fragment Shader minimaliste
void main (void)
{
  color = vec4(triangleColor, 0.0);
}
