from django.shortcuts import render
from rest_framework import generics, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import *
from .serializers import *
from drf_yasg.utils import swagger_auto_schema


class AppraisalTemplateViewSet(viewsets.ViewSet):
    @swagger_auto_schema(responses={200: AppraisalTemplateSerializer})
    @action(detail=False, methods=["get"], url_path="read")
    def read_appraisal_templates(self, request):

        try:
            queryset = AppraisalTemplate.objects.all()
            print(queryset)
        except:

            return Response(
                {"Message": "DOES NOT EXIST"}, status=status.HTTP_404_NOT_FOUND
            )

        try:
            serialized = AppraisalTemplateReadSerializer(queryset, many=True)
        except:
            return Response(
                {"Message": "SERIALIZER ERROR"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], url_path="read")
    @swagger_auto_schema(responses={200: AppraisalTemplateSerializer})
    def read_appraisal_template(self, request, pk):

        try:
            queryset = AppraisalTemplate.objects.get(id=pk)
        except:
            return Response({"Message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

        try:
            serialized = AppraisalTemplateReadSerializer(instance=queryset)

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

        serialized = AppraisalTemplateSerializer(data=request.data)

        if serialized.is_valid():

            serialized.save()

            queryset = AppraisalTemplate.objects.get(id=serialized.data["id"])

            serialized_response = AppraisalTemplateReadSerializer(queryset)

            return Response(data=serialized_response.data, status=status.HTTP_200_OK)

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
            serialized.save()

            queryset = AppraisalTemplate.objects.get(id=template)

            serialized_response = AppraisalTemplateReadSerializer(queryset)

            return Response(data=serialized_response.data, status=status.HTTP_200_OK)

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
    @swagger_auto_schema(responses={200: AppraisalReadSerializer})
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
            serialized = AppraisalReadSerializer(queryset, many=True)
        except:
            return Response(
                {"Message": "SERIALIZER ERROR"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={200: AppraisalReadSerializer})
    @action(detail=True, methods=["get"], url_path="read")
    def read_appraisal(self, request, pk):

        try:
            queryset = Appraisal.objects.get(id=pk)
        except:
            # print(ValueError)
            return Response(
                {"Message": "DOES NOT EXIST"}, status=status.HTTP_404_NOT_FOUND
            )

        try:
            serialized = AppraisalReadSerializer(instance=queryset)
        except:
            return Response(
                {"Message": "SERIALIZER ERROR"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(data=serialized.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=AppraisalCreateSerializer,
        responses={200: AppraisalCreateSerializer},
    )
    @action(detail=False, methods=["post"], url_path="create")
    def create_appraisal(self, request):

        serialized = AppraisalCreateSerializer(data=request.data)

        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=AppraisalCreateSerializer,
        responses={200: AppraisalCreateSerializer},
    )
    @action(detail=False, methods=["patch"], url_path="update")
    def update_appraisal(self, request):

        try:
            template_id = request.data["id"]

        except:
            return Response(
                {"Message": "Request body incorrect. Please specify ID."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        queryset = Appraisal.objects.get(id=template_id)
        serialized = AppraisalCreateSerializer(queryset, request.data, partial=True)

        if serialized.is_valid():
            serialized.save()

            queryset = Appraisal.objects.get(id=template_id)
            serialized_response = AppraisalCreateSerializer(queryset)

            return Response(data=serialized_response.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)


# class AppraisalGoal(viewsets.ViewSet):
#     @swagger_auto_schema(responses={200: AppraisalGoalMembershipSerializer})
#     @action(detail=False, methods=["get"], url_path="read")
#     def read_goal_score(self, request, ap=1):

#         try:
#             queryset = AppraisalGoalMembership.objects.filter(fk_appraisal=ap)
#             # queryset = AppraisalGoalMembership.objects.all()
#             print(queryset)

#         except:
#             # print(ValueError)
#             return Response(
#                 {"Message": "DOES NOT EXIST"}, status=status.HTTP_404_NOT_FOUND
#             )

#         try:
#             serialized = AppraisalGoalMembershipSerializer(queryset, many=True)
#         except:
#             return Response(
#                 {"Message": "SERIALIZER ERROR"},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             )

#         return Response(data=serialized.data, status=status.HTTP_200_OK)
