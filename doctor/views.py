from django.http import JsonResponse
from django.shortcuts import render, redirect
from registration.models import Doctors, Appointment, Blogs
from django.db.models import Q
from django.utils.timezone import now
from django.contrib import messages
from datetime import datetime

# Create your views here.
def d_home(request):
    if "id" in request.session:
        if request.method == 'GET':
            context = {}
            context['doc'] = Doctors.objects.filter(id = request.session['id']).first()
            context['completed'] = Appointment.objects.filter(Q(d_email=request.session['email']) & Q(date__lt=now())).count()
            context['pending'] = Appointment.objects.filter(Q(d_email=request.session['email']) & Q(date__gt=now())).count()
            return render(request, 'doctor/d_home.html', context)
    else:
        return redirect('/login')

    

def d_schedule(request):
    if "id" in request.session:
        if request.method == 'GET':
            context = {}
            context['doc'] = Doctors.objects.filter(id = request.session['id']).first()
            return render(request, "doctor/d_schedule.html", context)
    else:
        return redirect('/login')
    
def get_bookings(request):
    booked_dates = Appointment.objects.filter(d_email=request.session['email']).values().order_by('date')
    dates = []
    details = []
    for date in booked_dates:
        dates.append(date['date'])
    for detail in booked_dates:
        details.append({"name":detail['name'], "phoneno":detail['phoneno']})
    print("EQWE :" , details)
    return JsonResponse({'booked_dates': dates , 'details': details})


def d_writeblog(request):
    if "id" in request.session:
        if request.method == 'GET':
            context = {}
            context['doc'] = Doctors.objects.filter(id = request.session['id']).first()
            return render(request, 'doctor/d_writeblog.html', context)
        
        if request.method == "POST":
            title = request.POST['title']
            content = request.POST['content']
            img = request.FILES.get('image')
            d = Doctors.objects.filter(id=request.session['id']).first()
            d_email = d.email
            d_name = d.name
            date = datetime.now()

            blog = Blogs(title=title, content=content, img=img, d_name=d_name, d_email=d_email, date=date)
            blog.save()
            messages.success(request,"Your Blog is Uploaded successfully ")
            return redirect('/doctor/d_yourblog')

    else:
        return redirect('/login')
    
def d_viewblog(request):
    if "id" in request.session:
        if request.method == 'GET':
            context = {}
            context['doc'] = Doctors.objects.filter(id = request.session['id']).first()
            context['blogs'] = Blogs.objects.all().order_by('id').reverse()
            return render(request, 'doctor/d_viewblog.html', context)
    else:
        return redirect('/login')
    
def d_yourblog(request):
    if "id" in request.session:
        if request.method == 'GET':
            context = {}
            context['doc'] = Doctors.objects.filter(id = request.session['id']).first()
            context['blogs'] = Blogs.objects.filter(d_email = request.session['email']).order_by('id').reverse()
            return render(request, 'doctor/d_yourblog.html', context)
    else:
        return redirect('/login')
    

def remove_blog(request):
    if "id" in request.session:
        if request.method == "POST":
            id = request.POST['blog_id']
            b = Blogs.objects.get(id=id)
            b.delete()
            messages.success(request,"Your Blog is Deleted successfully ")
            return redirect('/doctor/d_yourblog', messages)
    return render(request, 'doctor/d_yourblog.html')
