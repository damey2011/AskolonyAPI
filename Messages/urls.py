from django.urls import path

from Messages import views

urlpatterns = [
    path('<slug:username>/send/', views.SendMessage.as_view(), name="send-message"),
    path('threads/', views.AllConversations.as_view(), name="all-conversations"),
    path('threads/<int:pk>/', views.ConversationMessages.as_view(), name="conversation-messages")
]
