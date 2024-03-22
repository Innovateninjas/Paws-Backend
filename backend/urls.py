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
router.register(r'campaigns', views.CampaignView, 'campaign')

urlpatterns = [
    path('register/user', views.CustomUserRegistration.as_view(), name='register user'),
    path('register/ngo', views.NgoUserRegistration.as_view(), name='register ngo'),
    path('info/user/', views.CustomUserView.as_view(), name='user info'),
    path('info/ngo/', views.NgoUserView.as_view(), name='ngo info'),
    path('ngo', views.NgoView.as_view(), name='ngo'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),

]
