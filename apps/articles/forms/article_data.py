from django import forms
from articles.models.articles import Articles


class ArticleDataCreateForm(forms.ModelForm):
    """Form to create article data."""

    class Meta:
        model = Articles
        fields = [
            'title', 'category',
            'description', 'thumbnail_image'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título del artículo'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Breve descripción (sinapsis) del artículo'
            }),
            'thumbnail_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = '-- Selecciona una categoría --'


class ArticleDataUpdateForm(forms.ModelForm):
    """Form to update article data."""

    class Meta:
        model = Articles
        fields = [
            'title', 'category',
            'description', 'thumbnail_image',
            'status', 'published_at'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'thumbnail_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = '-- Selecciona una categoría --'
        if self.instance.pk:
            self.fields['title'].widget.attrs['readonly'] = True
        if self.instance.pk and self.instance.status == Articles.ArticleStatus.PUBLISHED:
            self.fields['published_at'].widget.attrs['readonly'] = True
