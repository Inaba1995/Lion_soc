from django.urls import path
from . import views

urlpatterns = [
    path("", views.feed, name="feed"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("post/create/", views.post_create, name="post-create"),
    path("post/<int:pk>/delete/", views.post_delete, name="post-delete"),
    path("post/<int:pk>/like/", views.like_toggle, name="like-toggle"),
    path("post/<int:pk>/comment/", views.comment_create, name="comment-create"),
    path("follow/<str:username>/", views.follow_toggle, name="follow-toggle"),
    path("profile/<str:username>/", views.profile, name="profile"),
    path("search/", views.search_users, name="search"),
    path("notifications/", views.notifications, name="notifications"),
]
