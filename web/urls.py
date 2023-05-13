from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.loginPage, name='login'),
    path("register", views.registerPage, name='register'),
    path("logout", views.logoutUser, name='logout'),
    path("topics", views.topics, name='topics'),
    path("topics/hot", views.topics_hot, name='topics_hot'),
    path("topics/recent", views.topics_recent, name='topics_recent'),
    path("update/user", views.updateUser, name='updateUser'),
    path("create/post", views.createPost, name='createPost')

]