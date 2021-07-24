from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from .models import *

class EmployeesSerializer(serializers.ModelSerializer):
    # parent = sistField(s.ModelSerializerchild=RecursiveField())
    class Meta:

        model = Employees
        # fields = [
        #     "employee_id",
        #     "first_name",
        #     "last_name",
        #     "employment_type",
        #     "gender",
        #     "date_of_birth",
        #     "contact_no",
        #     "company_email",
        #     "department",
        #     "employee_group",
            
        # ]

        fields = "__all__"

class EmployeeGroupSerializer(serializers.ModelSerializer):

    class Meta:

        model = EmployeeGroup
        fields = "__all__"

class DepartmentsSerializer(serializers.ModelSerializer):

    class Meta:

        model = Departments
        fields = "__all__"

class DesignationsSerializer(serializers.ModelSerializer):

    class Meta:

        model = Designations
        fields = "__all__"

class AttendancesSerializer(serializers.ModelSerializer):

    class Meta:

        model = Attendances
        fields = "__all__"

class EmployeeCheckinsSerializer(serializers.ModelSerializer):

    class Meta:

        model = EmployeeCheckins
        fields = "__all__"

class LeavePoliciesSerializer(serializers.ModelSerializer):

    class Meta:

        model = LeavePolicies
        fields = "__all__"

class LeavesApplicationsSerializer(serializers.ModelSerializer):

    class Meta:

        model = LeavesApplications
        fields = "__all__"

class LeavesSerializer(serializers.ModelSerializer):
    
    class Meta:

        model = Leaves
        fields = "__all__"

class MonthlyReportsSerializer(serializers.ModelSerializer):

    class Meta:

        model = MonthlyReports
        fields = "__all__"



class LeavePolicy_TypeMembershipSerializer(serializers.ModelSerializer):

    class Meta:

        model = LeavePolicy_TypeMembership
        fields = "__all__"


class SchedulesSerializer(serializers.ModelSerializer):

    class Meta:

        model = Schedules
        fields = "__all__"

# class CalendarSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Calendar
#         fields = "__all__"


# class EventsSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Events
#         fields = "__all__"