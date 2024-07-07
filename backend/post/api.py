from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .models import Post
from .serializers import PostSerializer
from .forms import PostForm

@api_view(['GET'])
def post_list(request):
    user_id = request.GET.get('user', None)
    keyword = request.GET.get('keyword', None)

    filters = {}
    if user_id:
        filters['created_by_id'] = user_id
    if keyword:
        filters['body__icontains'] = keyword

    if filters:
        from django.db.models import Q
        q_object = Q(**filters)  # Create Q object for combined filtering
        posts = Post.objects.filter(q_object)
    else:
        posts = Post.objects.all()

    if posts:
        serializer = PostSerializer(posts, many=True)
        return JsonResponse({ 'data': serializer.data })
    else:
        return JsonResponse({'message': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def post_create(request):
    data = request.data

    form = PostForm(data)
    if form.is_valid():
        post = form.save(commit=False)
        post.created_by = request.user
        post.save()

        serializer = PostSerializer(post)
        return JsonResponse({ 'data': serializer.data })
    else:
        return JsonResponse({ 'Error': "Some Error Occurred..." }, status=status.HTTP_404_NOT_FOUND)