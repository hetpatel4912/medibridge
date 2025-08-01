from django.shortcuts import render, redirect
from .models import Users, Doctors
from itertools import chain

def set_session(request, user_obj):
    request.session['id'] = user_obj.id
    request.session['email'] = user_obj.email
    request.session['role'] = user_obj.role
    return request

def d_set_session(request, user_obj):
    request.session['id'] = user_obj.id
    request.session['email'] = user_obj.email
    request.session['approved'] = user_obj.approved
    return request



# Create your views here.
def login(request):
    if request.method == "GET":
        return render(request, 'registration/login.html')
    else:

        if request.POST['type'] == 'login':
            user_obj = Users.objects.filter(email=request.POST['email'].lower(), password=request.POST['password']).first()
            if user_obj:
                request = set_session(request, user_obj)
                print(user_obj.role)
                if user_obj.role == 1:
                    return redirect('/admin1')
                elif user_obj.role == 2:
                    return redirect('/')    

            else:
                user_obj = Doctors.objects.filter(email=request.POST['email'].lower(), password=request.POST['password']).first()
                if user_obj:
                    request = d_set_session(request, user_obj)
                    print(" eugwet : ", request)
                    return redirect('/doctor')
                
            warning={"warning":"*Invalid Credentials"} 
            return render(request, 'registration/login.html', warning)
            

        elif request.POST['type'] =='registration':

            # if request.POST['role'] == 'user':
            # elif request.POST['role'] == 'doctor':
            
            user_table= Users.objects.filter(email=request.POST['email'].lower())
            doctor_table = Doctors.objects.filter(email=request.POST['email'].lower())

            models_data = list(chain(user_table,doctor_table))
            if len(models_data) > 0:
                warning={"warning":"*Email Already Exist. Try another email"}
                return render(request, 'registration/login.html', warning)
            
            elif request.POST['password'] != request.POST['cpassword']:
                warning={"warning":"*Password and Confirm Password did not match"}
                return render(request, 'registration/login.html', warning)
        
            if request.POST['role'] == 'user':
                email = request.POST['email'].lower()
                password = request.POST['password']
                user = Users(password=password,email=email,role=2)
                user.save()


            elif request.POST['role'] == 'doctor':
                email           = request.POST['email'].lower()
                password        = request.POST['password']
                name            = request.POST['name']
                specialist      = request.POST['specialist']
                image           = request.FILES.get('doctor_image')
                user            = Doctors(email=email, name=name, specialist=specialist, password=password, image=image)
                user.save()
        
        return redirect('/login')
        