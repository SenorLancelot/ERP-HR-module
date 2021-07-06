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

# Create your views here.
class EmployeeViewSet(APIView):

    
    # def get_employee(self, request):

    def get_employee_list(self, request):
        queryset = Employees.objects.all()
        serialized = EmployeesSerializer(queryset, many = True)
        return Response(data=serialized.data, status= status.HTTP_200_OK)

    def post_to_employee(self, request):
            
        serialized = EmployeesSerializer(data=request.data)

        
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status= status.HTTP_200_OK)

        return Response(data=serialized.errors, status= status.HTTP_200_OK)

    def delete_employees(self, request):

        Employees.objects.filter(employee_id__in = request.data["employees"]).delete()


class EmployeeGroupViewSet(APIView):

    def get_employeegroup_list(self, request):

        queryset = EmployeeGroup.objects.all()
        serialized = EmployeeGroupSerializer(queryset, many = True)
        return Response(data = serialized.data, status=status.HTTP_200_OK)

    def post_employeegroup(self, request):

        serialized = EmployeeGroupSerializer(data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status= status.HTTP_200_OK)

        return Response(data=serialized.errors, status= status.HTTP_200_OK)

    def delete_employeegroup(self, request):

        EmployeeGroup.objects.filter(group_id__in = request.data["group_ids"]).delete()


class DepartmentsViewSet(APIView):

    def get_department_list(self, request):

        queryset = Departments.objects.all()
        serialized = DepartmentsSerializer(queryset, many = True)
        return Response(data=serialized.data, status= status.HTTP_200_OK)
    
    def post_department_list(self, request):

        serialized = DepartmentsSerializer(data = request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status= status.HTTP_200_OK)

        return Response(data=serialized.errors, status= status.HTTP_200_OK)

    def delete_department_list(self, request):

        Departments.objects.filter(department_id__in=request.data["department_ids"]).delete()

    
class DesignationsViewSet(APIView):

    def get_designations_list(self, request):

        queryset = Designations.objects.all()
        serialized = DesignationsSerializer(queryset, many = True)
        return Response(data=serialized.data, status= status.HTTP_200_OK)

    def post_designations_list(self, request):

        serialized = DesignationsSerializer(data = request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status= status.HTTP_200_OK)
        
        return Response(data=serialized.errors, status= status.HTTP_200_OK)

    def delete_designations_list(self, request):

        Designations.objects.filter(designation_id__in = request.data["designation_ids"]).delete()


class AttendancesViewSet(APIView):

    def get_attendances_list(self, request):
        
        queryset = Attendances.objects.filter(employee_id = request.GET.get("employee_id", ""))
        serialized = AttendancesSerializer(queryset, many = True)
        return Response(data=serialized.data, status= status.HTTP_200_OK)

    def post_attendances_list(self, request):

        serialized = AttendancesSerializer(data = request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status= status.HTTP_200_OK)
        
        return Response(data=serialized.errors, status= status.HTTP_200_OK)

    def delete_attendances_list(self, request):

        Attendances.objects.filter(employee_id  = request.GET.get("employee_id", "")).delete()


class EmployeeCheckinsViewSet(APIView):

    def get_employeecheckins_list(self, request):
        
        queryset = EmployeeCheckins.objects.filter(employee_id = request.GET.get("employee_id", ""))
        serialized = EmployeeCheckinsSerializer(queryset, many = True)
        return Response(data=serialized.data, status= status.HTTP_200_OK)

    def post_employeecheckins_list(self, request):

        serialized = EmployeeCheckinsSerializer(data = request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status= status.HTTP_200_OK)
        
        return Response(data=serialized.errors, status= status.HTTP_200_OK)

    def delete_employeecheckins_list(self, request):

        EmployeeCheckins.objects.filter(employee_id = request.GET.get("employee_id", "")).delete()



class LeavePoliciesViewSet(APIView):

    def get_leavepolicies_list(self, request):
    
        queryset = LeavePolicies.objects.all()
        serialized = LeavePoliciesSerializer(queryset, many = True)
        return Response(data=serialized.data, status= status.HTTP_200_OK)

    def post_leavepolicies_list(self, request):

        serialized = LeavePoliciesSerializer(data = request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status= status.HTTP_200_OK)
        
        return Response(data=serialized.errors, status= status.HTTP_200_OK)

    def delete_leavepolicies_list(self, request):

        LeavePolicies.objects.filter(id__in = request.data["leavepolicy_ids"]).delete()


class LeaveApplicationsViewSet(APIView):
    
    def get_leaveapplications_list(self, request):
    
        queryset = LeavesApplications.objects.all()
        serialized = LeavesApplicationsSerializer(queryset, many = True)
        return Response(data=serialized.data, status= status.HTTP_200_OK)

    def post_leavesapplications_list(self, request):

        serialized = LeavesApplicationsSerializer(data = request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status= status.HTTP_200_OK)
        
        return Response(data=serialized.errors, status= status.HTTP_200_OK)

    def delete_leavesapplications_list(self, request):

        LeavesApplications.objects.filter(id__in = request.data["leaveapplication_ids"]).delete()

class LeaveViewSet(APIView):


    def get_leave_list(self, request):
    
        queryset = Leave.objects.all()
        serialized = LeavesSerializer(queryset, many = True)
        return Response(data=serialized.data, status= status.HTTP_200_OK)

    def post_leave_list(self, request):

        serialized = LeavesSerializer(data = request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status= status.HTTP_200_OK)
        
        return Response(data=serialized.errors, status= status.HTTP_200_OK)

    def delete_leave_list(self, request):

        LeavePolicies.objects.filter(id__in = request.data["leave_ids"]).delete()
    






# Single Employee based attendance views (entries for that particular employee) (get/post) (when check in, see if an existing attendance, if not create)

# All attendees in a Day

# Department wise attendances

# monthly attendance and hours to see for overtime or absentee hours

# leave generation based on designation's leave policy for each empployee

# make leave application/get/post employee based should have all deets and all apps, whereas when requesting all, only get open

# accept/reject leave application

#  ask rugved about leave policy problem











    


        




    

