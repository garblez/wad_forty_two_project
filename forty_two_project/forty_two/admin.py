from django.contrib import admin

from .models import Subject, Solution, Comment

admin.site.register(Subject)
admin.site.register(Solution)
admin.site.register(Comment)