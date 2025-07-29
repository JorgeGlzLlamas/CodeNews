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
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'description': forms.Textarea(attrs={
                'rows': 4
            })
        }


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
            'category': forms.Select(),
            'description': forms.Textarea(),
            'status': forms.Select(),
            'published_at': forms.DateTimeInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk and self.instance.status == Articles.ArticleStatus.PUBLISHED:
            self.fields['published_at'].widget.attrs['readonly'] = True
