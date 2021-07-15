from django.db import models
import uuid
from mptt.models import MPTTModel, TreeForeignKey
import datetime
# Create your models here.
class Employees(MPTTModel):

    employee_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    
    employmentType = (
        ("Apprentice","Apprentice"),
        ("Intern", "Intern"),
        ("Piecework","Piecework"),
        ("Commision", "Commision"),
        ("Contract","Contract"),
        ("Probation","Probation"),
        ("Part-Time", "Part-Time"),
        ("Full-Time", "Full-Time")
    )

    ## make this into new table
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    employment_type = models.CharField(max_length=50, choices= employmentType, default="Full-Time")

    genderChoices = (
        ("Prefer not to say","Prefer not to say"),
        ("Male", "Male"),
        ("Female", "Female"),
        ("Transgender","Transgender"),
        ("Other", "Other")
    )

    gender = models.CharField(max_length=30, choices= genderChoices, default = "Prefer not to say")
    date_of_birth = models.DateField() #req
    date_of_joining = models.DateField(default=datetime.date.today) #req
    date_of_leaving = models.DateField(default=datetime.date.today)
    date_of_retirement = models.DateField(default=datetime.date.today)
    contact_no = models.CharField(max_length=15) #req
    personal_email = models.EmailField() #req
    company_email = models.EmailField() 
    
    current_address = models.CharField(max_length=200, )
    is_current_address_permanent = models.BooleanField(default=True)
    permanent_address = models.CharField(max_length=200, )

    identificationType = (
        ("Aadhar Card", "Aadhar Card"),
        ("PAN Card", "PAN Card"),
        ("Passport", "Passport"),
        ("VoterID","VoterID")
    )

    identification_document = models.CharField(max_length=30, choices= identificationType, default = "PAN Card")
    identification_number = models.CharField(max_length=50,)
    #TODO: probably new table (make dynamic)
    department = models.ForeignKey('Departments', on_delete=models.CASCADE)
    employee_group = models.ForeignKey('EmployeeGroup', on_delete=models.SET_NULL, null = True, blank= True)
    #  add qualification details to this as well as previous workex and history in company_email

    class Meta:
        verbose_name = "Employee"
        verbose_name_plural = "Employees"



class EmployeeGroup(models.Model):

    group_id = models.CharField(max_length=30, primary_key=True)
    group_name = models.CharField(max_length=50)

    objects = models.Manager()
    class Meta:
        verbose_name = "EmployeeGroup"
        verbose_name_plural = "EmployeeGroups"

#################### Departments and Designations ############################################


class Departments(MPTTModel):

    department_id = models.CharField(max_length=50, primary_key = True)

    department_name = models.CharField(max_length=30)

    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class Meta:
        verbose_name = "Department"
        verbose_name_plural = "Departments"



class Designations(models.Model):

    designation_id = models.CharField(max_length=30, primary_key = True)

    designation_name = models.CharField(max_length=30)

    description = models.CharField(max_length=300)

    #TODO: things like salary?

    class Meta:
        verbose_name = "Designation"
        verbose_name_plural = "Designations"

##################  Attendance Models ########################################################


class Attendances(models.Model):

    employee = models.ForeignKey('Employees', on_delete=models.CASCADE)
    attendance_date = models.DateField()
    
    attendanceType = (
        ("Half-Day", "Half-Day"),
        ("Full-Day", "Full-Day"),
        ("Work-From-Home","Work-From_Home")
    )
    objects = models.Manager()
    checks = models.ManyToManyField('EmployeeCheckins')
    #TODO: change terminology
    late_entry = models.BooleanField(default = False)
    early_exit = models.BooleanField(default = False)
    comment = models.CharField(max_length=100, null=True, blank=True)
    total_time = models.FloatField(default=0.0)
    class Meta:
        verbose_name = "Attendance"
        verbose_name_plural = "Attendances"


class EmployeeCheckins(models.Model):

    
    employee = models.ForeignKey('Employees', on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)
    # attendance = models.ForeignKey('Attendances', on_delete=models.CASCADE)
    checked_in = models.DateTimeField()
    checked_out = models.DateTimeField(blank=True, null=True)
    total_time_elapsed = models.FloatField(blank=True, null=True)

    objects = models.Manager()
    class Meta:
        verbose_name = "EmployeeCheckin"
        verbose_name_plural = "EmployeeCheckins"


##################  Leave models #############################################################
#TODO: maybe we should link leavepolicies with employee
class LeavePolicies(models.Model):

    leavepolicy_id = models.CharField(max_length=50, primary_key= True)

    leave_type = models.ManyToManyField('LeaveType', through= "LeavePolicy_TypeMembership")
    #TODO: leave policy (per designation), leave type (per leave policy) (through membership)
    objects = models.Manager()

    leaves_allowed = models.IntegerField()

    class Meta:
        verbose_name = "LeavePolicy"
        verbose_name_plural = "LeavePolicies"


class LeavePolicy_TypeMembership(models.Model):
    leave_policy = models.ForeignKey('LeavePolicies', on_delete=models.CASCADE)
    leave_type = models.ForeignKey('LeaveType', on_delete=models.CASCADE)
    total_days_allowed = models.IntegerField()
    total_consecutive_days = models.IntegerField()
    



class LeaveType(models.Model):

    leave_type = models.CharField(max_length=30)
    is_paid = models.BooleanField(default = False)
    is_carry_forward = models.BooleanField(default = False)
    is_optional = models.BooleanField(default = False)
    include_holidays_as_leaves = models.BooleanField(default = False)
    is_compensatory = models.BooleanField(default = False)
    allow_encashment = models.BooleanField(default = False)

class LeavesApplications(models.Model):

    leaveapplication_id = models.CharField(max_length=50, primary_key = True)
    leave_type = models.ForeignKey('LeaveType', on_delete=models.CASCADE)
    employee = models.ForeignKey('Employees', on_delete=models.CASCADE, related_name='employee')
    from_date = models.DateField()
    to_date = models.DateField()
    reason = models.CharField(max_length=50)
    leave_approver = models.ForeignKey('Employees', on_delete=models.CASCADE, related_name='leave_approver')
    objects = models.Manager()
    statusType = (
        ("Open", "Open"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
        ("Cancelled", "Cancelled")
    )
    status = models.CharField(max_length=50, choices = statusType, default= "Open")
    post_date = models.DateField()

    class Meta:
        verbose_name = "LeaveApplication"
        verbose_name_plural = "LeaveApplications"

class EmployeeLeaveReport(models.Model):

    employee = models.ForeignKey('Employees', on_delete=models.CASCADE)
    leave_types = models.ManyToManyField('LeaveType')

class LeaveReport_Membership(models.Model):

    employee_report = models.ForeignKey('EmployeeLeaveReport', on_delete=models.CASCADE)
    leave_type = models.ForeignKey('LeaveType', on_delete=models.CASCADE)
    leaves_taken = models.IntegerField()
    leaves_remaining = models.IntegerField()
    blocked_till = models.DateField()
    is_compulsory = models.BooleanField(default=False)


class Leaves(models.Model):

    employee = models.ForeignKey('Employees', on_delete=models.CASCADE)
    leave_type = models.ForeignKey('LeaveType', on_delete=models.CASCADE)
    objects = models.Manager()
    statusOptions = (
        ("Taken","Taken"),
        ("Free","Free"),
        ("Encashed","Encashed")
    )
    #leave_application = models.ForeignKey('LeavesApplication', null=True, on_delete = models.CASCADE)
    date_of_leave = models.DateField(null=True)
    
#Leaves get created at the start itself when an employee is assigned a designations

class MonthlyReports(models.Model):

    objects = models.Manager()
    employee = models.ForeignKey('Employees', on_delete=models.CASCADE)

    total_time_worked = models.FloatField(default=0, null=True, blank=True)