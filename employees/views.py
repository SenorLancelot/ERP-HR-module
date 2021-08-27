from django.db.models.query import QuerySet
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
from django.db.models import Sum
from utils.renderers import CustomRenderer
# from datetime import datetime
import datetime

# default value of detail, methods array,

# project imports
from rest_framework.decorators import action

from .models import *
from .serializers import *

from drf_yasg.utils import swagger_auto_schema


class EmployeeViewSet(viewsets.ViewSet):

    
    @swagger_auto_schema(responses={200: EmployeeResponseSerializer})
    @action(detail=True, methods=["get"], url_path="read")
    def read_employee(self, request, pk):

        try:
            queryset = Employee.objects.get(id=pk)
        except:
            return Response({"message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        fields = self.request.query_params.getlist('fields', '')
        try:

            if fields == '':
            
                serialized = EmployeeResponseSerializer(instance=queryset)
            else:
                serialized = EmployeeResponseSerializer(instance=queryset, fields=fields)
        except:
            return Response(
                {"message": "Serializer error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={200: EmployeeResponseSerializer})
    @action(detail=False, methods=["get"], url_path="read")
    def read_employees(self, request):
        
        
        
        
        
        try:
            queryset = Employee.objects.all()
        except:
            
            return Response({"message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        fields = self.request.query_params.getlist('fields', '')
        try:

            if fields == '':
            
                serialized = EmployeeResponseSerializer(instance=queryset, many=True)
            else:
                serialized = EmployeeResponseSerializer(instance=queryset, many=True, fields=fields)
                
        except:
            return Response(
                {"message": "Serializer error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=EmployeeRequestSerializer, responses={200: EmployeeRequestSerializer}
    )
    @action(detail=False, methods=["patch"], url_path="update")
    def update_employees(self, request):

        try:
            employee = request.data["id"]

        except:

            return Response(
                {"message": "Request body incorrect. Please specify ID."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:

            queryset = Employee.objects.get(id=employee)

        except:

            return Response({"message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        serialized = EmployeeRequestSerializer(queryset, request.data, partial=True)

        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], url_path="create")
    @swagger_auto_schema(
        request_body=EmployeeRequestSerializer, responses={200: EmployeeRequestSerializer}
    )
    def create_employees(self, request):

        serialized = EmployeeRequestSerializer(data=request.data, many=True)

        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["delete"], url_path="delete")
    @swagger_auto_schema(
        request_body=EmployeeListSerializer, responses={200: EmployeeListSerializer}
    )
    def delete_employees(self, request):

        serialized = EmployeeListSerializer(data=request.data)

        if serialized.is_valid():
            Employee.objects.filter(id__in=request.data["employee_ids"]).update(status = 'Hidden')

            return Response(data=request.data, status=status.HTTP_200_OK)
        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerViewSet(viewsets.ViewSet):
    @swagger_auto_schema(responses={200: CustomerResponseSerializer})
    @action(detail=True, methods=["get"], url_path="read")
    def read_customer(self, request, pk):

        try:
            queryset = Customer.objects.get(id=pk)
        except:
            return Response({"message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        fields = self.request.query_params.getlist('fields', '')
        try:

            if fields == '':
            
                serialized = CustomerResponseSerializer(instance=queryset)
            else:
                serialized = CustomerResponseSerializer(instance=queryset, fields=fields)
        except:
            return Response(
                {"message": "Serializer error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={200: CustomerResponseSerializer})
    @action(detail=False, methods=["get"], url_path="read")
    def read_customers(self, request):

        try:
            queryset = Customer.objects.all()
        except:
            return Response({"message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        fields = self.request.query_params.getlist('fields', '')
        try:

            if fields == '':
            
                serialized = CustomerResponseSerializer(instance=queryset, many=True)
            else:
                serialized = CustomerResponseSerializer(instance=queryset, many=True, fields=fields)
        except:
            return Response(
                {"message": "Serializer error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=CustomerRequestSerializer, responses={200: CustomerRequestSerializer}
    )
    @action(detail=False, methods=["patch"], url_path="update")
    def update_customers(self, request):

        try:
            employee = request.data["id"]

        except:

            return Response(
                {"message": "Request body incorrect. Please specify ID."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        queryset = Customer.objects.get(id=employee)

        serialized = CustomerRequestSerializer(queryset, request.data, partial=True)

        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], url_path="create")
    @swagger_auto_schema(
        request_body=CustomerRequestSerializer, responses={200: CustomerRequestSerializer}
    )
    def create_customers(self, request):

        serialized = CustomerRequestSerializer(data=request.data, many=True)

        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["delete"], url_path="delete")
    @swagger_auto_schema(
        request_body=CustomerListSerializer, responses={200: CustomerListSerializer}
    )
    def delete_customers(self, request):

        serialized = CustomerListSerializer(data=request.data)

        if serialized.is_valid():
            Customer.objects.filter(id__in=request.data["customer_ids"]).update(status = 'Hidden')

            return Response(data=request.data, status=status.HTTP_200_OK)
        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyViewSet(viewsets.ViewSet):
    @swagger_auto_schema(responses={200: CompanyResponseSerializer})
    @action(detail=True, methods=["get"], url_path="read")
    def read_company(self, request, pk):

        try:
            queryset = Company.objects.get(id=pk)
        except:
            return Response({"message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        fields = self.request.query_params.getlist('fields', '')
        try:

            if fields == '':
            
                serialized = CompanyResponseSerializer(instance=queryset)
            else:
                serialized = CompanyResponseSerializer(instance=queryset, fields=fields)

        except:

            return Response(
                {"message": "Serializer error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], url_path="read_employees")
    @swagger_auto_schema(responses={200: EmployeeResponseSerializer})
    def read_company_employees(self, request, pk):

        try:
            queryset = Employee.objects.filter(fk_company=pk)
        except:
            return Response({"message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)
        fields = self.request.query_params.getlist('fields', '')
        try:

            if fields == '':
            
                serialized = EmployeeResponseSerializer(instance=queryset, many=True)
            else:
                serialized = EmployeeResponseSerializer(instance=queryset, many=True, fields=fields)
        except:
            return Response(
                {"message": "Serializer error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["patch"], url_path="update")
    @swagger_auto_schema(
        request_body=CompanyRequestSerializer, responses={200: CompanyRequestSerializer}
    )
    def update_companies(self, request):

        try:
            company = request.data["id"]

        except:

            return Response(
                {"message": "Request body incorrect. Please specify  ID."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        queryset = Company.objects.get(id=company)

        serialized = CompanyRequestSerializer(queryset, request.data, partial=True)

        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"], url_path="read")
    @swagger_auto_schema(responses={200: CompanyResponseSerializer})
    def read_companies(self, request):

        try:
            queryset = Company.objects.all()
        except:
            return Response({"message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        fields = self.request.query_params.getlist('fields', '')
        try:

            if fields == '':
            
                serialized = CompanyResponseSerializer(instance=queryset, many=True)
            else:
                serialized = CompanyResponseSerializer(instance=queryset, many=True, fields=fields)

        except:

            return Response(
                {"message": "Serializer error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="create")
    @swagger_auto_schema(
        request_body=CompanyRequestSerializer, responses={200: CompanyRequestSerializer}
    )
    def create_companies(self, request):

        serialized = CompanyRequestSerializer(data=request.data, many=True)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["delete"], url_path="delete")
    @swagger_auto_schema(
        request_body=CompanyListSerializer, responses={200: CompanyListSerializer}
    )
    def delete_companies(self, request):

        serialized = CompanyListSerializer(data=request.data)

        if serialized.is_valid():

            Company.objects.filter(id__in=request.data["company_ids"]).update(status = 'Hidden')

            return Response(data=request.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeGradeViewSet(viewsets.ViewSet):
    @swagger_auto_schema(responses={200: EmployeeGradeResponseSerializer})
    @action(detail=True, methods=["get"], url_path="read")
    def read_employee_grade(self, request, pk):

        try:
            queryset = EmployeeGrade.objects.get(id=pk)
        except:
            return Response({"message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        fields = self.request.query_params.getlist('fields', '')
        try:

            if fields == '':
            
                serialized = EmployeeGradeResponseSerializer(instance=queryset)
            else:
                serialized = EmployeeGradeResponseSerializer(instance=queryset, fields=fields)

        except:

            return Response(
                {"message": "Serializer error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["patch"], url_path="update")
    @swagger_auto_schema(
        request_body=EmployeeGradeRequestSerializer, responses={200: EmployeeGradeRequestSerializer}
    )
    def update_employee_grades(self, request):

        try:
            employee_grade = request.data["id"]

        except:

            return Response(
                {"message": "Request body incorrect. Please specify  ID."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        queryset = EmployeeGrade.objects.get(id=employee_grade)

        serialized = EmployeeGradeRequestSerializer(queryset, request.data, partial=True)

        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"], url_path="read")
    @swagger_auto_schema(responses={200: EmployeeGradeResponseSerializer})
    def read_employee_grades(self, request):

        try:
            queryset = EmployeeGrade.objects.all()
        except:
            return Response({"message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        fields = self.request.query_params.getlist('fields', '')
        try:

            if fields == '':
            
                serialized = EmployeeGradeResponseSerializer(instance=queryset, many=True)
            else:
                serialized = EmployeeGradeResponseSerializer(instance=queryset, many=True, fields=fields)

        except:

            return Response(
                {"message": "Serializer error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="create")
    @swagger_auto_schema(
        request_body=EmployeeGradeRequestSerializer, responses={200: EmployeeGradeRequestSerializer}
    )
    def create_employee_grades(self, request):

        serialized = EmployeeGradeRequestSerializer(data=request.data, many=True)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["delete"], url_path="delete")
    @swagger_auto_schema(
        request_body=EmployeeGradeListSerializer,
        responses={200: EmployeeGradeListSerializer},
    )
    def delete_employee_grades(self, request):

        serialized = EmployeeGradeListSerializer(data=request.data)

        if serialized.is_valid():

            EmployeeGrade.objects.filter(
                id__in=request.data["employee_grade_ids"]
            ).update(status = 'Hidden')

            return Response(data=request.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeGroupViewSet(viewsets.ViewSet):
    @swagger_auto_schema(responses={200: EmployeeGroupResponseSerializer})
    @action(detail=True, methods=["get"], url_path="read")
    def read_employee_group(self, request, pk):

        try:
            queryset = EmployeeGroup.objects.get(id=pk)
        except:
            return Response({"message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        fields = self.request.query_params.getlist('fields', '')
        try:

            if fields == '':
            
                serialized = EmployeeGroupResponseSerializer(instance=queryset, many=True)
            else:
                serialized = EmployeeGroupResponseSerializer(instance=queryset, many=True, fields=fields)

        except:

            return Response(
                {"message": "Serializer error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], url_path="read_employees")
    @swagger_auto_schema(responses={200: EmployeeResponseSerializer})
    def read_employee_group_employees(self, request, pk):

        try:
            queryset = Employee.objects.filter(fk_employee_group=pk)
        except:
            return Response({"message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        fields = self.request.query_params.getlist('fields', '')
        try:

            if fields == '':
            
                serialized = EmployeeResponseSerializer(instance=queryset, many=True)
            else:
                serialized = EmployeeResponseSerializer(instance=queryset, many=True, fields=fields)

        except:

            return Response(
                {"message": "Serializer error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], url_path="read_employee_group_presence")
    @swagger_auto_schema()
    def read_employee_group_presence(self, request, pk):

        try:

            group = EmployeeGroup.objects.get(id=pk)
            print(group)
            employees = group.fk_employee.all()
            print(employees)
            sessions = EmployeeSession.objects.filter(
                fk_employee__in=employees, checked_out_at__isnull=True
            )

        except ValueError:

            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if len(employees) == sessions.count():

            return Response({"message": "All present"}, status=status.HTTP_200_OK)

        else:

            return Response({"message": "All not present"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["patch"], url_path="update")
    @swagger_auto_schema(
        request_body=EmployeeGroupRequestSerializer, responses={200: EmployeeGroupRequestSerializer}
    )
    def update_employee_group(self, request):

        try:
            employeegroup = request.data["id"]

        except:

            return Response(
                {"message": "No ID in request data"}, status=status.HTTP_400_BAD_REQUEST
            )

        queryset = EmployeeGroup.objects.get(id=employeegroup)

        serialized = EmployeeGroupRequestSerializer(queryset, request.data, partial=True)

        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"], url_path="read")
    @swagger_auto_schema(responses={200: EmployeeGroupResponseSerializer})
    def read_employee_groups(self, request):

        try:
            queryset = EmployeeGroup.objects.all()
        except:
            return Response({"message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        fields = self.request.query_params.getlist('fields', '')
        try:

            if fields == '':
            
                serialized = EmployeeGroupResponseSerializer(instance=queryset, many=True)
            else:
                serialized = EmployeeGroupResponseSerializer(instance=queryset, many=True, fields=fields)

        except:

            return Response(
                {"message": "Serializer error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="create")
    @swagger_auto_schema(
        request_body=EmployeeGroupRequestSerializer, responses={200: EmployeeGroupRequestSerializer}
    )
    def create_employee_group(self, request):

        serialized = EmployeeGroupRequestSerializer(data=request.data, many=True)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["delete"], url_path="delete")
    @swagger_auto_schema(
        request_body=EmployeeGroupListSerializer,
        responses={200: EmployeeGroupListSerializer},
    )
    def delete_employee_group(self, request):

        serialized = EmployeeGroupListSerializer(data=request.data)

        if serialized.is_valid():
            EmployeeGroup.objects.filter(id__in=request.data["group_ids"]).update(status = 'Hidden')

            return Response(data=request.data, status=status.HTTP_200_OK)
        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)





class DepartmentViewSet(viewsets.ViewSet):

    # renderer_classes = [CustomRenderer]

    @swagger_auto_schema(responses={200: DepartmentResponseSerializer})
    @action(detail=True, methods=["get"], url_path="read")
    def read_department(self, request, pk):

        try:
            queryset = Department.objects.get(id=pk)
        except:
            return Response({"message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        fields = self.request.query_params.getlist('fields', '')
        try:

            if fields == '':
            
                serialized = DepartmentResponseSerializer(instance=queryset)
            else:
                serialized = DepartmentResponseSerializer(instance=queryset, fields=fields)

        except:

            return Response(
                {"message": "Serializer error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], url_path="read_employees")
    @swagger_auto_schema(responses={200: EmployeeResponseSerializer})
    def read_department_employees(self, request, pk):

        try:
            queryset = Employee.objects.filter(fk_department=pk)
        except:
            return Response({"message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        fields = self.request.query_params.getlist('fields', '')
        try:

            if fields == '':
            
                serialized = EmployeeResponseSerializer(instance=queryset, many=True)
            else:
                serialized = EmployeeResponseSerializer(instance=queryset, many=True, fields=fields)

        except:

            return Response(
                {"message": "Serializer error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["patch"], url_path="update")
    @swagger_auto_schema(
        request_body=DepartmentRequestSerializer, responses={200: DepartmentRequestSerializer}
    )
    def update_departments(self, request):

        try:
            department = request.data["id"]

        except:

            return Response(
                {"message": "Request body incorrect. Please specify  ID."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        queryset = Department.objects.get(id=department)

        serialized = DepartmentRequestSerializer(queryset, request.data, partial=True)

        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"], url_path="read")
    @swagger_auto_schema(responses={200: DepartmentResponseSerializer})
    def read_departments(self, request):

        try:
            queryset = Department.objects.all()
        except:
            return Response({"message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        fields = self.request.query_params.getlist('fields', '')
        try:

            if fields == '':
            
                serialized = DepartmentResponseSerializer(instance=queryset, many=True)
            else:
                serialized = DepartmentResponseSerializer(instance=queryset, many=True, fields=fields)

        except:

            return Response(
                {"message": "Serializer error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="create")
    @swagger_auto_schema(
        request_body=DepartmentRequestSerializer, responses={200: DepartmentRequestSerializer}
    )
    def create_department(self, request):

        serialized = DepartmentRequestSerializer(data=request.data, many =True)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["delete"], url_path="delete")
    @swagger_auto_schema(
        request_body=DepartmentListSerializer,
        responses={200: DepartmentListSerializer},
    )
    def delete_department(self, request):

        serialized = DepartmentListSerializer(data=request.data)

        if serialized.is_valid():
            Department.objects.filter(id__in=request.data["department_ids"]).update(status = 'Hidden')

            return Response(data=request.data, status=status.HTTP_200_OK)
        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)


# LORAN
class DesignationViewSet(viewsets.ViewSet):
    @swagger_auto_schema(responses={200: DesignationResponseSerializer})
    @action(detail=True, methods=["get"], url_path="read")
    def read_designation(self, request, pk):

        try:
            queryset = Designation.objects.get(id=pk)
        except:
            return Response({"message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        fields = self.request.query_params.getlist('fields', '')
        try:

            if fields == '':
            
                serialized = DesignationResponseSerializer(instance=queryset)
            else:
                serialized = DesignationResponseSerializer(instance=queryset, fields=fields)

        except:

            return Response(
                {"message": "Serializer error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], url_path="read_employees")
    @swagger_auto_schema(responses={200: EmployeeResponseSerializer})
    def read_designation_employees(self, request, pk):

        try:
            queryset = Employee.objects.filter(fk_designation=pk)
        except:
            return Response({"message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        fields = self.request.query_params.getlist('fields', '')
        try:

            if fields == '':
            
                serialized = EmployeeResponseSerializer(instance=queryset, many=True)
            else:
                serialized = EmployeeResponseSerializer(instance=queryset, many=True, fields=fields)

        except:

            return Response(
                {"message": "Serializer error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["patch"], url_path="update")
    @swagger_auto_schema(
        request_body=DesignationRequestSerializer, responses={200: DesignationRequestSerializer}
    )
    def update_designations(self, request):

        try:
            designation = request.data["id"]

        except:

            return Response(
                {"message": "Request body incorrect. Please specify  ID."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        queryset = Designation.objects.get(id=designation)

        serialized = DesignationRequestSerializer(queryset, request.data, partial=True)

        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"], url_path="read")
    @swagger_auto_schema(responses={200: DesignationResponseSerializer})
    def read_designations(self, request):

        try:
            queryset = Designation.objects.all()
        except:
            return Response({"message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        fields = self.request.query_params.getlist('fields', '')
        try:

            if fields == '':
            
                serialized = DesignationResponseSerializer(instance=queryset, many=True)
            else:
                serialized = DesignationResponseSerializer(instance=queryset, many=True, fields=fields)

        except:

            return Response(
                {"message": "Serializer error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="create")
    @swagger_auto_schema(
        request_body=DesignationRequestSerializer, responses={200: DesignationRequestSerializer}
    )
    def create_designations(self, request):

        serialized = DesignationRequestSerializer(data=request.data, many=True)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["delete"], url_path="delete")
    @swagger_auto_schema(
        request_body=DesignationListSerializer,
        responses={200: DesignationListSerializer},
    )
    def delete_designations(self, request):

        serialized = DesignationListSerializer(data=request.data)

        if serialized.is_valid():
            Designation.objects.filter(id__in=request.data["designation_ids"]).update(status = 'Hidden')

            return Response(data=request.data, status=status.HTTP_200_OK)
        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class EmergencyContactViewSet(viewsets.ViewSet):

    @swagger_auto_schema(responses={200: EmergencyContactResponseSerializer})
    @action(detail=True, methods=["get"], url_path="read")
    def read_emergency_contact(self, request, pk):

        try:
            queryset = EmergencyContact.objects.get(id=pk)
        except:
            return Response({"message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        fields = self.request.query_params.getlist('fields', '')
        try:

            if fields == '':
            
                serialized = EmergencyContactResponseSerializer(instance=queryset)
            else:
                serialized = EmergencyContactResponseSerializer(instance=queryset, fields=fields)

        except:

            return Response(
                {"message": "Serializer error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    

    @action(detail=False, methods=["patch"], url_path="update")
    @swagger_auto_schema(request_body=EmergencyContactRequestSerializer, responses={200: EmergencyContactRequestSerializer})
    def update_emergency_contacts(self, request):

        try:
            emergency_contact = request.data["id"]

        except:

            return Response(
                {"message": "Request body incorrect. Please specify  ID."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        queryset = EmergencyContact.objects.get(emergency_contact_id=emergency_contact)

        serialized = EmergencyContactRequestSerializer(queryset, request.data, partial=True)

        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"], url_path="read")
    @swagger_auto_schema(responses={200: EmergencyContactResponseSerializer})
    def read_emergency_contacts(self, request):

        try:
            queryset = EmergencyContact.objects.all()
        except:
            return Response({"message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        fields = self.request.query_params.getlist('fields', '')
        try:

            if fields == '':
            
                serialized = EmergencyContactResponseSerializer(instance=queryset, many=True)
            else:
                serialized = EmergencyContactResponseSerializer(instance=queryset, many=True, fields=fields)

        except:

            return Response(
                {"message": "Serializer error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="create")
    @swagger_auto_schema(request_body=EmergencyContactRequestSerializer, responses={200: EmergencyContactRequestSerializer})
    def create_emergency_contacts(self, request):

        serialized = EmergencyContactRequestSerializer(data=request.data, many=True)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["delete"], url_path="delete")
    @swagger_auto_schema(
        request_body=EmergencyContactListSerializer, responses={200: EmergencyContactListSerializer}
    )
    def delete_emergency_contacts(self, request):

        serialized = EmergencyContactListSerializer(data=request.data)

        if serialized.is_valid():

            EmergencyContact.objects.filter(id__in=request.data["leave_ids"]).update(status = 'Hidden')

            return Response(data=request.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

class IdentificationDocumentViewSet(viewsets.ViewSet):

    
    @swagger_auto_schema(responses={200: IdentificationDocumentResponseSerializer})
    @action(detail=True, methods=["get"], url_path="read_employee_documents")
    def read_employee_documents(self, request, pk):
        try:
            queryset = IdentificationDocument.objects.filter(fk_employee=pk)
        except:
            return Response({"message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        fields = self.request.query_params.getlist('fields', '')
        try:

            if fields == '':
            
                serialized = IdentificationDocumentResponseSerializer(instance=queryset, many=True)
            else:
                serialized = IdentificationDocumentResponseSerializer(instance=queryset, many=True, fields=fields)

        except:

            return Response(
                {"message": "Serializer error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={200: IdentificationDocumentResponseSerializer})
    @action(detail=True, methods=["get"], url_path="read")
    def read_identification_document(self, request, pk):

        try:
            queryset = IdentificationDocument.objects.get(id=pk)
        except:
            return Response({"message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        fields = self.request.query_params.getlist('fields', '')
        try:

            if fields == '':
            
                serialized = IdentificationDocumentResponseSerializer(instance=queryset)
            else:
                serialized = IdentificationDocumentResponseSerializer(instance=queryset, fields=fields)

        except:

            return Response(
                {"message": "Serializer error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["patch"], url_path="update")
    @swagger_auto_schema(
        request_body=IdentificationDocumentRequestSerializer,
        responses={200: IdentificationDocumentRequestSerializer},
    )
    def update_identification_documents(self, request):

        try:
            identificationdoc = request.data["id"]

        except:

            return Response(
                {"message": "Request body incorrect. Please specify  ID."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        queryset = IdentificationDocument.objects.get(id=identificationdoc)

        serialized = IdentificationDocumentRequestSerializer(
            queryset, request.data, partial=True
        )

        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"], url_path="read")
    @swagger_auto_schema(responses={200: IdentificationDocumentResponseSerializer})
    def read_identification_documents(self, request):

        try:
            queryset = IdentificationDocument.objects.all()
        except:
            return Response({"message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        fields = self.request.query_params.getlist('fields', '')
        try:

            if fields == '':
            
                serialized = IdentificationDocumentResponseSerializer(instance=queryset, many=True)
            else:
                serialized = IdentificationDocumentResponseSerializer(instance=queryset, many=True, fields=fields)

        except:

            return Response(
                {"message": "Serializer error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="create")
    @swagger_auto_schema(
        request_body=IdentificationDocumentRequestSerializer,
        responses={200: IdentificationDocumentRequestSerializer},
    )
    
    def create_identification_documents(self, request):


        serialized = IdentificationDocumentRequestSerializer(data=request.data, many = True) #changed
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["delete"], url_path="delete")
    @swagger_auto_schema(
        request_body=IdentificationDocumentListSerializer,
        responses={200: IdentificationDocumentListSerializer},
    )
    def delete_identification_documents(self, request):

        serialized = IdentificationDocumentListSerializer(data=request.data)

        if serialized.is_valid():
            IdentificationDocument.objects.filter(
                id__in=request.data["identificationdocument_ids"]
            ).update(status = 'Hidden')

            return Response(data=request.data, status=status.HTTP_200_OK)
        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class IdentificationTypeViewSet(viewsets.ViewSet):
    @swagger_auto_schema(responses={200: IdentificationTypeResponseSerializer})
    @action(detail=True, methods=["get"], url_path="read")
    def read_identification_type(self, request, pk):

        try:
            queryset = IdentificationType.objects.get(id=pk)
        except:
            return Response({"message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        fields = self.request.query_params.getlist('fields', '')
        try:

            if fields == '':
            
                serialized = IdentificationTypeResponseSerializer(instance=queryset)
            else:
                serialized = IdentificationTypeResponseSerializer(instance=queryset, fields=fields)

        except:

            return Response(
                {"message": "Serializer error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["patch"], url_path="update")
    @swagger_auto_schema(
        request_body=IdentificationTypeRequestSerializer,
        responses={200: IdentificationTypeRequestSerializer},
    )
    def update_identification_types(self, request):

        try:
            designation = request.data["designation_id"]

        except:

            return Response(
                {"message": "Request body incorrect. Please specify  ID."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        queryset = IdentificationType.objects.get(id=designation)

        serialized = IdentificationTypeRequestSerializer(queryset, request.data, partial=True)

        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"], url_path="read")
    @swagger_auto_schema(responses={200: IdentificationTypeResponseSerializer})
    def read_identification_types(self, request):

        try:
            queryset = IdentificationType.objects.all()
        except:
            return Response({"message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        fields = self.request.query_params.getlist('fields', '')
        try:

            if fields == '':
            
                serialized = IdentificationTypeResponseSerializer(instance=queryset, many=True)
            else:
                serialized = IdentificationTypeResponseSerializer(instance=queryset, many=True, fields=fields)

        except:

            return Response(
                {"message": "Serializer error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="create")
    @swagger_auto_schema(
        request_body=IdentificationTypeRequestSerializer,
        responses={200: IdentificationTypeRequestSerializer},
    )
    def create_identification_types(self, request):

        serialized = IdentificationTypeRequestSerializer(data=request.data, many=True)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["delete"], url_path="delete")
    @swagger_auto_schema(
        request_body=IdentificationTypeListSerializer,
        responses={200: IdentificationTypeListSerializer},
    )
    def delete_identificationtypes(self, request):

        serialized = IdentificationTypeListSerializer(data=request.data)

        if serialized.is_valid():
            IdentificationType.objects.filter(
                id__in=request.data["identificationtype_ids"]
            ).update(status = 'Hidden')

            return Response(data=request.data, status=status.HTTP_200_OK)
        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)


# LORAN
class AttendanceViewSet(viewsets.ViewSet):
    @swagger_auto_schema(responses={200: AttendanceSerializer})
    @action(detail=True, methods=["get"], url_path="read")
    def read_attendance(self, request, pk):

        try:
            queryset = Attendance.objects.get(id=pk)
        except:
            return Response({"message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        try:
            serialized = AttendanceSerializer(instance=queryset)
        except:
            return Response(
                {"message": "Serializer error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], url_path="department")
    @swagger_auto_schema(responses={200: AttendanceSerializer})
    def read_department_attendances(self, request, pk):
        dep_id = pk

        try:

            start_date_req = request.GET.get("start_date")
            end_date_req = request.GET.get("end_date")
            queryset = Attendance.objects.filter(
                fk_employee__department=dep_id,
                attendance_date__range=[start_date_req, end_date_req],
            )
            serialized = AttendanceSerializer(instance=queryset, many=True)
            return Response(data=serialized.data, status=status.HTTP_200_OK)
        except:
            return Response(
                {"message": "Enter start date and end date"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=True, methods=["get"], url_path="company")
    @swagger_auto_schema(responses={200: AttendanceSerializer})
    def read_company_attendances(self, request, pk):
        dep_id = pk

        try:

            start_date_req = request.GET.get("start_date")
            end_date_req = request.GET.get("end_date")
            queryset = Attendance.objects.filter(
                fk_employee__company=dep_id,
                attendance_date__range=[start_date_req, end_date_req],
            )
            serialized = AttendanceSerializer(instance=queryset, many=True)
            return Response(data=serialized.data, status=status.HTTP_200_OK)
        except:
            return Response(
                {"message": "Enter start date and end date"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=True, methods=["get"], url_path="employee")
    def read_employee_attendances(self, request, pk):

        id = pk

        try:
            start_date_req = request.GET.get("start_date")
            end_date_req = request.GET.get("end_date")
            queryset = Attendance.objects.filter(
                id=id, attendance_date__range=[start_date_req, end_date_req]
            )
            serialized = AttendanceSerializer(instance=queryset, many=True)
            return Response(data=serialized.data, status=status.HTTP_200_OK)
        except:
            return Response(
                {"message": "Enter start date and end date"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=False, methods=["get"], url_path="read")
    def read_all_attendances(self, request):

        queryset = Attendance.objects.all()
        serialized = AttendanceSerializer(instance=queryset, many=True)
        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="create")
    @swagger_auto_schema(
        request_body=AttendanceSerializer, responses={200: AttendanceSerializer}
    )
    def create_attendances(self, request):

        serialized = AttendanceSerializer(data=request.data, many = True) #changed
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["delete"], url_path="delete")
    @swagger_auto_schema(
        request_body=AttendanceListSerializer,
        responses={200: AttendanceListSerializer},
    )
    def delete_attendances(self, request):

        serialized = AttendanceListSerializer(data=request.data)

        if serialized.is_valid():

            Attendance.objects.filter(id__in=request.data["attendance_ids"]).update(status = 'Hidden')

            return Response(data=request.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeSessionViewSet(viewsets.ViewSet):
    @swagger_auto_schema(responses={200: EmployeeSessionResponseSerializer})
    @action(detail=True, methods=["get"], url_path="read")
    def read_employee_session(self, request, pk):

        try:
            queryset = EmployeeSession.objects.get(id=pk)
        except:
            return Response({"message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        fields = self.request.query_params.getlist('fields', '')
        try:

            if fields == '':
            
                serialized = EmployeeSessionResponseSerializer(instance=queryset)
            else:
                serialized = EmployeeSessionResponseSerializer(instance=queryset, fields=fields)

        except:

            return Response(
                {"message": "Serializer error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="create_employee_checkin")
    @swagger_auto_schema(
        request_body=EmployeeSessionCheckinSerializer,
        responses={200: EmployeeSessionCheckinSerializer},
    )
    def create_employee_checkin(self, request):
        try:
            employee_id = request.data["fk_employee"]
            checked_in = request.data["checked_in_at"]
            # is_first_session = request.data["is_first_session"]
        except:
            return Response(
                {"message": "Request Body incorrect"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        employee = Employee.objects.get(id=employee_id)

        date = datetime.datetime.strptime(checked_in, "%Y-%m-%dT%H:%M:%S")
        try:
            attendance = Attendance.objects.get(
                attendance_date=date, fk_employee=employee_id
            )
        except Attendance.DoesNotExist:

            session = EmployeeSession(
                checked_in_at=request.data["checked_in_at"],
                fk_employee=employee,
                # is_first_session=is_first_session,
            )
            session.save()
            attendance = Attendance(fk_employee=employee, attendance_date=date)
            attendance.save()
            attendance.fk_sessions.add(session)
            attendance.save()
            return Response(status=status.HTTP_200_OK)

        serialized = EmployeeSessionCheckinSerializer(data=request.data)

        if serialized.is_valid():
            try:
                check = EmployeeSession.objects.filter(fk_employee=employee_id).latest(
                    "checked_in_at"
                )
            except EmployeeSession.DoesNotExist:

                serialized.save()
                e = EmployeeSession.objects.latest("checked_in_at")
                attendance.fk_sessions.add(e)

                return Response(data=serialized.data, status=status.HTTP_200_OK)

            if check.checked_out_at is not None:
                serialized.save()
                e = EmployeeSession.objects.latest("checked_in_at")
                attendance.fk_sessions.add(e)
                return Response(data=serialized.data, status=status.HTTP_200_OK)
            else:

                return Response(
                    {"message": "Check out of existing session"},
                    status=status.HTTP_200_OK,
                )

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], url_path="create_employee_checkout")
    @swagger_auto_schema(
        request_body=EmployeeSessionCheckoutSerializer,
        responses={200: EmployeeSessionCheckoutSerializer},
    )
    def create_employee_checkout(self, request):

        try:
            employee_id = request.data["fk_employee"]
            checked_out = request.data["checked_out_at"]
            # is_last_session = request.data["is_last_session"]
        except:
            return Response(
                {"message": "Request Body incorrect"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:

            session = EmployeeSession.objects.filter(fk_employee=employee_id).latest(
                "checked_in_at"
            )

        except EmployeeSession.DoesNotExist:

            return Response({"message": "No checkin for the employee found"})

        if session.checked_out_at is None:

            checked_in_date = datetime.datetime.strptime(
                checked_out, "%Y-%m-%dT%H:%M:%S"
            )
            print("787")
            checked_out_date = datetime.datetime.strptime(
                checked_out, "%Y-%m-%dT%H:%M:%S"
            )
            print("792")
            if (checked_out_date.day) > (session.checked_in_at.day):

                bridgetime = datetime.datetime(
                    checked_out_date.year,
                    checked_out_date.month,
                    checked_out_date.day,
                    0,
                    0,
                    0,
                )
                print("797")

                session.checked_out_at = bridgetime

                session.save()

                autosession = EmployeeSession(
                    fk_employee=session.fk_employee,
                    checked_in_at=bridgetime,
                    checked_out_at=checked_out_date,
                )

                autosession.save()

            else:

                session.checked_out_at = checked_out
                session.save()

            # e.checked_out_time = checked_out
            # e.total_time_elapsed = 8  # TODO do this using TIME DELTA
            # e.is_last_session = is_last_session

            # e.save()

            # if is_last_session:

            #     date = e.checked_in_time.date()

            #     employee = Employee.objects.get(id=employee_id)
            #     workhours = employee.fk_designation.fk_schedule.total_work_hours
            #     a = Attendance.objects.get(
            #         attendance_date=date, fk_employee=employee_id
            #     )

            #     time_worked = EmployeeSession.objects.filter(
            #         checked_in_at__date=date
            #     ).aggregate(Sum("total_time_elapsed"))
            #     print(time_worked)

            #     a.total_time = time_worked[
            #         "total_time_elapsed__sum"
            #     ]  # change variable name to time_elapsed_in_hours
            #     ot = time_worked["total_time_elapsed__sum"] - workhours

            #     if ot > 0:

            #         a.total_overtime = ot

            #     a.save()

            return Response(status=status.HTTP_200_OK)
        else:

            return Response(
                {"message": "Already checked out of existing session"},
                status=status.HTTP_200_OK,
            )

    @action(detail=False, methods=["get"], url_path="read")
    @swagger_auto_schema(responses={200: EmployeeSessionResponseSerializer})
    def read_employee_sessions(self, request, pk):

        queryset = EmployeeSession.objects.filter(fk_employee = pk)
        fields = self.request.query_params.getlist('fields', '')
        try:

            if fields == '':
            
                serialized = EmployeeSessionResponseSerializer(instance=queryset, many=True)
            else:
                serialized = EmployeeSessionResponseSerializer(instance=queryset, many=True, fields=fields)

        except:

            return Response(
                {"message": "Serializer error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="create")
    @swagger_auto_schema(
        request_body=EmployeeSessionRequestSerializer,
        responses={200: EmployeeSessionRequestSerializer},
    )
    def create_employee_sessions(self, request):

        serialized = EmployeeSessionRequestSerializer(data=request.data, many=True)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["delete"], url_path="delete")
    @swagger_auto_schema(
        request_body=EmployeeSessionListSerializer,
        responses={200: EmployeeSessionListSerializer},
    )
    def delete_employee_sessions(self, request):

        serialized = EmployeeSessionListSerializer(data=request.data)

        if serialized.is_valid():

            EmployeeSession.objects.filter(
                id__in=request.data["attendance_ids"]
            ).update(status = 'Hidden')

            return Response(data=request.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)


######################################################## Leave Viewsets #################################


class LeavePolicyViewSet(viewsets.ViewSet):
    @swagger_auto_schema(responses={200: LeavePolicySerializer})
    @action(detail=True, methods=["get"], url_path="read")
    def read_leave_policy(self, request, pk):

        try:
            queryset = LeavePolicy.objects.get(id=pk)
        except:
            return Response({"message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        try:
            serialized = LeavePolicySerializer(instance=queryset)
        except:
            return Response(
                {"message": "Serializer error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="leave_policy_generation")
    @swagger_auto_schema(
        request_body=LeavePolicyTypeMembershipSerializer,
        responses={200: LeavePolicyTypeMembershipSerializer},
    )
    def leave_policy_generation(self, request, pk):

        des_id = pk

        try:
            designation = Designation.objects.get(id=des_id)
        except:
            return Response(
                {"message": "No designation found"}, status=status.HTTP_400_BAD_REQUEST
            )
        if designation.fk_leave_policy is None:

            leave_policy = LeavePolicy()
            leave_policy.save()
            designation.fk_leave_policy = leave_policy
            designation.save()
            # leave_policy_id = leave_policy.leavepolicy_id
            for member in request.data:
                member["fk_leave_policy"] = leave_policy.id
            serialized = LeavePolicyTypeMembershipSerializer(
                data=request.data, many=True
            )
            if serialized.is_valid():
                serialized.save()
                return Response(data=serialized.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    data=serialized.errors, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {"message": "Leave Policy already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=False, methods=["patch"], url_path="update")
    @swagger_auto_schema(
        request_body=LeavePolicySerializer, responses={200: LeavePolicySerializer}
    )
    def update_leave_policies(self, request):

        try:
            leavepolicy = request.data["id"]

        except:

            return Response(
                {"message": "Request body incorrect. Please specify  ID."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        queryset = LeavePolicy.objects.get(id=leavepolicy)

        serialized = LeavePolicySerializer(queryset, request.data, partial=True)

        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"], url_path="read")
    @swagger_auto_schema(responses={200: LeavePolicySerializer})
    def read_leave_policies(self, request):

        try:
            queryset = LeavePolicy.objects.all()
        except:
            return Response({"message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        serialized = LeavePolicySerializer(instance=queryset, many=True)

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="create")
    @swagger_auto_schema(
        request_body=LeavePolicySerializer, responses={200: LeavePolicySerializer}
    )
    def create_leave_policies(self, request):

        serialized = LeavePolicySerializer(data=request.data, many=True)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["delete"], url_path="delete")
    @swagger_auto_schema(
        request_body=LeavePolicyListSerializer,
        responses={200: LeavePolicyListSerializer},
    )
    def delete_leave_policies(self, request):

        serialized = LeavePolicyListSerializer(data=request.data)

        if serialized.is_valid():

            LeavePolicy.objects.filter(id__in=request.data["leavepolicy_ids"]).update(status = 'Hidden')

            return Response(data=request.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)


# LORAN
class LeaveApplicationViewSet(viewsets.ViewSet):
    @swagger_auto_schema(responses={200: LeaveApplicationResponseSerializer})
    @action(detail=True, methods=["get"], url_path="read")
    def read_leave_application(self, request, pk):

        try:
            queryset = LeaveApplication.objects.get(id=pk)
        except:
            return Response({"message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        fields = self.request.query_params.getlist('fields', '')
        try:

            if fields == '':
            
                serialized = LeaveApplicationResponseSerializer(instance=queryset)
            else:
                serialized = LeaveApplicationResponseSerializer(instance=queryset, fields=fields)

        except:

            return Response(
                {"message": "Serializer error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="accept_applications")
    def accept_applications(self, request):
        try:
            accepted_ids = request.data["accepted_ids"]
        except:
            return Response({"message": "specify accepted ids"})

        try:
            LeaveApplication.objects.filter(id__in=accepted_ids).update(
                status="Approved"
            )

        except ValueError:
            print(ValueError)
            return Response(
                {"message": "Bad request, check body"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        leave_applications = LeaveApplication.objects.filter(id__in=accepted_ids)
        for app_id in accepted_ids:

            leave_application = leave_applications.get(app_id = app_id)
            leave_report = LeaveReportTypeMembership.objects.filter(fk_employee = leave_application.fk_employee)
            leave_details = LeaveReportTypeMembership.objects.get(fk_employee_report = leave_report.id)

            leave = Leave(
                fk_employee=leave_application.fk_employee,
                fk_leave_type=leave_application.fk_leave_type,
                from_date=leave_application.from_date,
                to_date=leave_application.to_date,
            )
            leave.save()
            
            leave_days = (leave_application.to_date - leave_application.from_date).days + 1 #USE TIME DELTA
            leave_details.leaves_remaining = leave_details.leaves_remaining - leave_days
            leave_details.leaves_taken = leave_details.leaves_taken + leave_days
            leave_details.save()



            # leaves = LeaveApplicationTypeMembership.objects.filter(
            #     fk_leave_application=app_id
            # )

            # for leave in leaves:

            #     leave = Leave(
            #         fk_employee=leave.fk_leave_application.fk_employee,
            #         fk_leave_type=leave.fk_leave_type,
            #         from_date=leave.from_date,
            #         to_date=leave.to_date,
            #     )
            #     leave.save()

        return Response(data=request.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="reject_applications")
    def reject_applications(self, request):
        try:
            rejected_ids = request.data["rejected_ids"]
        except:
            return Response({"message": "specify rejected ids"})

        try:
            LeaveApplication.objects.filter(id__in=rejected_ids).update(
                status="Rejected"
            )

            return Response(data=request.data)
        except ValueError:
            print(ValueError)
            return Response(
                {"message": "Bad request, check body"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=True, methods=["get"], url_path="read_employee_applications")
    def read_leave_applications_employee(self, request, pk):

        queryset = LeaveApplication.objects.filter(fk_employee=pk)
        fields = self.request.query_params.getlist('fields', '')
        try:

            if fields == '':
            
                serialized = LeaveApplicationResponseSerializer(instance=queryset, many=True)
            else:
                serialized = LeaveApplicationResponseSerializer(instance=queryset, many=True, fields=fields)

        except:

            return Response(
                {"message": "Serializer error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], url_path="read_department_applications")
    def read_leave_applications_department(self, request, pk):

        queryset = LeaveApplication.objects.filter(fk_employee__fk_department=pk)
        fields = self.request.query_params.getlist('fields', '')
        try:

            if fields == '':
            
                serialized = LeaveApplicationResponseSerializer(instance=queryset, many=True)
            else:
                serialized = LeaveApplicationResponseSerializer(instance=queryset, many=True, fields=fields)

        except:

            return Response(
                {"message": "Serializer error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["patch"], url_path="update")
    @swagger_auto_schema(
        request_body=LeaveApplicationRequestSerializer,
        responses={200: LeaveApplicationRequestSerializer},
    )
    def update_leave_applications(self, request):

        try:
            leaveapplication = request.data["leaveapplication_id"]

        except:

            return Response(
                {"message": "Request body incorrect. Please specify  ID."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        queryset = LeaveApplication.objects.get(id=leaveapplication)

        serialized = LeaveApplicationRequestSerializer(queryset, request.data, partial=True)

        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"], url_path="read")
    @swagger_auto_schema(responses={200: LeaveApplicationResponseSerializer})
    def read_leave_applications(self, request):

        try:
            queryset = LeaveApplication.objects.all()
        except:
            return Response({"message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        fields = self.request.query_params.getlist('fields', '')
        try:

            if fields == '':
            
                serialized = LeaveApplicationResponseSerializer(instance=queryset, many=True)
            else:
                serialized = LeaveApplicationResponseSerializer(instance=queryset, many=True, fields=fields)

        except:

            return Response(
                {"message": "Serializer error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="create")
    @swagger_auto_schema(
        request_body=CreateLeaveApplicationSerializer,
        responses={200: CreateLeaveApplicationSerializer},
    )
    def create_leave_applications(self, request):

        serialized = CreateLeaveApplicationSerializer(data=request.data)
        if serialized.is_valid():
            employee_leave_report = EmployeeLeaveReport.objects.get(fk_employee = request.data['fk_employee'])
            is_valid = True
            leave_details = LeaveReportTypeMembership.objects.filter(fk_employee_report = employee_leave_report.id, fk_leave_type = request.data['fk_leave_type'])
            to_date = datetime.datetime.strptime(request.data['to_date'], "%Y-%m-%d")
            from_date = datetime.datetime.strptime(request.data['from_date'], "%Y-%m-%d")
            leave_days = (to_date - from_date).days + 1
            allowed_days = leave_details.leaves_remaining
            consecutive_days = leave_details.consecutive_days_allowed

            if leave_days > allowed_days or leave_days > consecutive_days:
                    
                    is_valid = False

            if is_valid:
                serialized.save()    


            # employee_leave_report = EmployeeLeaveReport.objects.get(fk_employee = request.data['fk_employee'])
            # leaves = request.data['fk_leave_types'].copy()
            # print(leaves)
            # total_days = 0
            # is_valid = True
            # leave_details = LeaveReportTypeMembership.objects.filter(fk_employee_report = employee_leave_report.id)
            # for leave in leaves:

                
                # to_date = datetime.datetime.strptime(leave['to_date'], "%Y-%m-%d")
                # from_date = datetime.datetime.strptime(leave['from_date'], "%Y-%m-%d")
            #     print(to_date, from_date)
            #     leave_days = (to_date - from_date).days + 1 #USE TIME DELTA
            #     total_days+=leave_days
            #     leave_obj = leave_details.get(fk_leave_type = leave['fk_leave_type'])
            #     allowed_days = leave_obj.leaves_remaining
            #     print("allowed days", allowed_days)
            #     print("leave_days", leave_days)
            #     consecutive_days = leave_obj.consecutive_days_allowed
            #     if leave_days > allowed_days or leave_days > consecutive_days:
                    
            #         is_valid = False


                    
                    
            # net_days = (datetime.datetime.strptime(request.data['to_date'], "%Y-%m-%d"))-(datetime.datetime.strptime(request.data['from_date'], "%Y-%m-%d")) 
            # if total_days > (net_days.days + 1):
            #     print("total_days_mismatch")
            #     is_valid = False


            # if is_valid:
            #     serialized.save()
            #     for leave in leaves:

            #         leave_report_obj = leave_details.get(fk_leave_type = leave['fk_leave_type'])

            #         to_date = datetime.datetime.strptime(leave['to_date'], "%Y-%m-%d")
            #         from_date = datetime.datetime.strptime(leave['from_date'], "%Y-%m-%d")
                    
            #         leave_days = (to_date - from_date).days + 1 #USE TIME DELTA
            #         leave_report_obj.leaves_remaining = leave_report_obj.leaves_remaining - leave_days
            #         leave_report_obj.leaves_taken = leave_report_obj.leaves_taken + leave_days
            #         leave_report_obj.save()
            #     return Response(data=request.data, status=status.HTTP_200_OK)

            else:

                return Response({"message" : "Leave durations not valid, please enter valid leaves"}, status=status.HTTP_400_BAD_REQUEST)

            

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["delete"], url_path="delete")
    @swagger_auto_schema(
        request_body=LeaveApplicationListSerializer,
        responses={200: LeaveApplicationListSerializer},
    )
    def delete_leave_applications(self, request):

        serialized = LeaveApplicationListSerializer(data=request.data)

        if serialized.is_valid():

            LeaveApplication.objects.filter(
                id__in=request.data["leaveapplication_ids"]
            ).update(status = 'Hidden')

            return Response(data=request.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class LeaveViewSet(viewsets.ViewSet):

    @action(detail=True, methods=["get"], url_path="read_employee_leaves")
    def read_leaves_employee(self, request, pk):

        try:

            start_date_req = request.GET.get("start_date")
            end_date_req = request.GET.get("end_date")
            queryset = Leave.objects.filter(
                Q(from_date__range=[start_date_req, end_date_req], fk_employee=pk)
                | Q(to_date__range=[start_date_req, end_date_req], fk_employee=pk)
                | Q(Q(from_date__lte=start_date_req) & Q(to_date__gte=end_date_req))
            )
            fields = self.request.query_params.getlist('fields', '')
            try:

                if fields == '':
                
                    serialized = LeaveResponseSerializer(instance=queryset, many=True)
                else:
                    serialized = LeaveResponseSerializer(instance=queryset, many=True, fields=fields)

            except:

                return Response(
                    {"message": "Serializer error"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
            return Response(data=serialized.data, status=status.HTTP_200_OK)
        except:
            return Response(
                {"message": "Enter start date and end date"},
                status=status.HTTP_400_BAD_REQUEST,
            )


    @swagger_auto_schema(responses={200: LeaveResponseSerializer})
    @action(detail=True, methods=["get"], url_path="read")
    def read_leave(self, request, pk):

        try:
            queryset = Leave.objects.get(id=pk)
        except:
            return Response({"message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        fields = self.request.query_params.getlist('fields', '')
        try:

            if fields == '':
            
                serialized = LeaveResponseSerializer(instance=queryset)
            else:
                serialized = LeaveResponseSerializer(instance=queryset, fields=fields)

        except:

            return Response(
                {"message": "Serializer error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    

    @action(detail=False, methods=["patch"], url_path="update")
    @swagger_auto_schema(request_body=LeaveRequestSerializer, responses={200: LeaveRequestSerializer})
    def update_leaves(self, request):

        try:
            leave = request.data["leave_id"]

        except:

            return Response(
                {"message": "Request body incorrect. Please specify  ID."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        queryset = Leave.objects.get(leave_id=leave)

        serialized = LeaveRequestSerializer(queryset, request.data, partial=True)

        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"], url_path="read")
    @swagger_auto_schema(responses={200: LeaveResponseSerializer})
    def read_leaves(self, request):

        try:
            queryset = Leave.objects.all()
        except:
            return Response({"message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        fields = self.request.query_params.getlist('fields', '')
        try:

            if fields == '':
            
                serialized = LeaveResponseSerializer(instance=queryset, many=True)
            else:
                serialized = LeaveResponseSerializer(instance=queryset, many=True, fields=fields)

        except:

            return Response(
                {"message": "Serializer error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="create")
    @swagger_auto_schema(request_body=LeaveRequestSerializer, responses={200: LeaveRequestSerializer})
    def create_leaves(self, request):

        serialized = LeaveRequestSerializer(data=request.data, many=True)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["delete"], url_path="delete")
    @swagger_auto_schema(
        request_body=LeaveListSerializer, responses={200: LeaveListSerializer}
    )
    def delete_leaves(self, request):

        serialized = LeaveListSerializer(data=request.data)

        if serialized.is_valid():

            Leave.objects.filter(id__in=request.data["leave_ids"]).update(status = 'Hidden')

            return Response(data=request.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeLeaveReportViewSet(viewsets.ViewSet):
    @action(detail=True, methods=["post"], url_path="create_employee_leave_report")
    def create_employee_leave_report(self, request, pk):

        try:

            employee = Employee.objects.get(id=pk)
            leave_policy_id = employee.fk_designation.fk_leave_policy
            leave_policies = LeavePolicyTypeMembership.objects.filter(
                fk_leave_policy=leave_policy_id
            )
        except:

            return Response(
                {"message": "Serializer error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        if employee.fk_leave_report:

            return Response(
                {"message": "Report already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        else:

            leave_report = EmployeeLeaveReport(fk_employee=employee)
            leave_report.save()
            for policy in leave_policies:
                # leave_type = Leavetype.objects.get(id = policy.fk_leave_type)
                leave_record = LeaveReportTypeMembership(
                    fk_employee_report=leave_report,
                    fk_leave_type=policy.fk_leave_type,
                    leaves_taken=0,
                    leaves_remaining=policy.total_days_allowed,
                    consecutive_days_allowed = policy.consecutive_days_allowed,
                )
                leave_record.save()

            # employee.fk_leave_report = leave_report.id

            return Response({"message": "Successful"}, status=status.HTTP_200_OK)

    # Yearly basis report
    # Change it on designation change

    @swagger_auto_schema(responses={200: EmployeeLeaveReportSerializer})
    @action(detail=True, methods=["get"], url_path="read")
    def read_employee_leave_report(self, request, pk):

        try:
            queryset = EmployeeLeaveReport.objects.get(id=pk)
        except:
            return Response({"message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        try:
            serialized = EmployeeLeaveReportSerializer(instance=queryset)
        except:
            return Response(
                {"message": "Serializer error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={200: EmployeeLeaveReportSerializer})
    @action(detail=False, methods=["get"], url_path="read")
    def read_employee_leave_reports(self, request):

        try:
            queryset = EmployeeLeaveReport.objects.all()
        except:
            return Response({"message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        try:
            serialized = EmployeeLeaveReportSerializer(instance=queryset, many=True)
        except:
            return Response(
                {"message": "Serializer error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=EmployeeLeaveReportSerializer,
        responses={200: EmployeeLeaveReportSerializer},
    )
    @action(detail=False, methods=["patch"], url_path="update")
    def update_employee_leave_reports(self, request):

        try:
            EmployeeLeaveReport = request.data["id"]

        except:

            return Response(
                {"message": "Request body incorrect. Please specify ID."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        queryset = EmployeeLeaveReport.objects.get(id=EmployeeLeaveReport)

        serialized = EmployeeLeaveReportSerializer(queryset, request.data, partial=True)

        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], url_path="create")
    @swagger_auto_schema(
        request_body=EmployeeLeaveReportSerializer,
        responses={200: EmployeeLeaveReportSerializer},
    )
    def create_employee_leave_reports(self, request):

        serialized = EmployeeLeaveReportSerializer(data=request.data, many=True)

        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["delete"], url_path="delete")
    @swagger_auto_schema(
        request_body=EmployeeLeaveReportListSerializer,
        responses={200: EmployeeLeaveReportListSerializer},
    )
    def delete_employee_leave_reports(self, request):

        serialized = EmployeeLeaveReportListSerializer(data=request.data)

        if serialized.is_valid():
            EmployeeLeaveReport.objects.filter(
                id__in=request.data["employee_leave_report_ids"]
            ).update(status = 'Hidden')

            return Response(data=request.data, status=status.HTTP_200_OK)
        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class ScheduleViewSet(viewsets.ViewSet):
    @swagger_auto_schema(responses={200: ScheduleResponseSerializer})
    @action(detail=True, methods=["get"], url_path="read")
    def read_schedule(self, request, pk):

        try:
            queryset = Schedule.objects.get(id=pk)
        except:
            return Response({"message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        fields = self.request.query_params.getlist('fields', '')
        try:

            if fields == '':
            
                serialized = ScheduleResponseSerializer(instance=queryset)
            else:
                serialized = ScheduleResponseSerializer(instance=queryset, fields=fields)

        except:

            return Response(
                {"message": "Serializer error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["patch"], url_path="update")
    @swagger_auto_schema(
        request_body=ScheduleRequestSerializer, responses={200: ScheduleRequestSerializer}
    )
    def update_schedules(self, request):

        try:
            schedule = request.data["id"]

        except:

            return Response(
                {"message": "Request body incorrect. Please specify  ID."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        queryset = Schedule.objects.get(id=schedule)

        serialized = ScheduleRequestSerializer(queryset, request.data, partial=True)

        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"], url_path="read")
    @swagger_auto_schema(responses={200: ScheduleResponseSerializer})
    def read_schedules(self, request):

        try:
            queryset = Schedule.objects.all()
        except:
            return Response({"message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        fields = self.request.query_params.getlist('fields', '')
        try:

            if fields == '':
            
                serialized = ScheduleResponseSerializer(instance=queryset, many=True)
            else:
                serialized = ScheduleResponseSerializer(instance=queryset, many=True, fields=fields)

        except:

            return Response(
                {"message": "Serializer error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="create")
    @swagger_auto_schema(
        request_body=ScheduleRequestSerializer, responses={200: ScheduleRequestSerializer}
    )
    def create_schedules(self, request, des_id):

        designation_id = des_id

        try:

            designation = Designation.objects.get(id=designation_id)

        except Designation.DoesNotExist:

            return Response(
                {{"message": "No designation found"}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serialized = ScheduleRequestSerializer(data=request.data)

        if serialized.is_valid():
            print(serialized.data)
            schedule = Schedule(**serialized.data)
            schedule.save()
            designation.schedule = schedule
            designation.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["delete"], url_path="delete")
    @swagger_auto_schema(
        request_body=ScheduleListSerializer, responses={200: ScheduleListSerializer}
    )
    def delete_schedules(self, request):

        serialized = ScheduleListSerializer(data=request.data)

        if serialized.is_valid():

            Schedule.objects.filter(id__in=request.data["schedule_ids"]).update(status = 'Hidden')

            return Response(data=request.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkdayDivisionViewSet(viewsets.ViewSet):
    @swagger_auto_schema(responses={200: WorkdayDivisionResponseSerializer})
    @action(detail=True, methods=["get"], url_path="read")
    def read_workday_division(self, request, pk):

        try:
            queryset = WorkdayDivision.objects.get(id=pk)
        except:
            return Response({"message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        fields = self.request.query_params.getlist('fields', '')
        try:

            if fields == '':
            
                serialized = WorkdayDivisionResponseSerializer(instance=queryset)
            else:
                serialized = WorkdayDivisionResponseSerializer(instance=queryset, fields=fields)

        except:

            return Response(
                {"message": "Serializer error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["patch"], url_path="update")
    @swagger_auto_schema(
        request_body=WorkdayDivisionRequestSerializer,
        responses={200: WorkdayDivisionRequestSerializer},
    )
    def update_workday_divisons(self, request):

        try:
            leave = request.data["leave_id"]

        except:

            return Response(
                {"message": "Request body incorrect. Please specify  ID."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        queryset = WorkdayDivision.objects.get(leave_id=leave)

        serialized = WorkdayDivisionRequestSerializer(queryset, request.data, partial=True)

        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"], url_path="read")
    @swagger_auto_schema(responses={200: WorkdayDivisionResponseSerializer})
    def read_workday_divisons(self, request):

        try:
            queryset = WorkdayDivision.objects.all()
        except:
            return Response({"message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        fields = self.request.query_params.getlist('fields', '')
        try:

            if fields == '':
            
                serialized = WorkdayDivisionResponseSerializer(instance=queryset, many=True)
            else:
                serialized = WorkdayDivisionResponseSerializer(instance=queryset, many=True, fields=fields)

        except:

            return Response(
                {"message": "Serializer error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="create")
    @swagger_auto_schema(
        request_body=WorkdayDivisionRequestSerializer,
        responses={200: WorkdayDivisionRequestSerializer},
    )
    def create_workday_divisons(self, request):

        serialized = WorkdayDivisionRequestSerializer(data=request.data, many=True)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["delete"], url_path="delete")
    @swagger_auto_schema(
        request_body=WorkdayDivisionListSerializer,
        responses={200: WorkdayDivisionListSerializer},
    )
    def delete_workday_divisions(self, request):

        serialized = WorkdayDivisionListSerializer(data=request.data)

        if serialized.is_valid():

            WorkdayDivision.objects.filter(id__in=request.data["leave_ids"]).update(status = 'Hidden')

            return Response(data=request.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class DaysListViewSet(viewsets.ViewSet):
    @swagger_auto_schema(responses={200: DaysListResponseSerializer})
    @action(detail=True, methods=["get"], url_path="read")
    def read_day_list(self, request, pk):

        try:
            queryset = DaysList.objects.get(id=pk)
        except:
            return Response({"message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        fields = self.request.query_params.getlist('fields', '')
        try:

            if fields == '':
            
                serialized = DaysListResponseSerializer(instance=queryset)
            else:
                serialized = DaysListResponseSerializer(instance=queryset, fields=fields)

        except:

            return Response(
                {"message": "Serializer error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["patch"], url_path="update")
    @swagger_auto_schema(
        request_body=DaysListRequestSerializer, responses={200: DaysListRequestSerializer}
    )
    def update_days_lists(self, request):

        try:
            leave = request.data["id"]

        except:

            return Response(
                {"message": "Request body incorrect. Please specify  ID."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        queryset = DaysList.objects.get(id=leave)

        serialized = DaysListRequestSerializer(queryset, request.data, partial=True)

        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"], url_path="read")
    @swagger_auto_schema(responses={200: DaysListResponseSerializer})
    def read_days_lists(self, request):

        try:
            queryset = DaysList.objects.all()
        except:
            return Response({"message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        fields = self.request.query_params.getlist('fields', '')
        try:

            if fields == '':
            
                serialized = DaysListResponseSerializer(instance=queryset, many=True)
            else:
                serialized = DaysListResponseSerializer(instance=queryset, many=True, fields=fields)

        except:

            return Response(
                {"message": "Serializer error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="create")
    @swagger_auto_schema(
        request_body=DaysListRequestSerializer, responses={200: DaysListRequestSerializer}
    )
    def create_days_lists(self, request):

        serialized = DaysListRequestSerializer(data=request.data, many=True)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["delete"], url_path="delete")
    @swagger_auto_schema(
        request_body=DaysListListSerializer, responses={200: DaysListListSerializer}
    )
    def delete_days_lists(self, request):

        serialized = DaysListListSerializer(data=request.data)

        if serialized.is_valid():

            DaysList.objects.filter(id__in=request.data["days_list_ids"]).update(status = 'Hidden')

            return Response(data=request.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)


# class MonthlyReportViewSet(viewsets.ViewSet):
#     def update_monthlyreports(self, request):

#         try:
#             monthlyreport = request.data["monthlyreport_id"]

#         except:

#             return Response({"message": "Request body incorrect. Please specify  ID."}, status=status.HTTP_400_BAD_REQUEST)

#         queryset = MonthlyReport.objects.get(monthlyreport_id=monthlyreport)

#         serialized = MonthlyReportSerializer(queryset, request.data, partial=True)

#         if serialized.is_valid():
#             serialized.save()
#             return Response(data=serialized.data, status=status.HTTP_200_OK)

#         return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

#     def read_monthly_reports(self, request):

#         try:
#             queryset = MonthlyReport.objects.all()
#         except:
#             return Response({"message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

#         serialized = MonthlyReportSerializer(queryset, many=True)
#         if serialized.is_valid():
#             serialized.save()
#             return Response(data=serialized.data, status=status.HTTP_200_OK)

#         return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

#     def create_monthly_reports(self, request):

#         serialized = MonthlyReportSerializer(data=request.data)
#         if serialized.is_valid():
#             serialized.save()
#             return Response(data=serialized.data, status=status.HTTP_200_OK)

#         return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete_monthly_reports(self, request):

#         MonthlyReport.objects.filter(id__in=request.data["monthlyreport_ids"]).update(status = 'Hidden')

#         return Response(data=request.data, status=status.HTTP_200_OK)

#     def generate_monthly_report(self, request, emp_id):

#         month = request.GET.get("month", date.today().month)
#         year = request.GET.get("year", date.today().year)
#         work_hours = Attendance.objects.filter(
#             employee=emp_id, attendance_date__month=month, attendance_date__year=year
#         ).aggregate(Sum("total_time"))
#         print(work_hours)
#         dt = {"employee": emp_id, "total_time_worked": work_hours["total_time__sum"]}
#         serialized = MonthlyReportSerializer(data=dt)

#         if serialized.is_valid():

#             serialized.save()

#             return Response(data=serialized.data, status=status.HTTP_200_OK)

#         else:

#             return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)


# class CalendarViewSet(viewsets.ViewSet):


#     def update_calendar(self, request):

#         try:
#             date = request.data["date"]
#         except:
#             return Response({"message" : "Request body incorrect. Please specify  ID."}, status = status.HTTP_400_BAD_REQUEST)
#         queryset = Calendar.objects.get(date=date)

#         serialized = CalendarSerializer(queryset, request.data, partial = True)

#         if serialized.is_valid():
#             serialized.save()
#             return Response(data=serialized.data, status= status.HTTP_200_OK)

#         return Response(data=serialized.errors, status= status.HTTP_200_OK)

#     @swagger_auto_schema(responses={200: CalendarSerializer})
#     def read_calendar(self, request):

#         try:
#             queryset = Calendar.objects.all()
#         except:
#             return Response({"message" : "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND )

#         serialized = CalendarSerializer(queryset, many = True)
#         if serialized.is_valid():
#             serialized.save()
#             return Response(data=serialized.data, status= status.HTTP_200_OK)

#         return Response(data=serialized.errors, status= status.HTTP_200_OK)

#     @swagger_auto_schema(request_body=CalendarSerializer,responses={200: CalendarSerializer})
#     def create_calendar(self, request):

#         serialized = CalendarSerializer(data = request.data)
#         if serialized.is_valid():
#             serialized.save()
#             return Response(data=serialized.data, status= status.HTTP_200_OK)

#         return Response(data=serialized.errors, status= status.HTTP_200_OK)

#     def delete_leave(self, request):

#         Calendar.objects.filter(date__in = request.data["dates"]).update(status = 'Hidden')

#         return Response(data=request.data, status= status.HTTP_200_OK)


# class EventsViewset(viewsets.ViewSet):


#     def update_events(self, request):

#         try:
#             event_id = request.data["event_id"]
#         except:
#             return Response({"message" : "Request body incorrect. Please specify  ID."}, status = status.HTTP_400_BAD_REQUEST)
#         queryset = Events.objects.get(event_id=event_id)

#         serialized = EventSerializer(queryset, request.data, partial = True)

#         if serialized.is_valid():
#             serialized.save()
#             return Response(data=serialized.data, status= status.HTTP_200_OK)

#         return Response(data=serialized.errors, status= status.HTTP_200_OK)

#     @swagger_auto_schema(responses={200: EventSerializer})
#     def read_events(self, request):

#         try:
#             queryset = Events.objects.all()
#         except:
#             return Response({"message" : "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND )

#         serialized = EventSerializer(queryset, many = True)
#         if serialized.is_valid():
#             serialized.save()
#             return Response(data=serialized.data, status= status.HTTP_200_OK)

#         return Response(data=serialized.errors, status= status.HTTP_200_OK)

#     @swagger_auto_schema(request_body=EventSerializer,responses={200: EventSerializer})
#     def create_events(self, request):

#         serialized = EventSerializer(data = request.data)
#         if serialized.is_valid():
#             serialized.save()
#             return Response(data=serialized.data, status= status.HTTP_200_OK)

#         return Response(data=serialized.errors, status= status.HTTP_200_OK)

#     def delete_events(self, request):

#         Events.objects.filter(event_id__in = request.data["event_ids"]).update(status = 'Hidden')

#         return Response(data=request.data, status= status.HTTP_200_OK)


# class LeaveMembershipViewSet(viewsets.ViewSet):
#     @swagger_auto_schema(responses={200: LeavePolicySerializer})
#     def create_policy(self, request, design_id):
#         designation_id = design_id  # ask
#         serializer_class = LeavePolicySerializer
#         if LeavePolicy.objects.filter(
#             leave_type=request.data["leavetype_id"],
#             #designations=design_id,
#         ):
#             return Response(
#                 {"message": "Leave Policy exists"}, status=status.HTTP_400_BAD_REQUEST
#             )
#         else:
#             serializer = LeavePolicySerializer(data=request.data)
#             serializer.is_valid(raise_exception=True)
#             policy = serializer.save()

#     def create_leave_membership(self, request):
#         serializer = self.read_serializer(data=request.data, many=True)
#         serializer.is_valid(raise_exception=True)

#         for index in serializer.validated_data:
#             try:
#                 leaveid = LeavePolicy_TypeMembership.objects.get(
#                     leave_type=index["leavetype_id"],
#                     leave_policy=index["leavepolicy_id"],
#                 )
#                 leaveid.total_days_allowed = index["total_days"]
#                 leaveid.total_consecutive_days = index["total_cons"]
#                 leaveid.save()
#             except LeavePolicy_TypeMembership.DoesNotExist:
#                 membership = LeavePolicy_TypeMembership(
#                     leave_type=index["leavetype_id"],
#                     leave_policy=index["leavepoliccy_id"],
#                     total_days_allowed=index["total_days"],
#                     total_consecutive_days=index["total_cons"],
#                 )
#                 membership.save()

# Single Employee based attendance views (entries for that particular employee) (get/create) (when check in, see if an existing attendance, if not create) done

# All attendees in a Day done

# Department wise attendances done

# monthly attendance and hours to see for overtime or absentee hours remaining

# make leave application/get/create employee based should have all deets and all apps, whereas when requesting all, only get open #loran

# accept/reject leave application loran


# ask rugved about leave policy problem

# leave generation based on designation's leave policy for each employee

# privileged leave assigned per quarter/ carry forwarding /


# @swagger_auto_schema(responses={200: EmployeeSerializer})
# def read_all_employees(self, request):

#     try:
#         queryset = Employee.objects.all()
#     except:
#         return Response({"message" : "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND )

#     try:
#         serialized = EmployeeSerializer(queryset, many = True)
#     except:
#         return Response({"message" : "Serializer error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR )

#     return Response(data=serialized.data, status= status.HTTP_200_OK)

# @action(detail=True, methods=['create'])
