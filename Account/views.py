from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from Account.models import UserFollowings
from Account.permissions import IsProfileOwnerOrReadOnly
from Account.serializers import CreateUserSerializer, RetrieveUpdateDeleteUserSerializer

User = get_user_model()


class CreateAccount(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer


class RetrieveUpdateDeleteUser(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = RetrieveUpdateDeleteUserSerializer
    lookup_field = 'username'
    permission_classes = (IsProfileOwnerOrReadOnly,)
    authentication_classes = (TokenAuthentication,)


class CreateFollowing(APIView):
    def post(self, request, username):
        """This Class creates a new following record, the username in the URL is the user being followed
        The user that follows us gotten from the request object"""
        try:
            follower = request.user
            is_following = User.objects.filter(username=username).first()

            """Return HTTP 400 if the user is same as the following"""
            if follower == is_following:
                return JsonResponse({"error": "You cannot follow yourself"}, status=status.HTTP_400_BAD_REQUEST)

            """Return HTTP 404 if the following does not exist"""
            if is_following is None:
                return JsonResponse({"error": "User you requested to follow does not exist"}, status=status.HTTP_404_NOT_FOUND)

            """Check if the following record already exists, if not create it, but if it does, fail silently"""
            if not UserFollowings.objects.filter(user=follower, is_following=is_following).exists():
                UserFollowings.objects.create(user=follower, is_following=is_following)
                """Increment the users' following and followers respectively"""
                follower.followings += 1
                follower.save()
                is_following.followers += 1
                is_following.save()

            return JsonResponse({'status': True}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            # return JsonResponse({'status': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class DeleteFollowing(APIView):
    def post(self, request, username):
        """This Class deletes a following record, the username in the URL is the user being followed
        THe user that follows us gotten from the request object"""
        try:
            follower = request.user
            is_following = User.objects.filter(username=username).first()

            """Return HTTP 404 if the following does not exist"""
            if is_following is None:
                return JsonResponse({"error": "User you requested to unfollow does not exist"},
                                    status=status.HTTP_404_NOT_FOUND)

            """Check if the following record already exists, if not create it, but if it does, fail silently"""
            if UserFollowings.objects.filter(user=follower, is_following=is_following).exists():
                UserFollowings.objects.filter(user=follower, is_following=is_following).delete()
                """Increment the users' following and followers respectively"""
                follower.followings -= 1
                follower.save()
                is_following.followers -= 1
                is_following.save()

            return JsonResponse({'status': True}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            # return JsonResponse({'status': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
