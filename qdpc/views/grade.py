# views.py
from qdpc.core.modelviewset import BaseModelViewSet
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.http import JsonResponse
from rest_framework import status
from django.views import View
from qdpc_core_models.models.grade import Grade
from product.serializers.grade_serializer import GradeSerializer
from qdpc.core import constants


class GradeView(BaseModelViewSet):
    def get(self, request, format=None):
        grades = Grade.objects.all()
        serializer = GradeSerializer(grades, many=True)
        context={
            'grades': serializer.data,
        }
        print(context)
        return render(request, 'grade.html',context)     
       
    
    def post(self, request, format=None):
        data = {}
        is_success = False
        message = constants.GRADE_CREATION_FAILED
        status_code = status.HTTP_400_BAD_REQUEST
        serializer = GradeSerializer(data=request.data)

        try:
            if serializer.is_valid():
                serializer.save()
                is_success = True
                status_code = status.HTTP_201_CREATED
                data = serializer.data
                message = constants.GRADE_CREATION_SUCESSFULLY
            else:
                # pass
                is_success = False
                status_code = status.HTTP_400_BAD_REQUEST
                data = serializer.errors
                message = constants.GRADE_CREATION_FAILED


        except Exception as ex:
            is_success = False
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            message = constants.GRADE_CREATION_FAILED

        return self.render_response(data, is_success, message, status_code)


class DeleteGradeView(BaseModelViewSet):
    """
    View to handle the deletion of a source using the POST method.
    """

    def post(self, request, gradeId, format=None):
        try:
           grades= Grade.objects.get(id=gradeId)
           grades.delete()
           return Response({
                'success': True,
                'message': constants.GRADE_DELETE_SUCCESSFULLY
            }, status=status.HTTP_200_OK)
        except Grade.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Grade not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    