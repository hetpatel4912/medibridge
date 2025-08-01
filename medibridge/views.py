from django.shortcuts import render, redirect
from registration.models import Doctors,Donors, Users, Appointment, Blogs
from itertools import chain
from datetime import date


# Create your views here.
def index(request):
    context = {}
    context['doctors'] = Doctors.objects.filter(approved=True).count()
    context['patient'] = Users.objects.filter(role=2).count()
    context['donors'] = Donors.objects.all().count()
    return render(request, 'medibridge/index.html', context)

def about_us(request):
    return render(request,'medibridge/about_us.html')

def doctors(request):
    context = {}
    context['doctors'] = Doctors.objects.filter(approved=True)
    return render(request,'medibridge/doctors.html', context)

def donors(request):
    if 'id' in request.session:
        context = {}
        user = Donors.objects.filter(email=request.session['email'])
        donors = Donors.objects.exclude(email=request.session['email'])
        context['donors'] = list(chain(user,donors))
        print(context)
        return render(request,'medibridge/donors.html', context)
    else:
        return redirect('/login')

def review(request):
    return render(request,'medibridge/review.html')

def services(request):
    return render(request,'medibridge/services.html')

def book_now(request):
    if 'id' in request.session:
        context = {}
        context['doctors'] = Doctors.objects.filter(approved=True).values()
        context['user'] = Users.objects.get(email=request.session['email'])
        if 'd_id' in request.GET:
            context['doctor_id'] = Doctors.objects.filter(id=request.GET['d_id'], approved=True).values()
            print(context['doctor_id'])
            if len(context['doctor_id']) == 1:
                context['d_id'] = request.GET['d_id']
                context['doctors'] = Doctors.objects.exclude(id=request.GET['d_id'], approved=True).values()
            else:
                context['doctors'] = Doctors.objects.filter(approved=True).values()
        else:
            context['doctors'] = Doctors.objects.filter(approved=True).values()
        return render(request,'medibridge/book_now.html', context)
    else:
        return redirect('/login')

def blogs(request):
    context = {}
    context['blogs'] = Blogs.objects.all().order_by('id').reverse()
    return render(request,'medibridge/blogs.html', context)

def logout(request):
    if 'id' in request.session:
        del request.session['id']
        del request.session['email'] 

        if 'role' in request.session:
            del request.session['role']
        elif 'approved' in request.session:
            del request.session['approved']

    return redirect('/')




def view_appointment(request):
    if 'id' in request.session:
        context = {}
        appointments = Appointment.objects.filter(email=request.session['email']).order_by('id').values().reverse()
        appointment = []
        for appoint in appointments:
            data = {}
            data['id'] = appoint['id']
            data['name'] = appoint['name']
            data['phoneno'] = appoint['phoneno']
            data['date'] = appoint['date']
            try:
                data['doctor'] = Doctors.objects.get(email=appoint['d_email']).name
                data['specialist'] = Doctors.objects.get(email=appoint['d_email']).specialist
            except:
                data['doctor'] = "Doctor is removed by Admin"
                data['specialist'] = "Doctor is removed by Admin"

            appointment.append(data)
        
        context["appointment"] = appointment
        context['today'] = date.today()
        return render(request,'medibridge/view_appointment.html', context)
    else:
        return redirect('/login')