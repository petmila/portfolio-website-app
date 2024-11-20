from django.contrib import admin
from djsingleton.admin import SingletonAdmin
from . import models

# TODO: переписать

# class PostAdmin(admin.ModelAdmin):
#     list_display = ['pk', 'gender', 'word']
#     list_editable = ['gender', 'word']


# admin.site.register(models.Post, PostAdmin)
admin.site.register(models.Portfolio, SingletonAdmin)
admin.site.register(models.Post)
admin.site.register(models.Service)
admin.site.register(models.Tag)
admin.site.register(models.Client)
