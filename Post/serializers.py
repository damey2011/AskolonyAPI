from rest_framework import serializers

from Account.serializers import RetrieveUpdateDeleteUserSerializer, SimpleNoEmailUserSerializer
from Post.models import Post, PostFollow, Comment, PostUpvote, PostDownvote, StarredPost, FlaggedComment, FlaggedPost, \
    StarredComment, CommentUpvote, CommentDownvote, ReadPost


class CreatePostSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    comments = serializers.CharField(source='get_comments_url', read_only=True)
    comments_count = serializers.CharField(source='get_comments_count', read_only=True)
    ups = serializers.IntegerField(read_only=True)
    downs = serializers.IntegerField(read_only=True)
    followers = serializers.IntegerField(read_only=True)
    views = serializers.IntegerField(read_only=True)
    read_time = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = (
            'id',
            'user',
            'title',
            'content',
            'excerpt',
            'ups',
            'downs',
            'read_time',
            'views',
            'followers',
            'image_header',
            'is_anonymous',
            'slug',
            'comments',
            'comments_count',
            'created',
            'updated'
        )

        extra_kwargs = {
            'excerpt': {
                'read_only': True
            },
            'slug': {
                'read_only': True
            }
        }

    def get_user(self, obj):
        if obj.is_anonymous:
            return "Anonymous"
        return RetrieveUpdateDeleteUserSerializer(obj.user).data


class RetrieveUpdateDestroyPostSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    comments = serializers.CharField(source='get_comments_url', read_only=True)
    comments_count = serializers.CharField(source='get_comments_count', read_only=True)
    ups = serializers.IntegerField(read_only=True)
    downs = serializers.IntegerField(read_only=True)
    followers = serializers.IntegerField(read_only=True)
    views = serializers.IntegerField(read_only=True)
    read_time = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = (
            'id',
            'user',
            'title',
            'content',
            'excerpt',
            'ups',
            'downs',
            'read_time',
            'views',
            'followers',
            'image_header',
            'is_anonymous',
            'slug',
            'comments',
            'comments_count',
            'created',
            'updated'
        )
        extra_kwargs = {
            'excerpt': {
                'read_only': True
            },
            'slug': {
                'read_only': True
            }
        }

    def get_user(self, obj):
        if obj.is_anonymous:
            return "Anonymous"
        return RetrieveUpdateDeleteUserSerializer(obj.user).data


class PostFollowSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = PostFollow
        fields = (
            'id',
            'user',
            'post',
            'created'
        )
        extra_kwargs = {
            'user': {
                'required': False
            },
            'post': {
                'required': False
            }
        }

    def get_user(self, obj):
        return RetrieveUpdateDeleteUserSerializer(obj.user).data


class ListCommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            'id',
            'user',
            'body',
            'ups',
            'downs',
            'created'
        )

    def get_user(self, obj):
        return RetrieveUpdateDeleteUserSerializer(obj.user).data


class CreateCommentSerializer(serializers.ModelSerializer):
    parent_post = serializers.SerializerMethodField()
    parent_comment = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            'id',
            'user',
            'body',
            'parent_post',
            'parent_comment',
            'ups',
            'downs',
            'created'
        )

    def get_parent_post(self, obj):
        if obj.parent_post is not None:
            return RetrieveUpdateDestroyPostSerializer(obj.parent_post).data
        return None

    def get_parent_comment(self, obj):
        if obj.parent_comment is not None:
            return ListCommentSerializer(obj.parent_comment).data
        return None

    def get_user(self, obj):
        return RetrieveUpdateDeleteUserSerializer(obj.user).data


class PostUpvoteSerializer(serializers.ModelSerializer):
    post = RetrieveUpdateDestroyPostSerializer(required=False, write_only=True)
    user = RetrieveUpdateDeleteUserSerializer(required=False)

    class Meta:
        model = PostUpvote
        fields = (
            'id',
            'post',
            'user',
            'created'
        )


class PostDownvoteSerializer(serializers.ModelSerializer):
    post = RetrieveUpdateDestroyPostSerializer(required=False, write_only=True)
    user = RetrieveUpdateDeleteUserSerializer(required=False)

    class Meta:
        model = PostDownvote
        fields = (
            'id',
            'post',
            'user',
            'created'
        )


class StarredPostSerializer(serializers.ModelSerializer):
    post = RetrieveUpdateDestroyPostSerializer(required=False, write_only=True)
    user = RetrieveUpdateDeleteUserSerializer(required=False)

    class Meta:
        model = StarredPost
        fields = (
            'id',
            'post',
            'user',
            'created'
        )


class CreateCommentUpvoteSerializer(serializers.ModelSerializer):
    user = RetrieveUpdateDeleteUserSerializer(required=False)

    class Meta:
        model = CommentUpvote
        fields = (
            'id',
            'comment',
            'user',
            'created'
        )


class CreateCommentDownvoteSerializer(serializers.ModelSerializer):
    user = RetrieveUpdateDeleteUserSerializer(required=False)

    class Meta:
        model = CommentDownvote
        fields = (
            'id',
            'comment',
            'user',
            'created'
        )


class ListCommentUpvoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentUpvote
        fields = (
            'user',
        )

    def to_representation(self, instance):
        return RetrieveUpdateDeleteUserSerializer(instance.user).data


class StarredCommentSerializer(serializers.ModelSerializer):
    comment = ListCommentSerializer(required=False)
    user = RetrieveUpdateDeleteUserSerializer(required=False)

    class Meta:
        model = StarredComment
        fields = (
            'id',
            'comment',
            'user',
            'created'
        )


class FlaggedPostSerializer(serializers.ModelSerializer):
    post = RetrieveUpdateDestroyPostSerializer(required=False)
    user = RetrieveUpdateDeleteUserSerializer(required=False)

    class Meta:
        model = FlaggedPost
        fields = (
            'id',
            'post',
            'user',
            'reason',
            'action_taken',
            'created'
        )


class FlaggedCommentSerializer(serializers.ModelSerializer):
    post = RetrieveUpdateDestroyPostSerializer(required=False)
    user = RetrieveUpdateDeleteUserSerializer(required=False)

    class Meta:
        model = FlaggedComment
        fields = (
            'id',
            'post',
            'user',
            'reason',
            'action_taken',
            'created'
        )


class MyFollowedPostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostFollow
        fields = (
            'post'
        )

    def to_representation(self, instance):
        return RetrieveUpdateDestroyPostSerializer(instance.post).data


class MyStarredPostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StarredPost
        fields = (
            'post'
        )

    def to_representation(self, instance):
        return RetrieveUpdateDestroyPostSerializer(instance.post).data


class MyUpvotedPostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostUpvote
        fields = (
            'post'
        )

    def to_representation(self, instance):
        return RetrieveUpdateDestroyPostSerializer(instance.post).data


class MyUpvotedCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentUpvote
        fields = (
            'comment'
        )

    def to_representation(self, instance):
        return ListCommentSerializer(instance.comment).data


class PostReadersSerializer(serializers.ModelSerializer):
    user = RetrieveUpdateDeleteUserSerializer(read_only=True)
    post = RetrieveUpdateDestroyPostSerializer(read_only=True)

    class Meta:
        model = ReadPost
        fields = (
            'id',
            'user',
            'post'
        )

    def to_representation(self, instance):
        return SimpleNoEmailUserSerializer(instance.user, context=self.context).data


class ReadPostsSerializer(serializers.ModelSerializer):
    user = RetrieveUpdateDeleteUserSerializer(read_only=True)
    post = RetrieveUpdateDestroyPostSerializer(read_only=True)

    class Meta:
        model = ReadPost
        fields = (
            'id',
            'user',
            'post',
            'created'
        )

    def to_representation(self, instance):
        return RetrieveUpdateDestroyPostSerializer(instance.post).data
