from rest_framework import serializers

from .models import *

class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = '__all__'

class AppraisalTemplateSerializer(serializers.ModelSerializer):
    goals = GoalSerializer(many=True, source='fk_goal', read_only=True)

    class Meta:
        model = AppraisalTemplate
        fields = [
            'id',
            'name',
            'description',
            'created_at',
            'modified_at',
            'goals'
        ]


