# views.py
from qdpc.core.modelviewset import BaseModelViewSet
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.http import JsonResponse
from rest_framework import status
from django.views import View
from qdpc_core_models.models.unit import Unit
from product.serializers.unit_serializer import UnitSerializer
from qdpc.core import constants


class UnitView(BaseModelViewSet):
    def get(self, request, format=None):
        units = Unit.objects.all()
        serializer = UnitSerializer(units, many=True)
        context={
            'units': serializer.data,
        }
        print(context)
        return render(request, 'unit.html',context)     
       
    
    def post(self, request, format=None):
        data = {}
        is_success = False
        message = constants.UNIT_CREATION_FAILED
        status_code = status.HTTP_400_BAD_REQUEST
        serializer = UnitSerializer(data=request.data)

        try:
            if serializer.is_valid():
                serializer.save()
                is_success = True
                status_code = status.HTTP_201_CREATED
                data = serializer.data
                message = constants.UNIT_CREATION_SUCESSFULLY
            else:
                # pass
                is_success = False
                status_code = status.HTTP_400_BAD_REQUEST
                data = serializer.errors
                message = constants.UNIT_CREATION_FAILED


        except Exception as ex:
            is_success = False
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            message = constants.UNIT_CREATION_FAILED

        return self.render_response(data, is_success, message, status_code)


class DeleteUnitView(BaseModelViewSet):
    """
    View to handle the deletion of a source using the POST method.
    """

    def post(self, request, unitId, format=None):
        try:
           units= Unit.objects.get(id=unitId)
           units.delete()
           return Response({
                'success': True,
                'message': constants.UNIT_DELETE_SUCCESSFULLY
            }, status=status.HTTP_200_OK)
        except Unit.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Unit not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    