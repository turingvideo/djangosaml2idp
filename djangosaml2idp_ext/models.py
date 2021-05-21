from django.conf import settings
from django.contrib.auth.models import Group
from django.db import models
from djangosaml2idp.models import ServiceProvider


class UserSAMLRole(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)


class GroupSAMLRole(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
