from django.contrib import admin
from mptt.admin import MPTTModelAdmin

# Register your models here.
from .models import *


admin.site.register(Employee)
admin.site.register(Customer)
admin.site.register(EmployeeGroup)
admin.site.register(Department)
admin.site.register(Designation)
admin.site.register(Attendance)
admin.site.register(EmployeeSession)
admin.site.register(LeaveApplication)
admin.site.register(LeaveApplicationTypeMembership)
# admin.site.register(MonthlyReport)
admin.site.register(LeavePolicy)
admin.site.register(LeaveType)
admin.site.register(Leave)
admin.site.register(LeavePolicyTypeMembership)
admin.site.register(Schedule)
admin.site.register(WorkdayDivision)
admin.site.register(IdentificationDocument)
admin.site.register(IdentificationType)
