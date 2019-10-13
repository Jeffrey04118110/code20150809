from django.contrib import admin
from . import models

# Register your models here.


class UserManager(admin.ModelAdmin):
    list_display = ['id', 'username', 'password']


admin.site.register(models.User, UserManager)