from django.contrib import admin
from .models import Plan, Task

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'start_date', 'end_date', 'created_at']
    list_filter = ['user', 'start_date']
    search_fields = ['title', 'description']

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'plan', 'task_date', 'status', 'created_at']
    list_filter = ['status', 'task_date', 'plan']
    search_fields = ['title', 'description']
