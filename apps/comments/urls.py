from django.urls import path

from comments.views.comment import CommentView
from comments.views.comment_like import CommentLikeToggleView

app_name = 'comments'

urlpatterns = [
    path('<int:article_id>/nuevo/',
         CommentView.as_view(), 
         name='comment_create'),
    path('<int:comment_id>/like/',
         CommentLikeToggleView.as_view(), 
         name='comment_like_toggle'),
]
