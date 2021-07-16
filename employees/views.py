from django.db.models.query import QuerySet
from django.shortcuts import render
from rest_framework import generics, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum
# from datetime import datetime
import datetime
from datetime import date
# project imports
from rest_framework.decorators import action

from .models import *
from .serializers import *

from drf_yasg.utils import swagger_auto_schema

# Create your views here.
class EmployeeViewSet(viewsets.ViewSet):

    @swagger_auto_schema(request_body=EmployeesSerializer,responses={200: EmployeesSerializer})
    def patch_employees_list(self, request):
        
        try:
            employee = request.data["employee_id"]

        except:

            return Response({"Message" : "No data"}, status = status.HTTP_400_BAD_REQUEST)

        queryset = Employees.objects.get(employee_id = employee)

        serialized = EmployeesSerializer(queryset, request.data, partial = True)

        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status= status.HTTP_200_OK)

        return Response(data=serialized.errors, status= status.HTTP_200_OK)


    
    # def get_employee(self, request):
    @swagger_auto_schema(responses={200: EmployeesSerializer})
    def get_employee_list(self, request):


        try:
            queryset = Employees.objects.all()
        except:
            return Response({"Message" : "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND )
            
        try:
            serialized = EmployeesSerializer(queryset, many = True)
        except:
            return Response({"Message" : "Serializer error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR )
        
        return Response(data=serialized.data, status= status.HTTP_200_OK)
        


    # @swagger_auto_schema(responses={200: EmployeesSerializer})
    # def get_all_employees(self, request):

    #     try:
    #         queryset = Employees.objects.all()
    #     except:
    #         return Response({"Message" : "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND )
            
    #     try:
    #         serialized = EmployeesSerializer(queryset, many = True)
    #     except:
    #         return Response({"Message" : "Serializer error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR )
        
    #     return Response(data=serialized.data, status= status.HTTP_200_OK)


    # @action(detail=True, methods=['post'])
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

    def patch_departments_list(self, request):
        
        try:
            department = request.data["department_id"]

        except:

            return Response({"Message" : "No data"}, status = status.HTTP_400_BAD_REQUEST)

        queryset = Departments.objects.get(department_id = department)

        serialized = DepartmentsSerializer(queryset, request.data, partial = True)

        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status= status.HTTP_200_OK)

        return Response(data=serialized.errors, status= status.HTTP_200_OK)


    @swagger_auto_schema(responses={200: DepartmentsSerializer})
    def get_department_list(self, request):

        try:
            queryset = Departments.objects.all()
        except:
            return Response({"Message" : "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND )
        
        serialized = DepartmentsSerializer(queryset, many = True)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status= status.HTTP_200_OK)

        return Response(data=serialized.errors, status= status.HTTP_200_OK)
    
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

    def patch_designations_list(self, request):
        
        try:
            designation = request.data["designation_id"]

        except:

            return Response({"Message" : "No data"}, status = status.HTTP_400_BAD_REQUEST)

        queryset = Designations.objects.get(designation_id = designation)

        serialized = DesignationsSerializer(queryset, request.data, partial = True)

        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status= status.HTTP_200_OK)

        return Response(data=serialized.errors, status= status.HTTP_200_OK)

    @swagger_auto_schema(responses={200: DesignationsSerializer})
    def get_designations_list(self, request):

        try:
            queryset = Designations.objects.all()
        except:
            return Response({"Message" : "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND )
        
        serialized = DesignationsSerializer(queryset, many = True)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status= status.HTTP_200_OK)

        return Response(data=serialized.errors, status= status.HTTP_200_OK)

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


    # def get_monthly_reports(self, request):

    


    @swagger_auto_schema(responses={200: AttendancesSerializer})
    def get_department_attendances_list(self, request, dept_id):
        dep_id = dept_id

        if (request.GET.get('filter_by', False)):
            filter_type = request.GET.get('filter_by', "date")
            
            if(filter_type == "date"):
                date_req = request.GET.get('date', datetime.date.today)
                queryset = Attendances.objects.filter(employee__department = dep_id, attendance_date = date_req)
                serialized = AttendancesSerializer(queryset, many = True)
                return Response(data=serialized.data, status= status.HTTP_200_OK)

            else:
                month = request.GET.get('month', date.today().month)
                year = request.GET.get('year', date.today().year)
                queryset = Attendances.objects.filter(employee__department = dep_id, attendance_date__month = month, attendance_date__year = year)
                serialized = AttendancesSerializer(queryset, many = True)
                return Response(data=serialized.data, status= status.HTTP_200_OK)

        else:
            
            queryset = Attendances.objects.filter(employee__department = dep_id)
            serialized = AttendancesSerializer(queryset, many = True)
            return Response(data=serialized.data, status= status.HTTP_200_OK)

    

    def get_employee_attendances_list(self, request, emp_id):
        if isinstance(emp_id, uuid.UUID):

            employee_id = emp_id

        else:

            return Response({"Message" : "UUID Format wrong"}, status=status.HTTP_400_BAD_REQUEST)

        if(request.GET.get('isFilter',False)):
                
            start_date_req = request.GET.get("start_date",datetime.date.today())
            end_date_req = request.GET.get("end_date", datetime.date.today())
            queryset=Attendances.objects.filter(employee_id=employee_id,attendance_date__range=[start_date_req,end_date_req])
            serialized = AttendancesSerializer(queryset, many = True)
            return Response(data=serialized.data, status= status.HTTP_200_OK)

        
        else:

           queryset = Attendances.objects.filter(employee = employee_id)
           serialized = AttendancesSerializer(queryset, many = True)
           return Response(data=serialized.data, status= status.HTTP_200_OK)

        
        # if (request.GET.get('filter_by', False)):
        #     filter_type = request.GET.get('filter_by', "date")
            
        #     if(filter_type == "date"):
        #         date_req = request.GET.get('date', datetime.date.today)
        #         queryset = Attendances.objects.filter(employee_id = employee_id, attendance_date = date_req)
        #         serialized = AttendancesSerializer(queryset, many = True)
        #         return Response(data=serialized.data, status= status.HTTP_200_OK)

        #     else:

        #         month = request.GET.get('month', date.today().month)
        #         year = request.GET.get('year', date.today().year)
        #         queryset = Attendances.objects.filter(employee_id = employee_id, attendance_date__month = month, attendance_date__year = year)
        #         serialized = AttendancesSerializer(queryset, many = True)
        #         return Response(data=serialized.data, status= status.HTTP_200_OK)
            
        

        # else:
            
        #     queryset = Attendances.objects.filter(employee = employee_id)
        #     serialized = AttendancesSerializer(queryset, many = True)
        #     return Response(data=serialized.data, status= status.HTTP_200_OK)

    def get_attendances_list(self, request):

        queryset = Attendances.objects.all()
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

    
    @swagger_auto_schema(request_body=EmployeeCheckinsSerializer,responses={200: AttendancesSerializer})
    def post_employee_checkin(self, request):
        try:
            employee_id = request.data["employee"]
            date = request.data["date"]
        except:
            return Response({"Message" : "body not specified. Please specify employee_id and date"}, status= status.HTTP_400_BAD_REQUEST)
        employee = Employees.objects.get(employee_id=employee_id)
        try:
            attendance = Attendances.objects.get(attendance_date = date, employee_id=employee_id)
        except Attendances.DoesNotExist:


            e_check = EmployeeCheckins(date = request.data["date"], checked_in = request.data["checked_in"], total_time_elapsed = request.data["total_time_elapsed"],employee = employee)
            e_check.save()
            a = Attendances(employee = employee, attendance_date = date, comment = "haha")
            a.save()
            a.checks.add(e_check)
            a.save()
            return Response(status= status.HTTP_200_OK)
            
        serialized = EmployeeCheckinsSerializer(data=request.data)
            
        if(serialized.is_valid()):

            a = EmployeeCheckins.objects.filter(employee = employee_id).latest('checked_in')

            if a.checked_out is not None:          
                serialized.save()
                e = EmployeeCheckins.objects.latest('checked_in')
                attendance.checks.add(e)
                return Response(data=serialized.data, status= status.HTTP_200_OK)
            else:

                return Response({"Message" : "Check out of existing session"}, status=status.HTTP_200_OK)


    def post_employee_checkout(self, request):

        try:
            employee_id = request.data["employee"]
            checkout = request.data["checked_out"]
            
        except:
            return Response({"Message" : "Query parameters not specified. Please specify employee_id"}, status= status.HTTP_400_BAD_REQUEST)
        try:

            a = EmployeeCheckins.objects.filter(employee = employee_id).latest('checked_in')

        except EmployeeCheckins.DoesNotExist:

            return Response({"Message" : "No checkin for the employee found"})

        if a.checked_out is None:
                    
            a.checked_out = checkout
            a.save()
            return Response( status= status.HTTP_200_OK)
        else:

            return Response({"Message" : "ALready checked out of existing session"}, status=status.HTTP_200_OK)




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

######################################################## Leave Viewsets #################################

class LeavePoliciesViewSet(viewsets.ViewSet):


    
    def patch_leavepolicies_list(self, request):
        
        try:
            leavepolicy = request.data["leavepolicy_id"]

        except:

            return Response({"Message" : "No data"}, status = status.HTTP_400_BAD_REQUEST)

        queryset = LeavePolicies.objects.get(leavepolicy_id = leavepolicy)

        serialized = LeavePoliciesSerializer(queryset, request.data, partial = True)

        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status= status.HTTP_200_OK)

        return Response(data=serialized.errors, status= status.HTTP_200_OK)


    @swagger_auto_schema(responses={200: LeavePoliciesSerializer})
    def get_leavepolicies_list(self, request):
    
        try:
            queryset = LeavePolicies.objects.all()
        except:
            return Response({"Message" : "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)
        
        serialized = LeavePoliciesSerializer(queryset, many = True)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status= status.HTTP_200_OK)

        return Response(data=serialized.errors, status= status.HTTP_200_OK)

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

    def accept_applications(self,request):
        try:
            accepted_ids = request.data["accepted_ids"]
        except:
            return Response({"Message","specify accepted ids"})
        employee = Employees.objects.get(employee_id=accepted_ids)
        # aceepted = LeavesApplications.objects.filter(accepted_ids__in=employee.update(status='Approved'))
        try:
            leave_ids = LeavesApplications.objects.filter(employee_id__in=accepted_ids)
            accept = LeavesApplications.objects.filter(accepted_ids= employee.update(status='Approved'))
            serialized = LeavesApplicationsSerializer(accept, many=True)
            return Response(data=serialized.data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get_leaveapplications_employee(self,request,emp_id):
        if isinstance(emp_id, uuid.UUID):

            employee_id = emp_id
            
            queryset = LeavesApplications.objects.filter(employee = emp_id)
            serialized = LeavesApplicationsSerializer(queryset,many=True)
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        else:

            return Response({"Message" : "UUID Format wrong"}, status=status.HTTP_400_BAD_REQUEST)
    
    def patch_leavesapplications_list(self, request):
        
        try:
            leaveapplication = request.data["leaveapplication_id"]

        except:

            return Response({"Message" : "No data"}, status = status.HTTP_400_BAD_REQUEST)

        queryset = LeavesApplications.objects.get(leaveapplication_id = leaveapplication)

        serialized = LeavesApplicationsSerializer(queryset, request.data, partial = True)

        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status= status.HTTP_200_OK)

        return Response(data=serialized.errors, status= status.HTTP_200_OK)

    @swagger_auto_schema(responses={200: LeavesApplicationsSerializer})
    def get_leaveapplications_list(self, request):
    
        try:
            queryset = LeavesApplications.objects.all()
        except:
            return Response({"Message" : "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND )
        
        serialized = LeavesApplicationsSerializer(queryset, many = True)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status= status.HTTP_200_OK)

        return Response(data=serialized.errors, status= status.HTTP_200_OK)

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

    def patch_leaves_list(self, request):
        
        try:
            leave = request.data["leave_id"]

        except:

            return Response({"Message" : "No data"}, status = status.HTTP_400_BAD_REQUEST)

        queryset = Leaves.objects.get(leave_id = leave)

        serialized = LeavesSerializer(queryset, request.data, partial = True)

        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status= status.HTTP_200_OK)

        return Response(data=serialized.errors, status= status.HTTP_200_OK)

    @swagger_auto_schema(responses={200: LeavesSerializer})
    def get_leave_list(self, request):
    
        try:
            queryset = Leaves.objects.all()
        except:
            return Response({"Message" : "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND )
        
        serialized = LeavesSerializer(queryset, many = True)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status= status.HTTP_200_OK)

        return Response(data=serialized.errors, status= status.HTTP_200_OK)

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
    

class MonthlyReportsViewSet(viewsets.ViewSet):


    def patch_monthlyreports_list(self, request):
        
        try:
            monthlyreport = request.data["monthlyreport_id"]

        except:

            return Response({"Message" : "No data"}, status = status.HTTP_400_BAD_REQUEST)

        queryset = MonthlyReports.objects.get(monthlyreport_id = monthlyreport)

        serialized = MonthlyReportsSerializer(queryset, request.data, partial = True)

        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status= status.HTTP_200_OK)

        return Response(data=serialized.errors, status= status.HTTP_200_OK)


    def get_monthly_reports_list(self, request):

        try:
            queryset = MonthlyReports.objects.all()
        except:
            return Response({"Message" : "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND )
        
        serialized = MonthlyReportsSerializer(queryset, many = True)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status= status.HTTP_200_OK)

        return Response(data=serialized.errors, status= status.HTTP_200_OK)


    def post_monthly_reports_list(self, request):

        serialized = MonthlyReportsSerializer(data = request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status= status.HTTP_200_OK)
        
        return Response(data=serialized.errors, status= status.HTTP_200_OK)

    def delete_leave_list(self, request):
    
        MonthlyReports.objects.filter(id__in = request.data["monthlyreport_ids"]).delete()

        return Response(data=request.data, status= status.HTTP_200_OK)


    def generate_monthly_report(self, request, emp_id):

        month = request.GET.get('month', date.today().month)
        year = request.GET.get('year', date.today().year)
        work_hours = Attendances.objects.filter(employee = emp_id, attendance_date__month = month, attendance_date__year = year ).aggregate(Sum('total_time'))
        print(work_hours)
        dt = {"employee": emp_id, "total_time_worked" : work_hours["total_time__sum"]}
        serialized = MonthlyReportsSerializer(data = dt)

        if serialized.is_valid():

            serialized.save()

            return Response(data=serialized.data, status= status.HTTP_200_OK)

        else:

            return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)



class CalendarViewSet(viewsets.ViewSet):


    def patch_calendar_list(self, request):
        
        try:
            date = request.data["date"]
        except:
            return Response({"Message" : "No data"}, status = status.HTTP_400_BAD_REQUEST)
        queryset = Calendar.objects.get(date=date)

        serialized = CalendarSerializer(queryset, request.data, partial = True)

        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status= status.HTTP_200_OK)

        return Response(data=serialized.errors, status= status.HTTP_200_OK)

    @swagger_auto_schema(responses={200: CalendarSerializer})
    def get_calendar_list(self, request):
    
        try:
            queryset = Calendar.objects.all()
        except:
            return Response({"Message" : "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND )
        
        serialized = CalendarSerializer(queryset, many = True)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status= status.HTTP_200_OK)

        return Response(data=serialized.errors, status= status.HTTP_200_OK)

    @swagger_auto_schema(request_body=CalendarSerializer,responses={200: CalendarSerializer})
    def post_calendar_list(self, request):

        serialized = CalendarSerializer(data = request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status= status.HTTP_200_OK)
        
        return Response(data=serialized.errors, status= status.HTTP_200_OK)

    def delete_leave_list(self, request):

        Calendar.objects.filter(date__in = request.data["dates"]).delete()

        return Response(data=request.data, status= status.HTTP_200_OK)



class EventsViewset(viewsets.ViewSet):
    

    def patch_events_list(self, request):
        
        try:
            event_id = request.data["event_id"]
        except:
            return Response({"Message" : "No data"}, status = status.HTTP_400_BAD_REQUEST)
        queryset = Events.objects.get(event_id=event_id)

        serialized = EventsSerializer(queryset, request.data, partial = True)

        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status= status.HTTP_200_OK)

        return Response(data=serialized.errors, status= status.HTTP_200_OK)

    @swagger_auto_schema(responses={200: EventsSerializer})
    def get_events_list(self, request):
    
        try:
            queryset = Events.objects.all()
        except:
            return Response({"Message" : "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND )
        
        serialized = EventsSerializer(queryset, many = True)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status= status.HTTP_200_OK)

        return Response(data=serialized.errors, status= status.HTTP_200_OK)

    @swagger_auto_schema(request_body=EventsSerializer,responses={200: EventsSerializer})
    def post_events_list(self, request):

        serialized = EventsSerializer(data = request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status= status.HTTP_200_OK)
        
        return Response(data=serialized.errors, status= status.HTTP_200_OK)

    def delete_events_list(self, request):

        Events.objects.filter(event_id__in = request.data["event_ids"]).delete()

        return Response(data=request.data, status= status.HTTP_200_OK)

# Single Employee based attendance views (entries for that particular employee) (get/post) (when check in, see if an existing attendance, if not create) done

# All attendees in a Day done

# Department wise attendances done

# monthly attendance and hours to see for overtime or absentee hours remaining

# make leave application/get/post employee based should have all deets and all apps, whereas when requesting all, only get open #loran

# accept/reject leave application loran





# ask rugved about leave policy problem

# leave generation based on designation's leave policy for each employee

#privileged leave assigned per quarter/ carry forwarding / 



        # if(request.GET.get('isFilter',False)):
            
        #     start_date_req = request.GET.get("start_date",datetime.date.today())
        #     end_date_req = request.GET.get("end_date", datetime.date.today())
        #     queryset=Attendances.objects.filter(employee_id=employee_id,daterange=["attendance_datedate=start_date_req","attendance_date__date=end_date_req"])
        #     serialized = AttendancesSerializer(queryset, many = True)
        #     return Response(data=serialized.data, status= status.HTTP_200_OK)

        #good job on date range
        # else:

        #    queryset = Attendances.objects.filter(employee = employee_id)
        #    serialized = AttendancesSerializer(queryset, many = True)
        #    return Response(data=serialized.data, status= status.HTTP_200_OK)






    


        




    

