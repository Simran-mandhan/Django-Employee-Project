from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Employee
from .serializers import EmployeeSerializer

class EmployeeTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.employee_data = {'name': 'John Doe', 'department': 'Engineering', 'position': 'Software Developer', 'salary': 70000}
        self.response = self.client.post(reverse('employee-list'), self.employee_data, format='json')

    def test_create_employee(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_get_all_employees(self):
        response = self.client.get(reverse('employee-list'))
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_employee(self):
        employee = Employee.objects.first()
        response = self.client.get(reverse('employee-detail', kwargs={'pk': employee.id}))
        serializer = EmployeeSerializer(employee)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_employee(self):
        employee = Employee.objects.first()
        updated_employee_data = {'name': 'John Smith', 'department': 'HR', 'position': 'Manager', 'salary': 80000}
        response = self.client.put(reverse('employee-detail', kwargs={'pk': employee.id}), updated_employee_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_employee(self):
        employee = Employee.objects.first()
        response = self.client.delete(reverse('employee-detail', kwargs={'pk': employee.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)