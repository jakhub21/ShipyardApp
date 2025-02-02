from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from .models import Employee, Project, Certificate, Rotation
from .forms import ProjectForm, EmployeeForm, AddressForm, ContactPersonForm, CertificateForm
from django.db.models import Q
from django.http import HttpResponseNotAllowed, JsonResponse
from django.contrib import messages
from django.core.serializers import serialize
from django.core.paginator import Paginator
from datetime import datetime, timedelta
import json
from collections import defaultdict
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.utils.timezone import now
from django.db import models

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
    address = employee.address
    contact_person = employee.contact_person
    certificates = employee.certificates.all()

    return render(request, 'shipyard_management/employee_detail.html', {
        'employee': employee,
        'address': address,
        'contact_person': contact_person,
        'certificates': certificates,
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

            certificates = request.session.pop('new_employee_certificates', [])
            for cert_data in certificates:
                Certificate.objects.create(
                    employee=employee,
                    name=cert_data['name'],
                    issued_date=cert_data['issued_date'],
                    expiry_date=cert_data['expiry_date'],
                )

            return redirect('employee_list')  
    else:
        employee_form = EmployeeForm()
        address_form = AddressForm()
        contact_person_form = ContactPersonForm()

    certificates = request.session.get('new_employee_certificates', [])

    return render(request, 'shipyard_management/employee_form.html', {
        'employee_form': employee_form,
        'address_form': address_form,
        'contact_person_form': contact_person_form,
        'certificates': certificates,
    })

def edit_employee(request, slug):
    employee = get_object_or_404(Employee, slug=slug)
    certificates = employee.certificates.all()

    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        address_form = AddressForm(request.POST, instance=employee.address)
        contact_form = ContactPersonForm(request.POST, instance=employee.contact_person)

        if form.is_valid() and address_form.is_valid() and contact_form.is_valid():
            form.save()
            address_form.save()
            contact_form.save()
            return redirect('employee_detail', slug=employee.slug)
    else:
        form = EmployeeForm(instance=employee)
        address_form = AddressForm(instance=employee.address)
        contact_form = ContactPersonForm(instance=employee.contact_person)

    return render(request, 'shipyard_management/edit_employee.html', {
        'form': form,
        'address_form': address_form,
        'contact_form': contact_form,
        'employee': employee,
        'certificates': certificates,
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
    employees = Employee.objects.filter(projects=project)

    # Pobieramy pracowników, którzy NIE są w tym projekcie
    all_employees = Employee.objects.exclude(projects=project).prefetch_related("position", "projects")

    # Dodajemy bieżący projekt każdego pracownika
    for employee in all_employees:
        employee.current_project = employee.projects if employee.projects else "-"

    return render(request, 'shipyard_management/project_detail.html', {
        'project': project,
        'name': project.name,
        'description': project.description,
        'start_date': project.start_date,
        'status': project.status,
        'employees': employees,
        'all_employees': all_employees,
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

def rotation_list(request):
    projects = Project.objects.all()

    # Tworzymy paginację dla listy projektów
    paginator = Paginator(projects, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    employees = Employee.objects.all()


    profession_counts = defaultdict(int)
    for employee in employees:
        if employee.position: 
            profession_counts[employee.position.title] += 1

    # Pobieramy wszystkie rotacje
    all_rotations = Rotation.objects.all().select_related("employee__position")

    # Inicjalizujemy strukturę danych dla tabeli
    profession_week_counts = defaultdict(lambda: defaultdict(int))

    # Wypełniamy dane - liczymy ludzi z danej profesji w każdym tygodniu
    for rotation in all_rotations:
        profession = rotation.employee.position.title
        profession_week_counts[profession][rotation.week] += 1

    weeks = list(range(1, 53))  # Zakres tygodni 1-52

    return render(request, 'shipyard_management/rotation_list.html', {
        'projects': page_obj,  
        'weeks': weeks,
        'profession_week_counts': dict(profession_week_counts),
        'profession_counts': dict(profession_counts),
    })

def rotation_detail(request, slug, year):
    project = get_object_or_404(Project, slug=slug)
    employees = Employee.objects.filter(projects=project).order_by("position__title", "last_name")

    # Pobranie wszystkich pracowników spoza projektu
    all_employees = Employee.objects.exclude(projects=project).prefetch_related("projects", "position")

    for employee in all_employees:
        # 🔹 Sprawdzamy, czy `projects` jest ManyToManyField
        if hasattr(employee, "projects") and isinstance(employee._meta.get_field("projects"), models.ManyToManyField):
            projects_qs = employee.projects.all()  # ✅ Jeśli ManyToManyField, używamy `.all()`
            employee.current_project = projects_qs.first() if projects_qs.exists() else "-"
        else:
            employee.current_project = employee.projects if employee.projects else "-"

    employees_by_profession = defaultdict(list)
    for employee in employees:
        employees_by_profession[employee.position.title].append(employee)

    weeks = list(range(1, 53))

    rotation_dict = defaultdict(dict)
    for rotation in Rotation.objects.filter(project=project, year=year):
        rotation_dict[rotation.employee.id][rotation.week] = rotation.active

    return render(request, "shipyard_management/rotation_detail.html", {
        "project": project,
        "year": year,
        "employees_by_profession": dict(employees_by_profession),
        "weeks": weeks,
        "rotation_dict": rotation_dict,
        "all_employees": all_employees,
    })

@csrf_exempt
def add_employees_to_project(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            employee_ids = data.get("employee_ids", [])
            project_slug = data.get("project_slug")

            project = get_object_or_404(Project, slug=project_slug)

            employees = Employee.objects.filter(id__in=employee_ids)
            for employee in employees:
                employee.projects.add(project)

            return JsonResponse({"success": True, "message": "Employees added successfully!"})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid request"})

@csrf_exempt
def assign_employees_to_project(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            employee_ids = data.get("employee_ids", [])
            project_slug = data.get("project_slug")

            print(f"🔹 Otrzymany `project_slug`: {project_slug}")  # 🛠 Debugowanie
            print(f"🔹 Otrzymane `employee_ids`: {employee_ids}")  # 🛠 Debugowanie

            # Pobieramy projekt na podstawie sluga
            project = get_object_or_404(Project, slug=project_slug)

            # Pobieramy pracowników i przypisujemy im nowy projekt
            employees = Employee.objects.filter(id__in=employee_ids)
            for employee in employees:
                employee.projects = project  # Zmiana przypisanego projektu
                employee.save()  # Zapisujemy zmianę w bazie

            return JsonResponse({"success": True, "message": "Employees assigned successfully."})

        except Exception as e:
            print(f"⚠️ Błąd: {e}")  # 🛠 Debugowanie błędu
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid request"})

@csrf_exempt
def update_rotation(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            employee_id = data.get("employee_id")
            week = int(data.get("week"))
            project_slug = data.get("project_slug")
            year = int(data.get("year"))
            active = data.get("active")  # Nowa poprawka!

            # Pobieramy obiekty Employee i Project
            employee = Employee.objects.get(id=employee_id)
            project = Project.objects.get(slug=project_slug)

            # Jeśli `active` == True -> dodaj do bazy
            if active:
                rotation, created = Rotation.objects.get_or_create(
                    employee=employee,
                    project=project,
                    week=week,
                    year=year
                )
                return JsonResponse({"success": True, "added": True, "week": week})
            else:
                # Jeśli `active` == False -> usuń z bazy
                deleted_count, _ = Rotation.objects.filter(
                    employee=employee,
                    project=project,
                    week=week,
                    year=year
                ).delete()
                return JsonResponse({"success": True, "removed": deleted_count > 0, "week": week})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid request"})

def map_view(request):
    projects = Project.objects.filter(latitude__isnull=False, longitude__isnull=False)
    projects_json = serialize('json', projects)
    return render(request, 'shipyard_management/map.html', {'projects': projects_json})

def create_certificate(request, slug=None):
    previous_url = request.GET.get('next', None)
    
    if request.method == "POST":
        form = CertificateForm(request.POST)
        if form.is_valid():
            if slug:
                employee = get_object_or_404(Employee, slug=slug)
                certificate = form.save(commit=False)
                certificate.employee = employee
                certificate.save()
            else:
                certificates = request.session.get('new_employee_certificates', [])
                certificates.append({
                    'name': form.cleaned_data['name'],
                    'issued_date': form.cleaned_data['issued_date'].isoformat(),  # Konwersja na string
                    'expiry_date': form.cleaned_data['expiry_date'].isoformat() if form.cleaned_data['expiry_date'] else None,  # Konwersja na string lub None
                })
                request.session['new_employee_certificates'] = certificates

            return redirect(previous_url if previous_url else 'employee_list')  
    else:
        form = CertificateForm()

    return render(request, 'shipyard_management/certificate_form.html', {
        'form': form,
    })

def edit_certificate(request, slug, id):
    certificate = get_object_or_404(Certificate, id=id, employee__slug=slug)
    if request.method == "POST":
        form = CertificateForm(request.POST, instance=certificate)
        if form.is_valid():
            form.save()
            next_url = request.GET.get('next', 'edit_employee')
            return redirect(next_url, slug=slug)
    else:
        form = CertificateForm(instance=certificate)

    return render(request, 'shipyard_management/certificate_form.html', {
        'form': form,
        'employee': certificate.employee,
    })

def delete_certificate(request, slug, id):
    certificate = get_object_or_404(Certificate, id=id, employee__slug=slug)
    if request.method == "POST":
        certificate.delete()
        next_url = request.GET.get('next', 'edit_employee')
        return redirect(next_url, slug=slug)
    
    return render(request, 'shipyard_management/confirm_delete.html', {
        'object': certificate,
        'employee': certificate.employee, 
    })
