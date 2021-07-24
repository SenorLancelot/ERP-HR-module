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
# LORAN
class EmployeeViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        request_body=EmployeeSerializer, responses={200: EmployeeSerializer}
    )
    def update_employee(self, request):

        try:
            employee = request.data["id"]

        except:

            return Response({"Message": "No data"}, status=status.HTTP_400_BAD_REQUEST)

        queryset = Employee.objects.get(id=employee)

        serialized = EmployeeSerializer(queryset, request.data, partial=True)

        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_200_OK)

    # def read_employee(self, request):
    @swagger_auto_schema(responses={200: EmployeeSerializer})
    def read_employees(self, request):

        try:
            queryset = Employee.objects.all()
        except:
            return Response({"Message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        try:
            serialized = EmployeeSerializer(queryset, many=True)
        except:
            return Response(
                {"Message": "Serializer error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    # @swagger_auto_schema(responses={200: EmployeeSerializer})
    # def read_all_employees(self, request):

    #     try:
    #         queryset = Employee.objects.all()
    #     except:
    #         return Response({"Message" : "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND )

    #     try:
    #         serialized = EmployeeSerializer(queryset, many = True)
    #     except:
    #         return Response({"Message" : "Serializer error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR )

    #     return Response(data=serialized.data, status= status.HTTP_200_OK)

    # @action(detail=True, methods=['create'])
    @swagger_auto_schema(
        request_body=EmployeeSerializer, responses={200: EmployeeSerializer}
    )
    def create_employees(self, request):

        serialized = EmployeeSerializer(data=request.data, many=True)

        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=EmployeeDeleteSerializer, responses={200: EmployeeDeleteSerializer}
    )
    def delete_employees(self, request):

        # TODO serializer error handling
        Employee.objects.filter(id__in=request.data["employees"]).delete()

        return Response(data=request.data, status=status.HTTP_200_OK)


# LORAN
class EmployeeGroupViewSet(viewsets.ViewSet):
    @swagger_auto_schema(responses={200: EmployeeGroupSerializer})
    def read_employeegroup(self, request):

        try:
            queryset = EmployeeGroup.objects.all()
        except:
            return Response({"Message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        try:
            serialized = EmployeeGroupSerializer(queryset, many=True)
        except:
            return Response(
                {"Message": "Serializer error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=EmployeeGroupSerializer, responses={200: EmployeeGroupSerializer}
    )
    def create_employeegroup(self, request):

        serialized = EmployeeGroupSerializer(data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_200_OK)

    def delete_employeegroup(self, request):

        EmployeeGroup.objects.filter(group_id__in=request.data["group_ids"]).delete()

        return Response(data=request.data, status=status.HTTP_200_OK)


# LORAN
class DepartmentViewSet(viewsets.ViewSet):
    def update_departments(self, request):

        try:
            department = request.data["department_id"]

        except:

            return Response({"Message": "No data"}, status=status.HTTP_400_BAD_REQUEST)

        queryset = Department.objects.get(department_id=department)

        serialized = DepartmentSerializer(queryset, request.data, partial=True)

        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={200: DepartmentSerializer})
    def read_department(self, request):

        try:
            queryset = Department.objects.all()
        except:
            return Response({"Message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        serialized = DepartmentSerializer(queryset, many=True)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=DepartmentSerializer, responses={200: DepartmentSerializer}
    )
    def create_department(self, request):

        serialized = DepartmentSerializer(data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_200_OK)

    def delete_department(self, request):

        Department.objects.filter(
            department_id__in=request.data["department_ids"]
        ).delete()

        return Response(data=request.data, status=status.HTTP_200_OK)


# LORAN
class DesignationViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        request_body=DesignationSerializer, responses={200: DesignationSerializer}
    )
    def update_designations(self, request):

        try:
            designation = request.data["designation_id"]

        except:

            return Response({"Message": "No data"}, status=status.HTTP_400_BAD_REQUEST)

        queryset = Designation.objects.get(designation_id=designation)

        serialized = DesignationSerializer(queryset, request.data, partial=True)

        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={200: DesignationSerializer})
    def read_designations(self, request):

        try:
            queryset = Designation.objects.all()
        except:
            return Response({"Message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        serialized = DesignationSerializer(queryset, many=True)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=DesignationSerializer, responses={200: DesignationSerializer}
    )
    def create_designations(self, request):

        serialized = DesignationSerializer(data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_200_OK)

    def delete_designations(self, request):

        Designation.objects.filter(
            designation_id__in=request.data["designation_ids"]
        ).delete()

        return Response(data=request.data, status=status.HTTP_200_OK)


# LORAN
class AttendanceViewSet(viewsets.ViewSet):
    @swagger_auto_schema(responses={200: AttendanceSerializer})
    def read_department_attendances(self, request, dept_id):
        dep_id = dept_id

        if request.GET.get("isFilter", False):

            start_date_req = request.GET.get("start_date", datetime.date.today())
            end_date_req = request.GET.get("end_date", datetime.date.today())
            queryset = Attendance.objects.filter(
                employee__department=dep_id,
                attendance_date__range=[start_date_req, end_date_req],
            )
            serialized = AttendanceSerializer(queryset, many=True)
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        else:

            queryset = Attendance.objects.filter(employee__department=dep_id)
            serialized = AttendanceSerializer(queryset, many=True)
            return Response(data=serialized.data, status=status.HTTP_200_OK)

    def read_employee_attendances(self, request, emp_id):
        if isinstance(emp_id, uuid.UUID):

            id = emp_id

        else:

            return Response(
                {"Message": "UUID Format wrong"}, status=status.HTTP_400_BAD_REQUEST
            )

        if request.GET.get("isFilter", False):

            start_date_req = request.GET.get("start_date", datetime.date.today())
            end_date_req = request.GET.get("end_date", datetime.date.today())
            queryset = Attendance.objects.filter(
                id=id,
                attendance_date__range=[start_date_req, end_date_req],
            )
            serialized = AttendanceSerializer(queryset, many=True)
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        else:

            queryset = Attendance.objects.filter(employee=id)
            serialized = AttendanceSerializer(queryset, many=True)
            return Response(data=serialized.data, status=status.HTTP_200_OK)

    def read_all_attendancest(self, request):

        queryset = Attendance.objects.all()
        serialized = AttendanceSerializer(queryset, many=True)
        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=AttendanceSerializer, responses={200: AttendanceSerializer}
    )
    def create_attendances(self, request):

        serialized = AttendanceSerializer(data=request.data, many=True)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=AttendanceDeleteSerializer,
        responses={200: AttendanceDeleteSerializer},
    )
    def delete_attendances(self, request):

        serialized = AttendanceDeleteSerializer(data=request.data)

        if serialized.is_valid():

            Attendance.objects.filter(id__in=request.data["attendance_ids"]).delete()

            return Response(data=request.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_200_OK)


class EmployeeCheckinViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        request_body=EmployeeCheckinSerializer,
        responses={200: EmployeeCheckinSerializer},
    )
    def create_employee_checkin(self, request):
        try:
            employee_id = request.data["employee"]
            checked_in = request.data["checked_in"]
            is_first_session = request.data["is_first_session"]
        except:
            return Response(
                {"Message": "Request Body incorrect"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        employee = Employee.objects.get(id=employee_id)

        date = checked_in[0:10]
        try:
            attendance = Attendance.objects.get(
                attendance_date=date, fk_employee=employee_id
            )
        except Attendance.DoesNotExist:

            e_check = EmployeeCheckin(
                checked_in=request.data["checked_in"],
                fk_employee=employee,
                is_first_session=is_first_session,
            )
            e_check.save()
            a = Attendance(fk_employee=employee, attendance_date=date)
            a.save()
            a.fk_checks.add(e_check)
            a.save()
            return Response(status=status.HTTP_200_OK)

        serialized = EmployeeCheckinSerializer(data=request.data)

        if serialized.is_valid():

            a = EmployeeCheckin.objects.filter(employee=employee_id).latest(
                "checked_in"
            )

            if a.checked_out is not None:
                serialized.save()
                e = EmployeeCheckin.objects.latest("checked_in")
                attendance.fk_checks.add(e)
                return Response(data=serialized.data, status=status.HTTP_200_OK)
            else:

                return Response(
                    {"Message": "Check out of existing session"},
                    status=status.HTTP_200_OK,
                )

    @swagger_auto_schema(
        request_body=EmployeeCheckoutSerializer,
        responses={200: EmployeeCheckoutSerializer},
    )
    def create_employee_checkout(self, request):

        try:
            employee_id = request.data["employee"]
            checked_out = request.data["checked_out"]
            is_last_session = request.data["is_last_session"]
        except:
            return Response(
                {"Message": "Request Body incorrect"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:

            e = EmployeeCheckin.objects.filter(employee=employee_id).latest(
                "checked_in"
            )

        except EmployeeCheckin.DoesNotExist:

            return Response({"Message": "No checkin for the employee found"})

        if e.checked_out is None:
            e.checked_out = checked_out
            e.total_time_elapsed = (
                2  # * TODO change variable name to time_elapsed_in_hours
            )
            e.is_last_session = is_last_session
            # print(e.checked_out - e.checked_in)
            e.save()

            if is_last_session:
                print(e.checked_in)
                print(type(e.checked_in))

                print(e.checked_in.date())
                date = e.checked_in.date()

                employee = Employee.objects.get(id=employee_id)
                workhours = employee.designation.schedule.total_work_hours
                a = Attendance.objects.get(
                    attendance_date=date, fk_employee=employee_id
                )

                time_worked = EmployeeCheckin.objects.filter(
                    checked_in__date=date
                ).aggregate(Sum("total_time_elapsed"))
                print(time_worked)

                a.total_time = time_worked[
                    "total_time_elapsed__sum"
                ]  # change variable name to time_elapsed_in_hours
                ot = time_worked["total_time_elapsed__sum"] - workhours

                if ot > 0:

                    a.total_overtime = ot

                a.save()

            return Response(status=status.HTTP_200_OK)
        else:

            return Response(
                {"Message": "Already checked out of existing session"},
                status=status.HTTP_200_OK,
            )

    @swagger_auto_schema(responses={200: EmployeeCheckinSerializer})
    def read_employeecheckins(self, request):

        queryset = EmployeeCheckin.objects.filter(id=request.GET.get("id", ""))
        serialized = EmployeeCheckinSerializer(queryset, many=True)
        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=EmployeeCheckinSerializer,
        responses={200: EmployeeCheckinSerializer},
    )
    def create_employeecheckincheckout(self, request):

        serialized = EmployeeCheckinCheckoutSerializer(data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=EmployeeCheckinCheckoutDeleteSerializer,
        responses={200: EmployeeCheckinCheckoutDeleteSerializer},
    )
    def delete_attendances(self, request):

        serialized = EmployeeCheckinCheckoutDeleteSerializer(data=request.data)

        if serialized.is_valid():

            EmployeeCheckin.objects.filter(
                id__in=request.data["attendance_ids"]
            ).delete()

            return Response(data=request.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_200_OK)


######################################################## Leave Viewsets #################################


class LeavePolicyViewSet(viewsets.ViewSet):
    def leave_policy_generation(self, request, designation_id):

        des_id = designation_id

        try:
            designation = Designation.objects.get(id=des_id)
        except:
            return Response(
                {"Message": "No designation found"}, status=status.HTTP_400_BAD_REQUEST
            )
        if designation.leavepolicy is None:

            lp = LeavePolicy()
            lp.save()
            designation.leavepolicy = lp
            designation.save()
            # lp_id = lp.leavepolicy_id
            for member in request.data:
                member["leave_policy"] = lp.leavepolicy_id
            serialized = LeavePolicy_TypeMembershipSerializer(
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
                {"Message": "Leave Policy already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def update_leave_policies(self, request):

        try:
            leavepolicy = request.data["leavepolicy_id"]

        except:

            return Response({"Message": "No data"}, status=status.HTTP_400_BAD_REQUEST)

        queryset = LeavePolicy.objects.get(id=leavepolicy)

        serialized = LeavePolicySerializer(queryset, request.data, partial=True)

        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={200: LeavePolicySerializer})
    def read_leave_policies(self, request):

        try:
            queryset = LeavePolicy.objects.all()
        except:
            return Response({"Message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        serialized = LeavePolicySerializer(queryset, many=True)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=LeavePolicySerializer, responses={200: LeavePolicySerializer}
    )
    def create_leave_policies(self, request):

        serialized = LeavePolicySerializer(data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=LeavePolicyDeleteSerializer,
        responses={200: LeavePolicyDeleteSerializer},
    )
    def delete_leavepolicies(self, request):

        serialized = LeavePolicyDeleteSerializer(data=request.data)

        if serialized.is_valid():

            LeavePolicy.objects.filter(
                id__in=request.data["leavepolicy_ids"]
            ).delete()

            return Response(data=request.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_200_OK)


# LORAN
class LeaveApplicationViewSet(viewsets.ViewSet):
    def accept_applications(self, request):
        try:
            accepted_ids = request.data["accepted_ids"]
        except:
            return Response({"Message", "specify accepted ids"})
        employee = Employee.objects.get(id=accepted_ids)
        # aceepted = LeaveApplication.objects.filter(accepted_ids__in=employee.update(status='Approved'))
        try:
            leave_ids = LeaveApplication.objects.filter(id__in=accepted_ids)
            accept = LeaveApplication.objects.filter(
                accepted_ids=employee.update(status="Approved")
            )
            serialized = LeaveApplicationSerializer(accept, many=True)
            return Response(data=serialized.data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def read_leaveapplications_employee(self, request, emp_id):
        if isinstance(emp_id, uuid.UUID):

            id = emp_id

            queryset = LeaveApplication.objects.filter(employee=emp_id)
            serialized = LeaveApplicationSerializer(queryset, many=True)
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        else:

            return Response(
                {"Message": "UUID Format wrong"}, status=status.HTTP_400_BAD_REQUEST
            )

    def update_leavesapplications(self, request):

        try:
            leaveapplication = request.data["leaveapplication_id"]

        except:

            return Response({"Message": "No data"}, status=status.HTTP_400_BAD_REQUEST)

        queryset = LeaveApplication.objects.get(leaveapplication_id=leaveapplication)

        serialized = LeaveApplicationSerializer(queryset, request.data, partial=True)

        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={200: LeaveApplicationSerializer})
    def read_leaveapplications(self, request):

        try:
            queryset = LeaveApplication.objects.all()
        except:
            return Response({"Message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        serialized = LeaveApplicationSerializer(queryset, many=True)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=LeaveApplicationSerializer,
        responses={200: LeaveApplicationSerializer},
    )
    def create_leavesapplications(self, request):

        serialized = LeaveApplicationSerializer(data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=LeaveApplicationDeleteSerializer,
        responses={200: LeaveApplicationDeleteSerializer},
    )
    def delete_leavesapplications(self, request):

        serialized = LeaveApplicationDeleteSerializer(data=request.data)

        if serialized.is_valid():

            LeaveApplication.objects.filter(
                id__in=request.data["leaveapplication_ids"]
            ).delete()

            return Response(data=request.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_200_OK)


class LeaveViewSet(viewsets.ViewSet):
    @swagger_auto_schema(request_body=LeaveSerializer, responses={200: LeaveSerializer})
    def update_leaves(self, request):

        try:
            leave = request.data["leave_id"]

        except:

            return Response({"Message": "No data"}, status=status.HTTP_400_BAD_REQUEST)

        queryset = Leave.objects.get(leave_id=leave)

        serialized = LeaveSerializer(queryset, request.data, partial=True)

        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={200: LeaveSerializer})
    def read_leave(self, request):

        try:
            queryset = Leave.objects.all()
        except:
            return Response({"Message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        serialized = LeaveSerializer(queryset, many=True)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=LeaveSerializer, responses={200: LeaveSerializer})
    def create_leave(self, request):

        serialized = LeaveSerializer(data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=LeaveDeleteSerializer, responses={200: LeaveDeleteSerializer}
    )
    def delete_leave(self, request):

        serialized = LeaveDeleteSerializer(data=request.data)

        if serialized.is_valid():

            Leave.objects.filter(
                id__in=request.data["leave_ids"]
            ).delete()

            return Response(data=request.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_200_OK)


class ScheduleViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        request_body=ScheduleSerializer, responses={200: ScheduleSerializer}
    )
    def update_schedules(self, request):

        try:
            schedule = request.data["id"]

        except:

            return Response({"Message": "No data"}, status=status.HTTP_400_BAD_REQUEST)

        queryset = Schedule.objects.get(schedule_id=schedule)

        serialized = ScheduleSerializer(queryset, request.data, partial=True)

        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={200: ScheduleSerializer})
    def read_schedules(self, request):

        try:
            queryset = Schedule.objects.all()
        except:
            return Response({"Message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        serialized = ScheduleSerializer(queryset, many=True)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=ScheduleSerializer, responses={200: ScheduleSerializer}
    )
    def create_schedules(self, request, des_id):

        designation_id = des_id

        try:

            designation = Designation.objects.get(designation_id=designation_id)

        except Designation.DoesNotExist:

            return Response(
                {{"Message": "No designation found"}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serialized = ScheduleSerializer(data=request.data)

        if serialized.is_valid():
            print(serialized.data)
            schedule = Schedule(**serialized.data)
            schedule.save()
            designation.schedule = schedule
            designation.save()

        return Response(data=serialized.errors, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=ScheduleDeleteSerializer, responses={200: ScheduleDeleteSerializer}
    )
    def delete_schedules(self, request):

        serialized = ScheduleDeleteSerializer(data=request.data)

        if serialized.is_valid():

            Schedule.objects.filter(
                id__in=request.data["schedule_ids"]
            ).delete()

            return Response(data=request.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_200_OK)


# class MonthlyReportViewSet(viewsets.ViewSet):
#     def update_monthlyreports(self, request):

#         try:
#             monthlyreport = request.data["monthlyreport_id"]

#         except:

#             return Response({"Message": "No data"}, status=status.HTTP_400_BAD_REQUEST)

#         queryset = MonthlyReport.objects.get(monthlyreport_id=monthlyreport)

#         serialized = MonthlyReportSerializer(queryset, request.data, partial=True)

#         if serialized.is_valid():
#             serialized.save()
#             return Response(data=serialized.data, status=status.HTTP_200_OK)

#         return Response(data=serialized.errors, status=status.HTTP_200_OK)

#     def read_monthly_reports(self, request):

#         try:
#             queryset = MonthlyReport.objects.all()
#         except:
#             return Response({"Message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

#         serialized = MonthlyReportSerializer(queryset, many=True)
#         if serialized.is_valid():
#             serialized.save()
#             return Response(data=serialized.data, status=status.HTTP_200_OK)

#         return Response(data=serialized.errors, status=status.HTTP_200_OK)

#     def create_monthly_reports(self, request):

#         serialized = MonthlyReportSerializer(data=request.data)
#         if serialized.is_valid():
#             serialized.save()
#             return Response(data=serialized.data, status=status.HTTP_200_OK)

#         return Response(data=serialized.errors, status=status.HTTP_200_OK)

#     def delete_monthly_reports(self, request):

#         MonthlyReport.objects.filter(id__in=request.data["monthlyreport_ids"]).delete()

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
#             return Response({"Message" : "No data"}, status = status.HTTP_400_BAD_REQUEST)
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
#             return Response({"Message" : "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND )

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

#         Calendar.objects.filter(date__in = request.data["dates"]).delete()

#         return Response(data=request.data, status= status.HTTP_200_OK)


# class EventsViewset(viewsets.ViewSet):


#     def update_events(self, request):

#         try:
#             event_id = request.data["event_id"]
#         except:
#             return Response({"Message" : "No data"}, status = status.HTTP_400_BAD_REQUEST)
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
#             return Response({"Message" : "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND )

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

#         Events.objects.filter(event_id__in = request.data["event_ids"]).delete()

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


# if(request.GET.get('isFilter',False)):

#     start_date_req = request.GET.get("start_date",datetime.date.today())
#     end_date_req = request.GET.get("end_date", datetime.date.today())
#     queryset=Attendance.objects.filter(id=id,daterange=["attendance_datedate=start_date_req","attendance_date__date=end_date_req"])
#     serialized = AttendanceSerializer(queryset, many = True)
#     return Response(data=serialized.data, status= status.HTTP_200_OK)

# good job on date range
# else:

#    queryset = Attendance.objects.filter(employee = id)
#    serialized = AttendanceSerializer(queryset, many = True)
#    return Response(data=serialized.data, status= status.HTTP_200_OK)
