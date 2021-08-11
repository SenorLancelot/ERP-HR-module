from rest_framework import serializers

from .models import *


class GoalSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = Goal
        fields = [
            "id",
            "key_result_area",
            "weightage",
            "max_score",
        ]
        read_only_field = ['id',]

class GoalListSerializer(serializers.Serializer):

    goal_ids = serializers.ListField(child=serializers.IntegerField())


class AppraisalTemplateSerializer(serializers.ModelSerializer):
    fk_goal = GoalSerializer(many=True)

    class Meta:
        model = AppraisalTemplate
        fields = [
            "id",
            "name",
            "description",
            "fk_goal",
            "created_at",
            "modified_at",
        ]

    def create(self, validated_data):
        goals_data = validated_data.pop("fk_goal")

        appraisal_template = AppraisalTemplate(**validated_data)
        appraisal_template.save()
        for goal_data in goals_data:
            goal = Goal(**goal_data)
            goal.save()
            appraisal_template.fk_goal.add(goal)

        appraisal_template.save()

        return appraisal_template

    def update(self, instance, validated_data):

        # goals = (instance.fk_goal).all()
        # goals = list(goals)

        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        goals_data = validated_data.get("fk_goal")
        print(goals_data)
        for goal_data in goals_data:
            print (goal_data)  
            goal_id = goal_data.get('id', None)
            print(goal_id)
            if goal_id:
                goal = Goal.objects.get(id=goal_id)
                goal.key_result_area = goal_data.get('key_result_area', goal.key_result_area)
                goal.weightage = goal_data.get('weightage', goal.weightage)
                goal.max_score = goal_data.get('max_score', goal.max_score)
                goal.save()
            else:
                goal = Goal(**goal_data)
                goal.save()
                instance.fk_goal.add(goal)
        
        instance.save()
            
        return instance

class AppraisalTemplateDeleteSerializer(serializers.Serializer):

    template_ids = serializers.ListField(child=serializers.IntegerField())