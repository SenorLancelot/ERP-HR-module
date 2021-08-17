from re import template
from django.core.exceptions import ValidationError
from django.db.models import fields
from django.db.models.query_utils import Q
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

        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.save()

        goals_data = validated_data.get("fk_goal")
        for goal_data in goals_data:
            print(goal_data)
            goal_id = goal_data.get("id", None)
            print(goal_id)
            if goal_id:
                goal = Goal.objects.get(id=goal_id)
                goal.key_result_area = goal_data.get(
                    "key_result_area", goal.key_result_area
                )
                goal.weightage = goal_data.get("weightage", goal.weightage)
                goal.max_score = goal_data.get("max_score", goal.max_score)
                goal.save()
            else:
                goal = Goal(**goal_data)
                goal.save()
                instance.fk_goal.add(goal)

        instance.save()

        return instance


class AppraisalTemplateDeleteSerializer(serializers.Serializer):

    template_ids = serializers.ListField(child=serializers.IntegerField())


class ProjectSerializer(serializers.Serializer):
    class Meta:
        model = Project
        fields = ["fk_employee", "name"]


class AppraisalGoalMembershipSerializer(serializers.ModelSerializer):
    # fk_goal = GoalSerializer(many=True)

    class Meta:
        model = AppraisalGoalMembership
        fields = ["fk_goal", "score"]


class AppraisalProjectMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppraisalProjectMembership
        fields = ["fk_project", "rank"]


class AppraisalSerializer(serializers.ModelSerializer):
    fk_goal_score = AppraisalGoalMembershipSerializer(many=True, write_only=True)
    fk_project_ranks = AppraisalProjectMembershipSerializer(many=True, write_only=True)
    # fk_appraiser_template = AppraisalTemplateSerializer()

    class Meta:
        model = Appraisal
        fields = [
            "fk_appraiser",
            "fk_employee",
            "fk_appraiser_template",
            "fk_goal_score",
            "fk_project_ranks",
            "remarks",
            "total_score",
            "created_at",
            "modified_at",
        ]

    # def temp(self, instance):

    # def create(self, validated_data):

    def create(self, validated_data):
        goals_data = validated_data.pop("fk_goal_score")
        print(goals_data)
        project_ranks = validated_data.pop("fk_project_ranks")
        print(project_ranks)

        appraisal = Appraisal(**validated_data)
        appraisal.save()

        for goal_data in goals_data:
            print(goal_data)
            print(goal_data["fk_goal"])
            appraisal_goal = AppraisalGoalMembership(
                fk_appraisal=appraisal, **goal_data
            )
            appraisal_goal.save()

        for project_rank in project_ranks:
            appraisal_project = AppraisalProjectMembership(
                fk_appraisal=appraisal, **project_rank
            )
            appraisal_project.save()

        return appraisal

    # def update(self, instance, validated_data):
    #     instance.remarks = validated_data["remarks"]
    #     appraisal_id = instance.id
    #     instance.save()

    #     goals_data = validated_data.get("fk_goal_score")

    #     if goals_data.len() != 0:
    #         for goal_data in goals_data:
    #             goal_id = goals_data["id"]
    #             if goal_id:
    #                 goal = AppraisalGoalMembership.objects.filter(
    #                     fk_appraisal=appraisal_id, fk_goal=goal_id
    #                 )
    #                 goal.score = goal_data.get("score", goal.score)
    #             else:
    #                 raise ValidationError("No id in goal")

    #     instance.save()
    #     return instance
