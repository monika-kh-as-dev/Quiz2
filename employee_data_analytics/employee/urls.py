from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AttendanceTrendView, AvgPerformanceByDeptView, AvgSalaryByDeptView, DashboardView, EmployeeDistributionView, EmployeeViewSet, DepartmentViewSet, PerformanceViewSet, AttendanceViewSet, SummaryView, TenureDistributionView

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'performances', PerformanceViewSet)
router.register(r'attendance', AttendanceViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('summary/', SummaryView.as_view(), name='summary'),
    path('analytics/average-salary-by-department/', AvgSalaryByDeptView.as_view()), 
    path('analytics/attendance-trend/', AttendanceTrendView.as_view()),
    path('analytics/average-performance-by-department/', AvgPerformanceByDeptView.as_view()),
    path('analytics/employee-distribution/', EmployeeDistributionView.as_view()),
    path('analytics/tenure-distribution/', TenureDistributionView.as_view()),

]