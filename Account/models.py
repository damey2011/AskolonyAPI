from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class User(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField()
    picture = models.ImageField(upload_to='user-images', default='/default/user.png')
    followings = models.IntegerField(default=0)
    followers = models.IntegerField(default=0)

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.email

    def is_following(self, user, is_following):
        return UserFollowings.objects.filter(user=user, is_following=is_following).exists()


class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, related_name='profile')
    college = models.CharField(max_length=50, blank=True, default='NA')
    works = models.CharField(max_length=100, blank=True, default='NA')
    lives = models.CharField(max_length=50, blank=True, default='NA')
    facebook_link = models.URLField(max_length=100, blank=True, default='http://facebook.com')
    twitter_link = models.URLField(max_length=100, blank=True, default='http://twitter.com')
    linked_in_profile = models.URLField(max_length=100, blank=True, default='http://linkedin.com')

    def __str__(self):
        return self.user.get_full_name()


class UserStats(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, related_name='stats')
    reads = models.IntegerField(null=True, default=0)
    comments = models.IntegerField(default=0)
    writes = models.IntegerField(default=0)
    ups = models.IntegerField(default=0)
    downs = models.IntegerField(default=0)

    def __str__(self):
        return self.user.get_full_name()


# User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
# User.stats = property(lambda u: UserStats.objects.get_or_create(user=u)[0])

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        UserProfile.objects.create(user=instance)
        UserStats.objects.create(user=instance)


class UserFollowings(models.Model):
    user = models.ForeignKey(User, related_name='%(app_label)s_%(class)s_related', on_delete=models.CASCADE)
    is_following = models.ForeignKey(User, related_name='%(app_label)s_%(class)s', on_delete=models.CASCADE)
    created = models.DateTimeField(null=True)

    def follows(self, user, flwrsOrflwngs):
        if flwrsOrflwngs == 1:
            flwrsOrflwngs = self.is_following
        else:
            flwrsOrflwngs = self.user
        try:
            user_following = UserFollowings.objects.get(user=user, is_following=flwrsOrflwngs)
        except:
            user_following = None
        if user_following is not None:
            return True
        else:
            return False
