from django.db import models
from django.utils.timezone import now
# Create your models here.
class Company(models.Model):
    company = models.CharField(max_length=255)

class Employee(models.Model):
    name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, null=False, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255,default='None')
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.company_name = self.company.company  # Update company_name field with company name
        super().save(*args, **kwargs)
class Device(models.Model):
    name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, null=False, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255,default='None')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.company_name = self.company.company   # Update company_name field with company name
        super().save(*args, **kwargs)
class Lease(models.Model):
    company = models.CharField(max_length=255)
    employee_from = models.CharField(max_length=255)
    employee_to = models.CharField(max_length=255)
    device_name = models.CharField(max_length=255)
    action = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    date = models.DateTimeField(default=now)