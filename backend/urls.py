"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from rest_framework import routers
from aniresfr import views



router = routers.DefaultRouter()
router.register(r'animals', views.AnimalView, 'animal')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/customuser/register/', views.CustomUserRegistration.as_view(), name='customuser-register'),
    path('api/customuser/login/', views.CustomUserLogin.as_view(), name='customuser-login'),
    path('api/customuser/info', views.CustomUserView.as_view(), name='customuser-info'),
    path('api/ngouser/register/', views.NgoUserRegistration.as_view(), name='ngouser-register'),
    path('api/ngouser/login/', views.NgoUserLogin.as_view(), name='ngouser-login'),
    path('api/ngouser/info', views.NgoUserView.as_view(), name='ngouser-info'),
]
