from django.contrib import admin

# Register your models here.
from Post.models import Post, PostUpvote, PostDownvote, PostTag, PostFollow, Comment, CommentUpvote, CommentDownvote, \
    StarredPost, FlaggedPost, StarredComment, FlaggedComment

admin.site.register(Post)
admin.site.register(PostUpvote)
admin.site.register(PostDownvote)
admin.site.register(PostTag)
admin.site.register(PostFollow)
admin.site.register(Comment)
admin.site.register(CommentUpvote)
admin.site.register(CommentDownvote)
admin.site.register(StarredPost)
admin.site.register(FlaggedPost)
admin.site.register(StarredComment)
admin.site.register(FlaggedComment)
