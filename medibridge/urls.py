"""
URL configuration for medibridge project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import *
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin1/', include("admin1.urls")),
    path('doctor/', include("doctor.urls")),
    path('api/', include("api.urls")),
    path('login/', include("registration.urls")),
    path('', index , name="index"),
    path('about_us/', about_us, name="about_us"),
    path('services/', services, name="services"),
    path('donors/', donors, name="donors"),
    path('doctors/', doctors, name="doctors"),
    path('book_now/', book_now, name="book_now"),
    path('view_appointment/', view_appointment, name="view_appointment"),
    path('blogs/', blogs, name="blogs"),
    path('review/', review, name="review"),
    path('logout/', logout, name="logout"),

]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)        