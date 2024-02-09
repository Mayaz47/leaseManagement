from django.http import HttpResponse
from django.shortcuts import render, redirect
from CDLM.models import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.serializers import serialize
from django.http import JsonResponse

# Create your views here.



def home(request):
    c = Company.objects.all()
    if request.method == 'POST':
        if 'register_company' in request.POST:
            doop = True
            company = request.POST['addCompany']


            for i in c :
                if company == i.company:
                    doop = False
            if doop == True:
                new_data = Company(
                    company=company
                )
                new_data.save()
                o = Company.objects.all()
                return render(request, 'home.html', {'companies': o})

            else:
                return HttpResponse("Company already registered")
        elif 'register_employee' in request.POST:
            company_name = request.POST.get('company')
            add_employee = request.POST.get('addEmployee')
            company = Company.objects.get(company=company_name)
            employee = Employee(name=add_employee, company=company)
            employee.save()
            return HttpResponse("Employeed added to" + company_name)
        elif 'register_Device' in request.POST:
            company_name = request.POST.get('company')
            add_device = request.POST.get('addDevice')
            company = Company.objects.get(company=company_name)
            device = Device(name=add_device, company=company)
            device.save()
            return HttpResponse("Device added to"+ company_name)

    else:

        return render(request, 'home.html', {'companies': c})

def lease(request):
    c = Company.objects.all()
    e = Employee.objects.all()
    d = Device.objects.all()
    l = Lease.objects.all()
    employees_json = serialize('json', e)
    device_json = serialize('json', d)
    lease_json = serialize('json', l)
    context = {
        'companies': c,
        'employees': employees_json,
        'devices': device_json,
        'lease': lease_json,
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



            new_data = Lease(
                company=company,
                employee_from=employee_from,
                employee_to=employee_to,
                device_name=device_name,
                action=action,
                status=status,


            )

            # Save the new data to the database
            new_data.save()

            # Redirect to the display_data view after adding data
            return redirect('lease')
        elif 'clear' in request.POST:
            latest_entry = Lease.objects.latest('id')
            # Delete the latest entry
            latest_entry.delete()
            # Redirect to the same page after deletion
            return redirect('lease')

    else:

        return render(request, 'lease.html', context)
