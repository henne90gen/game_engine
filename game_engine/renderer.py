def draw(vao: VAO, vbo: VBO, vertex_attributes: List[VertexAttribute], uniforms: List[Uniform], shader: Shader):
    shader.bind()
    vao.bind()
    vbo.bind()

    for uniform in uniforms:
        uniform.bind(shader)

    for attrib in vertex_attributes:
        attrib.bind(shader)

    glDrawArrays(GL_TRIANGLES, 0, len(vbo))

    vbo.unbind()
    vao.unbind()
    shader.unbind()
