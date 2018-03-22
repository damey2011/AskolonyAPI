from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, DestroyAPIView, CreateAPIView
from rest_framework.mixins import DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from Post.models import Post, PostFollow, Comment, PostUpvote, PostDownvote, StarredPost, FlaggedPost, StarredComment, \
    FlaggedComment, CommentUpvote
from Post.paginations import PostPagination, PostFollowPagination, PostCommentPagination, PostVotePagination, \
    StarredPostPagination, FlaggedPostPagination
from Post.permissions import PostPermission, IsAuthenticatedOrReadOnly
from Post.serializers import CreatePostSerializer, RetrieveUpdateDestroyPostSerializer, PostFollowSerializer, \
    PostUpvoteSerializer, PostDownvoteSerializer, StarredPostSerializer, \
    FlaggedPostSerializer, StarredCommentSerializer, FlaggedCommentSerializer, ListCommentUpvoteSerializer, \
    CreateCommentUpvoteSerializer, CreateCommentDownvoteSerializer, ListCommentSerializer, CreateCommentSerializer


class RetrieveCreatePosts(ListCreateAPIView):
    """List and Create a new Post"""
    queryset = Post.objects.all().order_by('-created')
    serializer_class = CreatePostSerializer
    pagination_class = PostPagination
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RetrieveUpdateDestroyPost(RetrieveUpdateDestroyAPIView):
    """Retrieve Update and Delete Post"""
    queryset = Post.objects.all()
    serializer_class = RetrieveUpdateDestroyPostSerializer
    permission_classes = (IsAuthenticated, PostPermission)


class ListCreateDestroyPostFollow(ListCreateAPIView, DestroyModelMixin):
    serializer_class = PostFollowSerializer
    pagination_class = PostFollowPagination
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return PostFollow.objects.filter(topic_id=self.kwargs.get('pk')).order_by('-created')

    def delete(self, request, *args, **kwargs):
        post_id = self.kwargs.get('pk')
        user = request.user

        post_following = PostFollow.objects.filter(post_id=post_id, user=user)

        if post_following.exists():
            post_following.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return JsonResponse({"error": "The post you requested to unfollow does not exist"})

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, post_id=self.kwargs.get('pk'))

#
# class ListCreatePostFollow(ListCreateAPIView):
#     """Follow a post"""
#     def get_queryset(self):
#         return PostFollow.objects.filter(post_id=self.kwargs.get('pk'))
#
#     serializer_class = PostFollowSerializer
#     pagination_class = PostFollowPagination
#     permission_classes = (IsAuthenticated,)
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user, post_id=self.kwargs['pk'])
#
#
# class DestroyPostFollow(APIView):
#     """Unfollow Post"""
#
#     def post(self, request, pk):
#         post_following = PostFollow.objects.filter(user=request.user, post_id=pk)
#         if post_following.exists():
#             post_following.delete()
#             return JsonResponse({}, status=status.HTTP_200_OK)
#         else:
#             return JsonResponse({"error": "The post you requested to unfollow does not exist"})
#
#     permission_classes = (IsAuthenticated, PostPermission)


class ListCreatePostComment(ListCreateAPIView):
    def get_queryset(self):
        return Comment.objects.filter(parent_post_id=self.kwargs.get('parent_post_id')).order_by('-created')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ListCommentSerializer
        else:
            return CreateCommentSerializer

    pagination_class = PostCommentPagination
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, parent_post_id=self.kwargs.get('parent_post_id'))


class ListCreateCommentComment(ListCreateAPIView):
    def get_queryset(self):
        return Comment.objects.filter(parent_comment_id=self.kwargs.get('parent_comment_id'),
                                      parent_post_id=self.kwargs.get('parent_post_id')).order_by('-created')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ListCommentSerializer
        else:
            return CreateCommentSerializer

    pagination_class = PostCommentPagination
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user,
                        parent_post_id=self.kwargs.get('parent_post_id'),
                        parent_comment_id=self.kwargs.get('parent_comment_id'))


class RetrieveUpdateDeleteComment(RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        return Comment.objects.filter(pk=self.kwargs.get('pk'))

    serializer_class = ListCommentSerializer
    permission_classes = (IsAuthenticated, PostPermission,)
    lookup_field = 'pk'


class ListCreatePostUpvote(ListCreateAPIView):
    serializer_class = PostUpvoteSerializer
    pagination_class = PostVotePagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return PostUpvote.objects.filter(post_id=self.kwargs.get('pk')).order_by('-created')

    def post(self, request, *args, **kwargs):
        """TO whom it may concern, we are overriding the post method in other to check and avoid multiple upvotes"""
        user = request.user
        post_id = self.kwargs.get('pk')

        post_upvote = PostUpvote.objects.filter(user=user, post_id=post_id)
        if not post_upvote.exists():
            post_upvote = PostUpvote.objects.create(user=user, post_id=post_id)
        return Response(self.get_serializer(post_upvote).data, status=201)

    def delete(self, request, *args, **kwargs):
        """TO whom it may concern, we are overriding the post method in other to check and avoid multiple upvotes"""
        user = request.user
        post_id = self.kwargs.get('pk')

        post_upvote = PostUpvote.objects.filter(user=user, post_id=post_id)
        if post_upvote.exists():
            post_upvote.delete()
        return Response(self.get_serializer(post_upvote).data, status=204)


class ListCreatePostDownvote(ListCreateAPIView):
    serializer_class = PostDownvoteSerializer
    pagination_class = PostVotePagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return PostDownvote.objects.filter(post_id=self.kwargs.get('pk')).order_by('-created')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, post_id=self.kwargs.get('pk'))

    def post(self, request, *args, **kwargs):
        """To whom it may concern, we are overriding the post method in other to check and avoid multiple downvotes"""
        user = request.user
        post_id = self.kwargs.get('pk')

        post_downvote = PostDownvote.objects.filter(user=user, post_id=post_id)
        if not post_downvote.exists():
            post_downvote = PostDownvote.objects.create(user=user, post_id=post_id)
        return Response(self.get_serializer(post_downvote).data, status=201)

    def delete(self, request, *args, **kwargs):
        """TO whom it may concern, we are overriding the post method in other to check and avoid multiple upvotes"""
        user = request.user
        post_id = self.kwargs.get('pk')

        post_downvote = PostDownvote.objects.filter(user=user, post_id=post_id)
        if post_downvote.exists():
            post_downvote.delete()
        return Response(status=204)


class ListCreateDeleteStarPost(ListCreateAPIView):
    serializer_class = StarredPostSerializer
    pagination_class = StarredPostPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return StarredPost.objects.filter(post_id=self.kwargs.get('pk')).order_by('-created')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, post_id=self.kwargs.get('pk'))

    def post(self, request, *args, **kwargs):
        """To whom it may concern, we are overriding the post method in other to check and avoid multiple starring"""
        user = request.user
        post_id = self.kwargs.get('pk')

        starred_post = StarredPost.objects.filter(user=user, post_id=post_id)
        if not starred_post.exists():
            starred_post = StarredPost.objects.create(user=user, post_id=post_id)
        return Response(self.get_serializer(starred_post).data, status=201)

    def delete(self, request, *args, **kwargs):
        user = request.user
        post_id = self.kwargs.get('pk')

        starred_post = StarredPost.objects.filter(user=user, post_id=post_id)
        if starred_post.exists():
            starred_post.delete()
        return Response(status=204)


class ListCreateDeleteFlagPost(ListCreateAPIView):
    serializer_class = FlaggedPostSerializer
    pagination_class = FlaggedPostPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return FlaggedPost.objects.filter(post_id=self.kwargs.get('pk')).order_by('-created')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, post_id=self.kwargs.get('pk'))

    def post(self, request, *args, **kwargs):
        """To whom it may concern, we are overriding the post method in other to check and avoid multiple starring"""
        user = request.user
        post_id = self.kwargs.get('pk')

        flagged_post = FlaggedPost.objects.filter(user=user, post_id=post_id)
        if not flagged_post.exists():
            flagged_post = FlaggedPost.objects.create(user=user, post_id=post_id)
        return Response(self.get_serializer(flagged_post).data, status=201)

    def delete(self, request, *args, **kwargs):
        user = request.user
        post_id = self.kwargs.get('pk')

        flagged_post = FlaggedPost.objects.filter(user=user, post_id=post_id)
        if flagged_post.exists():
            flagged_post.delete()
        return Response(status=204)


class ListCreateDeleteStarComment(ListCreateAPIView):
    serializer_class = StarredCommentSerializer
    pagination_class = StarredPostPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return StarredComment.objects.filter(comment_id=self.kwargs.get('pk')).order_by('-created')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, comment_id=self.kwargs.get('pk'))

    def post(self, request, *args, **kwargs):
        """To whom it may concern, we are overriding the post method in other to check and avoid multiple starring"""
        user = request.user
        post_id = self.kwargs.get('pk')

        starred_comment = StarredComment.objects.filter(user=user, comment_id=post_id)
        if not starred_comment.exists():
            starred_comment = StarredComment.objects.create(user=user, comment_id=post_id)
        return Response(self.get_serializer(starred_comment).data, status=201)

    def delete(self, request, *args, **kwargs):
        user = request.user
        post_id = self.kwargs.get('pk')

        starred_comment = StarredComment.objects.filter(user=user, comment_id=post_id)
        if starred_comment.exists():
            starred_comment.delete()
        return Response(status=204)


class ListCreateDeleteFlagComment(ListCreateAPIView):
    serializer_class = FlaggedCommentSerializer
    pagination_class = FlaggedPostPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return FlaggedComment.objects.filter(comment_id=self.kwargs.get('pk')).order_by('-created')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, comment_id=self.kwargs.get('pk'))

    def post(self, request, *args, **kwargs):
        """To whom it may concern, we are overriding the post method in other to check and avoid multiple flagging"""
        user = request.user
        post_id = self.kwargs.get('pk')

        flagged_comment = FlaggedComment.objects.filter(user=user, comment_id=post_id)
        if not flagged_comment.exists():
            flagged_comment = FlaggedComment.objects.create(user=user, comment_id=post_id)
        return Response(self.get_serializer(flagged_comment).data, status=201)

    def delete(self, request, *args, **kwargs):
        user = request.user
        post_id = self.kwargs.get('pk')

        flagged_comment = FlaggedComment.objects.filter(user=user, comment_id=post_id)
        if flagged_comment.exists():
            flagged_comment.delete()
        return Response(status=204)


class ListCreateDeleteCommentUpvote(ListCreateAPIView):
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ListCommentUpvoteSerializer
        else:
            return CreateCommentUpvoteSerializer

    pagination_class = PostCommentPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return CommentUpvote.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ListCreateDeleteCommentDownvote(ListCreateAPIView):
    serializer_class = CreateCommentDownvoteSerializer
    pagination_class = PostCommentPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return CommentUpvote.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
