from django.contrib import admin
from .models import CustomUser, UserPost
from django.contrib.auth.models import Group

admin.site.register(CustomUser)
admin.site.register(UserPost)
admin.site.unregister(Group)
