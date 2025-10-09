from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Plan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='plans')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#3B82F6')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_task_stats(self):
        total_tasks = self.tasks.count()
        completed_tasks = self.tasks.filter(status='completed').count()
        return {
            'total': total_tasks,
            'completed': completed_tasks
        }

class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]

    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to='task_photos/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    task_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['task_date', '-created_at']

    def __str__(self):
        return f"{self.title} - {self.task_date}"

    def is_overdue(self):
        if self.status == 'completed':
            return False
        return self.task_date < timezone.now().date()
