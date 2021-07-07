from django.urls import path

from .views import *

urlpatterns = [

    path("employees/all/", EmployeeViewSet.as_view({'get' : 'get_all_employees'})),
    path("employees/list/", EmployeeViewSet.as_view({'get' : 'get_employee_list', "post" : 'post_to_employee_list', "delete" : 'delete_employees'})),
    path("employeegroup/list/", EmployeeGroupViewSet.as_view({'get' : 'get_employeegroup_list', "post" : 'post_employeegroup_list', "delete" : 'delete_employeegroup'})),
    path("departments/list/", DepartmentsViewSet.as_view({'get' : 'get_department_list', "post" : 'post_department_list', "delete" : "delete_department_list"})),
    path("designations/list/", DesignationsViewSet.as_view({'get' : 'get_designations_list', "post" : "post_designations_list", "delete" : "delete_designations_list"})),
    path("leavepolicies/list/", LeavePoliciesViewSet.as_view({'get' : 'get_leavepolicies_list', "post" : "post_leavepolicies_list", "delete" : "delete_leavepolicies_list"})),
    path("leaveapplications/list/", LeaveApplicationsViewSet.as_view({'get' : 'get_leaveapplications_list', "post" : "post_leaveapplications_list", "delete" : "delete_leaveapplications_list"})),
    path("leaves/list/", LeaveApplicationsViewSet.as_view({'get' : 'get_leave_list', "post" : "post_leaves_list", "delete" : "delete_leave_list"})),
    path("attendances/employee/<uuid:emp_id>", AttendancesViewSet.as_view({'get' : 'get_employee_attendances_list'})),
    path("attendances/department/<int:dept_id>", AttendancesViewSet.as_view({'get' : 'get_department_attendances_list'}))
    
    
]