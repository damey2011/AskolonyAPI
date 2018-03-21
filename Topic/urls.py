from django.urls import path

from Topic import views

urlpatterns = [
    path('', views.ListCreateTopic.as_view(), name='list-create-topic'),
    path('<int:pk>/', views.RetrieveUpdateDeleteTopic.as_view(), name='get-topic'),
    path('<int:pk>/follow/', views.ListCreateDestroyFollowTopic.as_view(), name='follow-topic'),
    # Accepts GET, POST and DELETE
]
