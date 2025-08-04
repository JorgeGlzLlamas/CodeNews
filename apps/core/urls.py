from django.urls import path
from core.views import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    
    # Rutas de Categorías
    path('categorias/', views.CategoriesListView.as_view(), name='categorias'),
    path('categoria/<slug:slug>/', views.articles_by_category, name='articles_by_category'),
    
    # Ruta de Autores
    path('autores/', views.AutoresListView.as_view(), name='autores'),
    path('autor/<slug:username>/', views.AutorDetailView.as_view(), name='autor'),
]