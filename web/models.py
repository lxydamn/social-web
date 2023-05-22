import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    username = models.CharField(max_length=100, null=True, unique=True)
    bio = models.TextField(null=True, default="这个人很懒~ 什么也没留下")
    avator = models.ImageField(null=True, default="https://img1.imgtp.com/2023/05/07/8NKt5JEn.png")
    email = models.EmailField(unique=True ,null =True)
    
    USERNAME_FIELD='username'
    REQUIRED_FIELDS = []

class Postings(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, null=False, blank=False)
    content = models.TextField(max_length=10000,null=False, blank=False)
    title = models.CharField(max_length=50,null=False, blank=False)
    subtitle = models.CharField(max_length=100,null=False, blank=False)
    create_time = models.DateTimeField(default = datetime.datetime.now)
    update_time = models.DateTimeField(auto_now=True)

class Message(models.Model):
    message = models.TextField(max_length=500, blank=True)
    time = models.DateTimeField(default = datetime.datetime.now)

    sender = models.ForeignKey("User", on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey("User", on_delete=models.CASCADE, related_name='receiver')