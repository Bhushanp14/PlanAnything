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
from django.urls import reverse
from django.http import HttpResponse

from .models import Plan, Task, ChatConversation, ChatMessage, ProposedPlan
from .forms import PlanForm, TaskForm
from .chatbot import chat_with_assistant, parse_plan_proposal

def register_view(request):
    if request.user.is_authenticated:
        return redirect('landing_page')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('landing_page')
    else:
        form = UserCreationForm()
    
    return render(request, 'planner/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('landing_page')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('landing_page')
    else:
        form = AuthenticationForm()
    
    return render(request, 'planner/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def about_view(request):
    return render(request, 'planner/about.html')

def landing_page(request):
    """Public landing page — dynamically changes based on user state."""
    if request.user.is_authenticated:
        plans = Plan.objects.filter(user=request.user)
        
        # If user has existing plans → Go directly to dashboard
        if plans.exists():
            return redirect('dashboard')
        
        # If user has no plans → Show landing page without login/signup buttons
        context = {
            'user_has_no_plans': True,
            'plans': [],
        }
        return render(request, 'planner/landing_page.html', context)
    
    # If not logged in → Show public landing with login/signup buttons
    return render(request, 'planner/landing_page.html', {'user_has_no_plans': False})


@login_required
def dashboard_view(request):
    """Main dashboard for logged-in users with plans."""
    plans = Plan.objects.filter(user=request.user)
    completed_plans= []
    incomplete_plans= []
    if plans:
        for plan in plans:
            if plan.tasks.count()>0:
                if plan.get_plan_status() == True:
                    completed_plans.append(plan)
                else:
                    incomplete_plans.append(plan)
            else:
                incomplete_plans.append(plan)
    # If no plans yet → redirect to landing page (which will show no-plan view)
    if not plans.exists():
        return redirect('landing_page')
    
    context = {
        'plans': plans,
        'completed_plans' : completed_plans,
        'incomplete_plans' : incomplete_plans,
        'has_plans': True
    }
    return render(request, 'planner/dashboard.html', context)

@login_required
def plan_create(request):
    if request.method == "POST":
        form = PlanForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.user = request.user
            plan.save()

            if request.headers.get('HX-Request'):
                return HttpResponse('<script>closeModalAndReload();</script>')
            return redirect('dashboard')
    else:
        form = PlanForm()

    # If HTMX request, render partial only
    template = 'planner/partials/plan_form_partial.html' if request.headers.get('HX-Request') else 'planner/plan_form.html'
    return render(request, template, {'form': form})
@login_required
def plan_detail(request, plan_id):
    plan = get_object_or_404(Plan, id=plan_id, user=request.user)
    first_task = plan.tasks.first()
    if first_task:
        try:
            if  first_task.task_date != request.GET.get('date', timezone.now().date):
                year = first_task.task_date.year
                month = first_task.task_date.month
                
            
        except Exception as e:
            print(f"I'm sorry, I encountered an error: {str(e)}")
        
    else:
        year = request.GET.get('year', timezone.now().year)
        month = request.GET.get('month', timezone.now().month)
    year = int(year)
    month = int(month)
    
    cal = calendar.monthcalendar(year, month)
    month_name = calendar.month_name[month]
    
    tasks_by_date = {}
    for task in plan.tasks.all():
        # ensure consistent string key (YYYY-MM-DD)
        date_key = task.task_date.strftime('%Y-%m-%d')
        tasks_by_date.setdefault(date_key, []).append(task)
        
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

@login_required
def chatbot_view(request):
    conversation = ChatConversation.objects.filter(user=request.user).order_by('-updated_at').first()
    if not conversation:
        conversation = ChatConversation.objects.create(user=request.user)
    
    messages = conversation.messages.all()
    proposed_plans = ProposedPlan.objects.filter(conversation=conversation, is_accepted=False)
    
    return render(request, 'planner/chatbot.html', {
        'conversation': conversation,
        'messages': messages,
        'proposed_plans': proposed_plans
    })

@login_required
@require_http_methods(["POST"])
def chatbot_send_message(request):
    data = json.loads(request.body)
    user_message = data.get('message', '').strip()
    conversation_id = data.get('conversation_id')
    
    if not user_message:
        return JsonResponse({'error': 'Message cannot be empty'}, status=400)
    
    conversation = get_object_or_404(ChatConversation, id=conversation_id, user=request.user)
    
    ChatMessage.objects.create(
        conversation=conversation,
        role='user',
        content=user_message
    )
    
    message_history = [
        {'role': msg.role, 'content': msg.content}
        for msg in conversation.messages.all()
    ]
    
    assistant_response = chat_with_assistant(message_history)
    
    ChatMessage.objects.create(
        conversation=conversation,
        role='assistant',
        content=assistant_response
    )
    
    plan_data = parse_plan_proposal(assistant_response)
    proposed_plan_id = None
    
    if plan_data:
        proposed_plan = ProposedPlan.objects.create(
            conversation=conversation,
            user=request.user,
            title=plan_data.get('title', 'Untitled Plan'),
            description=plan_data.get('description', ''),
            color=plan_data.get('color', '#3B82F6'),
            start_date=plan_data.get('start_date'),
            end_date=plan_data.get('end_date'),
            tasks_data=plan_data.get('tasks', [])
        )
        proposed_plan_id = proposed_plan.id
    
    conversation.save()
    
    return JsonResponse({
        'user_message': user_message,
        'assistant_message': assistant_response,
        'proposed_plan_id': proposed_plan_id
    })

@login_required
@require_http_methods(["POST"])
def chatbot_accept_plan(request, plan_id):
    proposed_plan = get_object_or_404(ProposedPlan, id=plan_id, user=request.user, is_accepted=False)
    
    plan = Plan.objects.create(
        user=request.user,
        title=proposed_plan.title,
        description=proposed_plan.description,
        color=proposed_plan.color,
        start_date=proposed_plan.start_date,
        end_date=proposed_plan.end_date
    )
    
    for task_data in proposed_plan.tasks_data:
        Task.objects.create(
            plan=plan,
            title=task_data.get('title', 'Untitled Task'),
            description=task_data.get('description', ''),
            task_date=task_data.get('task_date'),
            status=task_data.get('status', 'pending')
        )
    
    proposed_plan.is_accepted = True
    proposed_plan.save()
    
    return JsonResponse({
        'success': True,
        'plan_id': plan.id,
        'redirect_url': reverse('plan_detail', args=[plan.id])
    })

@login_required
@require_http_methods(["POST"])
def chatbot_new_conversation(request):
    conversation = ChatConversation.objects.create(user=request.user)
    return JsonResponse({
        'conversation_id': conversation.id,
        'redirect_url': reverse('chatbot')
    })
