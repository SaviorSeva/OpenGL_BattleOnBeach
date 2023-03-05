#version 330 core

uniform sampler2D water_tex;
uniform sampler2D beach_tex;
uniform sampler2D grass_tex;
uniform sampler2D texmap;

in vec2 frag_tex_coords;
// fragment position and normal of the fragment, in WORLD coordinates
in vec3 w_position, w_normal;

// light dir, in world coordinates
uniform vec3 light_dir;

// material properties
uniform vec3 k_d;
uniform float s;

out vec4 out_color;

void main() {
    // 0.00390625 = 1 / 256
    vec2 modded_coords = frag_tex_coords * 0.00390625;
    vec4 texmap_color = texture(texmap, modded_coords);
    vec4 water_color = texture(water_tex, frag_tex_coords) * texmap_color.b;
    vec4 beach_color = texture(beach_tex, frag_tex_coords) * texmap_color.r;
    vec4 grass_color = texture(grass_tex, frag_tex_coords) * texmap_color.g;

    vec4 final_texture_color = water_color + beach_color + grass_color;


    // vec4 final_texture_color = beach_color;
    vec3 n = normalize(w_normal);
    vec3 l = normalize(-light_dir);

    // vec4 texture_color = texture(diffuse_map, frag_tex_coords);

    vec3 diffuse_color = k_d * max(dot(n, l), 0);
    // vec4 water_color = texture(water_tex, frag_tex_coords);
    // out_color = water_color;
    out_color = final_texture_color * vec4(diffuse_color, 1);
}
