#version 330

in vec4 p3d_Vertex;
in vec3 p3d_Normal;
in vec4 p3d_Color;

out vec3 normal;
out vec3 color;
out vec3 fragPos;

uniform mat4 p3d_ModelViewProjectionMatrix;
uniform mat4 p3d_ModelMatrix;

void main() {
    gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;

    normal = p3d_Normal;
    color = p3d_Color.rgb;
    fragPos = vec3(p3d_ModelMatrix * p3d_Vertex);
}