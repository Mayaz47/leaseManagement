from django.core.mail.backends import console
from django.http import HttpResponse
from django.shortcuts import render, redirect
from rest_framework import status
import requests
from CDLM.models import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.serializers import serialize
from django.http import JsonResponse
from .serializers import *
# Create your views here.
company_url = 'http://127.0.0.1:8000/company/'
employee_url = 'http://127.0.0.1:8000/employee/'
device_url = 'http://127.0.0.1:8000/device/'
leaseAPI_url = 'http://127.0.0.1:8000/leaseAPI/'

@api_view(['GET','POST'])
def company(request):
    if request.method == 'GET':
        company = Company.objects.all()
        serializer = CompanySerializer(company, many=True)
        return JsonResponse({'company':serializer.data})
    if request.method == 'POST':
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET','POST'])
def employee(request):
    if request.method == 'GET':
        employee = Employee.objects.all()
        serializer = EmployeeSerializer(employee, many=True)
        return JsonResponse({'employee':serializer.data})
    if request.method == 'POST':
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET','POST'])
def device(request):
    if request.method == 'GET':
        device = Device.objects.all()
        serializer = DeviceSerializer(device, many=True)
        return JsonResponse({'device':serializer.data})
    if request.method == 'POST':
        serializer = DeviceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET','POST'])
def leaseAPI(request):
    if request.method == 'GET':
        lease = Lease.objects.all()
        serializer = LeaseSerializer(lease, many=True)
        return JsonResponse({'lease':serializer.data})
    if request.method == 'POST':
        serializer = LeaseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)



def home(request):
    c = Company.objects.all()
    if request.method == 'POST':
        if 'register_company' in request.POST:
            company_name = request.POST['addCompany']
            company_exists = Company.objects.filter(company=company_name).exists()

            if not company_exists:

                payload = {'company': company_name}
                response = requests.post(company_url, data=payload)

                if response.status_code == 201:

                    return redirect('home')
                else:
                    return HttpResponse(response.status_code)

            else:
                return HttpResponse("Company already exists")



        elif 'register_employee' in request.POST:
            company_name = request.POST.get('company')
            add_employee = request.POST.get('addEmployee')
            company = Company.objects.get(company=company_name)
            payload = {'name': add_employee, 'company': company.id}
            response = requests.post(employee_url, data=payload)
            if response.status_code == 201:
                return HttpResponse("Employeed added to" + company_name)
            else :
                return HttpResponse(response.status_code)
        elif 'register_Device' in request.POST:
            company_name = request.POST.get('company')
            add_device = request.POST.get('addDevice')
            company = Company.objects.get(company=company_name)
            payload = {'name': add_device, 'company': company.id}
            response = requests.post(device_url, data=payload)
            if response.status_code == 201:
                return HttpResponse("Device added to" + company_name)
            else:
                return HttpResponse(response.status_code)

    else:

        response = requests.get(company_url)

        if response.status_code == 200:  # Assuming the API returns a successful response
            companies = response.json()
        else:
            return HttpResponse(response.status_code)
        return render(request, 'home.html', {'companies': companies})


def lease(request):
    response = requests.get(company_url)
    companies = response.json()

    response2 = requests.get(employee_url)
    employees_data = response2.json()
    print(type(employees_data))
    employees = employees_data if isinstance(employees_data, list) else [employees_data]

    response3 = requests.get(device_url)
    devices_data = response3.json()
    devices = devices_data if isinstance(devices_data, list) else [devices_data]

    response4 = requests.get(leaseAPI_url)
    lease = response4.json()
    lease_data = lease if isinstance(lease, list) else [lease]
    context = {
        'companies': companies,
        'employees': employees,
        'devices': devices,
        'lease': lease_data,
    }
    if request.method == 'POST':
        if 'add_lease' in request.POST:
            # Get data from the form submission
            company = request.POST['company']
            employee_from = request.POST['empFrom']
            employee_to = request.POST['empTo']
            device_name= request.POST['device']
            action  = request.POST['action']
            status = request.POST['status']
            payload = {'company': company, 'employee_from': employee_from, 'employee_to': employee_to, 'device_name': device_name, 'action': action, 'status': status}
            response = requests.post(leaseAPI_url, data=payload)
            if response.status_code == 201:
                return redirect('lease')
            else:
                return HttpResponse(response.status_code)
        elif 'clear' in request.POST:
            latest_entry = Lease.objects.latest('id')
            # Delete the latest entry
            latest_entry.delete()
            # Redirect to the same page after deletion
            return redirect('lease')

    else:

        return render(request, 'lease.html', context)
