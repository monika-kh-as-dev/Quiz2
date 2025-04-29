from rest_framework import serializers
from .models import Employee, Department, Performance, Attendance

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())

    class Meta:
        model = Employee
        fields = '__all__'

    def validate_department(self, value):
        # Check if the department exists
        if not Department.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Department with the given ID does not exist.")
        return value
    
    def validate_salary(self, value):
        if value < 0:
            raise serializers.ValidationError("Salary cannot be negative.")
        return value
    
    
    def validate_email(self, value):
        if any(domain in value for domain in ["mailinator.com", "10minutemail.com"]):
            raise serializers.ValidationError("Disposable email addresses are not allowed.")
        return value        

class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'