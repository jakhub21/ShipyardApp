from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/new/', views.create_employee, name='employee_create'), 
    path('employees/edit/<slug:slug>/', views.edit_employee, name='edit_employee'),
    path('employees/delete/<slug:slug>/', views.delete_employee, name='delete_employee'),
    path('employees/<slug:slug>/', views.employee_detail, name='employee_detail'),
    
    path('certificates/new/', views.create_certificate, name='create_certificate_no_slug'),
    path('employees/<slug:slug>/certificates/new/', views.create_certificate, name='create_certificate'),
    path('employees/<slug:slug>/certificates/edit/<int:id>/', views.edit_certificate, name='edit_certificate'),
    path('employees/<slug:slug>/certificates/delete/<int:id>/', views.delete_certificate, name='delete_certificate'),
    
    path('projects/', views.projects_list, name='projects_list'),
    path('projects/new/', views.create_project, name='project_create'),
    path('projects/edit/<slug:slug>/', views.edit_project, name='edit_project'),
    path("projects/delete/<slug:slug>/", views.delete_project, name="delete_project"),
    path('projects/<slug:slug>/', views.project_detail, name='project_detail'),


    path('rotations/', views.rotation_list, name='rotation_list'),
    path('assign-employees/', views.assign_employees_to_project, name='assign_employees_to_project'),
    # path('rotations/<slug:slug>/', views.rotation_detail, name='rotation_detail'),
    path('rotations/<slug:slug>/<int:year>/', views.rotation_detail, name='rotation_detail'),
    path('rotations/update/', views.update_rotation, name="update_rotation"),

    path('map/', views.map_view, name='map_view'),
]
