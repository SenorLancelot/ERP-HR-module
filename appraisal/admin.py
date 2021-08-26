from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Appraisal)
admin.site.register(AppraisalTemplate)
admin.site.register(Goal)
admin.site.register(Project)
admin.site.register(AppraisalGoalMembership)
admin.site.register(AppraisalProjectMembership)
admin.site.register(AppraisalResult)
