from django.contrib.auth import get_user_model
from django.db import connection
from django.http import JsonResponse
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from Account.models import UserFollowings
from Account.paginations import FollowerPagination
from Account.permissions import IsProfileOwnerOrReadOnly, IsOwnerOrReadOnly
from Account.serializers import CreateUserSerializer, RetrieveUpdateDeleteUserSerializer, FollowerSerializer, \
    FollowingSerializer
from Poll.pagination import PollPagination
from Poll.serializers import PollSerializer
from Post.models import Post
from Post.paginations import PostPagination, PostCommentPagination
from Post.serializers import CreatePostSerializer, StarredCommentSerializer, \
    MyFollowedPostsSerializer, MyStarredPostsSerializer, MyUpvotedPostsSerializer, MyUpvotedCommentsSerializer, \
    ListCommentSerializer
from Topic.models import TopicFollowing, Topic
from Topic.pagination import TopicPagination
from Topic.serializers import TopicSerializer, TopicFollowedByUserSerializer

User = get_user_model()


class CreateAccount(ListCreateAPIView):
    queryset = User.objects.all()

    # serializer_class = CreateUserSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RetrieveUpdateDeleteUserSerializer
        else:
            return CreateUserSerializer

    pagination_class = FollowerPagination


class RetrieveUpdateDeleteUser(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = RetrieveUpdateDeleteUserSerializer
    lookup_field = 'username'
    permission_classes = (IsProfileOwnerOrReadOnly,)
    authentication_classes = (TokenAuthentication,)


class RetrieveUpdateDeleteMe(RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.id)

    serializer_class = RetrieveUpdateDeleteUserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


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
                return JsonResponse({"error": "User you requested to follow does not exist"},
                                    status=status.HTTP_404_NOT_FOUND)

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

    def delete(self, request, username):
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


# class DeleteFollowing(APIView):
#     def post(self, request, username):
#         """This Class deletes a following record, the username in the URL is the user being followed
#         THe user that follows us gotten from the request object"""
#         try:
#             follower = request.user
#             is_following = User.objects.filter(username=username).first()
#
#             """Return HTTP 404 if the following does not exist"""
#             if is_following is None:
#                 return JsonResponse({"error": "User you requested to unfollow does not exist"},
#                                     status=status.HTTP_404_NOT_FOUND)
#
#             """Check if the following record already exists, if not create it, but if it does, fail silently"""
#             if UserFollowings.objects.filter(user=follower, is_following=is_following).exists():
#                 UserFollowings.objects.filter(user=follower, is_following=is_following).delete()
#                 """Increment the users' following and followers respectively"""
#                 follower.followings -= 1
#                 follower.save()
#                 is_following.followers -= 1
#                 is_following.save()
#
#             return JsonResponse({'status': True}, status=status.HTTP_200_OK)
#         except Exception as e:
#             print(e)
#             # return JsonResponse({'status': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)


class ListUserPosts(ListAPIView):
    def get_queryset(self):
        return Post.objects.filter(user__username=self.kwargs.get('username')).order_by('-updated')

    serializer_class = CreatePostSerializer
    pagination_class = PostPagination
    permission_classes = (IsOwnerOrReadOnly,)


class ListFollowers(ListAPIView):
    def get_queryset(self):
        """Select related is to reduce the number of queries sent to the database, because we are also trying to
        make data more simple from the serializer end"""
        return UserFollowings.objects.select_related('user').filter(
            is_following__username=self.kwargs.get('username')).order_by('-created')

    serializer_class = FollowerSerializer
    pagination_class = FollowerPagination


class ListFollowings(ListAPIView):
    def get_queryset(self):
        return UserFollowings.objects.select_related('is_following').filter(
            user__username=self.kwargs.get('username')).order_by('-created')

    serializer_class = FollowingSerializer
    pagination_class = FollowerPagination


class ListMyCreatedTopics(ListAPIView):
    """These are topics that were created by the current authenticated user
    there is no point letting the creator of the topic public"""

    def get_queryset(self):
        return Topic.objects.filter(user=self.request.user).order_by('-created')

    serializer_class = TopicSerializer
    pagination_class = TopicPagination
    permission_classes = (IsAuthenticated,)


class ListMyFollowedTopics(ListAPIView):
    """These are the topics followed by the user, there is not also any point in making the followings of the user
    public so we just gon make use of the request.user to filter out the topics followed"""

    def get_queryset(self):
        return self.request.user.topicfollowing_set.all().order_by('-created')

    serializer_class = TopicFollowedByUserSerializer
    pagination_class = TopicPagination
    permission_classes = (IsAuthenticated,)


class ListMyComments(ListAPIView):
    def get_queryset(self):
        return self.request.user.comment_set.all().order_by('-created')

    serializer_class = ListCommentSerializer
    pagination_class = PostCommentPagination
    permission_classes = (IsAuthenticated,)


class ListMyStarredComments(ListAPIView):
    def get_queryset(self):
        return self.request.user.starredcomment_set.all().order_by('-created')

    serializer_class = StarredCommentSerializer
    pagination_class = PostCommentPagination
    permission_classes = (IsAuthenticated,)


class ListMyFollowedPosts(ListAPIView):
    def get_queryset(self):
        return self.request.user.postfollow_set.all().order_by('-created')

    serializer_class = MyFollowedPostsSerializer
    pagination_class = PostPagination
    permission_classes = (IsAuthenticated,)


class ListMyStarredPosts(ListAPIView):
    def get_queryset(self):
        return self.request.user.starredpost_set.all().order_by('-created')

    serializer_class = MyStarredPostsSerializer
    pagination_class = PostPagination
    permission_classes = (IsAuthenticated,)


class ListMyUpvotedPosts(ListAPIView):
    def get_queryset(self):
        return self.request.user.postupvote_set.all().order_by('-created')

    serializer_class = MyUpvotedPostsSerializer
    pagination_class = PostPagination
    permission_classes = (IsAuthenticated,)


class ListMyUpvotedComments(ListAPIView):
    def get_queryset(self):
        return self.request.user.commentupvote_set.all().order_by('-created')

    serializer_class = MyUpvotedCommentsSerializer
    pagination_class = PostCommentPagination
    permission_classes = (IsAuthenticated,)


class ListMyPolls(ListAPIView):
    def get_queryset(self):
        return self.request.user.my_polls.all().order_by('-created')

    serializer_class = PollSerializer
    pagination_class = PollPagination
    permission_classes = (IsAuthenticated,)
