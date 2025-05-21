#version 330 core

out vec4 FragColor;

uniform vec3 triangleColor;
// Variable de sortie (sera utilisé comme couleur)

//Un Fragment Shader minimaliste
void main ()
{
  FragColor = vec4(triangleColor, 1.0);
}
