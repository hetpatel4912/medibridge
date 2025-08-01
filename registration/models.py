from django.db import models

# Create your models here.
class Users(models.Model):

    class RoleChoice(models.IntegerChoices):
        Choice_1 = 1, "Admin"
        Choice_2 = 2, "User"

    email = models.CharField(max_length=50,unique=True)
    password = models.CharField(max_length=50)
    role = models.IntegerField(choices=RoleChoice.choices)
    # name = models.CharField(max_length=50, default="")
    # specialist = models.CharField(max_length=50, default="")
    # image = models.ImageField(upload_to='users/doctors/image', default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_At = models.DateTimeField(auto_now=True)

class Doctors(models.Model):
    email = models.CharField(max_length=50,unique=True)
    password = models.CharField(max_length=50)
    name = models.CharField(max_length=50, default="")
    specialist = models.CharField(max_length=50, default="")
    image = models.ImageField(upload_to='users/doctors/image', default="")
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_At = models.DateTimeField(auto_now=True)


class Donors(models.Model):
    email = models.CharField(max_length=50,unique=True)
    name = models.CharField(max_length=50)
    blood_group = models.CharField(max_length=5)
    contact_no = models.CharField(max_length=12)
    residence = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_At = models.DateTimeField(auto_now=True)


class Appointment(models.Model):
    email = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    phoneno = models.CharField(max_length=12)
    date = models.DateField()
    d_email = models.CharField(max_length=50)


class Blogs(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=1000)
    img = models.ImageField(upload_to='users/blogs/image', default="")
    d_name = models.CharField(max_length=50)
    d_email  = models.CharField(max_length=50)
    date = models.DateTimeField()