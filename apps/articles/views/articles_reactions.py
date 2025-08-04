# articles/views.py

from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from articles.models.articles import Articles
from articles.models.articles_reactions import ArticlesFavorites

class ArticleFavoriteToggleView(LoginRequiredMixin, View):
    """
    Handles adding or removing an article from a user's favorites.
    This view uses a "toggle" pattern.
    """
    
    def post(self, request, *args, **kwargs):
        """
        Handles the POST request to toggle the favorite status of an article.
        """
        # Obtenemos el slug del artículo desde los argumentos de la URL
        slug = self.kwargs.get('slug')
        article = get_object_or_404(Articles, slug=slug)
        user = self.request.user

        # Usamos get_or_create, que es perfecto para este caso de "toggle"
        favorite, created = ArticlesFavorites.objects.get_or_create(user=user, article=article)

        if created:
            # Si el objeto fue creado, significa que el usuario acaba de añadirlo a favoritos.
            messages.success(request, f'"{article.title}" ha sido añadido a tus favoritos.')
        else:
            # Si 'created' es False, el favorito ya existía y debemos eliminarlo.
            favorite.delete()
            messages.success(request, f'"{article.title}" ha sido eliminado de tus favoritos.')

        # Redirigimos de vuelta a la página de detalle del artículo.
        return redirect('articles:article_detail', slug=article.slug)