from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/', include('backend.account.urls')),
    path('api/posts/', include('backend.post.urls')),
    path('admin/', admin.site.urls),
]