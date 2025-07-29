from django import forms

from articles.models.articles import Articles


class ArticleContentForm(forms.ModelForm):
    """Form that manage article content
    in the create view."""

    class Meta:
        model = Articles
        fields = [
            'status', 'published_at',
            'content'
        ]
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': 'Inicia el contenido de tu artículo aquí',
                'rows': 10
            })   
        }

    # Add logic based on the view
    def __init__(self, *args, from_update=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.from_update = from_update

        """Drop the fields for update or detail view for content."""
        if self.from_update:
            del self.fields['published_at']
            del self.fields['status']
            

