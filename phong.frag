#version 330 core

// Variable de sortie (sera utilisé comme couleur)
out vec4 color;

in vec3 coordonnee_3d;
in vec3 coordonnee_3d_locale;
in vec3 vnormale;

vec3 light = vec3(0.5,0.5,5.0);

//Un Fragment Shader minimaliste
void main (void)
{
  vec3 n = normalize(vnormale);
  vec3 d = normalize(light-coordonnee_3d_locale);
  vec3 r = reflect(-d,n);
  vec3 o = normalize(-coordonnee_3d_locale);

  float diffuse  = 0.7*clamp(dot(n,d),0.0,1.0);
  float specular = 0.2*pow(clamp(dot(r,o),0.0,1.0),128.0);
  float ambiant  = 0.2;

  vec4 white = vec4(1.0,1.0,1.0,0.0);
  vec4 color_final = vec4(1.0,0.5,0.5,0.0);

  color = (ambiant+diffuse)*color_final+specular*white;
}