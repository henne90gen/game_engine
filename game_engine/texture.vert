attribute vec3 a_Position;
attribute vec2 a_UV;

uniform mat4 u_Model;
uniform mat4 u_View;
uniform mat4 u_Projection;

varying vec2 v_UV;
varying vec3 v_Position;

void main() {
    mat4 ModelViewProjection = u_Projection * u_View * u_Model;
    gl_Position = ModelViewProjection * vec4(a_Position, 1);
    v_UV = a_UV;
    v_Position = a_Position;
}
