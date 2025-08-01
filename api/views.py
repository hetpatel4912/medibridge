from django.shortcuts import render, redirect
from registration.models import Donors, Users, Doctors, Appointment
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q

# Create your views here.

def donor(request, id):
    if 'id' in request.session:
        user = Users.objects.get(id=id)
        try:
            donor = Donors.objects.get(email=user.email)
            messages.success(request,"User Already Exist in Donor list. Try another email to add new User")
            return redirect( "/donors")
        except:
            return render(request,"medibridge/donor_add.html")
    return redirect("/login")

def add_donor(request):
    if request.method == "POST":
        email = request.session['email']
        name = request.POST['name']
        contact_no = request.POST['contact_no']
        residence = request.POST['residence']
        blood_group = request.POST['blood_group']

        if not contact_no.isdigit() or len(contact_no) != 10:
            messages.success(request,"Contact number should contain 10 digit only")
            url = "/api/donor/" + str(request.session['id'])
            return redirect(url)

        try:
            donor = Donors(email=email, name=name, contact_no=contact_no, blood_group=blood_group, residence=residence)
            donor.save()
            messages.success(request,"Donor Successfully Added")
        except Exception as e:
            print(e)
        return redirect("/donors")
    
    return render(request,"medibridge/donors.html")


def donor_remove(request, id):
    if request.method == "POST":
        Donors.objects.filter(email=id).delete()
        messages.success(request,"Donor Successfully Removed")
        return redirect("/donors")
    return redirect("/donors")

def doctor(request, id):
    doctor = Doctors.objects.get(id=id)
    appointment = Appointment.objects.filter(d_email=doctor.email)
    dates=[]
    for appoint in appointment:
        dates.append(appoint.date.strftime("%Y-%m-%d"))
    context = {}
    context['doctor_name'] = doctor.name
    context['doctor_specialist'] = doctor.specialist
    context['dates'] = dates
    print("WEQE : ", type(context["dates"]))
    print("WEQE : ", context)
    return JsonResponse(context)


def appointment(request):
    if request.method == "POST":
        d_id = request.POST['d_id']
        d_name = request.POST['d_name']
        d_specialist = request.POST['d_specialist']
        name = request.POST['name']
        phoneno = request.POST['phoneno']
        email = request.POST['email']
        date = request.POST['date']

        if not phoneno.isdigit() or len(phoneno) != 10:
            messages.success(request,"Contact number should contain 10 digit only")
            return redirect("/book_now")

        try:
            doctor = Doctors.objects.get(id=d_id)
            appointment = Appointment(email=email, name=name, phoneno=phoneno, d_email=doctor.email, date=date)
            appointment.save()
            messages.success(request,"Appointment Booked Successfully")
        except Exception as e:
            print(e)
        return redirect("/book_now")
    
    return render(request,"medibridge/book_now.html")



def cancel_appointment(request, id):
    if request.method == "POST":

        try:
            appointment = Appointment(id=id)
            appointment.delete()
            messages.success(request,"Appointment Cancelled Successfully")
        except Exception as e:
            print(e)
        return redirect("/view_appointment")
    
    return render(request,"medibridge/index.html")