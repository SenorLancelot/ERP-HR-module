from django.urls import path

from .views import *

urlpatterns = [
    # path("employees/all/", EmployeeViewSet.as_view({'get' : 'read_all_employees'})),
    path(
        "employees/create/",
        EmployeeViewSet.as_view({"post": "create_to_employee_list"}),
    ),
    path("employees/read/", EmployeeViewSet.as_view({"get": "read_employee_list"})),
    path(
        "employees/update/", EmployeeViewSet.as_view({"patch": "patch_employees_list"})
    ),
    path("employees/delete/", EmployeeViewSet.as_view({"delete": "delete_employees"})),
    path(
        "employeegroup/create/",
        EmployeeGroupViewSet.as_view({"post": "create_employeegroup_list"}),
    ),
    path(
        "employeegroup/read/",
        EmployeeGroupViewSet.as_view({"get": "read_employeegroup_list"}),
    ),
    path(
        "employeegroup/update/",
        EmployeeGroupViewSet.as_view({"patch": "patch_employees_list"}),
    ),
    path(
        "employeegroup/delete/",
        EmployeeGroupViewSet.as_view({"delete": "delete_employeegroup"}),
    ),
    path(
        "departments/create/",
        DepartmentViewSet.as_view({"post": "create_department_list"}),
    ),
    path(
        "departments/read/", DepartmentViewSet.as_view({"get": "read_department_list"})
    ),
    path(
        "departments/update/",
        DepartmentViewSet.as_view({"patch": "patch_departments_list"}),
    ),
    path(
        "departments/delete/",
        DepartmentViewSet.as_view({"delete": "delete_department_list"}),
    ),
    path(
        "designations/create/",
        DesignationViewSet.as_view({"post": "create_designations_list"}),
    ),
    path(
        "designations/read/",
        DesignationViewSet.as_view({"get": "read_designations_list"}),
    ),
    path(
        "designations/update/",
        DesignationViewSet.as_view({"patch": "patch_designations_list"}),
    ),
    path(
        "designations/delete/",
        DesignationViewSet.as_view({"delete": "delete_designations_list"}),
    ),
    path(
        "leavepolicies/create/",
        LeavePolicyViewSet.as_view({"post": "create_leavepolicies_list"}),
    ),
    path(
        "leavepolicies/update/",
        LeavePolicyViewSet.as_view({"get": "read_leavepolicies_list"}),
    ),
    path(
        "leavepolicies/read/",
        LeavePolicyViewSet.as_view({"patch": "patch_leavepolicies_list"}),
    ),
    path(
        "leavepolicies/delete/",
        LeavePolicyViewSet.as_view({"delete": "delete_leavepolicies_list"}),
    ),
    path(
        "leavepolicygeneration/designation/<int:designation_id>",
        LeavePolicyViewSet.as_view({"post": "leave_policy_generation"}),
    ),
    path(
        "leaveapplications/create/",
        LeaveApplicationViewSet.as_view({"post": "create_leaveapplications_list"}),
    ),
    path(
        "leaveapplications/read/",
        LeaveApplicationViewSet.as_view({"get": "read_leaveapplications_list"}),
    ),
    path(
        "leaveapplications/update/",
        LeaveApplicationViewSet.as_view({"patch": "patch_leaveapplications_list"}),
    ),
    path(
        "leaveapplications/delete/",
        LeaveApplicationViewSet.as_view({"delete": "delete_leaveapplications_list"}),
    ),
    path("leaves/create/", LeaveViewSet.as_view({"post": "create_leaves_list"})),
    path("leaves/read/", LeaveViewSet.as_view({"get": "read_leave_list"})),
    path("leaves/update/", LeaveViewSet.as_view({"patch": "patch_leaves_list"})),
    path("leaves/delete/", LeaveViewSet.as_view({"delete": "delete_leave_list"})),
    path(
        "schedules/create/<int:des_id>",
        ScheduleViewSet.as_view({"post": "create_schedules_list"}),
    ),
    path("schedules/read/", ScheduleViewSet.as_view({"get": "read_shedules_list"})),
    path(
        "schedules/update/", ScheduleViewSet.as_view({"patch": "patch_schedules_list"})
    ),
    path(
        "schedules/delete/",
        ScheduleViewSet.as_view({"delete": "delete_schedules_list"}),
    ),
    path(
        "attendances/employee/<uuid:emp_id>",
        AttendanceViewSet.as_view({"get": "read_employee_attendances_list"}),
    ),
    path(
        "attendances/department/<int:dept_id>",
        AttendanceViewSet.as_view({"get": "read_department_attendances_list"}),
    ),
    path(
        "employeecheckins/checkin/",
        EmployeeCheckinViewSet.as_view({"post": "create_employee_checkin"}),
    ),
    path(
        "employeecheckins/checkout/",
        EmployeeCheckinViewSet.as_view({"post": "create_employee_checkout"}),
    ),
    # path(
    #     "monthlyreports/employee/<uuid:emp_id>",
    #     MonthlyReportViewSet.as_view(
    #         {"post": "generate_monthly_report", "patch": "patch_monthleyreports_list"}
    #     ),
    # ),
]
