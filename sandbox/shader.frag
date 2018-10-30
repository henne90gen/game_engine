uniform vec3 u_Color;

void main() {
    gl_FragColor = vec4(u_Color, 1.0);
    // gl_FragColor = vec4(1.0, 1.0, 1.0, 1.0);
}
