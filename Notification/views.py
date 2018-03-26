from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from Notification.models import Notification
from Notification.paginations import NotificationPagination
from Notification.permissions import IsNotificationOwner
from Notification.serializers import NotificationSerializer


class AllNotifications(ListAPIView):
    """List all the currently authenticated user's notifications"""
    def get_queryset(self):
        return Notification.objects.filter(owner=self.request.user).order_by('-created')

    serializer_class = NotificationSerializer
    pagination_class = NotificationPagination
    permission_classes = (IsAuthenticated,)


class MarkAllNotificationsAsRead(APIView):
    """Mark all the currently authenticated user's notifications as read"""
    def post(self, request):
        n = Notification.objects.filter(owner=self.request.user, read=False)
        for note in n:
            note.read = True
            note.save()
        return Response(data={'status': True}, status=status.HTTP_200_OK)

    permission_classes = (IsAuthenticated,)


class MarkNotificationAsRead(APIView):
    """Mark a single notification as read of currently authenticated user"""
    permission_classes = (IsNotificationOwner, IsAuthenticated,)

    def post(self, request, pk):
        note = Notification.objects.filter(pk=pk).first()
        note.read = True
        note.save()
        return Response(data={'status': True}, status=status.HTTP_200_OK)
