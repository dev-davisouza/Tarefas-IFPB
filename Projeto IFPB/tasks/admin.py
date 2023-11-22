from django.contrib import admin 
from .models import Category, Task

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'owner']

class TaskAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', ]

admin.site.register(Category, CategoryAdmin)
admin.site.register(Task, TaskAdmin)
