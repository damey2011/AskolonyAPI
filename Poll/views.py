from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from Poll.models import Poll, UserPolled, PollOption
from Poll.pagination import PollPagination
from Poll.serializers import PollSerializer


class ListCreatePoll(ListCreateAPIView):
    queryset = Poll.objects.all().order_by('-created')
    serializer_class = PollSerializer
    pagination_class = PollPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RetrieveDestroyPoll(DestroyAPIView):
    def get_queryset(self):
        return Poll.objects.filter(pk=self.kwargs.get('pk'))

    serializer_class = PollSerializer

    def get(self, request, pk):
        return Response(self.get_serializer(self.get_object()).data, status=status.HTTP_200_OK)


class VotePoll(APIView):
    def post(self, request, pk):
        # Check if the user has not polled earlier
        up = UserPolled.objects.filter(user=request.user, poll_id=pk)
        if not up.exists():
            po = PollOption.objects.filter(pk=request.data.get('option')).first()
            po.votes += 1
            po.save()
            UserPolled.objects.create(user=request.user, poll_id=pk, poll_option=po)
        return Response(status=status.HTTP_201_CREATED)
