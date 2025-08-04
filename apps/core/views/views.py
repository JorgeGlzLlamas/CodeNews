from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Max, Q, Prefetch
from django.core.paginator import Paginator
from django.utils.text import slugify
from django.http import Http404
from articles.models import Articles, ArticlesCategory, ArticlesTags
from users.models import User, SocialMedia

def home(request):
    """
    Renderiza la página de inicio con todas las secciones y datos optimizados.
    """
    # --- Para el Slider "En Boca de Todos" ---
    most_viewed_articles = Articles.objects.filter(
        status='published'
    ).select_related('user', 'category').order_by('-views_count')[:5]

    # --- Para el Grid de Categorías Populares ---
    popular_categories = ArticlesCategory.objects.annotate(
        article_count=Count('articles', filter=Q(articles__status='published'))
    ).filter(article_count__gt=0).order_by('-article_count')[:5]

    # --- Para el Grid de Artículos Recientes ---
    recent_articles = Articles.objects.filter(
        status='published'
    ).select_related('user', 'category').order_by('-published_at')[:6]

    # --- Para la Sección de Autores Destacados (Consulta Optimizada) ---
    # Usamos prefetch_related para traer las redes sociales de forma eficiente
    featured_authors = User.objects.annotate(
        article_count=Count('articles', filter=Q(articles__status='published'))
    ).filter(
        article_count__gt=0
    ).prefetch_related(
        'social_media' 
    ).select_related(
        'privacy', 'rol' # Asumiendo que tienes estos modelos relacionados
    ).order_by('-article_count')[:4] # Mostramos 4 para que el diseño se vea mejor


    # --- Contexto final para la Plantilla ---
    context = {
        'most_viewed_articles': most_viewed_articles,
        'popular_categories': popular_categories,
        'recent_articles': recent_articles, 
        'featured_authors': featured_authors,
    }
    
    return render(request, 'index.html', context)

def categorias(request):
    """
    Muestra las categorías con filtros, ordenamiento y paginación
    manejados desde el backend.
    """
    search_query = request.GET.get('q', '')
    sort_order = request.GET.get('sort', 'populares')
    items_per_page = request.GET.get('show', '8')

    categories_query = ArticlesCategory.objects.annotate(
        articles_count=Count('articles', filter=Q(articles__status='published'), distinct=True),
        most_recent_article_date=Max('articles__published_at', filter=Q(articles__status='published'))
    )

    if search_query:
        categories_query = categories_query.filter(name__icontains=search_query)

    if sort_order == 'recientes':
        categories_query = categories_query.order_by('-most_recent_article_date', 'name')
    elif sort_order == 'a-z':
        categories_query = categories_query.order_by('name')
    elif sort_order == 'z-a':
        categories_query = categories_query.order_by('-name')
    else:
        categories_query = categories_query.order_by('-articles_count', 'name')

    try:
        page_size = int(items_per_page) if items_per_page != 'all' else categories_query.count() or 1
    except (ValueError, TypeError):
        page_size = 8
    
    paginator = Paginator(categories_query, page_size)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    page_categories_ids = [cat.id for cat in page_obj.object_list]
    
    tags_data = ArticlesTags.objects.filter(
        article__category_id__in=page_categories_ids,
        article__status='published'
    ).values(
        'article__category_id', 'tag__name' 
    ).annotate(
        tag_count=Count('tag_id')
    ).order_by('article__category_id', '-tag_count')

    popular_tags_map = {}
    for tag in tags_data:
        category_id = tag['article__category_id']
        if category_id not in popular_tags_map:
            popular_tags_map[category_id] = {
                'name': tag['tag__name'],
                'color': '#6f42c1'
            }

    for category in page_obj.object_list:
        category.most_popular_tag = popular_tags_map.get(category.id)
    
    context = {
        'categories': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'template_name': 'categorias',
        'current_search': search_query,
        'current_sort': sort_order,
        'current_show': str(items_per_page)
    }
    
    return render(request, 'categorias.html', context)

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
        'template_name': 'articles_by_category',
        'current_search': search_query,
        'current_sort': sort_order,
    }
    
    return render(request, 'articles_by_category.html', context)

def autores(request):
    """
    Muestra los autores del sitio con filtros.
    """
    search_query = request.GET.get('q', '')
    sort_order = request.GET.get('sort', 'populares')
    items_per_page = request.GET.get('show', '12')

    authors_query = User.objects.filter(
        articles__status='published'
    ).annotate(
        articles_count=Count('articles', filter=Q(articles__status='published'))
    ).prefetch_related('privacy', 'social_media').distinct()

    if search_query:
        authors_query = authors_query.filter(
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )

    if sort_order == 'a-z':
        authors_query = authors_query.order_by('username')
    elif sort_order == 'z-a':
        authors_query = authors_query.order_by('-username')
    else:
        authors_query = authors_query.order_by('-articles_count', 'username')

    try:
        page_size = int(items_per_page) if items_per_page != 'all' else authors_query.count() or 1
    except (ValueError, TypeError):
        page_size = 12
    
    paginator = Paginator(authors_query, page_size)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'autores': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'template_name': 'autores',
        'current_search': search_query,
        'current_sort': sort_order,
        'current_show': str(items_per_page)
    }
    
    return render(request, 'autores.html', context)

def autor(request, user_id):
    user = get_object_or_404(User, id=user_id)
    published_articles = user.articles.filter(status='published')
    
    context = {
        'user': user,
        'published_articles': published_articles
    }
    return render(request, 'autor.html', context)
