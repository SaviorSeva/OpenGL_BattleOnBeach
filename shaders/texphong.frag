#version 330 core

in vec2 frag_tex_coords;

// fragment position and normal of the fragment, in WORLD coordinates
in vec3 w_position, w_normal;

uniform sampler2D diffuse_map;

// light dir, in world coordinates
uniform vec3 light_dir;

// material properties
uniform vec3 k_d, k_a, k_s;
uniform float s;

// world camera position
uniform vec3 w_camera_position;

out vec4 out_color;

void main() {
    // Compute all vectors, oriented outwards from the fragment
    vec3 n = normalize(w_normal);
    vec3 l = normalize(-light_dir);
    vec3 r = reflect(-l, n);
    vec3 v = normalize(w_camera_position - w_position);

    vec3 tex_color = texture(diffuse_map, frag_tex_coords).xyz;

    vec3 diffuse_color = k_d * max(dot(n, l), 0);
    vec3 specular_color = k_s * pow(max(dot(r, v), 0), s);

    vec3 tex_shaded_color = (k_a + diffuse_color) * tex_color + specular_color;

    out_color = vec4(tex_shaded_color, 1);
    // out_color = vec4(tex_color, 1);
}