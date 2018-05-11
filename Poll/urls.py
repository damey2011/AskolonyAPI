from django.urls import path

from Poll import views

urlpatterns = [
    path('', views.ListCreatePoll.as_view(), name='list-create-poll'),
    path('explore/', views.ListExplorePoll.as_view(), name='list-explore-poll'),
    path('<int:pk>/', views.RetrieveDestroyPoll.as_view(), name='get-delete-poll'),
    path('<int:pk>/vote/', views.VotePoll.as_view(), name='vote-poll'),
]
