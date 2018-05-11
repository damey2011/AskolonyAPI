from django.http import Http404
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, DestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from Poll.models import Poll, UserPolled, PollOption
from Poll.pagination import PollPagination
from Poll.permissions import IsPollOwnerOrReadOnly
from Poll.serializers import PollSerializer


class ListCreatePoll(ListCreateAPIView):
    """List all polls and create new poll"""
    queryset = Poll.objects.all().order_by('-created')
    serializer_class = PollSerializer
    pagination_class = PollPagination
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ListExplorePoll(ListAPIView):
    """List polls that user has not voted in"""
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Poll.objects.filter(is_public=True).exclude(pk__in=UserPolled.objects.filter(user=self.request.user).values_list('user', flat=True)).order_by('?')
        return Poll.objects.all()

    serializer_class = PollSerializer
    pagination_class = PollPagination


class RetrieveDestroyPoll(DestroyAPIView):
    """Delete Poll"""
    def get_queryset(self):
        return Poll.objects.filter(pk=self.kwargs.get('pk'))

    serializer_class = PollSerializer
    permission_classes = (IsPollOwnerOrReadOnly,)

    def get(self, request, pk):
        return Response(self.get_serializer(self.get_object()).data, status=status.HTTP_200_OK)


class VotePoll(APIView):
    """Vote in a poll"""
    def post(self, request, pk):
        # Check if the user has not polled earlier
        up = UserPolled.objects.filter(user=request.user, poll_id=pk)
        if not up.exists():
            po = PollOption.objects.filter(pk=request.data.get('option'))
            if not po.exists():
                raise Http404("The option you are voting does not exist")
            po = po.first()
            po.votes += 1
            po.save()
            UserPolled.objects.create(user=request.user, poll_id=pk, poll_option=po)
        return Response(status=status.HTTP_201_CREATED)

    permission_classes = (IsAuthenticated,)
