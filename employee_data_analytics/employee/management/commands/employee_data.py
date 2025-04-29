from django.core.management.base import BaseCommand
from faker import Faker
from employee.models import Employee, Department, Performance, Attendance
import random
from datetime import timedelta, date

class Command(BaseCommand):
    help = 'Generate synthetic employee data'

    def handle(self, *args, **kwargs):
        fake = Faker()
        departments = [Department.objects.create(name=dep) for dep in ['HR', 'Engineering', 'Sales', 'Finance']]

        for _ in range(5):
            dept = random.choice(departments)
            emp = Employee.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.unique.email(),
                department=dept,
                position=fake.job(),
                hire_date=fake.date_between(start_date='-5y', end_date='-1y'),
                salary=round(random.uniform(40000, 120000), 2)
            )
            # Performance
            for _ in range(3):
                Performance.objects.create(
                    employee=emp,
                    review_date=fake.date_between(start_date='-1y', end_date='today'),
                    rating=random.randint(1, 5),
                    notes=fake.text()
                )
            # Attendance
            for i in range(20):
                Attendance.objects.create(
                    employee=emp,
                    date=fake.date_between(start_date='-1m', end_date='today'),
                    status=random.choice(['Present', 'Absent', 'Leave'])
                )