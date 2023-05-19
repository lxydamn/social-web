from django.contrib import admin
from .models import User, Postings, Message
# Register your models here.

admin.site.register(User)
admin.site.register(Postings)
admin.site.register(Message)