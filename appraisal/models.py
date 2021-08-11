from django.db import models

# Create your models here.


class AppraisalTemplate(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()
    fk_goal = models.ManyToManyField("Goal")

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


# Remove this once Project model is made
class Project(models.Model):
    fk_employee = models.ForeignKey(
        "employees.Employee", on_delete=models.SET_NULL, null=True
    )
    name = models.CharField(max_length=20)


class Goal(models.Model):
    key_result_area = models.CharField(max_length=20)
    weightage = models.FloatField(default=0)
    max_score = models.FloatField(default=5)


class Appraisal(models.Model):

    fk_appraiser = models.ForeignKey(
        "employees.Employee",
        on_delete=models.SET_NULL,
        null=True,
        related_name="appraiser",
    )
    fk_employee = models.ForeignKey(
        "employees.Employee", on_delete=models.SET_NULL, null=True
    )
    fk_appraiser_template = models.ForeignKey(
        "AppraisalTemplate", on_delete=models.SET_NULL, null=True
    )
    fk_goal = models.ManyToManyField("Goal", through="AppraisalGoalMembership")
    fk_project_ranks = models.ManyToManyField(
        "Project", through="AppraisalProjectMembership"
    )
    remarks = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class AppraisalGoalMembership(models.Model):
    fk_appraisal = models.ForeignKey("Appraisal", on_delete=models.CASCADE)
    fk_goal = models.ForeignKey("Goal", on_delete=models.CASCADE)
    score = models.FloatField()


class AppraisalProjectMembership(models.Model):
    fk_appraisal = models.ForeignKey("Appraisal", on_delete=models.CASCADE)
    fk_project = models.ForeignKey("Project", on_delete=models.CASCADE)
    rank = models.PositiveIntegerField()