from django.http import HttpResponse
from django.shortcuts import render
from CDLM.models import *
# Create your views here.

c = Company.objects.all()
def home(request):
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