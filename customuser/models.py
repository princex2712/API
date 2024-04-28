from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.conf import settings


class CustomUser(AbstractUser):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    otp = models.IntegerField(default=123456)

    groups = models.ManyToManyField(Group, related_name='customuser_user_groups')
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_user_permissions'
    )
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class UserPost(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    caption = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return self.caption
