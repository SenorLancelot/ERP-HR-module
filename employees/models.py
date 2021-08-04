from django.db import models

from mptt.models import MPTTModel, TreeForeignKey
import datetime

# Add _at instead of _time,
# Add _date instead of date_of
# created at and updated at
# created by modified by
# change _name to only name


# Create your models here.
class Employee(MPTTModel):

    # employee_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    employmentType = (
        ("Apprentice", "Apprentice"),
        ("Intern", "Intern"),
        ("Piecework", "Piecework"),
        ("Commision", "Commision"),
        ("Contract", "Contract"),
        ("Probation", "Probation"),
        ("Part-Time", "Part-Time"),
        ("Full-Time", "Full-Time"),
    )

    # TODO make this into new table
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )

    employment_type = models.CharField(
        max_length=50, choices=employmentType, default="Full-Time"
    )

    genderChoices = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Others", "Others"),
    )

    gender = models.CharField(max_length=30, choices=genderChoices, default="Others")
    birth_date = models.DateField()  # req
    joining_date = models.DateField(default=datetime.date.today)  # req
    leaving_date = models.DateField(default=datetime.date.today)
    retirement_date = models.DateField(default=datetime.date.today)
    contact_no = models.CharField(max_length=15)  # req
    personal_email = models.EmailField()  # req
    company_email = models.EmailField()

    current_address = models.CharField(
        max_length=200,
    )
    is_current_address_permanent = models.BooleanField(default=True)
    permanent_address = models.CharField(
        max_length=200,
    )

    # TODO: probably new table (make dynamic)
    fk_department = models.ForeignKey(
        "Department", on_delete=models.CASCADE, null=True, blank=True
    )
    fk_designation = models.ForeignKey(
        "Designation", on_delete=models.CASCADE, null=True, blank=True
    )
    fk_employee_group = models.ForeignKey(
        "EmployeeGroup", on_delete=models.SET_NULL, null=True, blank=True
    )
    # TODO  add qualification details to this as well as previous workex and history in company_email

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class IdentificationDocument(models.Model):

    fk_employee = models.ForeignKey("Employee", on_delete=models.CASCADE)
    identification_number = models.CharField(max_length=100, null=False)
    fk_document_type = models.ForeignKey("IdentificationType", on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class IdentificationType(models.Model):

    name = models.CharField(max_length=100, null=False)
    issuing_authority = models.CharField(max_length=100, null=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class EmployeeGroup(models.Model):

    name = models.CharField(max_length=50)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


#################### Departments and Designations ############################################


class Department(MPTTModel):

    name = models.CharField(max_length=30)

    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Department"
        verbose_name_plural = "Departments"


class Designation(models.Model):

    name = models.CharField(max_length=30)

    description = models.CharField(max_length=300)
    fk_schedule = models.ForeignKey("Schedule", on_delete=models.SET_NULL, null=True)
    fk_leave_policy = models.ForeignKey(
        "LeavePolicy", on_delete=models.CASCADE, null=True, blank=True
    )
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    # TODO: things like salary?


##################  Attendance Models ########################################################


class Attendance(models.Model):

    fk_employee = models.ForeignKey("Employee", on_delete=models.CASCADE)
    attendance_date = models.DateField()

    attendanceType = (
        ("Half-Day", "Half-Day"),
        ("Full-Day", "Full-Day"),
        ("Work-From-Home", "Work-From_Home"),
    )

    fk_sessions = models.ManyToManyField("EmployeeSession")
    
    is_late_entry = models.BooleanField(default=False)  
    is_early_exit = models.BooleanField(default=False)
    comment = models.CharField(max_length=100, null=True, blank=True)
    total_time = models.FloatField(default=0.0)
    total_overtime = models.FloatField(default=0.0)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:

        verbose_name_plural = "Attendance"


class EmployeeSession(models.Model):

    fk_employee = models.ForeignKey("Employee", on_delete=models.CASCADE)

    # attendance = models.ForeignKey('Attendances', on_delete=models.CASCADE)
    checked_in_time = models.DateTimeField()
    checked_out_time = models.DateTimeField(blank=True, null=True)
    total_time_elapsed = models.FloatField(
        blank=True, null=True
    )  
    # is_last_session = models.BooleanField(
    #     default=False
    # )  # TODO repurpose using checked_in time
    # is_first_session = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    # TODO created by, modified by


##################  Leave models #############################################################


class LeavePolicy(models.Model):

    fk_leave_type = models.ManyToManyField(
        "LeaveType", through="LeavePolicyTypeMembership", null=True, blank=True
    )
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:

        verbose_name_plural = "Leave Policies"


class LeavePolicyTypeMembership(
    models.Model
):  # TODO change model name without underscores

    fk_leave_policy = models.ForeignKey("LeavePolicy", on_delete=models.CASCADE)
    fk_leave_type = models.ForeignKey("LeaveType", on_delete=models.CASCADE)
    total_days_allowed = models.FloatField(default=0)
    total_consecutive_days_allowed = models.FloatField(default=0)  


class LeaveType(models.Model):

    name = models.CharField(max_length=30)
    is_paid = models.BooleanField(default=False)
    is_carry_forward = models.BooleanField(default=False)
    is_optional = models.BooleanField(default=False)
    is_holiday_leave = models.BooleanField(default=False)  # TODO naming
    is_compensatory = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class LeaveApplication(models.Model):

    fk_leave_type = models.ForeignKey("LeaveType", on_delete=models.CASCADE)
    fk_employee = models.ForeignKey(
        "Employee", on_delete=models.CASCADE, related_name="employee"
    )

    from_date = models.DateField()
    to_date = models.DateField()
    reason = models.CharField(max_length=50)
    fk_leave_approver = models.ForeignKey(
        "Employee", on_delete=models.CASCADE, related_name="leave_approver"
    )

    statusType = (
        ("Open", "Open"),
        ("On Hold", "On Hold"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
        ("Cancelled", "Cancelled"),
    )
    status = models.CharField(max_length=50, choices=statusType, default="Open")
    post_date = models.DateField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)



class Leave(models.Model):

    fk_employee = models.ForeignKey("Employee", on_delete=models.CASCADE)
    fk_leave_type = models.ForeignKey("LeaveType", on_delete=models.CASCADE)

    statusOptions = (("Taken", "Taken"), ("Free", "Free"), ("Encashed", "Encashed"))
    # leave_application = models.ForeignKey('LeavesApplication', null=True, on_delete = models.CASCADE)
    date_of_leave = models.DateField(null=True)
    duration = models.FloatField(default=1)


# TODO Leaves get created at the start itself when an employee is assigned a designations


class Schedule(models.Model):

    total_work_hours = models.FloatField(default=8)
    workday_start_time = models.TimeField()
    workday_end_time = models.TimeField()
    half_day = models.FloatField(default=6)
    quarter_day = models.FloatField(default=3)
    # TODO create this







# class EmployeeLeaveReport(models.Model):

#     fk_employee = models.ForeignKey("Employee", on_delete=models.CASCADE)
#     fk_leave_types = models.ManyToManyField("LeaveType")


# class LeaveReport_Membership(models.Model):

#     fk_employee_report = models.ForeignKey(
#         "EmployeeLeaveReport", on_delete=models.CASCADE
#     )
#     fk_leave_type = models.ForeignKey("LeaveType", on_delete=models.CASCADE)
#     leaves_taken = models.IntegerField()
#     leaves_remaining = models.IntegerField()
#     blocked_till = models.DateField()
#     is_compulsory = models.BooleanField(default=False)




# class Calendar(models.Model):
#
#     date = models.DateField()
#     is_holiday = models.BooleanField(default = False)
#     is_compulsory_working = models.BooleanField(default = False)
#     comment = models.CharField(max_length=300, null=True, blank=True)
#     universal_blocked_leave = models.BooleanField(default = False)


# class Events(models.Model):
#
#     event_id = models.BigAutoField(primary_key=True)
#     fk_start_date = models.ForeignKey('Calendar', on_delete= models.CASCADE)
#     fk_end_date = models.ForeignKey('Calendar', on_delete= models.CASCADE)

#     start_time = models.TimeField()
#     end_time = models.TimeField()

#     fk_department = models.ForeignKey('Departments', on_delete= models.CASCADE)
#     fk_employees = models.ManyToManyField('Employee')

#     fk_administrator = models.ForeignKey('Employee', on_delete= models.CASCADE)
