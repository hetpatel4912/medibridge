from django.shortcuts import render, redirect
from registration.models import Doctors, Users, Donors
from django.contrib import messages
from admin1.decorators import only_admin

# Create your views here.

@only_admin
def a_home(request):
    context = {}
    context['doctors'] = Doctors.objects.filter(approved=True).count()
    context['patient'] = Users.objects.filter(role=2).count()
    context['donors'] = Donors.objects.all().count()
    return render(request, "admin1/a_home.html", context)

@only_admin
def doctors_request(request):
    if request.method == "GET":
        context = {}
        context['doctors'] = Doctors.objects.filter(approved=False)
        return render(request, "admin1/a_doctors_request.html", context)
    
@only_admin
def doctors_cancel(request):
    if request.method == "GET":
        context = {}
        context['doctors'] = Doctors.objects.filter(approved=True)
        return render(request, "admin1/a_doctors_cancel.html", context)
    
@only_admin
def approve_doctor(request, id):
    if request.method == 'POST':
        doctor = Doctors.objects.get(id=id)
        doctor.approved = True
        doctor.save()
        messages.success(request,"Doctor Request Approved Successfully")
        address = request.POST['add']
        return redirect(address)

@only_admin
def cancel_doctor(request, id):
    if request.method == 'POST':
        doctor = Doctors.objects.get(id=id)
        doctor.delete()
        messages.success(request,"Doctor Request Cancel Successfully")
        address = request.POST['add']
        return redirect(address)