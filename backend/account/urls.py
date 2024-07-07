from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import api

urlpatterns = [
    path('me/', api.me, name='me'),
    path('user/', api.users_list, name='users'),
    path('user/<str:id>/', api.user, name='user'),
    path('user/<str:id>/follow/', api.send_follow_request, name='send_follow_request'),
    path('user/<str:id>/accept/', api.accept_follow_request, name='accept_follow_request'),
    path('user/<str:id>/reject/', api.reject_follow_request, name='reject_follow_request'),
    path('user/<str:id>/cancel/', api.cancel_follow_request, name='cancel_follow_request'),
    path('user/<str:id>/unfollow/', api.unfollow_user, name='unfollow_user'),
    path('signup/', api.signup, name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh')
]