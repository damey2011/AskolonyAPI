from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.mixins import DestroyModelMixin
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from Post.models import PostTopic
from Post.paginations import PostPagination
from Topic.models import Topic, TopicFollowing
from Topic.pagination import TopicPagination
from Topic.serializers import TopicSerializer, TopicFollowSerializer, TopicPostSerializer


class ListCreateTopic(ListCreateAPIView):
    """Create and list all topics"""
    queryset = Topic.objects.all().order_by('-created')
    serializer_class = TopicSerializer
    pagination_class = TopicPagination
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ListTopicsToFollow(ListAPIView):
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Topic.objects.exclude(pk__in=TopicFollowing.objects.filter(user=self.request.user).values_list('topic', flat=True)).order_by('?')
        return Topic.objects.all().order_by('?')

    serializer_class = TopicSerializer
    pagination_class = TopicPagination


class RetrieveUpdateDeleteTopic(RetrieveUpdateDestroyAPIView):
    """Retrieve Update and Delete Topic"""
    serializer_class = TopicSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return Topic.objects.filter(pk=self.kwargs.get('pk'))


class ListCreateDestroyFollowTopic(ListCreateAPIView, DestroyModelMixin):
    """List Follows of a topic, follow and unfollow same topic"""
    serializer_class = TopicFollowSerializer
    pagination_class = TopicPagination
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return TopicFollowing.objects.filter(topic_id=self.kwargs.get('pk')).order_by('-created')

    def delete(self, request, *args, **kwargs):
        topic_id = self.kwargs.get('pk')
        user = request.user

        topic_following = TopicFollowing.objects.filter(topic_id=topic_id, user=user)

        if topic_following.exists():
            topic_following.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, topic_id=self.kwargs.get('pk'))


class ListTopicPosts(ListCreateAPIView):
    def get_queryset(self):
        return PostTopic.objects.filter(topic_id=self.kwargs.get('pk')).order_by('-created')

    serializer_class = TopicPostSerializer
    pagination_class = PostPagination

    def perform_create(self, serializer):
        serializer.save(topic_id=self.kwargs.get('pk'), created_by=self.request.user)
