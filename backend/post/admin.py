from django.contrib import admin

from backend.post.models import Post, PostAttachment

admin.site.register(Post)
admin.site.register(PostAttachment)
