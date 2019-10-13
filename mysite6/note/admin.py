from django.contrib import admin
from . import models

# Register your models here.


class NoteManager(admin.ModelAdmin):
    list_display = ['id',
                    'title',
                    'create_time',
                    'modify_time',
                    'user']


admin.site.register(models.Note, NoteManager)