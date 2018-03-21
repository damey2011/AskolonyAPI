from django.urls import path
from rest_framework.authtoken import views as rest_framework_views

from Account import views

urlpatterns = [
    path('get_auth_token/', rest_framework_views.obtain_auth_token, name='get_auth_token'),
    path('user/', views.CreateAccount.as_view(), name='sign-up'),
    path('user/<slug:username>/', views.RetrieveUpdateDeleteUser.as_view(), name='get-user'),
    path('user/<slug:username>/follow/', views.CreateFollowing.as_view(), name='follow-user'),
    path('user/<slug:username>/unfollow/', views.DeleteFollowing.as_view(), name='unfollow-user')
]