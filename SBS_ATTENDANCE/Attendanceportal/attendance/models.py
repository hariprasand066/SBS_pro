import datetime
from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now

from django.db import models
from django.contrib.auth.hashers import make_password

class Employee(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=100, blank=True)
    role = models.CharField(max_length=20, blank=True)

    def save(self, *args, **kwargs):
        # Automatically hash the password before saving
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class Attendance(models.Model):
    Staff_name = models.ForeignKey(Employee, on_delete=models.CASCADE) 
    Day=models.DateTimeField(default=now)
    Date=models.DateTimeField(default=now)
    login_time = models.DateTimeField(default=now)
    logout_time = models.DateTimeField(null=True, blank=True)
    is_on_break = models.BooleanField(default=False)
    break_start_time = models.DateTimeField(null=True, blank=True)
    break_end_time = models.DateTimeField(null=True, blank=True)
    total_break_time = models.DurationField(default=datetime.timedelta())
    total_working_hours = models.DurationField(null=True, blank=True)
    auto_logged_out = models.BooleanField(default=False)
    
    
    def __str__(self):
        return f"{self.employee.user} - {self.login_time}"
