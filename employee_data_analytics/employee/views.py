from datetime import date
from rest_framework import viewsets, filters ,views
from .models import Employee, Department, Performance, Attendance
from .serializers import EmployeeSerializer, DepartmentSerializer, PerformanceSerializer, AttendanceSerializer
from django.db.models import Avg, Count
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models.functions import TruncMonth
from django.views.generic import TemplateView
from rest_framework.permissions import IsAuthenticated ,AllowAny
from rest_framework.throttling import UserRateThrottle
from rest_framework.pagination import PageNumberPagination

class PaginatedResults(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class ThrottleRate(UserRateThrottle):
    rate = '10/min'

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ThrottleRate]
    pagination_class = PaginatedResults

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'email']
    ordering_fields = ['salary', 'hire_date']
    permission_classes = [IsAuthenticated]
    throttle_classes = [ThrottleRate]
    pagination_class = PaginatedResults

class PerformanceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer
    permission_classes = [IsAuthenticated]

class AttendanceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PaginatedResults

class SummaryView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        total_employees = Employee.objects.count()
        avg_salary = Employee.objects.aggregate(avg_salary=Avg('salary'))['avg_salary']
        avg_rating = Performance.objects.aggregate(avg_rating=Avg('rating'))['avg_rating']
        attendance_summary = Attendance.objects.values('status').annotate(count=Count('status'))

        return Response({
            'total_employees': total_employees,
            'average_salary': avg_salary,
            'average_performance_rating': avg_rating,
            'attendance_summary': attendance_summary,
        })
    
class AttendanceTrendView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        data = (Attendance.objects
                .annotate(month=TruncMonth('date'))
                .values('month', 'status')
                .annotate(count=Count('id'))
                .order_by('month'))
        return Response(data)
    
class AvgPerformanceByDeptView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        data = (Performance.objects
                .values('employee__department')
                .annotate(avg_rating=Avg('rating')))
        return Response(data)

class EmployeeDistributionView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        data = Employee.objects.values('department').annotate(count=Count('id'))
        return Response(data)        

class TenureDistributionView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        today = date.today()
        employees = Employee.objects.all()
        distribution = {
            '<1 year': 0,
            '1-3 years': 0,
            '3+ years': 0,
        }
        for emp in employees:
            tenure = (today - emp.date_joined).days / 365
            if tenure < 1:
                distribution['<1 year'] += 1
            elif tenure < 3:
                distribution['1-3 years'] += 1
            else:
                distribution['3+ years'] += 1
        return Response(distribution)    
    
class AvgSalaryByDeptView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        data = Employee.objects.values('department').annotate(avg_salary=Avg('salary'))
        return Response(data)    
    
    
class DashboardView( TemplateView):
    template_name = 'employees/dashboard.html'