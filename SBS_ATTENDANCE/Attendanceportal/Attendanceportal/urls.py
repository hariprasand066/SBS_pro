"""
URL configuration for Attendanceportal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.shortcuts import redirect

from attendance.views import break_toggle_view, change_password, dashboard_view, login_view, logout_view

def redirect_to_login(request):
    return redirect('login')

urlpatterns = [
  path('admin/', admin.site.urls),
  path('', redirect_to_login, name='home'),
  path(' ', login_view, name='login'), 
  path('dashboard/', dashboard_view, name='dashboard'),
  path('logout/', logout_view, name='logout'),
  path('break-toggle/', break_toggle_view, name='break_toggle'),
  path('attendance/', include('attendance.urls')),
  path('change-password/', change_password, name='change_password'),

   path('api/', include('attendance.urls')),  
]


