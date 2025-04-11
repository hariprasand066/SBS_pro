from time import timezone
from django.http import JsonResponse
from django.utils.timezone import now
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from .models import Attendance

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import *
from .serializers import AttendanceSerializer
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    #permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            employee = Employee.objects.get(user=user)
            attendance = Attendance.objects.create(employee=employee, login_time=now())
            return Response({'message': 'Login successful', 'attendance_id': attendance.id})
        return Response({'error': 'Invalid User'}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['get'])
    def get_username(self, request):
        if request.user.is_authenticated:
            return Response({'username': request.user.username})
        return Response({'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['post'])
    def start_break(self, request):
        attendance_id = request.data.get('attendance_id')
        
        if not attendance_id:
            return Response({'error': 'Attendance ID required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            attendance = Attendance.objects.get(id=attendance_id)
            
            if attendance.is_on_break:
                return Response({'error': 'Break already started'}, status=status.HTTP_400_BAD_REQUEST)
            
            attendance.is_on_break = True
            attendance.break_start_time = timezone.now()
            attendance.save()

            return Response({'message': 'Break started successfully'}, status=status.HTTP_200_OK)

        except Attendance.DoesNotExist:
            return Response({'error': 'Attendance record not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'])
    def end_break(self, request):
        attendance_id = request.data.get('attendance_id')

        if not attendance_id:
            return Response({'error': 'Attendance ID required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            attendance = Attendance.objects.get(id=attendance_id)

            if not attendance.is_on_break:
                return Response({'error': 'No active break to end'}, status=status.HTTP_400_BAD_REQUEST)

            # Calculate total break time
            if attendance.break_start_time:
                attendance.break_end_time = timezone.now()
                attendance.total_break_time += attendance.break_end_time - attendance.break_start_time
                attendance.is_on_break = False
                attendance.break_start_time = None
                attendance.break_end_time = None
                attendance.save()

            return Response({'message': 'Break ended successfully'}, status=status.HTTP_200_OK)

        except Attendance.DoesNotExist:
            return Response({'error': 'Attendance record not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'])
    def logout(self, request):
        attendance_id = request.data.get('attendance_id')
        auto_logout = request.data.get('auto_logout', False)  # Check if it's an auto-logout

        try:
            attendance = Attendance.objects.get(id=attendance_id)
            attendance.logout_time = now()
            attendance.total_working_hours = (attendance.logout_time - attendance.login_time) - attendance.total_break_time
            
            if auto_logout:  # If the logout is due to inactivity
                attendance.auto_logged_out = True

            attendance.save()
            return Response({
                'message': 'Logout successful', 
                'total_hours': str(attendance.total_working_hours),
                'auto_logged_out': attendance.auto_logged_out
            })
        except Attendance.DoesNotExist:
            return Response({'error': 'Attendance record not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['get'])
    def start_session(self, request):
        user = request.user
        attendance = Attendance.objects.create(staff_name=user, login_time=timezone.now())
        return Response({'attendance_id': attendance.id}) 
csrf_exempt
def login_view(request):
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/dashboard/") 
            else:
                return render(request, "login.html", {"error": "Invalid credentials"})

        return render(request, "login.html")



@login_required
def dashboard_view(request):
        return render(request, "dashboard.html", {'username': request.user.username})

@csrf_exempt  # Disable CSRF protection for this view
def logout_view(request):
        if request.method == "POST":
            if request.user.is_authenticated:
                logout(request)
                return JsonResponse({"message": "Logout successful"}, status=200)
            else:
                return JsonResponse({"error": "User not authenticated"}, status=401)
        
        return JsonResponse({"error": "Invalid request method"}, status=400)

@login_required
def break_toggle_view(request):
        if request.method == "POST":
            user = request.user

            # Fetch the user's active attendance record (must be logged in and not logged out)
            attendance = Attendance.objects.filter(employee__user=user, logout_time__isnull=True).first()

            if attendance:
                if attendance.is_on_break:
                    # Stop the break and calculate the total break time
                    if attendance.break_start_time:
                        attendance.total_break_time += now() - attendance.break_start_time
                        attendance.break_start_time = None
                    attendance.is_on_break = False
                    message = "Break ended, working hours resumed"
                else:
                    # Start the break
                    attendance.break_start_time = now()
                    attendance.is_on_break = True
                    message = "Break started"

                attendance.save()
                return JsonResponse({"message": message, "is_on_break": attendance.is_on_break}, status=200)

            return JsonResponse({"error": "No active attendance record found"}, status=400)

        return JsonResponse({"error": "Invalid request method"}, status=400)
@login_required
def change_password(request):
        if request.method == 'POST':
            form = PasswordChangeForm(user=request.user, data=request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Keep user logged in
                return redirect('/dashboard/')
        else:
            form = PasswordChangeForm(user=request.user)
        return render(request, 'password.html', {'form': form})

    

    
@action(detail=False, methods=['post'])
def start_break(self, request):
    attendance_id = request.data.get('attendance_id')
    try:
        attendance = Attendance.objects.get(id=attendance_id)
    except Attendance.DoesNotExist:
        return Response({'error': 'Attendance record not found'}, status=404)
