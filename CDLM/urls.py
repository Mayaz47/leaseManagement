from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('lease/', lease, name='lease'),
    path('company/', company, name='company'),
    path('employee/', employee, name='employee'),
    path('device/', device, name='device'),
    path('leaseAPI/', leaseAPI, name='leaseAPI')
]