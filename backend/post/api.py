from django.http import JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .models import Post, Comment
from .serializers import PostSerializer, UserSerializer, CommentSerializer
from .forms import PostForm, CommentForm, PostAttachmentForm

@api_view(['GET', 'POST'])
def post(request):
    if request.method == 'GET':
        user_id = request.GET.get('user', None)
        keyword = request.GET.get('keyword', None)
        page_number = request.GET.get('page', 1)

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
        
        paginator = Paginator(posts, 10)

        try:
            page = paginator.page(page_number)
        except PageNotAnInteger:
            return JsonResponse({'message': 'Invalid page number'}, status=status.HTTP_400_BAD_REQUEST)
        except EmptyPage:
            return JsonResponse({'message': 'No posts found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PostSerializer(page, many=True, context={'request': request})
        return JsonResponse({
            'data': serializer.data,
            'page': page.number,
            'total': paginator.num_pages,
        })
    
    data = request.data
    files = request.FILES

    form = PostForm(data)

    if form.is_valid():
        post = form.save(commit=False)
        post.created_by = request.user

        image = files.get('image')
        print(type(image), image)

        if image:
            attachment_form = PostAttachmentForm(data, files)
            if attachment_form.is_valid():
                attachment = attachment_form.save(commit=False)
                attachment.created_by = request.user
                attachment.save()
                post.save()
                post.attachments.add(attachment)
            else:
                attachment_errors = attachment_form.errors.as_json()
                print(attachment_errors)
                return JsonResponse({ 'errors': attachment_errors, "message": "Image Upload Failed" }, status = status.HTTP_400_BAD_REQUEST)

        post.save()

        serializer = PostSerializer(post, context = { 'request': request })
        return JsonResponse({ 'data': serializer.data })
    else:
        errors = form.errors.as_json()
        return JsonResponse({ 'error': errors }, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'DELETE'])
def post_get_delete(request, id):
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return JsonResponse({'message': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PostSerializer(post, context = { 'request': request })
        return JsonResponse(serializer.data)


    if post.created_by != request.user:
        print(post.created_by, request.user)
        return JsonResponse({'message': 'You cannot delete this post'}, status=status.HTTP_403_FORBIDDEN)

    post.delete()
    return JsonResponse({'message': 'Post deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST', 'DELETE'])
def post_like(request, id):
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return JsonResponse({ 'message': 'Post not found' }, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        liked_users = post.likes.all()
        serializer = UserSerializer(liked_users, many=True)
        return JsonResponse(serializer.data)
    
    user = request.user
    if request.method == 'POST':
        if user in post.likes.all():
            return JsonResponse({'message': 'You already liked this post'}, status=status.HTTP_400_BAD_REQUEST)

        post.likes.add(user)
        post.likes_count += 1
        post.save()
        return JsonResponse({'message': 'Post liked successfully'}, status=status.HTTP_201_CREATED)

    if user not in post.likes.all():
        return JsonResponse({'message': 'You have not liked this post'}, status=status.HTTP_400_BAD_REQUEST)

    post.likes.remove(user)
    post.likes_count -= 1
    post.save()
    return JsonResponse({'message': 'Post unliked successfully'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def post_comment(request, id):
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return JsonResponse({'message': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        page_number = request.GET.get('page', 1)
        comments = post.comments.all()
        paginator = Paginator(comments, 10)

        try:
            page = paginator.page(page_number)
        except PageNotAnInteger:
            return JsonResponse({'message': 'Invalid page number'}, status=status.HTTP_400_BAD_REQUEST)
        except EmptyPage:
            return JsonResponse({'message': 'No posts found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(page, many=True, context={'request': request})
        return JsonResponse({
            'data': serializer.data,
            'page': page.number,
            'total': paginator.num_pages,
        })
    
    form = CommentForm(request.data)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.user = request.user
        comment.save()
        post.comments_count += 1
        post.save()
        serializer = CommentSerializer(comment, context={'request': request})
        return JsonResponse({'message': 'Comment added successfully', 'data': serializer.data}, status=status.HTTP_201_CREATED)
    return JsonResponse(form.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def comment_edit(request, id): # id -> comment_id
    try:
        comment = Comment.objects.get(id=id)
    except Comment.DoesNotExist:
        return JsonResponse({'message': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)

    if comment.user != request.user:
        return JsonResponse({'message': 'You cannot edit this comment'}, status=status.HTTP_403_FORBIDDEN)

    form = CommentForm(request.POST, instance=comment)
    if form.is_valid():
        form.save()
        return JsonResponse({'message': 'Comment updated successfully'}, status=status.HTTP_200_OK)
    return JsonResponse(form.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def comment_delete(request, id): # id -> comment_id
    try:
        comment = Comment.objects.get(id=id)
    except Comment.DoesNotExist:
        return JsonResponse({'message': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)

    if comment.user != request.user:
        return JsonResponse({'message': 'You cannot delete this comment'}, status=status.HTTP_403_FORBIDDEN)

    post = comment.post
    post.comments_count -= 1
    post.save()
    comment.delete()
    return JsonResponse(status=status.HTTP_204_NO_CONTENT)