from django.db import models
from functools import reduce

# Create your models here.
from django.urls import reverse
from django.utils.text import slugify

from AskolonyAPI import settings


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.TextField()
    content = models.TextField()
    excerpt = models.TextField()
    ups = models.PositiveIntegerField(default=0)
    downs = models.PositiveIntegerField(default=0)
    read_time = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)  # No of views on the post
    slug = models.SlugField(max_length=100, unique=True)
    followers = models.PositiveIntegerField(default=0)
    image_header = models.ImageField(upload_to='post-headers', default='/default/post-header.png')
    is_anonymous = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{0} - {1}'.format(self.user.get_full_name(), self.title)

    def get_comments_url(self):
        return str(reverse('list-create-post-comment', kwargs={'parent_post_id': self.pk}))

    def get_comments_count(self):
        return str(Comment.objects.filter(parent_post=self, parent_comment=None).count())

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = slugify(self.title)[:40]
        self.excerpt = reduce(lambda excerpt, next_item: excerpt + ' ' + next_item, self.content.split(' ')[:15])
        super(Post, self).save(*args, **kwargs)


class PostUpvote(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='upvotes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{0} - {1}'.format(self.user.get_full_name(), self.post.title)


class PostDownvote(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='downvotes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{0} - {1}'.format(self.user.get_full_name(), self.post.title)


class PostTag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='tags')
    tag = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{0} [{1}]'.format(self.tag, self.post.title)


class PostFollow(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{0}-{1}'.format(self.user.get_full_name(), self.post.title)


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    parent_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    ups = models.PositiveIntegerField(default=0)
    downs = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.parent_post.title


class CommentUpvotes(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='upvotes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{0} - {1}'.format(self.user.get_full_name(), self.comment.parent_post.title)


class CommentDownvote(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='downvotes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{0} - {1}'.format(self.user.get_full_name(), self.comment.parent_post.title)


class StarredPost(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s starred %s" % (self.user.username, self.post.title)


class FlaggedPost(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    reason = models.TextField()
    action_taken = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s flagged %s" % (self.user.username, self.post.title)


class StarredComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s starred %s" % (self.user.username, self.comment.parent_post.title)


class FlaggedComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    reason = models.TextField()
    action_taken = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s flagged %s" % (self.user.username, self.comment.parent_post.title)