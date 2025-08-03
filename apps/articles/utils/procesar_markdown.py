import markdown

# Utilidad para procesar Markdown (para no repetir código)
def process_markdown_util(markdown_content):
    """Procesa el contenido Markdown y devuelve HTML."""
    extensions = [
        'markdown.extensions.fenced_code', 'markdown.extensions.tables',
        'markdown.extensions.nl2br', 'markdown.extensions.toc',
        'markdown.extensions.codehilite', 'markdown.extensions.extra',
        'markdown.extensions.footnotes', 'markdown.extensions.admonition',
    ]
    extension_configs = {
        'markdown.extensions.codehilite': {'css_class': 'highlight', 'use_pygments': True, 'linenums': False},
        'markdown.extensions.toc': {'permalink': True, 'permalink_class': 'headerlink', 'permalink_title': 'Enlace permanente a este encabezado'}
    }
    md = markdown.Markdown(extensions=extensions, extension_configs=extension_configs, tab_length=4)
    html_content = md.convert(markdown_content)

    if not markdown_content or not markdown_content.strip():
        return '''
        <div class="text-center text-muted py-5">
            <i class="bi bi-eye display-4 mb-3"></i>
            <h4>Preview aparecerá aquí</h4>
            <p>Comienza a escribir en la pestaña "Escribir" para ver el resultado</p>
        </div>
        '''
    return html_content