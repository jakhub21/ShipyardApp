from django.shortcuts import render, get_object_or_404, redirect
from .models import Employee, Project
from .forms import ProjectForm, EmployeeForm, AddressForm, ContactPersonForm
from django.db.models import Q
from django.http import HttpResponseNotAllowed
from django.contrib import messages
from django.core.serializers import serialize
from django.core.paginator import Paginator


def home(request):
    employees = Employee.objects.all()[:5]
    displayed_projects = Project.objects.all()[:5]
    all_projects = Project.objects.all()
    serialized_projects = serialize('json', all_projects)

    return render(request, 'shipyard_management/home.html', {
        'employees': employees,
        'projects': displayed_projects,
        'serialized_projects': serialized_projects
    })

def employee_list(request):
    query = request.GET.get('q')
    
    if query:
        employees = Employee.objects.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query)
        )
    else:
        employees = Employee.objects.all()

    paginator = Paginator(employees, 7)
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)  

    return render(request, 'shipyard_management/employee_list.html', {
        'employees': page_obj,  
        'query': query,         
        'page_obj': page_obj,   
    })

def employee_detail(request, slug):
    employee = get_object_or_404(Employee, slug=slug)

    return render(request, 'shipyard_management/employee_detail.html', {
        'firstname': employee.first_name,
        'lastname': employee.last_name,
        'personal_number': employee.personal_number,
        'phone_number': employee.phone_number,
        'bank_account_number': employee.bank_account_number,
        'address': employee.address,
        'contact_person': employee.contact_person,
        'position': employee.position,
        'projects': employee.projects,
        'status': employee.status
        })

def create_employee(request):
    if request.method == 'POST':
        employee_form = EmployeeForm(request.POST)
        address_form = AddressForm(request.POST)
        contact_person_form = ContactPersonForm(request.POST)

        if employee_form.is_valid() and address_form.is_valid() and contact_person_form.is_valid():
            address = address_form.save()
            contact_person = contact_person_form.save()
            employee = employee_form.save(commit=False)
            employee.address = address
            employee.contact_person = contact_person
            employee.save()

            return redirect('employee_list')  
    else:
        employee_form = EmployeeForm()
        address_form = AddressForm()
        contact_person_form = ContactPersonForm()

    return render(request, 'shipyard_management/employee_form.html', {
        'employee_form': employee_form,
        'address_form': address_form,
        'contact_person_form': contact_person_form
    })

def edit_employee(request, slug):
    employee = get_object_or_404(Employee, slug=slug)
    address = employee.address
    contact = employee.contact_person

    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        address_form = AddressForm(request.POST, instance=address)
        contact_form = ContactPersonForm(request.POST, instance=contact)

        if form.is_valid() and address_form.is_valid() and contact_form.is_valid():
            form.save()
            address_form.save()
            contact_form.save()
            return redirect('employee_list') 
    else:
        form = EmployeeForm(instance=employee)
        address_form = AddressForm(instance=address)
        contact_form = ContactPersonForm(instance=contact)

    return render(request, 'shipyard_management/edit_employee.html', {
        'form': form,
        'address_form': address_form,
        'contact_form': contact_form,
    })

def delete_employee(request, slug):
    if request.method == 'POST':
        employee = get_object_or_404(Employee, slug=slug)
        employee.delete()
        return redirect('employee_list')
    return HttpResponseNotAllowed(['POST'])

def projects_list(request):
    query = request.GET.get('q')  
    if query:
        projects = Project.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    else:
        projects = Project.objects.all()

    paginator = Paginator(projects, 7)
    page_number = request.GET.get('page') 
    page_obj = paginator.get_page(page_number)  

    return render(request, 'shipyard_management/projects_list.html', {
        'projects': page_obj,  
        'query': query,    
        'page_obj': page_obj,    
    })

def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    employees = project.employee_set.all()
    return render(request, 'shipyard_management/project_detail.html', {
        'name': project.name,
        'description': project.description,
        'start_date': project.start_date,
        'end_date': project.end_date,
        'status': project.status,
        'employees': employees
        })

def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('projects_list')  
    else:
        form = ProjectForm()

    return render(request, 'shipyard_management/project_form.html', {'form': form})

def edit_project(request, slug):
    project = get_object_or_404(Project, slug=slug)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects_list')  
    else:
        form = ProjectForm(instance=project)
    
    return render(request, 'shipyard_management/edit_project.html', {
        'form': form,
        'project': project
        })

def delete_project(request, slug):
    project = get_object_or_404(Project, slug=slug)
    project.delete()
    messages.success(request, f"Projekt '{project.name}' został usunięty.")
    return redirect("projects_list")

def map_view(request):
    projects = Project.objects.filter(latitude__isnull=False, longitude__isnull=False)
    projects_json = serialize('json', projects)
    return render(request, 'shipyard_management/map.html', {'projects': projects_json})