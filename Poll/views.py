from rest_framework.generics import ListCreateAPIView

from Poll.models import Poll
from Poll.serializers import PollSerializer


class ListCreatePoll(ListCreateAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
