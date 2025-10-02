from django.urls import path
from django.contrib.auth.views import LogoutView 
from . import views
from .views import *

urlpatterns = [
    path("home/", views.home, name="home"),
    path("", views.login_view, name="login"),
    path("add/", AddView.as_view(), name="add"),
    path("detail/<int:pk>/", PostDetailView.as_view(), name="post_details"),
    path("edit/<int:pk>/", EditView.as_view(), name="edit"),
    path("delete/<int:pk>/", DeleteView.as_view(), name="delete"),
    path("my_blogs/", views.my_blogs, name="my_blogs"),
    path("logout/",CustomLogoutView.as_view(), name="logout"),
    path("comment/<int:post_id>/", views.comment, name="comment"),
    path("like_post/", views.like, name="like"),
] 