from django.shortcuts import render
from rest_framework import generics, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response



from rest_framework.decorators import action

from .models import *
from .serializers import *

from drf_yasg.utils import swagger_auto_schema


class AppraisalViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['get'], url_path='read')
    @swagger_auto_schema(responses={200: AppraisalTemplateSerializer})
    def read_appraisal_template(self, request):

        try:
            queryset = AppraisalTemplate.objects.all()
            print(queryset)
        except:
            # print(ValueError)
            return Response({'Message': 'DOES NOT EXIST'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            serialized = AppraisalTemplateSerializer(queryset, many=True)
        except:
            return Response(
                {'Message': 'SERIALIZER ERROR'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'], url_path='create')
    @swagger_auto_schema(request_body=AppraisalTemplateSerializer, responses={200: AppraisalTemplateSerializer})
    def create_appraisal_template(self, request):

        print(request.data['fk_goal'])
        total_weightage = 0
        serialized = AppraisalTemplateSerializer(data=request.data)
        
        if serialized.is_valid():
            
            for goal in request.data['fk_goal']:
                total_weightage+=goal['weightage']
            
            if total_weightage is not 100:
                return Response({'Message': 'Summation of all weightages must be equal to 100'})
            
            serialized.save()
            
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['patch'], url_path='update')
    @swagger_auto_schema(request_body=AppraisalTemplateSerializer, responses={200: AppraisalTemplateSerializer})
    def update_appraisal_template(self, request):

        try:
            template = request.data['id']
        
        except:
            return Response(
                {"Message": "Request body incorrect. Please specify ID."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        queryset = AppraisalTemplate.objects.get(id=template)
        serialized = AppraisalTemplateSerializer(queryset, request.data, partial=True)

        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["delete"], url_path="delete")
    @swagger_auto_schema(request_body=AppraisalTemplateDeleteSerializer, responses={200: AppraisalTemplateDeleteSerializer})
    def delete_appraisal_template(self, request):

        serialized = AppraisalTemplateDeleteSerializer(data=request.data)

        if serialized.is_valid():
            AppraisalTemplate.objects.filter(id__in=request.data['template_ids']).delete()

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

    @swagger_auto_schema(
        request_body=GoalSerializer, responses={200: GoalSerializer}
    )
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
    @swagger_auto_schema(
        request_body=GoalSerializer, responses={200: GoalSerializer}
    )
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


