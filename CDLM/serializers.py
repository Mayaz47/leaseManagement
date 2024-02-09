from rest_framework import serializers
from .models import *

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['company']

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['name','company','company_name']

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['name','company','company_name']

class LeaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lease
        fields = ['company','employee_from','employee_to','device_name','action','status','date']
