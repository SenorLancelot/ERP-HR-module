from django.db.models.aggregates import StdDev, Sum, Avg
from django.shortcuts import render
from rest_framework import generics, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from rest_framework.decorators import action

from .models import *
from .serializers import *

from drf_yasg.utils import swagger_auto_schema
import math

def standardized_score(employee_id):
    queryset = Appraisal.objects.filter(fk_employee = employee_id) #get all the appraisals of an employee
    total_appraisers = 0
    total_score=0
    for query in queryset:
        #for an appraiser get average of the total_percentage_scores that appraiser gave to all the employees
        mean = Appraisal.objects.filter(fk_appraiser=query.fk_appraiser.id).aggregate(Avg('total_score_percentage'))['total_score_percentage__avg']
        #for an appraiser get standard deviation the total_percentage_scores that appraiser gave to all the employees
        std_dev = Appraisal.objects.filter(fk_appraiser=query.fk_appraiser.id).aggregate(StdDev('total_score_percentage'))['total_score_percentage__stddev']
        #standardized_score for that appraisal
        z_score = (query.total_score_percentage - mean)/std_dev
        #z_score to points out of 5
        standardised_score = .5 * (math.erf(z_score / 2 ** .5) + 1)*10/2
        
        total_appraisers+=1
        total_score+=standardised_score
        
        print(query.fk_appraiser.id, mean, std_dev, z_score)
    print(round(total_score/total_appraisers))



# def generate_raise(lb, ub, divisions, pay_grade_raise_ratio, performance_raise_ratio):
#     queryset = AppraisalResult.objects.all()
#       x = queryset.filter(compa_ratio__level__lte = , gte, standa_avg=)
#       for i in x:
#           i.current_salary*
#     for pay_grade in pay_grade_raise_ratio:


class AppraisalTemplateViewSet(viewsets.ViewSet):
    @swagger_auto_schema(responses={200: AppraisalTemplateSerializer})
    @action(detail=False, methods=["get"], url_path="read")
    def read_appraisal_templates(self, request):


        try:
            queryset = AppraisalTemplate.objects.all()
            print(queryset)
        except:
            # print(ValueError)
            return Response(
                {"Message": "DOES NOT EXIST"}, status=status.HTTP_404_NOT_FOUND
            )

        try:
            serialized = AppraisalTemplateSerializer(queryset, many=True)
        except:
            return Response(
                {"Message": "SERIALIZER ERROR"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], url_path="read")
    @swagger_auto_schema(responses={200: AppraisalTemplateSerializer})
    def read_appraisal_template(self, request, pk):

        standardized_score(pk)

        try:
            queryset = AppraisalTemplate.objects.get(id=pk)
        except:
            return Response({"Message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        try:
            serialized = AppraisalTemplateSerializer(instance=queryset)

        except:
            return Response(
                {"Message": "Serializer Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=AppraisalTemplateSerializer,
        responses={200: AppraisalTemplateSerializer},
    )
    @action(detail=False, methods=["post"], url_path="create")
    def create_appraisal_template(self, request):

        print(request.data['fk_goal'])
        serialized = AppraisalTemplateSerializer(data=request.data)

        if serialized.is_valid():

            # for goal in request.data['fk_goal']:
            #     total_weightage+=goal['weightage']

            # if total_weightage is not 100:
            #     return Response({'Message': 'Summation of all weightages must be equal to 100'})

            serialized.save()

            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=AppraisalTemplateSerializer,
        responses={200: AppraisalTemplateSerializer},
    )
    @action(detail=False, methods=["patch"], url_path="update")
    def update_appraisal_template(self, request):

        try:
            template = request.data["id"]

        except:
            return Response(
                {"Message": "Request body incorrect. Please specify ID."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        queryset = AppraisalTemplate.objects.get(id=template)
        serialized = AppraisalTemplateSerializer(queryset, request.data, partial=True)

        if serialized.is_valid():
            total_weightage = 0.0
            for goal in request.data["fk_goal"]:
                total_weightage += goal["weightage"]
            if not (total_weightage >= 0 and total_weightage <= 100):
                return Response(
                    {"Message": "weightage cant excede 100%"},
                )
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=AppraisalTemplateDeleteSerializer,
        responses={200: AppraisalTemplateDeleteSerializer},
    )
    @action(detail=False, methods=["delete"], url_path="delete")
    def delete_appraisal_template(self, request):

        serialized = AppraisalTemplateDeleteSerializer(data=request.data)

        if serialized.is_valid():
            AppraisalTemplate.objects.filter(
                id__in=request.data["template_ids"]
            ).delete()

            return Response(data=request.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class GoalViewSet(viewsets.ViewSet):
    @swagger_auto_schema(responses={200: GoalSerializer})
    @action(detail=True, methods=["get"], url_path="read")
    def read_goal(self, request, pk):

        try:
            queryset = Goal.objects.get(id=pk)
        except:
            return Response({"Message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        try:
            serialized = GoalSerializer(instance=queryset)
        except:
            return Response(
                {"Message": "Serializer error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={200: GoalSerializer})
    @action(detail=False, methods=["get"], url_path="read")
    def read_goals(self, request):

        try:
            queryset = Goal.objects.all()
        except:
            return Response({"Message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        try:
            serialized = GoalSerializer(instance=queryset, many=True)
        except:
            return Response(
                {"Message": "Serializer error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=GoalSerializer, responses={200: GoalSerializer})
    @action(detail=False, methods=["patch"], url_path="update")
    def update_goals(self, request):

        try:
            goal = request.data["id"]

        except:

            return Response(
                {"Message": "Request body incorrect. Please specify ID."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        queryset = Goal.objects.get(id=goal)

        serialized = GoalSerializer(queryset, request.data, partial=True)

        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], url_path="create")
    @swagger_auto_schema(request_body=GoalSerializer, responses={200: GoalSerializer})
    def create_goals(self, request):

        serialized = GoalSerializer(data=request.data, many=True)

        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["delete"], url_path="delete")
    @swagger_auto_schema(
        request_body=GoalListSerializer, responses={200: GoalListSerializer}
    )
    def delete_goals(self, request):

        serialized = GoalListSerializer(data=request.data)

        if serialized.is_valid():
            Goal.objects.filter(id__in=request.data["goal_ids"]).delete()

            return Response(data=request.data, status=status.HTTP_200_OK)
        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class AppraisalViewSet(viewsets.ViewSet):
    @swagger_auto_schema(responses={200: AppraisalSerializer})
    @action(detail=False, methods=["get"], url_path="read")
    def read_appraisals(self, request):

        try:
            queryset = Appraisal.objects.all()

        except:
            # print(ValueError)
            return Response(
                {"Message": "DOES NOT EXIST"}, status=status.HTTP_404_NOT_FOUND
            )

        try:
            serialized = AppraisalSerializer(queryset, many=True)
        except:
            return Response(
                {"Message": "SERIALIZER ERROR"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=AppraisalSerializer, responses={200: AppraisalSerializer}
    )
    @action(detail=False, methods=["post"], url_path="create")
    def create_appraisal(self, request):

        serialized = AppraisalSerializer(data=request.data)

        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)
