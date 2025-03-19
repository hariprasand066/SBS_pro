from django.contrib import admin
from .models import Employee

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('username', 'role')     

admin.site.register(Employee, EmployeeAdmin)
