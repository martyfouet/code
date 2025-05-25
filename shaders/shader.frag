#version 330 core

in vec3 coordonnee_3d; // Reçoit la position originale du sommet depuis le vertex shader

out vec4 FragColor;

void main()
{
    // Utilisation des composantes x, y, z comme R, G, B
    FragColor = vec4(coordonnee_3d.x, coordonnee_3d.y, coordonnee_3d.z, 1.0);
}
