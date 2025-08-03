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
    path('<slug:slug>/', articles.ArticleDetailView.as_view(), 
         name='article_detail'),
    path('<slug:title>/editar/',
         articles.ArticleUpdateView.as_view(),
         name='article_update'),
     path('preview/markdown/', 
          articles.MarkdownPreviewView.as_view(),
          name='markdown_preview'),
]
