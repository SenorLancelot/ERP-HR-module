from django.contrib import admin
from mptt.admin import MPTTModelAdmin

# Register your models here.
from .models import *


admin.site.register(Employee)
admin.site.register(EmployeeGroup)
admin.site.register(Department)
admin.site.register(Designation)
admin.site.register(Attendance)
admin.site.register(EmployeeCheckin)
admin.site.register(LeaveApplication)
admin.site.register(MonthlyReport)
admin.site.register(LeavePolicy)
admin.site.register(LeaveType)
admin.site.register(LeavePolicy_Type_Membership)
admin.site.register(Schedule)
