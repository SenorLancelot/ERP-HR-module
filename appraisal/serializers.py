from django.db.models import fields
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
        read_only_field = [
            "id",
        ]

    def validate_max_score(self, max_score):
        if max_score<=0:
            raise serializers.ValidationError("max_score must be positive")
        return max_score


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
        for goal_data in goals_data:
            goal = Goal(**goal_data)
            goal.save()
            appraisal_template.fk_goal.add(goal)

        appraisal_template.save()

        return appraisal_template

    def update(self, instance, validated_data):

        # goals = (instance.fk_goal).all()
        # goals = list(goals)

        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.save()
        goals_data = validated_data.get("fk_goal")

        new_fk_ids = []
        for goal_data in goals_data:
            goal_id = goal_data.get("id", None)
            if goal_id and Goal.objects.get(id = goal_id):
                goal = Goal.objects.get(id=goal_id)
                goal.key_result_area = goal_data.get(
                    "key_result_area", goal.key_result_area
                )
                goal.weightage = goal_data.get("weightage", goal.weightage)
                goal.max_score = goal_data.get("max_score", goal.max_score)
                goal.save()
                if(goal_id not in list(instance.fk_goal.all().values_list('id', flat=True))):
                    instance.fk_goal.add(goal_id)
                new_fk_ids.append(goal.id)
            else:
                goal = Goal(**goal_data)
                goal.save()
                new_fk_ids.append(goal.id)
                instance.fk_goal.add(goal)
        
        remove_fk_goal = instance.fk_goal.all().exclude(id__in=new_fk_ids)
        instance.fk_goal.remove(*remove_fk_goal)
        instance.save()

        return instance

    def validate_fk_goal(self, goals_data):
        total_weightage=0
        for goal_data in goals_data:
            total_weightage+=goal_data['weightage']
            # if goal_data['max_score']<=0:
            #     raise serializers.ValidationError("max_score must be positive")
            
        if total_weightage != 100.0:
            raise serializers.ValidationError("total weightage must be equal to 100")
        
        return goals_data
    
    


class AppraisalTemplateDeleteSerializer(serializers.Serializer):

    template_ids = serializers.ListField(child=serializers.IntegerField())


class ProjectSerializer(serializers.Serializer):
    class Meta:
        model = Project
        fields = ["fk_employee", "name"]


class AppraisalGoalMembershipSerializer(serializers.Serializer):
    class Meta:
        model = AppraisalGoalMembership
        fields = "__all__"


class AppraisalProjectMembershipSerializer(serializers.Serializer):
    class Meta:
        model = AppraisalProjectMembership
        fields = "__all__"


class AppraisalSerializer(serializers.Serializer):
    fk_goal = AppraisalGoalMembership()
    fk_project_ranks = AppraisalProjectMembershipSerializer()

    class Meta:
        model = Appraisal
        fields = [
            "fk_appraiser",
            "fk_employee",
            "fk_appraiser_template",
            "fk_goal",
            "fk_project_ranks",
            "remarks",
            "created_at",
            "modified_at",
        ]

