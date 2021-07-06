from rest_framework import serializers

from .models import Employees, EmployeeGroup, Departments, Designations, Attendances, EmployeeCheckins, LeavePolicies, LeavesApplications, Leave

class EmployeesSerializer(serializers.Serializer):

    class Meta:

        model = Employees
        fields = "__all__"

class EmployeeGroupSerializer(serializers.Serializer):

    class Meta:

        model = EmployeeGroup
        fields = "__all__"

class DepartmentsSerializer(serializers.Serializer):

    class Meta:

        model = Departments
        fields = "__all__"

class DesignationsSerializer(serializers.Serializer):

    class Meta:

        model = Designations
        fields = "__all__"

class AttendancesSerializer(serializers.Serializer):

    class Meta:

        model = Attendances
        fields = "__all__"

class EmployeeCheckinsSerializer(serializers.Serializer):

    class Meta:

        model = EmployeeCheckins
        fields = "__all__"

class LeavePoliciesSerializer(serializers.Serializer):

    class Meta:

        model = LeavePolicies
        fields = "__all__"

class LeavesApplicationsSerializer(serializers.Serializer):

    class Meta:

        model = LeavesApplications
        fields = "__all__"

class LeavesSerializer(serializers.Serializer):
    
    class Meta:

        model = Leave
        fields = "__all__"