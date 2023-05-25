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
    path("search/<str:tabs>", views.search, name='search'),
    path("post/<int:id>", views.postContent, name="postContent"),
    path("chat", views.message, name='message'),
    path("chat/<str:username>", views.chat, name='chat')
]