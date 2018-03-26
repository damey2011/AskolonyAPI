from django.http import JsonResponse
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, DestroyAPIView, CreateAPIView
from rest_framework.mixins import DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from Post.models import Post, PostFollow, Comment, PostUpvote, PostDownvote, StarredPost, FlaggedPost, StarredComment, \
    FlaggedComment, CommentUpvote, ReadPost
from Post.paginations import PostPagination, PostFollowPagination, PostCommentPagination, PostVotePagination, \
    StarredPostPagination, FlaggedPostPagination
from Post.permissions import PostPermission, IsAuthenticatedOrReadOnly
from Post.serializers import CreatePostSerializer, RetrieveUpdateDestroyPostSerializer, PostFollowSerializer, \
    PostUpvoteSerializer, PostDownvoteSerializer, StarredPostSerializer, \
    FlaggedPostSerializer, StarredCommentSerializer, FlaggedCommentSerializer, ListCommentUpvoteSerializer, \
    CreateCommentUpvoteSerializer, CreateCommentDownvoteSerializer, ListCommentSerializer, CreateCommentSerializer, \
    PostReadersSerializer


class RetrieveCreatePosts(ListCreateAPIView):
    """List and Create a new Post, also allows search with URL. e.g http://example.com/posts/?search=React.
    It also permits us to add ordering to the results, based on 'upvotes', 'views', 'created' hereby allowing us have
    URL like http://sample.com/posts/?ordering=upvotes and same applies to the other fields that can be used for sorting.
    created means the time of creation"""
    queryset = Post.objects.all().order_by('-created')
    serializer_class = CreatePostSerializer
    pagination_class = PostPagination
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (SearchFilter, OrderingFilter,)
    filter_fields = ('title',)
    ordering_fields = ('-upvotes', '-views', '-created',)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RetrieveUpdateDestroyPost(RetrieveUpdateDestroyAPIView):
    """Retrieve Update and Delete Post"""
    queryset = Post.objects.all()
    serializer_class = RetrieveUpdateDestroyPostSerializer
    permission_classes = (IsAuthenticated, PostPermission)


class ListCreateDestroyPostFollow(ListCreateAPIView, DestroyModelMixin):
    """Follow and unfollow post"""
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
    """Create and list all comments of a particular post"""

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
    """List children comments of comment and also create child comment of comment"""

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
    """Retrieve Update and Delete a comment"""

    def get_queryset(self):
        return Comment.objects.filter(pk=self.kwargs.get('pk'))

    serializer_class = ListCommentSerializer
    permission_classes = (IsAuthenticated, PostPermission,)
    lookup_field = 'pk'


class ListCreatePostUpvote(ListCreateAPIView):
    """List upvotes of a particular post and also Upvote and Unupvote same post"""
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
    """List downvotes of a particular post and also Downvote and Undownvote same post"""
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
    """List stars of a particular post and also star and unstar same post"""

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
    """List flags of a particular post and also flag and unflag same post"""
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
    """List stars of a particular comment and also star and unstar same comment"""

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
    """List flags of a particular comment and also flag and unflag same comment"""

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
    """List upvotes of a particular comment and also upvote and unupvote same comment"""

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
    """List downvotes of a particular comment and also downvote and undownvote same comment"""

    serializer_class = CreateCommentDownvoteSerializer
    pagination_class = PostCommentPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return CommentUpvote.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MarkPostAsRead(ListCreateAPIView):
    """List those that have read a post and also mark a post as read by the currently authenticated user"""

    def post(self, request, *args, **kwargs):
        # Check if the user has already been recorded to have read the post
        rp = ReadPost.objects.filter(user=request.user, post_id=self.kwargs.get('pk'))

        if not rp.exists():
            ReadPost.objects.create(post_id=self.kwargs.get('pk'), user=request.user)

        return Response(status=status.HTTP_201_CREATED)

    def get_queryset(self):
        return ReadPost.objects.filter(post_id=self.kwargs.get('pk')).order_by('-created')

    serializer_class = PostReadersSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = PostPagination
