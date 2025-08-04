from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from django.db.models import Count, Max, Q, Prefetch
from django.core.paginator import Paginator
from django.utils.text import slugify
from django.http import Http404
from articles.models import Articles, ArticlesCategory, ArticlesTags
from users.models.user import User

class HomeView(TemplateView): 
    """
    Renderiza la página de inicio utilizando una Vista Basada en Clases.
    """
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        """
        Sobrescribimos este método para añadir todos los datos necesarios
        al contexto de la plantilla.
        """
        context = super().get_context_data(**kwargs)

        # --- Para el Slider "En Boca de Todos" ---
        context['most_viewed_articles'] = Articles.objects.filter(
            status='published'
        ).select_related('user', 'category').order_by('-views_count')[:5]

        # --- Para el Grid de Categorías Populares ---
        context['popular_categories'] = ArticlesCategory.objects.annotate(
            article_count=Count('articles', filter=Q(articles__status='published'))
        ).filter(article_count__gt=0).order_by('-article_count')[:5]

        # --- Para el Grid de Artículos Recientes ---
        context['recent_articles'] = Articles.objects.filter(
            status='published'
        ).select_related('user', 'category').order_by('-published_at')[:6]

        # --- Para la Sección de Autores Destacados ---
        context['featured_authors'] = User.objects.annotate(
            article_count=Count('articles', filter=Q(articles__status='published'))
        ).filter(
            article_count__gt=0
        ).order_by('-article_count')[:4]

        context['template_name'] = 'inicio'

        # 4. Devolvemos el contexto finalizado.
        return context

class CategoriesListView(ListView):
    """
    Muestra una lista de categorías con búsqueda, filtros, ordenamiento y 
    paginación, utilizando una Vista Basada en Clases.
    """
    model = ArticlesCategory
    template_name = 'categorias.html'
    context_object_name = 'categories'

    def get_queryset(self):
        """
        Sobrescribimos este método para construir la consulta principal.
        Aquí se maneja la anotación, búsqueda y ordenamiento.
        """
        # 1. Obtenemos el queryset base y los parámetros de la URL
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q', '')
        sort_order = self.request.GET.get('sort', 'populares')

        # 2. Anotamos los campos necesarios para el conteo y la fecha
        queryset = queryset.annotate(
            articles_count=Count('articles', filter=Q(articles__status='published'), distinct=True),
            most_recent_article_date=Max('articles__published_at', filter=Q(articles__status='published'))
        )

        # 3. Aplicamos el filtro de búsqueda si existe
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)

        # 4. Aplicamos el ordenamiento según el parámetro
        if sort_order == 'recientes':
            queryset = queryset.order_by('-most_recent_article_date', 'name')
        elif sort_order == 'a-z':
            queryset = queryset.order_by('name')
        elif sort_order == 'z-a':
            queryset = queryset.order_by('-name')
        else: # Por defecto (o 'populares')
            queryset = queryset.order_by('-articles_count', 'name')
            
        return queryset

    def get_paginate_by(self, queryset):
        """
        Sobrescribimos para que el número de ítems por página sea dinámico,
        basado en el parámetro 'show' de la URL.
        """
        items_per_page = self.request.GET.get('show', '8')

        if items_per_page == 'all':
            # Si es 'all', devolvemos el total de objetos para desactivar la paginación.
            return self.get_queryset().count() or 1
        
        try:
            return int(items_per_page)
        except (ValueError, TypeError):
            # Si el valor no es un número válido, usamos 8 por defecto.
            return 8

    def get_context_data(self, **kwargs):
        """
        Sobrescribimos para añadir lógica adicional al contexto:
        1. Calculamos el tag más popular para cada categoría EN LA PÁGINA ACTUAL.
        2. Pasamos el estado de los filtros para mantenerlos en la UI.
        """
        # 1. Obtenemos el contexto base de ListView (que ya incluye page_obj, paginator, etc.)
        context = super().get_context_data(**kwargs)
        
        # 2. Obtenemos los objetos de la página actual
        page_categories = context.get('object_list', [])
        page_categories_ids = [cat.id for cat in page_categories]
        
        # 3. Hacemos la consulta de tags solo para las categorías de esta página
        tags_data = ArticlesTags.objects.filter(
            article__category_id__in=page_categories_ids,
            article__status='published'
        ).values(
            'article__category_id', 'tag__name' 
        ).annotate(
            tag_count=Count('tag_id')
        ).order_by('article__category_id', '-tag_count')

        # 4. Creamos un mapa para asignar el tag más popular a cada categoría
        popular_tags_map = {}
        for tag in tags_data:
            category_id = tag['article__category_id']
            if category_id not in popular_tags_map:
                popular_tags_map[category_id] = {'name': tag['tag__name'], 'color': '#6f42c1'} # Color por defecto

        # 5. Adjuntamos el tag popular a cada objeto de categoría en el contexto
        for category in page_categories:
            category.most_popular_tag = popular_tags_map.get(category.id)

        # 6. Añadimos el estado de los filtros al contexto para la plantilla
        context['current_search'] = self.request.GET.get('q', '')
        context['current_sort'] = self.request.GET.get('sort', 'populares')
        context['current_show'] = str(self.request.GET.get('show', '8'))
        context['template_name'] = 'categorias'
        
        return context

def articles_by_category(request, slug):
    """
    Muestra los artículos de una categoría específica.
    """
    category = get_object_or_404(ArticlesCategory, slug=slug)
    
    search_query = request.GET.get('q', '')
    sort_order = request.GET.get('sort', 'recientes')

    articles_list = Articles.objects.filter(
        category=category,
        status='published'
    ).select_related('user', 'category')

    if search_query:
        articles_list = articles_list.filter(title__icontains=search_query)

    if sort_order == 'populares':
        articles_list = articles_list.order_by('-views_count')
    elif sort_order == 'a-z':
        articles_list = articles_list.order_by('title')
    else:
        articles_list = articles_list.order_by('-published_at')

    paginator = Paginator(articles_list, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'articles': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'current_search': search_query,
        'current_sort': sort_order,
    }
    
    return render(request, 'articles_by_category.html', context)

class AutoresListView(ListView):
    """
    Muestra una lista de autores con búsqueda, filtros y paginación,
    utilizando una Vista Basada en Clases (ListView).
    """
    model = User
    template_name = 'autores.html'
    context_object_name = 'autores'

    def get_queryset(self):
        """
        Define la consulta principal para obtener los autores.
        Aquí se aplica el filtrado, la anotación, la búsqueda y el ordenamiento.
        """
        # 1. Obtenemos el queryset base y los parámetros de la URL
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q', '')
        sort_order = self.request.GET.get('sort', 'populares')

        # 2. Filtramos y anotamos la consulta base
        #    - Solo autores con artículos publicados
        #    - Contamos sus artículos publicados
        #    - Optimizamos con prefetch_related
        queryset = queryset.filter(
            articles__status='published'
        ).annotate(
            articles_count=Count('articles', filter=Q(articles__status='published'))
        ).prefetch_related('privacy').distinct()

        # 3. Aplicamos el filtro de búsqueda si existe
        if search_query:
            queryset = queryset.filter(
                Q(username__icontains=search_query) |
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query)
            )

        # 4. Aplicamos el ordenamiento
        if sort_order == 'a-z':
            queryset = queryset.order_by('username')
        elif sort_order == 'z-a':
            queryset = queryset.order_by('-username')
        else:  # Por defecto o 'populares'
            queryset = queryset.order_by('-articles_count', 'username')

        return queryset

    def get_paginate_by(self, queryset):
        """
        Permite que el número de ítems por página sea dinámico,
        leyendo el parámetro 'show' de la URL.
        """
        items_per_page = self.request.GET.get('show', '12')

        if items_per_page == 'all':
            # Devolvemos el total para desactivar la paginación
            return self.get_queryset().count() or 1
        
        try:
            return int(items_per_page)
        except (ValueError, TypeError):
            # Si el valor no es válido, usamos 12 por defecto
            return 12

    def get_context_data(self, **kwargs):
        """
        Añade variables extra al contexto de la plantilla, como el
        estado actual de los filtros.
        """
        # Obtenemos el contexto base de ListView (que ya incluye el paginator y page_obj)
        context = super().get_context_data(**kwargs)
        
        # Añadimos el estado de los filtros para mantenerlos en los menús de la UI
        context['current_search'] = self.request.GET.get('q', '')
        context['current_sort'] = self.request.GET.get('sort', 'populares')
        context['current_show'] = str(self.request.GET.get('show', '12'))
        
        context['template_name'] = 'autores'
        
        return context

class AutorDetailView(DetailView):
    """
    Muestra la página de detalle de un autor y una lista de sus artículos
    publicados, utilizando una DetailView de Django.
    """
    model = User
    template_name = 'autor.html'
    context_object_name = 'user'
    slug_field = 'slug'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        """
        Sobrescribimos este método para añadir datos adicionales al contexto.
        En este caso, añadiremos la lista de artículos publicados del autor.
        """

        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['published_articles'] = user.articles.filter(status='published').order_by('-published_at')
        return context
