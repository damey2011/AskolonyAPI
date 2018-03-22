from django.urls import path

from Post import views

urlpatterns = [
    path('', views.RetrieveCreatePosts.as_view(), name='create-post'),
    path('<int:pk>/', views.RetrieveUpdateDestroyPost.as_view(), name='get-post'),
    path('<int:pk>/upvote/', views.ListCreatePostUpvote.as_view(), name='upvote-post'),  # Accepts GET, POST, DELETE
    path('<int:pk>/downvote/', views.ListCreatePostDownvote.as_view(), name='downvote-post'),  # Accepts GET, POST, DELETE
    path('<int:pk>/follow/', views.ListCreateDestroyPostFollow.as_view(), name='follow-post'),  # Accepts GET, POST, DELETE
    path('<int:pk>/star/', views.ListCreateDeleteStarPost.as_view(), name='star-post'),   # Accepts GET, POST, DELETE
    path('<int:pk>/flag/', views.ListCreateDeleteFlagPost.as_view(), name='flag-post'),   # Accepts GET, POST, DELETE
    path('<int:parent_post_id>/comment/', views.ListCreatePostComment.as_view(), name='list-create-post-comment'),
    path('<int:parent_post_id>/comment/<int:pk>/', views.RetrieveUpdateDeleteComment.as_view(), name='get-comment'),
    path('<int:parent_post_id>/comment/<int:parent_comment_id>/reply/', views.ListCreateCommentComment.as_view(), name='list-create-comment-comment'),
    # This path is used to retrieve any comment detail irrespective of the parent
    path('<int:parent_post_id>/comment/<int:pk>/upvote/', views.ListCreateDeleteCommentUpvote.as_view(), name='upvote-comment'),   # Accepts GET, POST, DELETE
    path('<int:parent_post_id>/comment/<int:pk>/downvote/', views.ListCreateDeleteCommentDownvote.as_view(), name='downvote-comment'),   # Accepts GET, POST, DELETE
    path('<int:parent_post_id>/comment/<int:pk>/star/', views.ListCreateDeleteStarComment.as_view(), name='star-comment'),   # Accepts GET, POST, DELETE
    path('<int:parent_post_id>/comment/<int:pk>/flag/', views.ListCreateDeleteFlagComment.as_view(), name='flag-comment'),   # Accepts GET, POST, DELETE
]
