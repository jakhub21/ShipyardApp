from django.db import models
from django.urls import reverse 

class Address(models.Model):
    street = models.CharField(max_length=100)
    house_number = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=6)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.street} {self.house_number}, {self.city} {self.postal_code}"
    
class ContactPerson(models.Model):
    contact_first_name = models.CharField(max_length=100)
    contact_last_name = models.CharField(max_length=100)
    contact_email = models.EmailField(max_length=100)
    contact_phone_number = models.CharField(max_length=15)
    relation_to_employee = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.contact_first_name} {self.contact_last_name}"
    
class Position(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title
    
class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=50)
    latitude = models.FloatField(null=True, blank=True) 
    longitude = models.FloatField(null=True, blank=True) 
    slug = models.SlugField(default="", blank=True, null=False, db_index=True)

    def get_absolute_url(self):
        return reverse("project_detail", args=[self.slug])

    def __str__(self):
        return self.name
    
class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    personal_number = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=15)
    bank_account_number = models.CharField(max_length=26)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    contact_person = models.ForeignKey(ContactPerson, on_delete=models.SET_NULL, null=True)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True)
    projects = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20)
    slug = models.SlugField(default="", blank=True, null=False, db_index=True)

    def get_absolute_url(self):
        return reverse("employee_detail", args=[self.slug])
    

    # def __str__(self):
    #     return f"{self.first_name} {self.last_name} | status: {self.status} | zawód: {self.position}"
    
class Certificate(models.Model):
    name = models.CharField(max_length=100)
    issued_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.employee}"

class Document(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=[('CV', 'CV'), ('Contract', 'Contract')])
    file = models.FileField(upload_to='documents/')
    upload_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} for {self.employee}"
