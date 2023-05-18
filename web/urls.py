from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.loginPage, name='login'),
    path("register", views.registerPage, name='register'),
    path("logout", views.logoutUser, name='logout'),
    path("topics", views.topics, name='topics'),
    path("update/user", views.updateUser, name='updateUser'),
    path("create/post", views.createPost, name='createPost'),
    path("get/page", views.indexGetPage, name="getPage"),
    path("post/<int:id>", views.postContent, name="postContent"),
    path("message", views.message, name='message')
]