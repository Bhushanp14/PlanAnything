from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('about/', views.about_view, name='about'),
    
    path('plan/create/', views.plan_create, name='plan_create'),
    path('plan/<int:plan_id>/', views.plan_detail, name='plan_detail'),
    path('plan/<int:plan_id>/edit/', views.plan_edit, name='plan_edit'),
    path('plan/<int:plan_id>/delete/', views.plan_delete, name='plan_delete'),
    
    path('plan/<int:plan_id>/task/create/', views.task_create, name='task_create'),
    path('task/<int:task_id>/edit/', views.task_edit, name='task_edit'),
    path('task/<int:task_id>/delete/', views.task_delete, name='task_delete'),
    path('task/<int:task_id>/toggle/', views.task_toggle_status, name='task_toggle_status'),
]
