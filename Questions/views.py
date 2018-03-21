from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from Post.permissions import IsAuthenticatedOrReadOnly
from Questions.models import Question, QuestionFollowing
from Questions.paginations import QuestionPagination
from Questions.permissions import QuestionPermission
from Questions.serializers import QuestionCreateSerializer, QuestionRetrieveUpdateDeleteSerializer


class ListCreateQuestion(ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionCreateSerializer
    pagination_class = QuestionPagination
    permission_classes = (IsAuthenticatedOrReadOnly, QuestionPermission,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class QuestionRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    serializer_class = QuestionRetrieveUpdateDeleteSerializer
    permission_classes = (QuestionPermission,)

    def get_queryset(self):
        return Question.objects.filter(pk=self.kwargs.get('pk'))

    def perform_update(self, serializer):
        serializer.save(last_updated_by=self.request.user)


class FollowQuestion(APIView):
    def post(self, request, pk):
        """This Class creates a new following record, the pk in the URL is the question being followed
        THe user that follows is gotten from the request object"""
        try:
            follower = request.user
            question = Question.objects.filter(pk=pk).first()

            """Return HTTP 404 if the question does not exist"""
            if question is None:
                return JsonResponse({"error": "Question you requested to follow does not exist"}, status=status.HTTP_404_NOT_FOUND)

            """Check if the following record already exists, if not create it, but if it does, fail silently"""
            if not QuestionFollowing.objects.filter(user=follower, question=question).exists():
                QuestionFollowing.objects.create(user=follower, question=question)
                """Increment the question's following"""
                question.followings += 1
                question.save()

            return JsonResponse({'status': True}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            # return JsonResponse({'status': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    permission_classes = (IsAuthenticated,)


class UnFollowQuestion(APIView):
    def post(self, request, pk):
        try:
            follower = request.user
            question = Question.objects.filter(pk=pk).first()

            """Return HTTP 404 if the question does not exist"""
            if question is None:
                return JsonResponse({"error": "Question you requested to unfollow does not exist"},
                                    status=status.HTTP_404_NOT_FOUND)

            """Check if the following record already exists, if not create it, but if it does, fail silently"""
            if QuestionFollowing.objects.filter(user=follower, question=question).exists():
                QuestionFollowing.objects.filter(user=follower, question=question).delete()
                """Decrement the question's following"""
                question.followings -= 1
                question.save()

            return JsonResponse({'status': True}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            # return JsonResponse({'status': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    permission_classes = (IsAuthenticated,)
