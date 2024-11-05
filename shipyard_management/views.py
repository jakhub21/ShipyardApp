from django.shortcuts import render, get_object_or_404
from .models import Employee



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
        'projects': employee.projects.all(),
        'status': employee.status
        })

