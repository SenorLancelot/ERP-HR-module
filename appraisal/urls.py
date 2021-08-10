from rest_framework import routers
from .views import *
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'appraisal_template', AppraisalViewSet, basename='appraisal_template')

urlpatterns = router.urls
