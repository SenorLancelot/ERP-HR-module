from rest_framework import serializers

from rest_framework.exceptions import NotFound, ParseError, ValidationError
from rest_framework.response import Response
from .models import *
from rest_framework import status

class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop("fields", None)

        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:

            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class DepartmentRequestSerializer(DynamicFieldsModelSerializer):
    class Meta:

        model = Department
        fields = ["name", "parent"]


class DepartmentResponseSerializer(DynamicFieldsModelSerializer):
    class Meta:

        model = Department
        fields = "__all__"


class CompanyRequestSerializer(DynamicFieldsModelSerializer):
    class Meta:

        model = Company
        fields = ["name", "domain", "parent"]


class CompanyResponseSerializer(DynamicFieldsModelSerializer):
    class Meta:

        model = Company
        fields = "__all__"


class DesignationResponseSerializer(DynamicFieldsModelSerializer):
    class Meta:

        model = Designation
        fields = ["name", "description", "fk_schedule", "fk_leave_policy"]


class DesignationRequestSerializer(DynamicFieldsModelSerializer):
    class Meta:

        model = Designation
        fields = ["name", "description", "fk_schedule", "fk_leave_policy"]


class EmployeeResponseSerializer(DynamicFieldsModelSerializer):

    fk_department = DepartmentResponseSerializer(required=False)
    fk_designation = DesignationResponseSerializer(required=False)
    fk_company = CompanyResponseSerializer(required=False)

    class Meta:
        model = Employee
        fields = [
            "first_name",
            "last_name",
            "gender",
            "birth_date",
            "primary_contact_no",
            "secondary_contact_no",
            "personal_email",
            "current_address",
            "is_current_address_permanent",
            "permanent_address",
            "employment_type",
            "joining_date",
            "leaving_date",
            "retirement_date",
            "company_email",
            "parent",
            "fk_company",
            "fk_department",
            "fk_designation",
        ]


class EmployeeRequestSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Employee
        fields = [
            "first_name",
            "last_name",
            "gender",
            "birth_date",
            "primary_contact_no",
            "secondary_contact_no",
            "personal_email",
            "current_address",
            "is_current_address_permanent",
            "permanent_address",
            "employment_type",
            "joining_date",
            "leaving_date",
            "retirement_date",
            "company_email",
            "parent",
            "fk_company",
            "fk_department",
            "fk_designation",
        ]

    def create(self, validated_data):
        is_current_address_permanent = validated_data.get("is_current_permanent")
        obj = None
        if is_current_address_permanent:
            current_add = validated_data.pop("current_address")
            perm_add = current_add
            obj = Employee.objects.create(
                current_add=current_add, perm_add=perm_add, **validated_data
            )
        else:
            obj = Employee.objects.create(**validated_data)
        return obj


class EmployeeListSerializer(serializers.Serializer):

    employee_ids = serializers.ListField(child=serializers.IntegerField())


class EmployeeLeaveReportMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveReportTypeMembership
        fields = "__all__"


class EmployeeLeaveReportResponseSerializer(serializers.ModelSerializer):
    fk_leave_types = EmployeeLeaveReportMembershipSerializer(
        source="leavereporttypemembership_set", many=True
    )

    class Meta:
        model = EmployeeLeaveReport
        fields = "__all__"


class EmployeeLeaveReportRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeLeaveReport
        fields = "__all__"


class EmployeeLeaveReportListSerializer(serializers.Serializer):

    employee_ids = serializers.ListField(child=serializers.IntegerField())


class CustomerRequestSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"


class CustomerResponseSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"


class CustomerListSerializer(serializers.Serializer):

    customer_ids = serializers.ListField(child=serializers.IntegerField())


class EmergencyContactRequestSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = EmergencyContact
        fields = "__all__"


class EmergencyContactResponseSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = EmergencyContact
        fields = "__all__"


class EmergencyContactListSerializer(serializers.Serializer):

    emergency_contact_ids = serializers.ListField(child=serializers.IntegerField())


class IdentificationTypeRequestSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = IdentificationType
        fields = ["name", "issuing_authority"]


class IdentificationTypeResponseSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = IdentificationType
        fields = ["name", "issuing_authority"]


class IdentificationDocumentResponseSerializer(DynamicFieldsModelSerializer):
    fk_identification_type = IdentificationTypeResponseSerializer(many=False)

    class Meta:
        model = IdentificationDocument
        fields = ["identification_number", "fk_employee", "fk_identification_type"]


class IdentificationDocumentRequestSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = IdentificationDocument
        fields = ["identification_number", "fk_employee", "fk_identification_type"]


class IdentificationDocumentListSerializer(serializers.Serializer):

    identificationdocument_ids = serializers.ListField(child=serializers.IntegerField())


class IdentificationTypeListSerializer(serializers.Serializer):

    identificationtype_ids = serializers.ListField(child=serializers.IntegerField())


class EmployeeGroupResponseSerializer(DynamicFieldsModelSerializer):
    fk_employee = EmployeeResponseSerializer(required=False, many=True)

    class Meta:

        model = EmployeeGroup
        fields = ["name", "fk_employee"]


class EmployeeGroupRequestSerializer(DynamicFieldsModelSerializer):
    class Meta:

        model = EmployeeGroup
        fields = ["name", "fk_employee"]


class EmployeeGroupListSerializer(serializers.Serializer):

    group_ids = serializers.ListField(child=serializers.IntegerField())


class DepartmentListSerializer(serializers.Serializer):

    department_ids = serializers.ListField(child=serializers.IntegerField())


class CompanyListSerializer(serializers.Serializer):

    company_ids = serializers.ListField(child=serializers.IntegerField())


class EmployeeGradeRequestSerializer(DynamicFieldsModelSerializer):
    class Meta:

        model = EmployeeGrade
        fields = "__all__"


class EmployeeGradeResponseSerializer(DynamicFieldsModelSerializer):
    class Meta:

        model = EmployeeGrade
        fields = "__all__"


class EmployeeGradeListSerializer(serializers.Serializer):

    employee_grade_ids = serializers.ListField(child=serializers.IntegerField())


class DesignationListSerializer(serializers.Serializer):

    designation_ids = serializers.ListField(child=serializers.IntegerField())


class AttendanceRequestSerializer(serializers.ModelSerializer):
    class Meta:

        model = Attendance
        fields = [
            "attendance_date",
            "is_late_entry",
            "is_early_exit",
            "comment",
            "total_time",
            "total_overtime",
            "fk_employee",
            
        ]


class AttendanceResponseSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = Attendance
        fields = [
            "attendance_date",
            "is_late_entry",
            "is_early_exit",
            "comment",
            "total_time",
            "total_overtime",
            "fk_employee",
            
        ]


class AttendanceListSerializer(serializers.Serializer):

    attendance_ids = serializers.ListField(child=serializers.IntegerField())


class EmployeeSessionRequestSerializer(DynamicFieldsModelSerializer):
    class Meta:

        model = EmployeeSession
        fields = "__all__"


class EmployeeSessionResponseSerializer(DynamicFieldsModelSerializer):
    class Meta:

        model = EmployeeSession
        fields = "__all__"


class EmployeeSessionCheckinSerializer(serializers.ModelSerializer):
    class Meta:

        model = EmployeeSession
        # fields = ["fk_employee", "checked_in_at"]
        fields = "__all__"


class EmployeeSessionCheckoutSerializer(serializers.ModelSerializer):
    class Meta:

        model = EmployeeSession
        fields = ["fk_employee", "checked_out_at"]


class EmployeeSessionListSerializer(serializers.Serializer):

    check_ids = serializers.ListField(child=serializers.IntegerField())


class DaysListSerializer(serializers.ModelSerializer):
    class Meta:

        model = DaysList
        fields = "__all__"


class LeavePolicyTypeMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeavePolicyTypeMembership
        fields = "__all__"


class LeavePolicyResponseSerializer(serializers.ModelSerializer):
    fk_leave_type = LeavePolicyTypeMembershipSerializer(
        source="leavepolicytypemembership_set", many=True
    )
    # fk_blocked_leaves = DaysListSerializer(many=True)

    class Meta:

        model = LeavePolicy
        fields = [
            "fk_leave_type",
            "created_at",
            "modified_at",
            # "fk_blocked_leaves",
        ]

class LeavePolicyRequestSerializer(serializers.ModelSerializer):
    

    class Meta:

        model = LeavePolicy
        fields = [
            "fk_leave_type",
            "created_at",
            "modified_at",
            # "fk_blocked_leaves",
        ]

class LeavePolicyListSerializer(serializers.Serializer):

    leave_policy_ids = serializers.ListField(child=serializers.IntegerField())


# class LeavePolicyTypeMembershipSerializer(serializers.ModelSerializer):
#     class Meta:

#         model = LeavePolicyTypeMembership
#         fields = "__all__"


class LeaveApplicationResponseSerializer(DynamicFieldsModelSerializer):
    class Meta:
        depth = 1
        model = LeaveApplication
        fields = "__all__"


class LeaveApplicationRequestSerializer(DynamicFieldsModelSerializer):
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

    # fk_leave_types = LeaveApplicationTypeMembershipSerializer(many=True)

    class Meta:

        model = LeaveApplication
        fields = [
            "fk_leave_type",
            "fk_employee",
            "fk_leave_approver",
            "from_date",
            "to_date",
            "status",
            "post_date",
        ]
    
    def validate(self, data):

        employee_leave_report = EmployeeLeaveReport.objects.get(
            fk_employee=data["fk_employee"], status=LIVE
        )
        
        leave_details = LeaveReportTypeMembership.objects.get(
            fk_employee_report=employee_leave_report.id,
            fk_leave_type=data["fk_leave_type"],
        )
        to_date = datetime.datetime.strptime(str(data["to_date"]), "%Y-%m-%d")
        from_date = datetime.datetime.strptime(
            str(data["from_date"]), "%Y-%m-%d"
        )
        holidays_in_leave = DaysList.objects.filter(
            is_holiday=True, date__range=[from_date, to_date], status=LIVE
        )

        leave_days = (
            (to_date - from_date).days + 1 
            if leave_details.fk_leave_type.is_holiday
            else (to_date - from_date).days + 1 - holidays_in_leave.count()
        )
        allowed_days = leave_details.leaves_remaining
        consecutive_days = leave_details.consecutive_days_allowed

        blocked_leaves = DaysList.objects.filter(
            is_blocked_leave=True, date__range=[from_date, to_date], status=LIVE
        )

        if blocked_leaves.count() > 0:
            
            raise ValidationError("Leave Duration contains blocked leaves")

        if leave_days > allowed_days or leave_days > consecutive_days:
            raise ValidationError("Leave Duration exceeds allowed leaves or consecutive days")

        return super().validate(data)
    # def create(self, validated_data):

    #     leave_type_membership = validated_data.pop("fk_leave_types")

    #     leave_application = LeaveApplication(**validated_data)

    #     leave_application.save()

    #     for leave_type in leave_type_membership:

    #         leave_application_type = LeaveApplicationTypeMembership(
    #             fk_leave_application=leave_application, **leave_type
    #         )

    #         leave_application_type.save()

    #     return leave_application


class LeaveTypeRequestSerializer(DynamicFieldsModelSerializer):
    class Meta:

        model = LeaveType
        fields = "__all__"


class LeaveTypeResponseSerializer(DynamicFieldsModelSerializer):
    class Meta:

        model = LeaveType
        fields = "__all__"


class LeaveTypeListSerializer(serializers.Serializer):

    compensate_leave_application_ids = serializers.ListField(
        child=serializers.IntegerField()
    )


class LeaveRequestSerializer(DynamicFieldsModelSerializer):
    fk_employee = EmployeeResponseSerializer()
    fk_leave_type = LeaveTypeResponseSerializer()

    class Meta:

        model = Leave
        fields = ["from_date", "to_date", "fk_employee", "fk_leave_type"]


class LeaveResponseSerializer(DynamicFieldsModelSerializer):
    class Meta:

        model = Leave
        fields = ["from_date", "to_date", "fk_employee", "fk_leave_type"]


class LeaveListSerializer(serializers.Serializer):

    leave_ids = serializers.ListField(child=serializers.IntegerField())


class WorkdayDivisionRequestSerializer(DynamicFieldsModelSerializer):
    class Meta:

        model = WorkdayDivision
        fields = "__all__"


class WorkdayDivisionResponseSerializer(DynamicFieldsModelSerializer):
    class Meta:

        model = WorkdayDivision
        fields = "__all__"


class WorkdayDivisionListSerializer(serializers.Serializer):

    leave_ids = serializers.ListField(child=serializers.IntegerField())


# class MonthlyReportSerializer(serializers.ModelSerializer):
#     class Meta:

#         model = MonthlyReport
#         fields = "__all__"


# class LeavePolicyTypeMembershipSerializer(serializers.ModelSerializer):
#     class Meta:

#         model = LeavePolicyTypeMembership
#         fields = "__all__"


class ScheduleRequestSerializer(DynamicFieldsModelSerializer):
    class Meta:

        model = Schedule
        fields = "__all__"


class ScheduleResponseSerializer(DynamicFieldsModelSerializer):
    class Meta:

        model = Schedule
        fields = "__all__"


class ScheduleListSerializer(serializers.Serializer):

    schedule_ids = serializers.ListField(child=serializers.IntegerField())


class DaysListResponseSerializer(DynamicFieldsModelSerializer):
    class Meta:

        model = DaysList
        fields = "__all__"


class DaysListRequestSerializer(DynamicFieldsModelSerializer):
    class Meta:

        model = DaysList
        fields = "__all__"


class DaysListListSerializer(serializers.Serializer):

    days_list_ids = serializers.ListField(child=serializers.IntegerField())


class CompensateLeaveApplicationRequestSerializer(DynamicFieldsModelSerializer):
    class Meta:

        model = CompensateLeaveApplication
        fields = "__all__"

    def validate(self, data):

        try:
            employee_leave_report = EmployeeLeaveReport.objects.get(
                fk_employee=data["fk_employee"], status=LIVE
            )
        except :

            raise ValidationError(f'Leave Report for employee id {data["fk_employee"]} does not exist')
        
        leave_details = LeaveReportTypeMembership.objects.get(
            fk_employee_report=employee_leave_report.id,
            fk_leave_type=data["fk_leave_type"],
        )

        leave_days = data["leaves"]
        allowed_days = leave_details.leaves_remaining

        if leave_days > allowed_days:

            raise ValidationError("Leaves to be compensated more than remaining leaves")

        return super().validate(data)

class CompensateLeaveApplicationResponseSerializer(DynamicFieldsModelSerializer):
    class Meta:

        model = CompensateLeaveApplication
        fields = "__all__"


class CompensateLeaveApplicationListSerializer(serializers.Serializer):

    compensate_leave_application_ids = serializers.ListField(
        child=serializers.IntegerField()
    )


# class CalendarSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Calendar
#         fields = "__all__"


# class EventsSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Events
#         fields = "__all__"
