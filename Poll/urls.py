from django.urls import path

from Poll import views

urlpatterns = [
    path('', views.ListCreatePoll.as_view(), name='list-create-poll')
]
