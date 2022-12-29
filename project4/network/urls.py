
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/", views.reProfile, name="reProfile"),
    path("profile/<slug:username>", views.profile, name="profile"),
    path("following/", views.following, name="following"),

    # APIs
    path("follow/", views.follow, name="follow"),
    path("unfollow/", views.unfollow, name="unfollow"),
    path("check/following/<slug:username>", views.check_following, name="checkfollowing"),
    path("editpost/", views.editPost, name="editPost"),
    path("like/", views.like, name="like"),
    path("getpost/<int:postId>", views.getpost, name="getpost")
]
