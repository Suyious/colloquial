from django.urls import path
from . import api

urlpatterns = [
    path('', api.post, name='post'),
    path('<str:id>/likes/', api.post_like, name='post_like'),
    path('<str:id>/comments/', api.post_comment, name='get_post_comments'),
    path('comments/<str:id>/edit', api.comment_edit, name='comment_edit'),
    path('comments/<str:id>/delete', api.comment_delete, name='comment_delete'),
    path('<str:id>/', api.post_get_delete, name='post_get'),
]