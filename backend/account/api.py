from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status

from .forms import SignupForm
from .models import User, FollowRequest
from .serializers import UserSerializer

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request):
    data = request.data

    if User.objects.filter(email=data.get('email')).exists():
        return JsonResponse({'message': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

    form = SignupForm({
        'email': data.get('email'),
        'name': data.get('name'),
        'password1': data.get('password1'),
        'password2': data.get('password2'),
    })

    if form.is_valid():
        form.save()
        # send verification email
        return JsonResponse({'status': 'success', 'message': 'Registration successful'})

    errors = form.errors.as_json()
    print(errors)
    return JsonResponse({'status': 'error', 'errors' : errors }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def me(request):
    return JsonResponse({
        'id': request.user.id,
        'name': request.user.name,
        'email': request.user.email,
    })

@api_view(['GET'])
def user(request, id):
    try:
        user_to_get = User.objects.get(pk=id)
    except User.DoesNotExist:
        return JsonResponse({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = UserSerializer(user_to_get, context={'request': request})
    response_data = serializer.data

    return JsonResponse(response_data, safe=False)

@api_view(['GET'])
def users_list(request):
    name = request.GET.get('keyword', None)
    if name:
        users = User.objects.filter(name__icontains=name)
    else:
        users = None

    if users:
        serializer = UserSerializer(users, context={'request': request}, many=True)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'message': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def send_follow_request(request, id):
    try:
        user_to_follow = User.objects.get(pk=id)
    except User.DoesNotExist:
        return JsonResponse({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    if user_to_follow == request.user:
        return JsonResponse({'message': 'You cannot follow yourself.'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if user already follows or has a pending request
    if user_to_follow in request.user.following.all() or FollowRequest.objects.filter(from_user=request.user, to_user=user_to_follow).exists():
        return JsonResponse({'message': 'You are already following this user or have a pending request.'}, status=status.HTTP_400_BAD_REQUEST)

    # Create a new FollowRequest object
    FollowRequest.objects.create(from_user=request.user, to_user=user_to_follow)

    return JsonResponse({'message': 'Follow request sent successfully.'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def accept_follow_request(request, id):
    try:
        user_to_accept = User.objects.get(pk=id)
    except User.DoesNotExist:
        return JsonResponse({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Check if there's a pending request from the user
    try:
        follow_request = FollowRequest.objects.get(from_user=user_to_accept, to_user=request.user)
    except FollowRequest.DoesNotExist:
        return JsonResponse({'message': 'There is no pending follow request from this user.'}, status=status.HTTP_400_BAD_REQUEST)

    # Accept the request by adding user_to_accept to following and removing the request
    request.user.followers.add(user_to_accept)
    request.user.save()  # Save the updated following list

    # Remove the FollowRequest object after accepting
    follow_request.delete()

    return JsonResponse({'message': 'Follow request accepted successfully.'}, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def reject_follow_request(request, user_id):
    try:
        user_to_reject = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Check if there's a pending request from the user
    try:
        follow_request = FollowRequest.objects.get(from_user=user_to_reject, to_user=request.user)
    except FollowRequest.DoesNotExist:
        return JsonResponse({'message': 'There is no pending follow request from this user.'}, status=status.HTTP_400_BAD_REQUEST)

    # Delete the FollowRequest object to reject the request
    follow_request.delete()

    return JsonResponse({'message': 'Follow request rejected successfully.'}, status=204)

@api_view(['DELETE'])
def cancel_follow_request(request, id):
    try:
        user_to_cancel = User.objects.get(pk=id)
    except User.DoesNotExist:
        return JsonResponse({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Check if there's a pending request from the current user to the specified user
    try:
        follow_request = FollowRequest.objects.get(from_user=request.user, to_user=user_to_cancel)
    except FollowRequest.DoesNotExist:
        return JsonResponse({'message': 'You have no pending follow request to this user.'}, status=status.HTTP_400_BAD_REQUEST)

    # Delete the FollowRequest object to cancel the request
    follow_request.delete()

    return JsonResponse({'message': 'Follow request cancelled successfully.'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['DELETE'])
def unfollow_user(request, id):
    try:
        user_to_unfollow = User.objects.get(pk=id)
    except User.DoesNotExist:
        return JsonResponse({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Get current user (assuming request is authenticated)
    current_user = request.user

    # Check if current user is already following the user_to_unfollow
    if not current_user.following.filter(pk=id).exists():
        return JsonResponse({'message': 'You are not following this user.'}, status=status.HTTP_400_BAD_REQUEST)

    # Remove the user from the following list
    current_user.following.remove(user_to_unfollow)

    return JsonResponse({'message': 'Unfollowed user successfully.'}, status=status.HTTP_204_NO_CONTENT)