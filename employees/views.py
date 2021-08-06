from django.db.models.query import QuerySet
from django.shortcuts import render
from rest_framework import generics, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.db.models import Sum

# from datetime import datetime
import datetime

#default value of detail, methods array,

# project imports
from rest_framework.decorators import action

from .models import *
from .serializers import *

from drf_yasg.utils import swagger_auto_schema


class EmployeeViewSet(viewsets.ViewSet):
    @swagger_auto_schema(responses={200: EmployeeSerializer})
    @action(detail=False, methods=["get"], url_path="read")
    def read_employees(self, request):

        try:
            queryset = Employee.objects.all()
        except:
            return Response({"Message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        try:
            serialized = EmployeeSerializer(instance=queryset, many=True)
        except:
            return Response(
                {"Message": "Serializer error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=EmployeeSerializer, responses={200: EmployeeSerializer}
    )
    @action(detail=False, methods=["patch"], url_path="update")
    def update_employees(self, request):

        try:
            employee = request.data["id"]

        except:

            return Response(
                {"Message": "Request body incorrect. Please specify ID."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        queryset = Employee.objects.get(id=employee)

        serialized = EmployeeSerializer(queryset, request.data, partial=True)

        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="create")
    @swagger_auto_schema(
        request_body=EmployeeSerializer, responses={200: EmployeeSerializer}
    )
    def create_employees(self, request):

        serialized = EmployeeSerializer(data=request.data, many=True)

        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_200_OK)

    @action(detail=False, methods=["delete"], url_path="delete")
    @swagger_auto_schema(
        request_body=EmployeeDeleteSerializer, responses={200: EmployeeDeleteSerializer}
    )
    def delete_employees(self, request):

        serialized = EmployeeDeleteSerializer(data=request.data)

        if serialized.is_valid():
            Employee.objects.filter(id__in=request.data["employee_ids"]).delete()

            return Response(data=request.data, status=status.HTTP_200_OK)
        return Response(data=serialized.errors, status=status.HTTP_200_OK)

class CustomerViewSet(viewsets.ViewSet):
    @swagger_auto_schema(responses={200: CustomerSerializer})
    @action(detail=False, methods=["get"], url_path="read")
    def read_customers(self, request):

        try:
            queryset = Customer.objects.all()
        except:
            return Response({"Message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        try:
            serialized = CustomerSerializer(instance=queryset, many=True)
        except:
            return Response(
                {"Message": "Serializer error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=CustomerSerializer, responses={200: CustomerSerializer}
    )
    @action(detail=False, methods=["patch"], url_path="update")
    def update_customers(self, request):

        try:
            employee = request.data["id"]

        except:

            return Response(
                {"Message": "Request body incorrect. Please specify ID."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        queryset = Customer.objects.get(id=employee)

        serialized = CustomerSerializer(queryset, request.data, partial=True)

        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="create")
    @swagger_auto_schema(
        request_body=CustomerSerializer, responses={200: CustomerSerializer}
    )
    def create_customers(self, request):

        serialized = CustomerSerializer(data=request.data, many=True)

        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_200_OK)

    @action(detail=False, methods=["delete"], url_path="delete")
    @swagger_auto_schema(
        request_body=CustomerDeleteSerializer, responses={200: CustomerDeleteSerializer}
    )
    def delete_customers(self, request):

        serialized = CustomerDeleteSerializer(data=request.data)

        if serialized.is_valid():
            Customer.objects.filter(id__in=request.data["customer_ids"]).delete()

            return Response(data=request.data, status=status.HTTP_200_OK)
        return Response(data=serialized.errors, status=status.HTTP_200_OK)
# LORAN
class EmployeeGroupViewSet(viewsets.ViewSet):

    @action(detail=True, methods=["get"], url_path="read_employees")
    @swagger_auto_schema(responses={200: DesignationSerializer})
    def read_employee_group_employees(self, request, pk):

        try:
            queryset = Employee.objects.filter(fk_employee_group=pk)
        except:
            return Response({"Message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        serialized = EmployeeSerializer(instance=queryset, many=True)

        return Response(data=serialized.data, status=status.HTTP_200_OK)


    @action(detail=False, methods=["patch"], url_path="update")
    @swagger_auto_schema(
        request_body=EmployeeGroupSerializer, responses={200: EmployeeGroupSerializer}
    )
    def update_employee_group(self, request):

        try:
            employeegroup = request.data["id"]

        except:

            return Response(
                {"Message": "No ID in request data"}, status=status.HTTP_400_BAD_REQUEST
            )

        queryset = EmployeeGroup.objects.get(id=employeegroup)

        serialized = EmployeeGroupSerializer(queryset, request.data, partial=True)

        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="read")
    @swagger_auto_schema(responses={200: EmployeeGroupSerializer})
    def read_employee_group(self, request):

        try:
            queryset = EmployeeGroup.objects.all()
        except:
            return Response({"Message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        try:
            serialized = EmployeeGroupSerializer(instance=queryset, many=True)
        except:
            return Response(
                {"Message": "Serializer error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="create")
    @swagger_auto_schema(
        request_body=EmployeeGroupSerializer, responses={200: EmployeeGroupSerializer}
    )
    def create_employee_group(self, request):

        serialized = EmployeeGroupSerializer(data=request.data, many=True)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_200_OK)

    @action(detail=False, methods=["delete"], url_path="delete")
    @swagger_auto_schema(
        request_body=EmployeeGroupDeleteSerializer,
        responses={200: EmployeeGroupDeleteSerializer},
    )
    def delete_employee_group(self, request):

        serialized = EmployeeGroupDeleteSerializer(data=request.data)

        if serialized.is_valid():
            EmployeeGroup.objects.filter(id__in=request.data["group_ids"]).delete()

            return Response(data=request.data, status=status.HTTP_200_OK)
        return Response(data=serialized.errors, status=status.HTTP_200_OK)


# LORAN
class DepartmentViewSet(viewsets.ViewSet):
    @action(detail=True, methods=["get"], url_path="read_employees")
    @swagger_auto_schema(responses={200: EmployeeSerializer})
    def read_department_employees(self, request, pk):

        try:
            queryset = Employee.objects.filter(fk_department=pk)
        except:
            return Response({"Message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        serialized = EmployeeSerializer(instance=queryset, many=True)

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["patch"], url_path="update")
    @swagger_auto_schema(
        request_body=DepartmentSerializer, responses={200: DepartmentSerializer}
    )
    def update_departments(self, request):

        try:
            department = request.data["id"]

        except:

            return Response(
                {"Message": "Request body incorrect. Please specify  ID."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        queryset = Department.objects.get(id=department)

        serialized = DepartmentSerializer(queryset, request.data, partial=True)

        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="read")
    @swagger_auto_schema(responses={200: DepartmentSerializer})
    def read_department(self, request):

        try:
            queryset = Department.objects.all()
        except:
            return Response({"Message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        serialized = DepartmentSerializer(instance=queryset, many=True)

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="create")
    @swagger_auto_schema(
        request_body=DepartmentSerializer, responses={200: DepartmentSerializer}
    )
    def create_department(self, request):

        serialized = DepartmentSerializer(data=request.data, many=True)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_200_OK)

    @action(detail=False, methods=["delete"], url_path="delete")
    @swagger_auto_schema(
        request_body=DepartmentDeleteSerializer,
        responses={200: DepartmentDeleteSerializer},
    )
    def delete_department(self, request):

        serialized = DepartmentDeleteSerializer(data=request.data)

        if serialized.is_valid():
            Department.objects.filter(id__in=request.data["department_ids"]).delete()

            return Response(data=request.data, status=status.HTTP_200_OK)
        return Response(data=serialized.errors, status=status.HTTP_200_OK)


# LORAN
class DesignationViewSet(viewsets.ViewSet):
    @action(detail=True, methods=["get"], url_path="read_employees")
    @swagger_auto_schema(responses={200: DesignationSerializer})
    def read_designation_employees(self, request, pk):

        try:
            queryset = Employee.objects.filter(fk_designation=pk)
        except:
            return Response({"Message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        serialized = EmployeeSerializer(instance=queryset, many=True)

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["patch"], url_path="update")
    @swagger_auto_schema(
        request_body=DesignationSerializer, responses={200: DesignationSerializer}
    )
    def update_designations(self, request):

        try:
            designation = request.data["id"]

        except:

            return Response(
                {"Message": "Request body incorrect. Please specify  ID."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        queryset = Designation.objects.get(id=designation)

        serialized = DesignationSerializer(queryset, request.data, partial=True)

        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="read")
    @swagger_auto_schema(responses={200: DesignationSerializer})
    def read_designations(self, request):

        try:
            queryset = Designation.objects.all()
        except:
            return Response({"Message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        serialized = DesignationSerializer(instance=queryset, many=True)

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="create")
    @swagger_auto_schema(
        request_body=DesignationSerializer, responses={200: DesignationSerializer}
    )
    def create_designations(self, request):

        serialized = DesignationSerializer(data=request.data, many=True)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_200_OK)

    @action(detail=False, methods=["delete"], url_path="delete")
    @swagger_auto_schema(
        request_body=DesignationDeleteSerializer,
        responses={200: DesignationDeleteSerializer},
    )
    def delete_designations(self, request):

        serialized = DesignationDeleteSerializer(data=request.data)

        if serialized.is_valid():
            Designation.objects.filter(id__in=request.data["designation_ids"]).delete()

            return Response(data=request.data, status=status.HTTP_200_OK)
        return Response(data=serialized.errors, status=status.HTTP_200_OK)


class IdentificationDocumentViewSet(viewsets.ViewSet):
    @action(detail=False, methods=["patch"], url_path="update")
    @swagger_auto_schema(
        request_body=IdentificationDocumentSerializer,
        responses={200: IdentificationDocumentSerializer},
    )
    def update_identificationdocuments(self, request):

        try:
            identificationdoc = request.data["id"]

        except:

            return Response(
                {"Message": "Request body incorrect. Please specify  ID."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        queryset = IdentificationDocument.objects.get(id=identificationdoc)

        serialized = IdentificationDocumentSerializer(
            queryset, request.data, partial=True
        )

        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="read")
    @swagger_auto_schema(responses={200: IdentificationDocumentSerializer})
    def read_identificationdocuments(self, request):

        try:
            queryset = IdentificationDocument.objects.all()
        except:
            return Response({"Message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        try:
            serialized = IdentificationDocumentSerializer(instance=queryset, many=True)
        except:
            return Response(
                {"Message": "Serializer error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="create")
    @swagger_auto_schema(
        request_body=IdentificationDocumentSerializer,
        responses={200: IdentificationDocumentSerializer},
    )
    def create_identificationdocuments(self, request):

        serialized = IdentificationDocumentSerializer(data=request.data, many=True)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_200_OK)

    @action(detail=False, methods=["delete"], url_path="delete")
    @swagger_auto_schema(
        request_body=IdentificationDocumentDeleteSerializer,
        responses={200: IdentificationDocumentDeleteSerializer},
    )
    def delete_identificationdocuments(self, request):

        serialized = IdentificationDocumentDeleteSerializer(data=request.data)

        if serialized.is_valid():
            IdentificationDocument.objects.filter(
                id__in=request.data["identificationdocument_ids"]
            ).delete()

            return Response(data=request.data, status=status.HTTP_200_OK)
        return Response(data=serialized.errors, status=status.HTTP_200_OK)


class IdentificationTypeViewSet(viewsets.ViewSet):
    @action(detail=False, methods=["patch"], url_path="update")
    @swagger_auto_schema(
        request_body=IdentificationTypeSerializer,
        responses={200: IdentificationTypeSerializer},
    )
    def update_identificationtypes(self, request):

        try:
            designation = request.data["designation_id"]

        except:

            return Response(
                {"Message": "Request body incorrect. Please specify  ID."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        queryset = IdentificationType.objects.get(id=designation)

        serialized = IdentificationTypeSerializer(queryset, request.data, partial=True)

        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="read")
    @swagger_auto_schema(responses={200: IdentificationTypeSerializer})
    def read_identificationtypes(self, request):

        try:
            queryset = IdentificationType.objects.all()
        except:
            return Response({"Message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        try:
            serialized = IdentificationTypeSerializer(instance=queryset, many=True)
        except:
            return Response(
                {"Message": "Serializer error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="create")
    @swagger_auto_schema(
        request_body=IdentificationTypeSerializer,
        responses={200: IdentificationTypeSerializer},
    )
    def create_identificationtypes(self, request):

        serialized = IdentificationTypeSerializer(data=request.data, many=True)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_200_OK)

    @action(detail=False, methods=["delete"], url_path="delete")
    @swagger_auto_schema(
        request_body=IdentificationTypeDeleteSerializer,
        responses={200: IdentificationTypeDeleteSerializer},
    )
    def delete_identificationtypes(self, request):

        serialized = IdentificationTypeDeleteSerializer(data=request.data)

        if serialized.is_valid():
            IdentificationType.objects.filter(
                id__in=request.data["identificationtype_ids"]
            ).delete()

            return Response(data=request.data, status=status.HTTP_200_OK)
        return Response(data=serialized.errors, status=status.HTTP_200_OK)


# LORAN
class AttendanceViewSet(viewsets.ViewSet):
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
                {"Message": "Enter start date and end date"},
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
                {"Message": "Enter start date and end date"},
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

        serialized = AttendanceSerializer(data=request.data, many=True)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_200_OK)

    @action(detail=False, methods=["delete"], url_path="delete")
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


class EmployeeSessionViewSet(viewsets.ViewSet):

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
                {"Message": "Request Body incorrect"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        employee = Employee.objects.get(id=employee_id)

        date = datetime.datetime.strptime(checked_in, "%Y-%m-%d %H:%M:%S")
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
                    {"Message": "Check out of existing session"},
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
                {"Message": "Request Body incorrect"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:

            session = EmployeeSession.objects.filter(fk_employee=employee_id).latest(
                "checked_in_at"
            )

        except EmployeeSession.DoesNotExist:

            return Response({"Message": "No checkin for the employee found"})

        if session.checked_out_at is None:

            checked_in_date = datetime.datetime.strptime(session.checked_out_time, "%Y-%m-%d %H:%M:%S")
            checked_out_date = datetime.datetime.strptime(session.checked_out_time, "%Y-%m-%d %H:%M:%S")
            if (checked_out_date.day)>(checked_in_date.day):

                bridgetime = datetime.datetime(checked_out_date.year,checked_out_date.month,checked_out_date.day,0,0,0)

                session.checked_out_at = bridgetime

                session.save()

                autosession = EmployeeSession(fk_employee = employee_id, checked_in_at = bridgetime, checked_out_at = checked_out_date)

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
                {"Message": "Already checked out of existing session"},
                status=status.HTTP_200_OK,
            )

    @action(detail=False, methods=["get"], url_path="read")
    @swagger_auto_schema(responses={200: EmployeeSessionSerializer})
    def read_employee_sessions(self, request):

        queryset = EmployeeSession.objects.filter(id=request.GET.get("id", ""))
        serialized = EmployeeSessionCheckoutSerializer(instance=queryset, many=True)
        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="create")
    @swagger_auto_schema(
        request_body=EmployeeSessionSerializer,
        responses={200: EmployeeSessionSerializer},
    )
    def create_employee_sessions(self, request):

        serialized = EmployeeSessionSerializer(data=request.data, many=True)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_200_OK)

    @action(detail=False, methods=["delete"], url_path="delete")
    @swagger_auto_schema(
        request_body=EmployeeSessionDeleteSerializer,
        responses={200: EmployeeSessionDeleteSerializer},
    )
    def delete_employee_sessions(self, request):

        serialized = EmployeeSessionDeleteSerializer(data=request.data)

        if serialized.is_valid():

            EmployeeSession.objects.filter(
                id__in=request.data["attendance_ids"]
            ).delete()

            return Response(data=request.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_200_OK)


######################################################## Leave Viewsets #################################


class LeavePolicyViewSet(viewsets.ViewSet):
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
                {"Message": "No designation found"}, status=status.HTTP_400_BAD_REQUEST
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
                {"Message": "Leave Policy already exists"},
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
                {"Message": "Request body incorrect. Please specify  ID."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        queryset = LeavePolicy.objects.get(id=leavepolicy)

        serialized = LeavePolicySerializer(queryset, request.data, partial=True)

        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="read")
    @swagger_auto_schema(responses={200: LeavePolicySerializer})
    def read_leave_policies(self, request):

        try:
            queryset = LeavePolicy.objects.all()
        except:
            return Response({"Message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

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

        return Response(data=serialized.errors, status=status.HTTP_200_OK)

    @action(detail=False, methods=["delete"], url_path="delete")
    @swagger_auto_schema(
        request_body=LeavePolicyDeleteSerializer,
        responses={200: LeavePolicyDeleteSerializer},
    )
    def delete_leave_policies(self, request):

        serialized = LeavePolicyDeleteSerializer(data=request.data)

        if serialized.is_valid():

            LeavePolicy.objects.filter(id__in=request.data["leavepolicy_ids"]).delete()

            return Response(data=request.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_200_OK)


# LORAN
class LeaveApplicationViewSet(viewsets.ViewSet):
    @action(detail=False, methods=["post"], url_path="accept_applications")
    def accept_applications(self, request):
        try:
            accepted_ids = request.data["accepted_ids"]
        except:
            return Response({"Message": "specify accepted ids"})

        try:
            LeaveApplication.objects.filter(id__in=accepted_ids).update(
                status="Approved"
            )

        except ValueError:
            print(ValueError)
            return Response(
                {"Message": "Bad request, check body"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        for app_id in accepted_ids:

            leaves = LeaveApplicationTypeMembership.objects.filter(fk_leave_application = app_id)

            for leave in leaves:

                leave = Leave(fk_employee = leave.fk_leave_application.fk_employee, fk_leave_type = leave.fk_leave_type, from_date = leave.from_date, to_date = leave.to_date)
                leave.save()

        return Response(data = request.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="reject_applications")
    def reject_applications(self, request):
        try:
            rejected_ids = request.data["rejected_ids"]
        except:
            return Response({"Message": "specify rejected ids"})

        try:
            LeaveApplication.objects.filter(id__in=rejected_ids).update(
                status="Rejected"
            )

            return Response(data=request.data)
        except ValueError:
            print(ValueError)
            return Response(
                {"Message": "Bad request, check body"},
                status=status.HTTP_400_BAD_REQUEST,
            )
    @action(detail=True, methods=["post"], url_path="read_employee_applications")
    def read_leave_applications_employee(self, request, pk):
       
        queryset = LeaveApplication.objects.filter(fk_employee=pk)
        serialized = LeaveApplicationSerializer(instance=queryset, many=True)
        return Response(data=serialized.data, status=status.HTTP_200_OK)

        

    @action(detail=False, methods=["patch"], url_path="update")
    @swagger_auto_schema(
        request_body=LeaveApplicationSerializer,
        responses={200: LeaveApplicationSerializer},
    )
    def update_leave_applications(self, request):

        try:
            leaveapplication = request.data["leaveapplication_id"]

        except:

            return Response(
                {"Message": "Request body incorrect. Please specify  ID."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        queryset = LeaveApplication.objects.get(id=leaveapplication)

        serialized = LeaveApplicationSerializer(queryset, request.data, partial=True)

        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="read")
    @swagger_auto_schema(responses={200: LeaveApplicationSerializer})
    def read_leave_applications(self, request):

        try:
            queryset = LeaveApplication.objects.all()
        except:
            return Response({"Message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        serialized = LeaveApplicationSerializer(instance=queryset, many=True)

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="create")
    @swagger_auto_schema(
        request_body=CreateLeaveApplicationSerializer,
        responses={200: CreateLeaveApplicationSerializer},
    )
    def create_leave_applications(self, request):

        serialized = CreateLeaveApplicationSerializer(data=request.data, many=True)
        if serialized.is_valid():
            serialized.save()
            
            return Response(data = request.data, status=status.HTTP_200_OK)

        return Response(data = serialized.errors, status=status.HTTP_200_OK)

    @action(detail=False, methods=["delete"], url_path="delete")
    @swagger_auto_schema(
        request_body=LeaveApplicationDeleteSerializer,
        responses={200: LeaveApplicationDeleteSerializer},
    )
    def delete_leave_applications(self, request):

        serialized = LeaveApplicationDeleteSerializer(data=request.data)

        if serialized.is_valid():

            LeaveApplication.objects.filter(
                id__in=request.data["leaveapplication_ids"]
            ).delete()

            return Response(data=request.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_200_OK)


class LeaveViewSet(viewsets.ViewSet):

    @action(detail=True, methods=["post"], url_path="read_employee_leaves")
    def read_leaves_employee(self, request, pk):
       
        try:

            start_date_req = request.GET.get("start_date")
            end_date_req = request.GET.get("end_date")
            queryset = Leave.objects.filter(
                from_date__range=[start_date_req, end_date_req],
                to_date__range=[start_date_req, end_date_req],
                fk_employee = pk
            )
            serialized = LeaveSerializer(instance=queryset, many=True)
            return Response(data=serialized.data, status=status.HTTP_200_OK)
        except:
            return Response(
                {"Message": "Enter start date and end date"},
                status=status.HTTP_400_BAD_REQUEST,
            )


    @action(detail=False, methods=["patch"], url_path="update")
    @swagger_auto_schema(request_body=LeaveSerializer, responses={200: LeaveSerializer})
    def update_leaves(self, request):

        try:
            leave = request.data["leave_id"]

        except:

            return Response(
                {"Message": "Request body incorrect. Please specify  ID."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        queryset = Leave.objects.get(leave_id=leave)

        serialized = LeaveSerializer(queryset, request.data, partial=True)

        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="read")
    @swagger_auto_schema(responses={200: LeaveSerializer})
    def read_leaves(self, request):

        try:
            queryset = Leave.objects.all()
        except:
            return Response({"Message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        serialized = LeaveSerializer(instance=queryset, many=True)

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="create")
    @swagger_auto_schema(request_body=LeaveSerializer, responses={200: LeaveSerializer})
    def create_leaves(self, request):

        serialized = LeaveSerializer(data=request.data, many=True)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_200_OK)

    @action(detail=False, methods=["delete"], url_path="delete")
    @swagger_auto_schema(
        request_body=LeaveDeleteSerializer, responses={200: LeaveDeleteSerializer}
    )
    def delete_leaves(self, request):

        serialized = LeaveDeleteSerializer(data=request.data)

        if serialized.is_valid():

            Leave.objects.filter(id__in=request.data["leave_ids"]).delete()

            return Response(data=request.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_200_OK)


class ScheduleViewSet(viewsets.ViewSet):
    @action(detail=False, methods=["patch"], url_path="update")
    @swagger_auto_schema(
        request_body=ScheduleSerializer, responses={200: ScheduleSerializer}
    )
    def update_schedules(self, request):

        try:
            schedule = request.data["id"]

        except:

            return Response(
                {"Message": "Request body incorrect. Please specify  ID."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        queryset = Schedule.objects.get(id=schedule)

        serialized = ScheduleSerializer(queryset, request.data, partial=True)

        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="read")
    @swagger_auto_schema(responses={200: ScheduleSerializer})
    def read_schedules(self, request):

        try:
            queryset = Schedule.objects.all()
        except:
            return Response({"Message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        serialized = ScheduleSerializer(instance=queryset, many=True)

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="create")
    @swagger_auto_schema(
        request_body=ScheduleSerializer, responses={200: ScheduleSerializer}
    )
    def create_schedules(self, request, des_id):

        designation_id = des_id

        try:

            designation = Designation.objects.get(id=designation_id)

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
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_200_OK)

    @action(detail=False, methods=["delete"], url_path="delete")
    @swagger_auto_schema(
        request_body=ScheduleDeleteSerializer, responses={200: ScheduleDeleteSerializer}
    )
    def delete_schedules(self, request):

        serialized = ScheduleDeleteSerializer(data=request.data)

        if serialized.is_valid():

            Schedule.objects.filter(id__in=request.data["schedule_ids"]).delete()

            return Response(data=request.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_200_OK)



class WorkdayDivisionViewSet(viewsets.ViewSet):
    @action(detail=False, methods=["patch"], url_path="update")
    @swagger_auto_schema(request_body=WorkdayDivisionSerializer, responses={200: WorkdayDivisionSerializer})
    def update_workday_divisons(self, request):

        try:
            leave = request.data["leave_id"]

        except:

            return Response(
                {"Message": "Request body incorrect. Please specify  ID."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        queryset = WorkdayDivision.objects.get(leave_id=leave)

        serialized = WorkdayDivisionSerializer(queryset, request.data, partial=True)

        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="read")
    @swagger_auto_schema(responses={200: WorkdayDivisionSerializer})
    def read_workday_divisons(self, request):

        try:
            queryset = WorkdayDivision.objects.all()
        except:
            return Response({"Message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        serialized = WorkdayDivisionSerializer(instance=queryset, many=True)

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="create")
    @swagger_auto_schema(request_body=WorkdayDivisionSerializer, responses={200: WorkdayDivisionSerializer})
    def create_workday_divisons(self, request):

        serialized = WorkdayDivisionSerializer(data=request.data, many=True)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_200_OK)

    @action(detail=False, methods=["delete"], url_path="delete")
    @swagger_auto_schema(
        request_body=WorkdayDivisionDeleteSerializer, responses={200: WorkdayDivisionDeleteSerializer}
    )
    def delete_workday_divisions(self, request):

        serialized = WorkdayDivisionDeleteSerializer(data=request.data)

        if serialized.is_valid():

            WorkdayDivision.objects.filter(id__in=request.data["leave_ids"]).delete()

            return Response(data=request.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_200_OK)





# class MonthlyReportViewSet(viewsets.ViewSet):
#     def update_monthlyreports(self, request):

#         try:
#             monthlyreport = request.data["monthlyreport_id"]

#         except:

#             return Response({"Message": "Request body incorrect. Please specify  ID."}, status=status.HTTP_400_BAD_REQUEST)

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
#             return Response({"Message" : "Request body incorrect. Please specify  ID."}, status = status.HTTP_400_BAD_REQUEST)
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
#             return Response({"Message" : "Request body incorrect. Please specify  ID."}, status = status.HTTP_400_BAD_REQUEST)
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
