from rest_framework import routers
from .views import *
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r"employees", EmployeeViewSet, basename="employees")
router.register(r"employee_grades", EmployeeGradeViewSet, basename="employee_grades")
router.register(r"companies", CompanyViewSet, basename="companies")
router.register(r"departments", DepartmentViewSet, basename="departments")
router.register(r"designations", DesignationViewSet, basename="designations")
router.register(r"employee_groups", EmployeeGroupViewSet, basename="employee_groups")
router.register(r"leave_policies", LeavePolicyViewSet, basename="leave_policies")
router.register(r"leave_applications", LeaveApplicationViewSet, basename="leave_applications")
router.register(r"leaves", LeaveViewSet, basename="leaves")
router.register(r"identification_docs", IdentificationDocumentViewSet, basename="identification_docs")
router.register(r"identification_types", IdentificationTypeViewSet, basename="identification_types")
router.register(r"attendances", AttendanceViewSet, basename="attendances")
router.register(r"schedules", ScheduleViewSet, basename="schedules")
router.register(r"employee_leave_reports", EmployeeLeaveReportViewSet, basename="employee_leave_reports")
router.register(r"day_lists", DaysListViewSet, basename="day_lists")
router.register(r"employee_sessions", EmployeeSessionViewSet, basename="employee_sessions")
router.register(r"customers", CustomerViewSet, basename="customers")
router.register(r"compensate_leave_applications", CompensateLeaveApplicationViewSet, basename="compensate_leave_applications")
router.register(r"workday_division", WorkdayDivisionViewSet, basename="workday_division")

urlpatterns = [
    path('', include(router.urls)),
    path('', include('appraisal.urls'))
]









# urlpatterns = [
#     path(
#         "employees/create/",
#         EmployeeViewSet,
#     ),
#     path("employees/read/", EmployeeViewSet.as_view({"get": "read_employees"})),
#     path("employees/update/", EmployeeViewSet.as_view({"patch": "update_employee"})),
#     path("employees/delete/", EmployeeViewSet.as_view({"delete": "delete_employees"})),
#     ##############################################################################################################################################################################
#     path(
#         "employee_group/create/",
#         EmployeeGroupViewSet.as_view({"post": "create_employee_group"}),
#     ),
#     path(
#         "employee_group/read/",
#         EmployeeGroupViewSet.as_view({"get": "read_employee_group"}),
#     ),
#     path(
#         "employee_group/update/",
#         EmployeeGroupViewSet.as_view(
#             {"patch": "update_employee_group"}
#         ),  # TODO change names to have underscores
#     ),
#     path(
#         "employee_group/delete/",
#         EmployeeGroupViewSet.as_view({"delete": "delete_employee_group"}),
#     ),
#     ##########################################################
#     path(
#         "departments/create/",
#         DepartmentViewSet.as_view({"post": "create_department"}),
#     ),
#     path("departments/read/", DepartmentViewSet.as_view({"get": "read_department"})),
#     path(
#         "departments/update/",
#         DepartmentViewSet.as_view({"patch": "update_departments"}),
#     ),
#     path(
#         "departments/delete/",
#         DepartmentViewSet.as_view({"delete": "delete_department"}),
#     ),
#     path(
#         "departments/employees/<int:dept_id>",
#         DepartmentViewSet.as_view({"get": "read_department_employees"}),
#     ),
#     ##########################################################
#     path(
#         "designations/create/",
#         DesignationViewSet.as_view({"post": "create_designations"}),
#     ),
#     path(
#         "designations/read/",
#         DesignationViewSet.as_view({"get": "read_designations"}),
#     ),
#     path(
#         "designations/update/",
#         DesignationViewSet.as_view({"patch": "update_designations"}),
#     ),
#     path(
#         "designations/delete/",
#         DesignationViewSet.as_view({"delete": "delete_designations"}),
#     ),
#     path(
#         "designations/employees/<int:des_id>",
#         DesignationViewSet.as_view({"get": "read_designation_employees"}),
#     ),
#     ##########################################################
#     path(
#         "leavepolicies/create/",
#         LeavePolicyViewSet.as_view({"post": "create_leavepolicies"}),
#     ),
#     path(
#         "leavepolicies/update/",
#         LeavePolicyViewSet.as_view({"get": "read_leavepolicies"}),
#     ),
#     path(
#         "leavepolicies/read/",
#         LeavePolicyViewSet.as_view({"patch": "update_leavepolicies"}),
#     ),
#     path(
#         "leavepolicies/delete/",
#         LeavePolicyViewSet.as_view({"delete": "delete_leavepolicies"}),
#     ),
#     path(
#         "leavepolicies/generation/<int:designation_id>",
#         LeavePolicyViewSet.as_view({"post": "leave_policy_generation"}),
#     ),
#     ##########################################################
#     path(
#         "leave_applications/create/",
#         LeaveApplicationViewSet.as_view({"post": "create_leave_applications"}),
#     ),
#     path(
#         "leave_applications/read/",
#         LeaveApplicationViewSet.as_view({"get": "read_leave_applications"}),
#     ),
#     path(
#         "leave_applications/update/",
#         LeaveApplicationViewSet.as_view({"patch": "update_leave_applications"}),
#     ),
#     path(
#         "leave_applications/delete/",
#         LeaveApplicationViewSet.as_view({"delete": "delete_leave_applications"}),
#     ),
#     ##########################################################
#     path("leaves/create/", LeaveViewSet.as_view({"post": "create_leaves"})),
#     path("leaves/read/", LeaveViewSet.as_view({"get": "read_leaves"})),
#     path("leaves/update/", LeaveViewSet.as_view({"patch": "update_leaves"})),
#     path("leaves/delete/", LeaveViewSet.as_view({"delete": "delete_leaves"})),
#     ##########################################################
#     path(
#         "schedules/create/<int:des_id>",
#         ScheduleViewSet.as_view({"post": "create_schedules"}),
#     ),
#     path("schedules/read/", ScheduleViewSet.as_view({"get": "read_schedules"})),
#     path("schedules/update/", ScheduleViewSet.as_view({"patch": "update_schedules"})),
#     path(
#         "schedules/delete/",
#         ScheduleViewSet.as_view({"delete": "delete_schedules"}),
#     ),
#     ##########################################################
#     path(
#         "attendances/create/", AttendanceViewSet.as_view({"post": "create_attendances"})
#     ),
#     path("attendances/read/", AttendanceViewSet.as_view({"get": "read_attendances"})),
#     path(
#         "attendances/delete/",
#         AttendanceViewSet.as_view({"delete": "delete_attendances"}),
#     ),
#     path(
#         "attendances/employee/<uuid:emp_id>",
#         AttendanceViewSet.as_view({"get": "read_employee_attendances"}),
#     ),
#     path(
#         "attendances/department/<int:dept_id>",
#         AttendanceViewSet.as_view({"get": "read_department_attendances"}),
#     ),
#     ##########################################################
#     path(
#         "employee_sessions/checkin/",
#         EmployeeSessionViewSet.as_view({"post": "create_employee_checkin"}),
#     ),
#     path(
#         "employee_sessions/checkout/",
#         EmployeeSessionViewSet.as_view({"post": "create_employee_checkout"}),
#     ),
#     ##########################################################
#     path(
#         "identificationdocs/create/",
#         IdentificationDocumentViewSet.as_view(
#             {"post": "create_identificationdocuments"}
#         ),
#     ),
#     path(
#         "identificationdocs/read/",
#         IdentificationDocumentViewSet.as_view({"get": "read_identificationdocuments"}),
#     ),
#     path(
#         "identificationdocs/update/",
#         IdentificationDocumentViewSet.as_view(
#             {"patch": "update_identificationdocuments"}
#         ),
#     ),
#     path(
#         "identificationdocs/delete/",
#         IdentificationDocumentViewSet.as_view(
#             {"delete": "delete_identificationdocuments"}
#         ),
#     ),
#     ##########################################################
#     path(
#         "identificationtypes/create/",
#         IdentificationTypeViewSet.as_view({"post": "create_identificationtypes"}),
#     ),
#     path(
#         "identificationtypes/read/",
#         IdentificationTypeViewSet.as_view({"get": "read_identificationtypes"}),
#     ),
#     path(
#         "identificationtypes/update/",
#         IdentificationTypeViewSet.as_view({"patch": "update_identificationtypes"}),
#     ),
#     path(
#         "identificationtypes/delete/",
#         IdentificationTypeViewSet.as_view({"delete": "delete_identificationtypes"}),
#     ),
#     ##########################################################
# ]
