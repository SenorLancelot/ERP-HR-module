from django.db import models

# Create your models here.
HIDDEN = 0
DRAFT = 1
LIVE = 2
STATUS_CHOICES = ((HIDDEN, "Hidden"), (DRAFT, "Draft"), (LIVE, "Live"))


class AppraisalTemplate(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()
    fk_goal = models.ManyToManyField("Goal")
    status = models.IntegerField(choices=STATUS_CHOICES, default=LIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


# Remove this once Project model is made
class Project(models.Model):
    fk_employee = models.ForeignKey(
        "employees.Employee", on_delete=models.SET_NULL, null=True
    )
    name = models.CharField(max_length=20)


class Goal(models.Model):
    name = models.CharField(max_length=20)
    weightage = models.FloatField(default=0)
    max_score = models.FloatField(default=5)
    status = models.IntegerField(choices=STATUS_CHOICES, default=LIVE)
    # fk_project = models.ForeignKey("Project", on_delete=models.CASCADE, null=True,  blank=True) #REMOVE THIS FIELD, CREATED ONLY FOR TEsting


class Appraisal(models.Model):

    fk_appraiser = models.ForeignKey(
        "employees.Employee",
        on_delete=models.DO_NOTHING,
        null=True,
        related_name="appraiser",
    )
    fk_employee = models.ForeignKey(
        "employees.Employee", on_delete=models.DO_NOTHING, null=True
    )
    fk_appraiser_template = models.ForeignKey(
        "AppraisalTemplate", on_delete=models.DO_NOTHING, null=True
    )
    fk_goal_score = models.ManyToManyField(
        "Goal", through="AppraisalGoalMembership"
    )  # Check for Naming
    fk_project_ranks = models.ManyToManyField(
        "Project", through="AppraisalProjectMembership"
    )
    # other_contributions_toggle = models.BooleanField(default=False)
    fk_other_contribution = models.ManyToManyField("OtherContribution")

    remarks = models.TextField()
    total_score_percentage = models.FloatField(default=0)
    normalized_score_percentage = models.FloatField(default=0)
    status = models.IntegerField(choices=STATUS_CHOICES, default=LIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class OtherContribution(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    reference_link = models.URLField(max_length=500)
    status = models.IntegerField(choices=STATUS_CHOICES, default=LIVE)


class AppraisalGoalMembership(models.Model):
    fk_appraisal = models.ForeignKey("Appraisal", on_delete=models.DO_NOTHING)
    fk_goal = models.ForeignKey("Goal", on_delete=models.DO_NOTHING)
    score = models.FloatField()


class AppraisalProjectMembership(models.Model):
    fk_appraisal = models.ForeignKey("Appraisal", on_delete=models.DO_NOTHING)
    fk_project = models.ForeignKey("Project", on_delete=models.DO_NOTHING)
    rank = models.PositiveIntegerField()


class AppraisalResult(models.Model):
    fk_employee = models.ForeignKey(
        "employees.Employee", on_delete=models.SET_NULL, null=True
    )
    market_salary = models.FloatField(default=0)
    current_salary = models.FloatField(default=0)
    compa_ratio = models.FloatField(default=1)
    standardized_average = models.IntegerField(default=3)
