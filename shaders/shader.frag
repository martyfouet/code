#version 330 core

in vec3 vcolor;
in vec2 vtex;

uniform sampler2D texture;

out vec4 fragColor;

void main() {
    vec4 texColor = texture(texture, vtex); // Utiliser 'texture' (fonction) au lieu de 'texture2D'
    fragColor = texColor * vec4(vcolor, 1.0); // Multiplier la couleur de texture avec la couleur vertex
}
