# Generated by Django 5.1.7 on 2025-03-19 09:43

import datetime
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150, unique=True)),
                ('password', models.CharField(blank=True, max_length=100)),
                ('role', models.CharField(blank=True, max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Day', models.DateTimeField(default=django.utils.timezone.now)),
                ('Date', models.DateTimeField(default=django.utils.timezone.now)),
                ('login_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('logout_time', models.DateTimeField(blank=True, null=True)),
                ('is_on_break', models.BooleanField(default=False)),
                ('break_start_time', models.DateTimeField(blank=True, null=True)),
                ('break_end_time', models.DateTimeField(blank=True, null=True)),
                ('total_break_time', models.DurationField(default=datetime.timedelta(0))),
                ('total_working_hours', models.DurationField(blank=True, null=True)),
                ('auto_logged_out', models.BooleanField(default=False)),
                ('Staff_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.employee')),
            ],
        ),
    ]
