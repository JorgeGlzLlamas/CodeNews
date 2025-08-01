from django import forms

from articles.models.articles import Articles


class ArticleContentForm(forms.ModelForm):
    """Form that manage article content in the create view."""

    class Meta:
        model = Articles
        fields = [
            'status', 'published_at',
            'content'
        ]
        widgets = {
            'published_at': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                    'placeholder': 'Fecha de Publicación'
                }
            ),
            'status': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),
            'content': forms.Textarea(
                attrs={
                    'placeholder': 'Inicia el contenido de tu artículo aquí',
                    'rows': 10
                }
            ),
        }

    def __init__(self, *args, from_update=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.from_update = from_update

        # Elimina campos si es actualización o detalle
        if self.from_update:
            del self.fields['published_at']
            del self.fields['status']

            

