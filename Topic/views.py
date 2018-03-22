from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import DestroyModelMixin
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from Topic.models import Topic, TopicFollowing
from Topic.pagination import TopicPagination
from Topic.serializers import TopicSerializer, TopicFollowSerializer


class ListCreateTopic(ListCreateAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    pagination_class = TopicPagination
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class RetrieveUpdateDeleteTopic(RetrieveUpdateDestroyAPIView):
    serializer_class = TopicSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Topic.objects.filter(pk=self.kwargs.get('pk'))


class ListCreateDestroyFollowTopic(ListCreateAPIView, DestroyModelMixin):
    serializer_class = TopicFollowSerializer
    pagination_class = TopicPagination
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return TopicFollowing.objects.filter(user=self.request.user, topic_id=self.kwargs.get('pk'))

    def delete(self, request, *args, **kwargs):
        topic_id = self.kwargs.get('pk')
        user = request.user

        topic_following = TopicFollowing.objects.filter(topic_id=topic_id, user=user)

        if topic_following.exists():
            topic_following.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, topic_id=self.kwargs.get('pk'))
