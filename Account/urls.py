from django.urls import path
from rest_framework.authtoken import views as rest_framework_views

from Account import views

urlpatterns = [
    path('get_auth_token/', rest_framework_views.obtain_auth_token, name='get_auth_token'),
    path('user/', views.CreateAccount.as_view(), name='sign-up'),

    # All Private and populated with the request.user object
    path('user/me/', views.RetrieveUpdateDeleteMe.as_view(), name='get-me'),
    path('user/me/posts-followed/', views.ListMyFollowedPosts.as_view(), name='list-my-followed-posts'),
    path('user/me/posts-starred/', views.ListMyStarredPosts.as_view(), name='list-my-starred-posts'),
    path('user/me/posts-upvoted/', views.ListMyUpvotedPosts.as_view(), name='list-my-upvoted-posts'),
    path('user/me/posts-read/', views.ListMyReadPosts.as_view(), name='list-my-read-posts'),

    path('user/me/feeds/', views.ListMyFeeds.as_view(), name='list-my-feeds'),

    path('user/me/topics/', views.ListMyCreatedTopics.as_view(), name='list-my-topics'),
    path('user/me/topics-followed/', views.ListMyFollowedTopics.as_view(), name='list-my-followed-topics'),

    path('user/me/comments/', views.ListMyComments.as_view(), name='list-my-comments'),
    path('user/me/comments-starred/', views.ListMyStarredComments.as_view(), name='list-my-starred-comments'),
    path('user/me/comments-upvoted/', views.ListMyUpvotedComments.as_view(), name='list-my-comments'),

    path('user/me/polls/', views.ListMyPolls.as_view(), name='list-my-polls'),

    # All public and populated with the username field
    path('user/<slug:username>/', views.RetrieveUpdateDeleteUser.as_view(), name='get-user'),
    path('user/<slug:username>/posts/', views.ListUserPosts.as_view(), name='list-user-posts'),
    path('user/<slug:username>/follow/', views.CreateFollowing.as_view(), name='follow-user'),  # accepts POST and DELETE
    path('user/<slug:username>/followers/', views.ListFollowers.as_view(), name='list-user-followers'),
    path('user/<slug:username>/followings/', views.ListFollowings.as_view(), name='list-user-followings'),
]
