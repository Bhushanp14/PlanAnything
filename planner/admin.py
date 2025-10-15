from django.contrib import admin
from .models import Plan, Task, ChatConversation, ChatMessage, ProposedPlan

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

@admin.register(ChatConversation)
class ChatConversationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at', 'updated_at']
    list_filter = ['user', 'created_at']

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'conversation', 'role', 'created_at']
    list_filter = ['role', 'created_at']
    search_fields = ['content']

@admin.register(ProposedPlan)
class ProposedPlanAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'is_accepted', 'created_at']
    list_filter = ['is_accepted', 'created_at']
    search_fields = ['title', 'description']
