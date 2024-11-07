from django.shortcuts import render, get_object_or_404, redirect
from .models import Employee, Project
from .forms import ProjectForm, EmployeeForm, AddressForm, ContactPersonForm




# Create your views here.

def home(request):
    return render(request, 'shipyard_management/home.html')

def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'shipyard_management/employee_list.html', {
        'employees': employees
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

def projects_list(request):
    projects = Project.objects.all()

    return render(request, 'shipyard_management/projects_list.html', {
        'projects': projects
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
