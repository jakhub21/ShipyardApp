from django import forms
from .models import Project, Employee, Address, ContactPerson, Certificate
from django.forms import modelformset_factory
from django.utils.text import slugify


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'status', 'latitude', 'longitude', 'slug']

    def clean_slug(self):
        name = self.cleaned_data.get('name', '')
        slug = slugify(name)

        original_slug = slug
        counter = 1
        while Project.objects.filter(slug=slug).exists():
            slug = f"{original_slug}-{counter}"
            counter += 1

        return slug

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'personal_number', 'phone_number', 'bank_account_number', 'position', 'projects', 'status', 'slug']

    def clean_slug(self):
        first_name = self.cleaned_data.get('first_name', '')
        last_name = self.cleaned_data.get('last_name', '')
        personal_number = self.cleaned_data.get('personal_number', '')

        slug = slugify(f"{first_name}-{last_name}-{personal_number}")

        original_slug = slug
        counter = 1
        while Employee.objects.filter(slug=slug).exists():
            slug = f"{original_slug}-{counter}"
            counter += 1

        return slug

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


