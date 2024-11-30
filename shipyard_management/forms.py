from django import forms
from .models import Project, Employee, Address, ContactPerson, Certificate

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'end_date', 'status', 'latitude', 'longitude', 'slug']

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'personal_number', 'phone_number', 'bank_account_number', 'position', 'projects', 'status', 'slug']

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['street', 'house_number', 'city', 'postal_code', 'country']

class ContactPersonForm(forms.ModelForm):
    class Meta:
        model = ContactPerson
        fields = ['contact_first_name', 'contact_last_name', 'contact_email', 'contact_phone_number', 'relation_to_employee']

class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ['name', 'issued_date', 'expiry_date']
