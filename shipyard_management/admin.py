from django.contrib import admin
from .models import Address, Certificate, ContactPerson, Employee, Position, Project, Document

# Register your models here.

class EmployeeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('first_name', 'last_name', 'personal_number')}
    list_display = ('first_name', 'last_name', 'personal_number')

class ProjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Address)
admin.site.register(Certificate)
admin.site.register(ContactPerson)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Position)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Document)
