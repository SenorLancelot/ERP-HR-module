from rest_framework import routers
from .views import *
from django.urls import path, include

router = routers.DefaultRouter()
router.register(
    r"appraisal_template", AppraisalTemplateViewSet, basename="appraisal_template"
)
router.register(r"appraisal", AppraisalViewSet, basename="appraisal")
router.register(r"goals", GoalViewSet, basename="goal")
router.register(
    r"other_contribution", OtherContributionViewset, basename="other_contribution"
)


urlpatterns = router.urls
