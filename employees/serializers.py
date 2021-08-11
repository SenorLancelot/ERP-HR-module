from rest_framework import serializers


from .models import *


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"


class EmployeeListSerializer(serializers.Serializer):

    employee_ids = serializers.ListField(child=serializers.IntegerField())


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"


class CustomerListSerializer(serializers.Serializer):

    customer_ids = serializers.ListField(child=serializers.IntegerField())


class IdentificationDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdentificationDocument
        fields = "__all__"


class IdentificationDocumentListSerializer(serializers.Serializer):

    identificationdocument_ids = serializers.ListField(child=serializers.IntegerField())


class IdentificationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdentificationType
        fields = "__all__"


class IdentificationTypeListSerializer(serializers.Serializer):

    identificationtype_ids = serializers.ListField(child=serializers.IntegerField())


class EmployeeGroupSerializer(serializers.ModelSerializer):
    class Meta:

        model = EmployeeGroup
        fields = "__all__"


class EmployeeGroupListSerializer(serializers.Serializer):

    group_ids = serializers.ListField(child=serializers.IntegerField())


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:

        model = Department
        fields = "__all__"


class DepartmentListSerializer(serializers.Serializer):

    department_ids = serializers.ListField(child=serializers.IntegerField())



class CompanySerializer(serializers.ModelSerializer):
    class Meta:

        model = Company
        fields = "__all__"


class CompanyListSerializer(serializers.Serializer):

    company_ids = serializers.ListField(child=serializers.IntegerField())

class EmployeeGradeSerializer(serializers.ModelSerializer):
    class Meta:

        model = EmployeeGrade
        fields = "__all__"


class EmployeeGradeListSerializer(serializers.Serializer):

    employee_grade_ids = serializers.ListField(child=serializers.IntegerField())

class DesignationSerializer(serializers.ModelSerializer):
    class Meta:

        model = Designation
        fields = "__all__"


class DesignationListSerializer(serializers.Serializer):

    designation_ids = serializers.ListField(child=serializers.IntegerField())


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:

        model = Attendance
        fields = "__all__"


class AttendanceListSerializer(serializers.Serializer):

    attendance_ids = serializers.ListField(child=serializers.IntegerField())


class EmployeeSessionSerializer(serializers.ModelSerializer):
    class Meta:

        model = EmployeeSession
        fields = "__all__"


class EmployeeSessionCheckinSerializer(serializers.ModelSerializer):
    class Meta:

        model = EmployeeSession
        fields = ["fk_employee", "checked_in_at"]


class EmployeeSessionCheckoutSerializer(serializers.ModelSerializer):
    class Meta:

        model = EmployeeSession
        fields = ["fk_employee", "checked_out_at"]


class EmployeeSessionListSerializer(serializers.Serializer):

    check_ids = serializers.ListField(child=serializers.IntegerField())


class LeavePolicySerializer(serializers.ModelSerializer):
    class Meta:

        model = LeavePolicy
        fields = "__all__"


class LeavePolicyListSerializer(serializers.Serializer):

    leavepolicy_ids = serializers.ListField(child=serializers.IntegerField())


# class LeavePolicyTypeMembershipSerializer(serializers.ModelSerializer):
#     class Meta:

#         model = LeavePolicyTypeMembership
#         fields = "__all__"


class LeaveApplicationSerializer(serializers.ModelSerializer):
    class Meta:

        model = LeaveApplication
        fields = "__all__"


class LeaveApplicationListSerializer(serializers.Serializer):

    leaveapplication_ids = serializers.ListField(child=serializers.IntegerField())


class LeaveApplicationTypeMembershipSerializer(serializers.ModelSerializer):
    class Meta:

        model = LeaveApplicationTypeMembership
        fields = ["fk_leave_type", "from_date", "to_date"]


class CreateLeaveApplicationSerializer(serializers.ModelSerializer):

    fk_leave_types = LeaveApplicationTypeMembershipSerializer(many=True)

    class Meta:

        model = LeaveApplication
        fields = [
            "fk_leave_types",
            "fk_employee",
            "fk_leave_approver",
            "from_date",
            "to_date",
            "status",
            "post_date",
        ]

    def create(self, validated_data):

        leave_type_membership = validated_data.pop("fk_leave_types")

        leave_application = LeaveApplication(**validated_data)

        leave_application.save()

        for leave_type in leave_type_membership:

            leave_application_type = LeaveApplicationTypeMembership(
                fk_leave_application=leave_application, **leave_type
            )

            leave_application_type.save()

        return leave_application


class LeaveApplicationResponseSerializer(serializers.ModelSerializer):
    class Meta:

        model = LeaveApplication
        fields = "__all__"


class LeaveSerializer(serializers.ModelSerializer):
    class Meta:

        model = Leave
        fields = "__all__"


class LeaveListSerializer(serializers.Serializer):

    leave_ids = serializers.ListField(child=serializers.IntegerField())


class WorkdayDivisionSerializer(serializers.ModelSerializer):
    class Meta:

        model = WorkdayDivision
        fields = "__all__"


class WorkdayDivisionListSerializer(serializers.Serializer):

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


class ScheduleListSerializer(serializers.Serializer):

    schedule_ids = serializers.ListField(child=serializers.IntegerField())


class DaysListSerializer(serializers.ModelSerializer):
    class Meta:

        model = DaysList
        fields = "__all__"


class DaysListListSerializer(serializers.Serializer):

    days_list_ids = serializers.ListField(child=serializers.IntegerField())


# class CalendarSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Calendar
#         fields = "__all__"


# class EventsSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Events
#         fields = "__all__"
