from django.contrib import admin
from mptt.admin import MPTTModelAdmin

# Register your models here.
from .models import (Employees, EmployeeGroup, Departments, Designations, Attendances, EmployeeCheckins, LeavePolicies, LeavesApplications)


admin.site.register(Employees)
admin.site.register(EmployeeGroup)
admin.site.register(Departments, MPTTModelAdmin)
admin.site.register(Designations)
admin.site.register(Attendances)
#admin.site.register(EmployeeCheckins)
admin.site.register(LeavesApplications)


