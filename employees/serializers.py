from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from .models import *


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"


class EmployeeDeleteSerializer(serializers.Serializer):

    employees = serializers.ListField(child=serializers.IntegerField())


class EmployeeGroupSerializer(serializers.ModelSerializer):
    class Meta:

        model = EmployeeGroup
        fields = "__all__"


class EmployeeGroupDeleteSerializer(serializers.Serializer):

    group_ids = serializers.ListField(child=serializers.IntegerField())


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:

        model = Department
        fields = "__all__"


class DepartmentDeleteSerializer(serializers.Serializer):

    group_ids = serializers.ListField(child=serializers.IntegerField())


class DesignationSerializer(serializers.ModelSerializer):
    class Meta:

        model = Designation
        fields = "__all__"

class DesignationDeleteSerializer(serializers.Serializer):

    group_ids = serializers.ListField(child=serializers.IntegerField())




class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:

        model = Attendance
        fields = "__all__"


class AttendanceDeleteSerializer(serializers.Serializer):

    attendance_ids = serializers.ListField(child=serializers.IntegerField())


class EmployeeCheckinCheckoutSerializer(serializers.ModelSerializer):
    class Meta:

        model = EmployeeCheckin
        fields = ["fk_employee", "checked_in_time", "is_first_session"]


class EmployeeCheckinSerializer(serializers.ModelSerializer):
    class Meta:

        model = EmployeeCheckin
        fields = ["fk_employee", "checked_in_time", "is_first_session"]


class EmployeeCheckoutSerializer(serializers.ModelSerializer):
    class Meta:

        model = EmployeeCheckin
        fields = ["fk_employee", "checked_out_time", "is_last_session"]


class EmployeeCheckinCheckoutDeleteSerializer(serializers.Serializer):

    check_ids = serializers.ListField(child=serializers.IntegerField())


class LeavePolicySerializer(serializers.ModelSerializer):
    class Meta:

        model = LeavePolicy
        fields = "__all__"


class LeavePolicyDeleteSerializer(serializers.Serializer):

    leavepolicy_ids = serializers.ListField(child=serializers.IntegerField())


class LeaveApplicationSerializer(serializers.ModelSerializer):
    class Meta:

        model = LeaveApplication
        fields = "__all__"


class LeaveApplicationDeleteSerializer(serializers.Serializer):

    leaveapplication_ids = serializers.ListField(child=serializers.IntegerField())


class LeaveSerializer(serializers.ModelSerializer):
    class Meta:

        model = Leave
        fields = "__all__"


class LeaveDeleteSerializer(serializers.Serializer):

    leave_ids = serializers.ListField(child=serializers.IntegerField())


class MonthlyReportSerializer(serializers.ModelSerializer):
    class Meta:

        model = MonthlyReport
        fields = "__all__"


class LeavePolicy_TypeMembershipSerializer(serializers.ModelSerializer):
    class Meta:

        model = LeavePolicy_Type_Membership
        fields = "__all__"


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:

        model = Schedule
        fields = "__all__"


class ScheduleDeleteSerializer(serializers.Serializer):

    schedule_ids = serializers.ListField(child=serializers.IntegerField())


# class CalendarSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Calendar
#         fields = "__all__"


# class EventsSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Events
#         fields = "__all__"
