from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/new/', views.create_employee, name='employee_create'), 
    path('employees/<slug:slug>/', views.employee_detail, name='employee_detail'),
    path('projects/', views.projects_list, name='projects_list'),
    path('projects/new/', views.create_project, name='project_create'),
    path('projects/<slug:slug>/', views.project_detail, name='project_detail'),
]
