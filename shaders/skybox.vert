#version 330 core
in vec3 position;

out vec3 TexCoords;

uniform mat4 model;
uniform mat4 projection;
uniform mat4 view;

void main()
{
    TexCoords = position;
    vec4 pos = model * projection * view * vec4(position, 1.0);
    gl_Position = pos.xyww;
}  