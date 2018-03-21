from django.urls import path

from Questions import views

urlpatterns = [
    path('', views.ListCreateQuestion.as_view(), name='list-create-question'),
    path('<int:pk>/', views.QuestionRetrieveUpdateDestroy.as_view(), name='get-question'),
    path('<int:pk>/follow/', views.FollowQuestion.as_view(), name='follow-question'),
    path('<int:pk>/unfollow/', views.UnFollowQuestion.as_view(), name='unfollow-question'),
]