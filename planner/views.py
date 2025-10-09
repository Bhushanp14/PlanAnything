from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from datetime import datetime, timedelta
import calendar
import json

from .models import Plan, Task
from .forms import PlanForm, TaskForm

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    
    return render(request, 'planner/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = AuthenticationForm()
    
    return render(request, 'planner/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def about_view(request):
    return render(request, 'planner/about.html')

@login_required
def dashboard_view(request):
    plans = Plan.objects.filter(user=request.user)
    context = {
        'plans': plans,
        'has_plans': plans.exists()
    }
    return render(request, 'planner/dashboard.html', context)

@login_required
def plan_create(request):
    if request.method == 'POST':
        form = PlanForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.user = request.user
            plan.save()
            messages.success(request, 'Plan created successfully!')
            return redirect('plan_detail', plan_id=plan.id)
    else:
        form = PlanForm()
    
    return render(request, 'planner/plan_form.html', {'form': form, 'is_edit': False})

@login_required
def plan_detail(request, plan_id):
    plan = get_object_or_404(Plan, id=plan_id, user=request.user)
    
    year = request.GET.get('year', timezone.now().year)
    month = request.GET.get('month', timezone.now().month)
    
    year = int(year)
    month = int(month)
    
    cal = calendar.monthcalendar(year, month)
    month_name = calendar.month_name[month]
    
    tasks_by_date = {}
    for task in plan.tasks.all():
        date_key = task.task_date.strftime('%Y-%m-%d')
        if date_key not in tasks_by_date:
            tasks_by_date[date_key] = []
        tasks_by_date[date_key].append(task)
    
    context = {
        'plan': plan,
        'calendar': cal,
        'year': year,
        'month': month,
        'month_name': month_name,
        'tasks_by_date': tasks_by_date,
        'today': timezone.now().date(),
    }
    
    return render(request, 'planner/plan_detail.html', context)

@login_required
def plan_edit(request, plan_id):
    plan = get_object_or_404(Plan, id=plan_id, user=request.user)
    
    if request.method == 'POST':
        form = PlanForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            messages.success(request, 'Plan updated successfully!')
            return redirect('plan_detail', plan_id=plan.id)
    else:
        form = PlanForm(instance=plan)
    
    return render(request, 'planner/plan_form.html', {'form': form, 'is_edit': True, 'plan': plan})

@login_required
def plan_delete(request, plan_id):
    plan = get_object_or_404(Plan, id=plan_id, user=request.user)
    
    if request.method == 'POST':
        plan.delete()
        messages.success(request, 'Plan deleted successfully!')
        return redirect('dashboard')
    
    return render(request, 'planner/plan_confirm_delete.html', {'plan': plan})

@login_required
def task_create(request, plan_id):
    plan = get_object_or_404(Plan, id=plan_id, user=request.user)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save(commit=False)
            task.plan = plan
            task.save()
            messages.success(request, 'Task created successfully!')
            return redirect('plan_detail', plan_id=plan.id)
    else:
        task_date = request.GET.get('date', timezone.now().date())
        form = TaskForm(initial={'task_date': task_date})
    
    return render(request, 'planner/task_form.html', {'form': form, 'plan': plan, 'is_edit': False})

@login_required
def task_edit(request, task_id):
    task = get_object_or_404(Task, id=task_id, plan__user=request.user)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('plan_detail', plan_id=task.plan.id)
    else:
        form = TaskForm(instance=task)
    
    return render(request, 'planner/task_form.html', {'form': form, 'plan': task.plan, 'task': task, 'is_edit': True})

@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id, plan__user=request.user)
    plan_id = task.plan.id
    
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully!')
        return redirect('plan_detail', plan_id=plan_id)
    
    return render(request, 'planner/task_confirm_delete.html', {'task': task})

@login_required
@require_http_methods(["POST"])
def task_toggle_status(request, task_id):
    task = get_object_or_404(Task, id=task_id, plan__user=request.user)
    
    if task.status == 'pending':
        task.status = 'completed'
    else:
        task.status = 'pending'
    
    task.save()
    
    return JsonResponse({
        'status': task.status,
        'is_overdue': task.is_overdue()
    })
