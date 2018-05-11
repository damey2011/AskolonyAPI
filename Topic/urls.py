from django.urls import path

from Topic import views

urlpatterns = [
    path('', views.ListCreateTopic.as_view(), name='list-create-topic'),
    path('explore/', views.ListTopicsToFollow.as_view(), name='list-explore-topic'),
    path('<int:pk>/', views.RetrieveUpdateDeleteTopic.as_view(), name='get-topic'),
    path('<int:pk>/follow/', views.ListCreateDestroyFollowTopic.as_view(), name='follow-topic'),
    path('<int:pk>/posts/', views.ListTopicPosts.as_view(), name='topic-posts'),
    # Accepts GET, POST and DELETE
]
