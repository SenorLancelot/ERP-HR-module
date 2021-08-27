from django.core.exceptions import ValidationError
from django.db.models import fields
from django.db.models.query_utils import Q
from rest_framework import serializers
from django.db.models.aggregates import Sum
from rest_framework.fields import ReadOnlyField
from rest_framework.response import Response
from rest_framework import status

from .models import *


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = [
            "id",
            "name",
            "weightage",
            "max_score",
        ]
        read_only_field = [
            "id",
        ]

    def validate_weightage(self, weightage):
        if weightage < 0 or weightage > 100:
            raise serializers.ValidationError("percent must range from 0 to 100")
        return weightage

    def validate_max_score(self, max_score):
        if max_score <= 0:
            raise serializers.ValidationError("max_score must be positive")
        return max_score


class GoalListSerializer(serializers.Serializer):

    goal_ids = serializers.ListField(child=serializers.IntegerField())


class AppraisalTemplateReadSerializer(serializers.ModelSerializer):
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
        read_only_field = ["id", "fk_goal"]


class AppraisalTemplateSerializer(serializers.ModelSerializer):
    # fk_goal = GoalSerializer(many=True, read_only=True)
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
        read_only_field = ["id", "fk_goal"]

    def validate_fk_goal(self, fk_goal):
        total_weightage = 0
        print(type(fk_goal))
        print(fk_goal)
        for goal in fk_goal:
            print(goal.weightage)
            print(type(goal.weightage))
            total_weightage += goal.weightage

        if total_weightage != 100:
            raise ValidationError(
                f"Summation of weightages for a template must be 100 but its comming out to be {total_weightage}"
            )

        return fk_goal


#  ================================= CREATION and UPDATE VIA LIST OF GOAL OBJECTS =====================================

# def create(self, validated_data):
#     goals_data = validated_data.pop("fk_goal")

#     appraisal_template = AppraisalTemplate(**validated_data)
#     appraisal_template.save()
#     for goal_data in goals_data:
#         goal = Goal(**goal_data)
#         goal.save()
#         appraisal_template.fk_goal.add(goal)

#     appraisal_template.save()

#     return appraisal_template


# def update(self, instance, validated_data):

#     # goals = (instance.fk_goal).all()
#     # goals = list(goals)

#     instance.name = validated_data.get("name", instance.name)
#     instance.description = validated_data.get("description", instance.description)
#     instance.save()
#     goals_data = validated_data.get("fk_goal")

#     new_fk_ids = []
#     for goal_data in goals_data:
#         goal_id = goal_data.get("id", None)
#         if goal_id and Goal.objects.get(id=goal_id):
#             goal = Goal.objects.get(id=goal_id)
#             goal.key_result_area = goal_data.get(
#                 "key_result_area", goal.key_result_area
#             )
#             goal.weightage = goal_data.get("weightage", goal.weightage)
#             goal.max_score = goal_data.get("max_score", goal.max_score)
#             goal.save()
#             if goal_id not in list(
#                 instance.fk_goal.all().values_list("id", flat=True)
#             ):
#                 instance.fk_goal.add(goal_id)
#             new_fk_ids.append(goal.id)
#         else:
#             goal = Goal(**goal_data)
#             goal.save()
#             new_fk_ids.append(goal.id)
#             instance.fk_goal.add(goal)

#     remove_fk_goal = instance.fk_goal.all().exclude(id__in=new_fk_ids)
#     instance.fk_goal.remove(*remove_fk_goal)
#     instance.save()

#     return instance

# def validate_fk_goal(self, goals_data):
#     total_weightage = 0
#     for goal_data in goals_data:
#         total_weightage += goal_data["weightage"]
#         # if goal_data['max_score']<=0:
#         #     raise serializers.ValidationError("max_score must be positive")

#     if total_weightage != 100.0:
#         raise serializers.ValidationError("total weightage must be equal to 100")

#     return goals_data
# ================================= CREATION VIA LIST OF GOAL OBJECTS =====================================


class AppraisalTemplateDeleteSerializer(serializers.Serializer):

    template_ids = serializers.ListField(child=serializers.IntegerField())


class ProjectSerializer(serializers.Serializer):
    class Meta:
        model = Project
        fields = ["fk_employee", "name"]


class AppraisalGoalMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppraisalGoalMembership
        fields = ["fk_goal", "score"]


class AppraisalProjectMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppraisalProjectMembership
        fields = ["fk_project", "rank"]


class AppraisalReadSerializer(serializers.ModelSerializer):
    fk_goal_score = AppraisalGoalMembershipSerializer(
        source="appraisalgoalmembership_set", many=True
    )
    fk_project_ranks = AppraisalProjectMembershipSerializer(
        source="appraisalprojectmembership_set", many=True
    )

    class Meta:
        model = Appraisal
        fields = [
            "id",
            "fk_appraiser",
            "fk_employee",
            "fk_appraiser_template",
            "fk_goal_score",
            "fk_project_ranks",
            "remarks",
            "total_score_percentage",
            "created_at",
            "modified_at",
        ]

        read_only_field = ["id"]
        # depth = 1

        # def score_objects(self,id):
        #     obj = AppraisalGoalMembership.objects.filter(fk_appraisal=id)
        #     fk_goal_score = AppraisalGoalMembershipSerializer(obj, many=True)
        #     return fk_goal_score


class AppraisalCreateSerializer(serializers.ModelSerializer):
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
            "total_score_percentage",
            "created_at",
            "modified_at",
        ]
        read_only_field = ["total_score_percentage"]

    def create(self, validated_data):
        goals_data = validated_data.pop("fk_goal_score")
        project_ranks = validated_data.pop("fk_project_ranks")

        try:
            template_id = validated_data.get("fk_appraiser_template").id
            query = AppraisalTemplate.objects.filter(id=template_id)

        except AppraisalTemplate.DoesNotExist:
            return Response(
                {"Message": "The Request Body incorrect"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        appraisal = Appraisal(**validated_data)
        appraisal.save()

        total_score_percentage = 0
        if (query.values_list("fk_goal__id", flat=True).count()) == len(goals_data):
            for goal_data in goals_data:
                if (
                    goal_data["score"] < 0
                    or goal_data["score"] > goal_data["fk_goal"].max_score
                ):
                    goal_data["score"] = 0
                    # appraisal.status=0 #invalid
                    pass

                appraisal_goal = AppraisalGoalMembership(
                    fk_appraisal=appraisal, **goal_data
                )

                total_score_percentage += (
                    goal_data["score"] / (goal_data["fk_goal"]).max_score
                ) * goal_data["fk_goal"].weightage

                appraisal_goal.save()
        else:
            raise serializers.ValidationError(
                "Total number of goal scores recieved is not according to template goals"
            )
        appraisal.total_score_percentage = total_score_percentage
        appraisal.save()

        for project_rank in project_ranks:
            appraisal_project = AppraisalProjectMembership(
                fk_appraisal=appraisal, **project_rank
            )
            appraisal_project.save()

        return appraisal

    def update(self, instance, validated_data):
        instance.remarks = validated_data["remarks"]
        instance.save()

        try:
            template_id = validated_data.get("fk_appraiser_template").id
            query = AppraisalTemplate.objects.filter(id=template_id)

        except AppraisalTemplate.DoesNotExist:
            return Response(
                {"Message": "The Request Body incorrect"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # template_goal_length =
        total_score_percentage = 0

        goals_data = validated_data.get("fk_goal_score")
        project_ranks = validated_data.get("fk_project_ranks")

        if query.values_list("fk_goal__id", flat=True).count() == len(goals_data):
            for goal_data in goals_data:
                # goal_id =
                # print(goal_id)
                if goal_data["fk_goal"].id:
                    if (
                        goal_data["score"] < 0
                        or goal_data["score"] > goal_data["fk_goal"].max_score
                    ):
                        goal_data["score"] = 0
                        # instance.status=0
                        pass

                    try:
                        goal = AppraisalGoalMembership.objects.get(
                            fk_appraisal=instance.id,
                            fk_goal=goal_data["fk_goal"].id,
                        )
                        goal.score = goal_data.get("score", goal.score)
                        goal.save()
                        total_score_percentage += (
                            goal_data["score"] / goal_data["fk_goal"].max_score
                        ) * (goal_data["fk_goal"]).weightage
                    except AppraisalGoalMembership.DoesNotExist:
                        return Response(
                            {"Message": "Appraisal score doesn't exist"},
                            status=status.HTTP_404_NOT_FOUND,
                        )
                    # Error handling of getting score
                else:
                    raise ValidationError("No id in goal")
        else:
            raise serializers.ValidationError(
                "Total number of goal scores recieved is not according to template goals"
            )

        for project_rank in project_ranks:
            if project_rank["fk_project"].id:
                try:
                    project = AppraisalProjectMembership.objects.get(
                        fk_appraisal=instance.id,
                        fk_project=project_rank["fk_project"].id,
                    )

                    project.rank = project_rank.get("rank", project.rank)
                    project.save()

                except AppraisalProjectMembership.DoesNotExist:
                    return Response(
                        {"Message": "Project Task doesn't exist"},
                        status=status.HTTP_404_NOT_FOUND,
                    )

            else:
                raise ValidationError("No id in Project")

        instance.total_score_percentage = total_score_percentage
        instance.save()
        return instance
