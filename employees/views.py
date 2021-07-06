from django.db.models.query import QuerySet
from django.shortcuts import render
from rest_framework import generics, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# project imports
from . import models
from .models import *
from .serializers import *

from drf_yasg.utils import swagger_auto_schema

# Create your views here.
class EmployeeViewSet(viewsets.ViewSet):

    
    # def get_employee(self, request):
    @swagger_auto_schema(responses={200: EmployeesSerializer})
    def get_employee_list(self, request):

        try:
            employee_ids = request.data["employees"]
        except:
            return Response({"Message" : "BAD REQUEST"}, status=status.HTTP_404_NOT_FOUND )

        try:
            queryset = Employees.objects.filter(employee_id__in = request.data["employees"])    
        except:
            return Response({"Message" : "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND )

        try:
            serialized = EmployeesSerializer(queryset, many = True)
        except:
            return Response({"Message" : "Serializer error"}, status=status.HTTP_404_NOT_FOUND )
        
        return Response(data=serialized.data, status= status.HTTP_200_OK)
        


    @swagger_auto_schema(responses={200: EmployeesSerializer})
    def get_all_employees(self, request):

        try:
            queryset = Employees.objects.all()
        except:
            return Response({"Message" : "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND )
            
        try:
            serialized = EmployeesSerializer(queryset, many = True)
        except:
            return Response({"Message" : "Serializer error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR )
        
        return Response(data=serialized.data, status= status.HTTP_200_OK)



    @swagger_auto_schema(request_body=EmployeesSerializer,responses={200: EmployeesSerializer})
    def post_to_employee_list(self, request):
        
        
        serialized = EmployeesSerializer(data=request.data, many = True)
        
        
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status= status.HTTP_200_OK)

        return Response(data=serialized.errors, status= status.HTTP_200_OK)


    def delete_employees(self, request):

        Employees.objects.filter(employee_id__in = request.data["employees"]).delete()

        return Response(data=request.data, status= status.HTTP_200_OK)


class EmployeeGroupViewSet(viewsets.ViewSet):

    @swagger_auto_schema(responses={200: EmployeeGroupSerializer})
    def get_employeegroup_list(self, request):


        try:
            queryset = EmployeeGroup.objects.all()
        except:
            return Response({"Message" : "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND )
            
        try:
            serialized = EmployeeGroupSerializer(queryset, many = True)
        except:
            return Response({"Message" : "Serializer error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR )
        
        return Response(data=serialized.data, status= status.HTTP_200_OK)

    @swagger_auto_schema(request_body=EmployeeGroupSerializer,responses={200: EmployeeGroupSerializer})
    def post_employeegroup_list(self, request):

        serialized = EmployeeGroupSerializer(data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status= status.HTTP_200_OK)

        return Response(data=serialized.errors, status= status.HTTP_200_OK)

    def delete_employeegroup(self, request):

        EmployeeGroup.objects.filter(group_id__in = request.data["group_ids"]).delete()

        return Response(data=request.data, status= status.HTTP_200_OK)


class DepartmentsViewSet(viewsets.ViewSet):

    @swagger_auto_schema(responses={200: DepartmentsSerializer})
    def get_department_list(self, request):

        if not (request.data["department_ids"]):
            queryset = Departments.objects.all()
        else:
            queryset = Departments.objects.filter(department_id__in=request.data["department_ids"])
        
        serialized = DepartmentsSerializer(queryset, many = True)
        return Response(data=serialized.data, status= status.HTTP_200_OK)
    
    @swagger_auto_schema(request_body=DepartmentsSerializer,responses={200: DepartmentsSerializer})
    def post_department_list(self, request):

        serialized = DepartmentsSerializer(data = request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status= status.HTTP_200_OK)

        return Response(data=serialized.errors, status= status.HTTP_200_OK)

    def delete_department_list(self, request):

        Departments.objects.filter(department_id__in=request.data["department_ids"]).delete()

        return Response(data=request.data, status= status.HTTP_200_OK)

    
class DesignationsViewSet(viewsets.ViewSet):

    @swagger_auto_schema(responses={200: DesignationsSerializer})
    def get_designations_list(self, request):

        if not (request.data["designation_ids"]):
            queryset = Designations.objects.all()
        else:
            queryset = Designations.objects.filter(designation_id__in=request.data["designation_ids"])
        serialized = DesignationsSerializer(queryset, many = True)
        return Response(data=serialized.data, status= status.HTTP_200_OK)

    @swagger_auto_schema(request_body=DesignationsSerializer,responses={200: DesignationsSerializer})
    def post_designations_list(self, request):

        serialized = DesignationsSerializer(data = request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status= status.HTTP_200_OK)
        
        return Response(data=serialized.errors, status= status.HTTP_200_OK)

    def delete_designations_list(self, request):

        Designations.objects.filter(designation_id__in = request.data["designation_ids"]).delete()

        return Response(data=request.data, status= status.HTTP_200_OK)


class AttendancesViewSet(viewsets.ViewSet):

    @swagger_auto_schema(responses={200: AttendancesSerializer})
    def get_attendances_list(self, request):
        
        queryset = Attendances.objects.filter(employee_id = request.GET.get("employee_id", ""))
        serialized = AttendancesSerializer(queryset, many = True)
        return Response(data=serialized.data, status= status.HTTP_200_OK)

    @swagger_auto_schema(request_body=AttendancesSerializer,responses={200: AttendancesSerializer})
    def post_attendances_list(self, request):

        serialized = AttendancesSerializer(data = request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status= status.HTTP_200_OK)
        
        return Response(data=serialized.errors, status= status.HTTP_200_OK)

    def delete_attendances_list(self, request):

        Attendances.objects.filter(employee_id  = request.GET.get("employee_id", "")).delete()

        return Response(data=request.data, status= status.HTTP_200_OK)



class EmployeeCheckinsViewSet(viewsets.ViewSet):

    def post_employee_checkins(self, request):
        employee_id = request.GET.get("employee_id")
        queryset = EmployeeCheckins.objects.filter(attendance_attendance_date = request.GET.get("date"))

        

    @swagger_auto_schema(responses={200: EmployeeCheckinsSerializer})
    def get_employeecheckins_list(self, request):
        
        queryset = EmployeeCheckins.objects.filter(employee_id = request.GET.get("employee_id", ""))
        serialized = EmployeeCheckinsSerializer(queryset, many = True)
        return Response(data=serialized.data, status= status.HTTP_200_OK)

    @swagger_auto_schema(request_body=EmployeeCheckinsSerializer,responses={200: EmployeeCheckinsSerializer})
    def post_employeecheckins_list(self, request):

        serialized = EmployeeCheckinsSerializer(data = request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status= status.HTTP_200_OK)
        
        return Response(data=serialized.errors, status= status.HTTP_200_OK)

    def delete_employeecheckins_list(self, request):

        EmployeeCheckins.objects.filter(employee_id = request.GET.get("employee_id", "")).delete()

        return Response(data=request.data, status= status.HTTP_200_OK)



class LeavePoliciesViewSet(viewsets.ViewSet):

    
    @swagger_auto_schema(responses={200: LeavePoliciesSerializer})
    def get_leavepolicies_list(self, request):
    
        if not (request.data["leavepolicy_ids"]):
            queryset = LeavePolicies.objects.all()
        else:
            queryset = LeavePolicies.objects.filter(designation_id__in=request.data["leavepolicy_ids"])
        serialized = LeavePoliciesSerializer(queryset, many = True)
        return Response(data=serialized.data, status= status.HTTP_200_OK)

    @swagger_auto_schema(request_body=LeavePoliciesSerializer,responses={200: LeavePoliciesSerializer})
    def post_leavepolicies_list(self, request):

        serialized = LeavePoliciesSerializer(data = request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status= status.HTTP_200_OK)
        
        return Response(data=serialized.errors, status= status.HTTP_200_OK)

    def delete_leavepolicies_list(self, request):

        LeavePolicies.objects.filter(id__in = request.data["leavepolicy_ids"]).delete()

        return Response(data=request.data, status= status.HTTP_200_OK)


class LeaveApplicationsViewSet(viewsets.ViewSet):
    
    @swagger_auto_schema(responses={200: LeavesApplicationsSerializer})
    def get_leaveapplications_list(self, request):
    
        if not (request.data["leaveapplication_ids"]):
            queryset = LeavesApplications.objects.all()
        else:
            queryset = LeavesApplications.objects.filter(id__in=request.data["leaveapplication_ids"])
        serialized = LeavesApplicationsSerializer(queryset, many = True)
        return Response(data=serialized.data, status= status.HTTP_200_OK)

    @swagger_auto_schema(request_body=LeavesApplicationsSerializer,responses={200: LeavesApplicationsSerializer})
    def post_leavesapplications_list(self, request):

        serialized = LeavesApplicationsSerializer(data = request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status= status.HTTP_200_OK)
        
        return Response(data=serialized.errors, status= status.HTTP_200_OK)

    def delete_leavesapplications_list(self, request):

        LeavesApplications.objects.filter(id__in = request.data["leaveapplication_ids"]).delete()

        return Response(data=request.data, status= status.HTTP_200_OK)

class LeaveViewSet(viewsets.ViewSet):

    @swagger_auto_schema(responses={200: LeavesSerializer})
    def get_leave_list(self, request):
    
        if not (request.data["leave_ids"]):
            queryset = Leave.objects.all()
        else:
            queryset = Leave.objects.filter(id__in=request.data["leave_ids"])
        serialized = LeavesSerializer(queryset, many = True)
        return Response(data=serialized.data, status= status.HTTP_200_OK)

    @swagger_auto_schema(request_body=LeavesSerializer,responses={200: LeavesSerializer})
    def post_leave_list(self, request):

        serialized = LeavesSerializer(data = request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status= status.HTTP_200_OK)
        
        return Response(data=serialized.errors, status= status.HTTP_200_OK)

    def delete_leave_list(self, request):

        LeavePolicies.objects.filter(id__in = request.data["leave_ids"]).delete()

        return Response(data=request.data, status= status.HTTP_200_OK)
    






# Single Employee based attendance views (entries for that particular employee) (get/post) (when check in, see if an existing attendance, if not create)

# All attendees in a Day

# Department wise attendances

# monthly attendance and hours to see for overtime or absentee hours

# leave generation based on designation's leave policy for each empployee

# make leave application/get/post employee based should have all deets and all apps, whereas when requesting all, only get open

# accept/reject leave application

#  ask rugved about leave policy problem











    


        




    

