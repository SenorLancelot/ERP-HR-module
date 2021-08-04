from rest_framework import serializers


from .models import *


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"


class EmployeeDeleteSerializer(serializers.Serializer):

    employees = serializers.ListField(child=serializers.IntegerField())


class IdentificationDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdentificationDocument
        fields = "__all__"


class IdentificationDocumentDeleteSerializer(serializers.Serializer):

    identificationdocument_ids = serializers.ListField(child=serializers.IntegerField())


class IdentificationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdentificationType
        fields = "__all__"


class IdentificationTypeDeleteSerializer(serializers.Serializer):

    identificationtype_ids = serializers.ListField(child=serializers.IntegerField())


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

    department_ids = serializers.ListField(child=serializers.IntegerField())


class DesignationSerializer(serializers.ModelSerializer):
    class Meta:

        model = Designation
        fields = "__all__"


class DesignationDeleteSerializer(serializers.Serializer):

    designation_ids = serializers.ListField(child=serializers.IntegerField())


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:

        model = Attendance
        fields = "__all__"


class AttendanceDeleteSerializer(serializers.Serializer):

    attendance_ids = serializers.ListField(child=serializers.IntegerField())


class EmployeeSessionSerializer(serializers.ModelSerializer):
    class Meta:

        model = EmployeeSession
        fields = "__all__"


class EmployeeSessionCheckinSerializer(serializers.ModelSerializer):
    class Meta:

        model = EmployeeSession
        fields = ["fk_employee", "checked_in_time", "is_first_session"]


class EmployeeSessionCheckoutSerializer(serializers.ModelSerializer):
    class Meta:

        model = EmployeeSession
        fields = ["fk_employee", "checked_out_time", "is_last_session"]


class EmployeeSessionDeleteSerializer(serializers.Serializer):

    check_ids = serializers.ListField(child=serializers.IntegerField())


class LeavePolicySerializer(serializers.ModelSerializer):
    class Meta:

        model = LeavePolicy
        fields = "__all__"


class LeavePolicyDeleteSerializer(serializers.Serializer):

    leavepolicy_ids = serializers.ListField(child=serializers.IntegerField())


# class LeavePolicyTypeMembershipSerializer(serializers.ModelSerializer):
#     class Meta:

#         model = LeavePolicyTypeMembership
#         fields = "__all__"


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


# class MonthlyReportSerializer(serializers.ModelSerializer):
#     class Meta:

#         model = MonthlyReport
#         fields = "__all__"


class LeavePolicyTypeMembershipSerializer(serializers.ModelSerializer):
    class Meta:

        model = LeavePolicyTypeMembership
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
