from django.urls import path
from core.views import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    
    # Rutas de Categorías
    path('categorias/', views.categorias, name='categorias'),
    path('categoria/<slug:slug>/', views.articles_by_category, name='articles_by_category'),
    
    # Ruta de Autores
    path('autores/', views.autores, name='autores'),
    path('autor/<int:user_id>/', views.autor, name='autor'),
]