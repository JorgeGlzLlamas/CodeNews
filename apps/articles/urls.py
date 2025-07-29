from django.urls import path
from articles.views import articles

app_name = 'articles'

urlpatterns = [
    # Articles URLs
    path('nuevo/',
         articles.ArticleCreateView.as_view(),
         name='article_create'),
    path('<slug:title>/contenido/',
         articles.ArticleContentView.as_view(),
         name='article_content'),
    path('<slug:title>/editar/',
         articles.ArticleUpdateView.as_view(),
         name='article_update'),
    # Set update flag for redirecting after content creation
    path('<slug:slug>/set-update-flag/',
         articles.set_from_update_view,
         name='set_update_flag')
]
