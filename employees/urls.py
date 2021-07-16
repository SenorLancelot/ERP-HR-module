from django.urls import path

from .views import *

urlpatterns = [

    #path("employees/all/", EmployeeViewSet.as_view({'get' : 'get_all_employees'})),
    path("employees/create/", EmployeeViewSet.as_view({"post" : 'post_to_employee_list'})),
    path("employees/read/", EmployeeViewSet.as_view({'get' : 'get_employee_list'})),
    path("employees/update/", EmployeeViewSet.as_view({"patch" : 'patch_employees_list'})),
    path("employees/delete/", EmployeeViewSet.as_view({"delete" : 'delete_employees'})),


    path("employeegroup/create/", EmployeeGroupViewSet.as_view({"post" : 'post_employeegroup_list'})),
    path("employeegroup/read/", EmployeeGroupViewSet.as_view({'get' : 'get_employeegroup_list'})),
    path("employeegroup/update/", EmployeeGroupViewSet.as_view({"patch" : 'patch_employees_list'})),
    path("employeegroup/delete/", EmployeeGroupViewSet.as_view({"delete" : 'delete_employeegroup'})),


    path("departments/create/", DepartmentsViewSet.as_view({"post" : 'post_department_list'})),
    path("departments/read/", DepartmentsViewSet.as_view({'get' : 'get_department_list'})),
    path("departments/update/", DepartmentsViewSet.as_view({"patch" : 'patch_departments_list'})),
    path("departments/delete/", DepartmentsViewSet.as_view({"delete" : "delete_department_list"})),


    path("designations/create/", DesignationsViewSet.as_view({"post" : "post_designations_list"})),
    path("designations/read/", DesignationsViewSet.as_view({'get' : 'get_designations_list'})),
    path("designations/update/", DesignationsViewSet.as_view({"patch" : 'patch_designations_list'})),
    path("designations/delete/", DesignationsViewSet.as_view({"delete" : "delete_designations_list"})),


    path("leavepolicies/create/", LeavePoliciesViewSet.as_view({"post" : "post_leavepolicies_list"})),
    path("leavepolicies/update/", LeavePoliciesViewSet.as_view({'get' : 'get_leavepolicies_list'})),
    path("leavepolicies/read/", LeavePoliciesViewSet.as_view({"patch" : 'patch_leavepolicies_list'})),
    path("leavepolicies/delete/", LeavePoliciesViewSet.as_view({"delete" : "delete_leavepolicies_list"})),

    path("leaveapplications/create/", LeaveApplicationsViewSet.as_view({"post" : "post_leaveapplications_list"})),
    path("leaveapplications/read/", LeaveApplicationsViewSet.as_view({'get' : 'get_leaveapplications_list'})),
    path("leaveapplications/update/", LeaveApplicationsViewSet.as_view({"patch" : 'patch_leaveapplications_list'})),
    path("leaveapplications/delete/", LeaveApplicationsViewSet.as_view({"delete" : "delete_leaveapplications_list"})),


    path("leaves/create/", LeaveApplicationsViewSet.as_view({"post" : "post_leaves_list"})),
    path("leaves/read/", LeaveApplicationsViewSet.as_view({'get' : 'get_leave_list'})),
    path("leaves/update/", LeaveApplicationsViewSet.as_view({"patch" : 'patch_leaves_list'})),
    path("leaves/delete/", LeaveApplicationsViewSet.as_view({"delete" : "delete_leave_list"})),


    path("attendances/employee/<uuid:emp_id>", AttendancesViewSet.as_view({'get' : 'get_employee_attendances_list'})),
    path("attendances/department/<int:dept_id>", AttendancesViewSet.as_view({'get' : 'get_department_attendances_list'})),
    path("employeecheckins/checkin/", EmployeeCheckinsViewSet.as_view({"post" : "post_employee_checkin"})),
    path("employeecheckins/checkout/", EmployeeCheckinsViewSet.as_view({"post" : "post_employee_checkout"})),
    path("monthlyreports/employee/<uuid:emp_id>", MonthlyReportsViewSet.as_view({"post" : "generate_monthly_report", "patch" : 'patch_monthleyreports_list'}))
      
]

