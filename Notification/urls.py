from django.urls import path

from Notification import views

urlpatterns = [
    path('', views.AllNotifications.as_view(), name="get-notifications"),
    path('mark/', views.MarkAllNotificationsAsRead.as_view(), name="mark-all-as-read"),
    path('<int:pk>/mark/', views.MarkNotificationAsRead.as_view(), name="mark-as-read")
]