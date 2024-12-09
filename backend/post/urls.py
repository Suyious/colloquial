from django.urls import path
from . import api

urlpatterns = [
    path('', api.post_list, name='post_list'),
    path('create/', api.post_create, name='post_create'),
    path('<str:id>/like/', api.post_like, name='post_like'),
    path('<str:id>/likes/', api.get_post_likes, name='get_post_likes'),
    path('<str:id>/unlike/', api.post_unlike, name='post_unlike'),
    path('<str:id>/comment/', api.comment_add, name='comment_add'),
    path('<str:id>/comments/', api.get_post_comments, name='get_post_comments'),
    path('comment/<str:id>/edit', api.comment_edit, name='comment_edit'),
    path('comment/<str:id>/delete', api.comment_delete, name='comment_delete'),
    path('<str:id>/', api.post_get_delete, name='post_get'),
]