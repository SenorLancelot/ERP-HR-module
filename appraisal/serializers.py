from django.core.exceptions import ValidationError
from django.db.models import fields
from django.db.models.query_utils import Q
from rest_framework import serializers
from django.db.models.aggregates import Sum
from rest_framework.fields import ReadOnlyField

from .models import *


class GoalSerializer(serializers.ModelSerializer):
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
        temp_id = (validated_data.get("fk_appraiser_template")).id
        qr = AppraisalTemplate.objects.filter(id=temp_id)
        template_goal_length = qr.values_list("fk_goal__id", flat=True).count()
        total_score_percentage = 0
        appraisal = Appraisal(**validated_data)
        appraisal.save()
        if template_goal_length == len(goals_data):
            for goal_data in goals_data:
                if (
                    goal_data["score"] < 0
                    or goal_data["score"] > (goal_data["fk_goal"]).max_score
                ):
                    appraisal.delete()
                    raise serializers.ValidationError(
                        f"score given is more than maximum score in goal {(goal_data['fk_goal']).id}"
                    )
                else:
                    total_score_percentage += (
                        goal_data["score"] / (goal_data["fk_goal"]).max_score
                    ) * (goal_data["fk_goal"]).weightage
                    appraisal_goal = AppraisalGoalMembership(
                        fk_appraisal=appraisal, **goal_data
                    )
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
        appraisal_id = instance.id
        instance.save()

        temp_id = validated_data.get("fk_appraiser_template").id
        qr = AppraisalTemplate.objects.filter(id=temp_id)
        template_goal_length = qr.values_list("fk_goal__id", flat=True).count()
        total_score_weightage = 0

        goals_data = validated_data.get("fk_goal_score")
        print(goals_data)
        project_ranks = validated_data.get("fk_project_ranks")
        print(project_ranks)

        if template_goal_length == len(goals_data):
            for goal_data in goals_data:
                goal_id = (goal_data["fk_goal"]).id
                print(goal_id)
                if goal_id:
                    if (
                        goal_data["score"] < 0
                        or goal_data["score"] > goal_data["fk_goal"].max_score
                    ):
                        raise serializers.ValidationError("blah")
                    else:
                        total_score_weightage += (
                            goal_data["score"] / (goal_data["fk_goal"]).max_score
                        ) * (goal_data["fk_goal"]).weightage
                        goal = AppraisalGoalMembership.objects.get(
                            fk_appraisal=appraisal_id, fk_goal=goal_id
                        )

                        goal.score = goal_data.get("score", goal.score)
                        goal.save()
                else:
                    raise ValidationError("No id in goal")
        else:
            raise serializers.ValidationError(
                "Total number of goal scores recieved is not according to template goals"
            )
        for project_rank in project_ranks:
            project_id = (project_rank["fk_project"]).id
            if project_id:
                project = AppraisalProjectMembership.objects.get(
                    fk_appraisal=appraisal_id, fk_project=project_id
                )
                project.rank = project_rank.get("rank", project.rank)
            else:
                raise ValidationError("No id in Project")
        # print(total_score_weightage)
        instance.total_score_percentage = total_score_weightage
        instance.save()
        return instance
