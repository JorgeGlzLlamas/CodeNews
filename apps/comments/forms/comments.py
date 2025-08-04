from comments.models.comment import Comment
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control mt-1',
                'placeholder': 'Escribe tu comentario aquí...',
                'rows': 4,
                'maxlength': 500
            })
        }
