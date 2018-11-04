uniform sampler2D u_TextureSampler;

varying vec2 v_UV;
varying vec3 v_Position;

void main() {
    // gl_FragColor = vec4(u_Color, 1.0);
    gl_FragColor = texture2D(u_TextureSampler, v_UV);
    // gl_FragColor = vec4(1.0, 1.0, 1.0, 1.0);
    // gl_FragColor = vec4(v_UV, 0.0, 1.0);
}
