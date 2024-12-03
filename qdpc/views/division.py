from rest_framework import status
from rest_framework.response import Response
from qdpc.core.modelviewset import BaseModelViewSet
from qdpc_core_models.models.division import Division
from qdpc_core_models.models.center import Center
from product.serializers.div_center_serializers import DivisionSerializer  
from django.shortcuts import render
from qdpc.core import constants

class DivisionListView(BaseModelViewSet):

    def get(self, request, center_id=None, format=None):
        if center_id is not None:
            return self.get_divisions_by_center(request, center_id)
        
        divisions = Division.objects.all()
        center_name = self.get_all_obj(Center)
        serializer = DivisionSerializer(divisions, many=True)
        context = {
            'divisions': serializer.data,
            'center_name': center_name
        }
        return render(request, 'division.html', context)

    def post(self, request, format=None):
        serializer = DivisionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': constants.DIVISION_CREATION_SUCESSFULLY,
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'success': False,
                'message': constants.DIVISION_CREATION_FAILED,
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def get_divisions_by_center(self, request, center_id):
        """
        Retrieve divisions based on the selected center ID.
        """
        try:
            divisions = Division.objects.filter(center_id=center_id)
            serializer = DivisionSerializer(divisions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DeleteDivisonView(BaseModelViewSet):
    """
    View to handle the deletion of a center using the POST method.
    """

    def post(self, request, divisionId, format=None):
        try:
            divison = Division.objects.get(id=divisionId)
            divison.delete()
            return Response({
                'success': True,
                'message': constants.DIVISION_DELETE_SUCCESSFULLY
            }, status=status.HTTP_200_OK)
        except Division.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Center not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)