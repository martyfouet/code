#version 330 core

layout(location = 0) in vec3 position; // Position d'entrée du sommet

out vec3 coordonnee_3d; // Variable de sortie vers le fragment shader

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main()
{
    // On stocke la position du sommet avant toute transformation
    coordonnee_3d = position;

    // Application des transformations
    gl_Position = projection * view * model * vec4(position, 1.0);
}
