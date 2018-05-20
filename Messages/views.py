from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import Http404, JsonResponse
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from Messages.models import Message, Conversation
from Messages.paginations import MessageThreadPagination
from Messages.serializers import MessageThreadSerializer, MessageSerializer

User = get_user_model()


class AllConversations(ListAPIView):
    """List all the currently authenticated user's conversation threads"""

    def get_queryset(self):
        user = self.request.user

        return Message.objects.filter(
            Q(sender=user) |
            Q(recipient=user)
        ).distinct('conversation').order_by('-conversation_id', '-created')

    serializer_class = MessageThreadSerializer
    # pagination_class = MessageThreadPagination
    permission_classes = (IsAuthenticated,)


class ConversationMessages(ListAPIView):
    """List and also create messages of a particular thread """

    def get_queryset(self):
        return Message.objects.filter(conversation_id=self.kwargs.get('pk')).order_by('created')

    serializer_class = MessageSerializer
    # pagination_class = MessageThreadPagination
    permission_classes = (IsAuthenticated,)


class SendMessage(CreateAPIView):
    """Send message to a user or start a new conversation, carries only 'text' as payload e.g. {'text': 'Hello George'}"""
    permission_classes = (IsAuthenticated,)
    serializer_class = MessageSerializer

    def post(self, request, *args, **kwargs):
        username = self.kwargs.get('username')

        recipient = User.objects.filter(username=username)
        if recipient.count() == 0:
            raise Http404
        recipient = recipient.first()

        m = Message.objects.filter(
            Q(sender=request.user, recipient=recipient) |
            Q(sender=recipient, recipient=request.user)
        )

        global message

        if m.exists():
            message = Message.objects.create(sender=request.user,
                                             recipient=recipient,
                                             text=request.data.get('text', ''),
                                             conversation_id=m.first().conversation_id)
        else:
            new_conversation = Conversation.objects.create(starter=request.user)
            message = Message.objects.create(sender=request.user,
                                             recipient=recipient,
                                             text=request.data.get('text', ''),
                                             conversation_id=new_conversation.id)

        return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)


class MarkMessageAsRead(APIView):
    def post(self, request, pk):
        ms = Message.objects.filter(conversation_id=pk, recipient=request.user, read=False)
        for m in ms:
            m.read = True
            m.save()
        return JsonResponse({'status': True}, safe=False, status=201)

    permission_classes = (IsAuthenticated,)


class MarkAllMessageAsRead(APIView):
    def post(self, request):
        ms = Message.objects.filter(recipient=request.user, read=False)
        for m in ms:
            m.read = True
            m.save()
        return JsonResponse({'status': True}, safe=False, status=201)

    permission_classes = (IsAuthenticated,)
