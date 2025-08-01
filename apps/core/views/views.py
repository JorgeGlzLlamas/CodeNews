from django.shortcuts import render


def home(request):
    context = {
        'template_name': 'inicio'
    }
    return render(request, 'index.html', context)
