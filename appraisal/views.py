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
    def read_template(self, request):

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
    def create_AppraisalTemplate(self, request):

        
        serialized = AppraisalTemplateSerializer(data=request.data)
        
        if serialized.is_valid():
            serialized.save()
            return Response(data=serialized.data, status=status.HTTP_200_OK)

        return Response(data=serialized.errors, status=status.HTTP_200_OK)

