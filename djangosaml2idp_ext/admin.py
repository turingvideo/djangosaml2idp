from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin

from . import models


@admin.register(models.UserSAMLRole)
class UserSAMLRoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'provider', 'name')
    readonly_fields = ('created_at',)
    search_fields = ['name'] + ['user__%s' % f for f in UserAdmin.search_fields]


@admin.register(models.GroupSAMLRole)
class GroupSAMLRoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'group', 'provider', 'name')
    readonly_fields = ('created_at',)
    search_fields = ['name'] + ['group__%s' % f for f in GroupAdmin.search_fields]
