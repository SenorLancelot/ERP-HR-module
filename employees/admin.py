from django.contrib import admin
from mptt.admin import MPTTModelAdmin

# Register your models here.
from .models import *


admin.site.register(Employees)
admin.site.register(EmployeeGroup)
admin.site.register(Departments)
admin.site.register(Designations)
admin.site.register(Attendances)
admin.site.register(EmployeeCheckins)
admin.site.register(LeavesApplications)
admin.site.register(MonthlyReports)
admin.site.register(LeavePolicies)
admin.site.register(LeaveType)
admin.site.register(LeavePolicy_TypeMembership)
admin.site.register(Schedules)
