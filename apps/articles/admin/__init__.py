# articles/admin.py

from django.contrib import admin
from django.utils.html import format_html
from articles.models.articles_category import ArticlesCategory

# Define una clase que hereda de ModelAdmin para personalizar la interfaz
@admin.register(ArticlesCategory)
class ArticlesCategoryAdmin(admin.ModelAdmin):
    """Custom Admin interface for ArticlesCategory model."""

    # Campos a mostrar en la lista de categorías
    list_display = ('image_preview', 'name', 'slug')
    # Campos por los que se puede buscar
    search_fields = ('name',)
    # Función para mostrar una miniatura de la imagen en el listado
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 100px;" />',
                obj.image.url
            )
        return "Sin imagen"

    image_preview.short_description = 'Vista Previa'