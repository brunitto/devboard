from django.urls import path
from main.views import (
    home_view,
    post_comment_downvote_create_view,
    post_comment_upvote_create_view,
    post_upvote_create_view,
    user_create_view,
    user_follow_create_view,
    user_login_view,
    user_list_view,
    user_detail_view,
    post_list_view,
    post_create_view,
    post_detail_view,
    post_comment_create_view,
    post_downvote_create_view,
    user_follow_delete_view,
    user_logout_view
)


urlpatterns = [
    path('', home_view),
    path('user/', user_list_view),
    path('user/create/', user_create_view),
    path('user/login/', user_login_view),
    path('user/logout/', user_logout_view),
    path('user/<id>/', user_detail_view), # paths with variables should be last
    path('user/<id>/follow/create/', user_follow_create_view),
    path('user/<id>/follow/delete/', user_follow_delete_view),
    path('post/', post_list_view),
    path('post/create/', post_create_view),
    path('post/<id>/', post_detail_view), # paths with variables should be last
    path('post/<id>/comment/create/', post_comment_create_view), # paths with variables should be last
    path('post/<id>/upvote/create/', post_upvote_create_view),
    path('post/<id>/downvote/create/', post_downvote_create_view),
    path('post/<post_id>/comment/<comment_id>/upvote/create/', post_comment_upvote_create_view),
    path('post/<post_id>/comment/<comment_id>/downvote/create/', post_comment_downvote_create_view),
]
