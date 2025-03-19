from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from attendance.views import (
    AttendanceViewSet, login_view, dashboard_view, logout_view, break_toggle_view
)
from django.contrib.auth import views as auth_views
router = DefaultRouter()
router.register(r'attendance', AttendanceViewSet, basename='attendance')

urlpatterns = [
    path("", login_view, name="login"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("logout/", logout_view, name="logout"),
    path("break-toggle/", break_toggle_view, name="break_toggle"),
    path("api/", include(router.urls)),
     path('change-password/', auth_views.PasswordChangeView.as_view(template_name='password.html'), name='password_change'),
    path('change-password-done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_done.html'), name='password_change_done'),

    path('api/attendance/start_break/', AttendanceViewSet.as_view({'post': 'start_break'}), name='start_break'),
    path('api/attendance/end_break/', AttendanceViewSet.as_view({'post': 'end_break'}), name='end_break'),
    path('api/attendance/logout/', AttendanceViewSet.as_view({'post': 'logout'}), name='logout_api'),
    path('attendance/get_username/', AttendanceViewSet.as_view({'get': 'get_username'}), name='get_username'),
    path('api/attendance/auto_logout_count/', AttendanceViewSet.as_view({'get': 'auto_logout_count'}), name='auto_logout_count'),
]

urlpatterns += router.urls  