from django.db import models

# Create your models here.
class Company(models.Model):
    company = models.CharField(max_length=255)

class Employee(models.Model):
    name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, null=False, on_delete=models.CASCADE)
class Device(models.Model):
    name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, null=False, on_delete=models.CASCADE)