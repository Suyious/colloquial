from django.forms import ModelForm

from .models import Post, Comment, PostAttachment

class PostAttachmentForm(ModelForm):
    class Meta:
        model = PostAttachment
        fields = ('image',)

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('body',)

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)