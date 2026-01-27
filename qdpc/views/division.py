from rest_framework import status
from rest_framework.response import Response
from qdpc.core.modelviewset import BaseModelViewSet
from qdpc_core_models.models.division import Division
from qdpc_core_models.models.center import Center
from product.serializers.div_center_serializers import DivisionSerializer  
from django.shortcuts import render
from qdpc.core import constants
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from rest_framework.views import APIView




class DivisionAjax(APIView):
    permission_classes = [AllowAny]  
    authentication_classes = []  

    def get(self, request, center_id=None, format=None):
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

        if center_id is not None:
            divisions = Division.objects.filter(center_id=center_id)
            center = get_object_or_404(Center, id=center_id)

            division_data = [
                {
                    'id': div.id,
                    'name': div.name,
                    'center_id': div.center_id,
                    'center_name': center.name
                }
                for div in divisions
            ]

            if is_ajax:
                return JsonResponse({'divisions': division_data})

            return render(request, 'division.html', {
                'divisions': division_data,
                'center_name': center.name
            })

        # No center_id: return all divisions
        divisions = Division.objects.all()
        centers = Center.objects.all()

        division_data = [
            {
                'id': div.id,
                'name': div.name,
                'center_id': div.center_id,
                'center_name': div.center.name
            }
            for div in divisions
        ]

        if is_ajax:
            return JsonResponse({'divisions': division_data})

        return render(request, 'division.html', {
            'divisions': division_data,
            'center_name': [center.name for center in centers]  # or pass full center objects
        })



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
            
class EditDivisionView(BaseModelViewSet):
    """
    View to handle editing of a Division using the PUT method and support division retrieval by center.
    """

    def get(self, request, divisionId=None, center_id=None):
        """
        Handle retrieval of division data by divisionId or filter divisions by center_id.
        """
        try:
            if divisionId is not None:
                # Retrieve a specific division by ID
                division = Division.objects.get(id=divisionId)
                all_centers = Center.objects.all()

                # Create a response data object for the division
                data = {
                    'id': division.id,
                    'name': division.name,
                    'center': {
                        'id': division.center.id,
                        'name': division.center.name
                    },
                    'all_centers': [{'id': center.id, 'name': center.name} for center in all_centers],
                }
                return Response({'data': data}, status=status.HTTP_200_OK)

            elif center_id is not None:
                # Filter divisions by center ID
                divisions = Division.objects.filter(center_id=center_id)
                serializer = DivisionSerializer(divisions, many=True)
                return Response({'divisions': serializer.data}, status=status.HTTP_200_OK)

            else:
                return Response({'message': 'Invalid parameters.'}, status=status.HTTP_400_BAD_REQUEST)

        except Division.DoesNotExist:
            return Response({'detail': 'Division not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Center.DoesNotExist:
            return Response({'detail': 'Center not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, divisionId):
        """
        Handle editing a division by its ID.
        """
        try:
            division = Division.objects.get(id=divisionId)
        except Division.DoesNotExist:
            return Response({'detail': 'Division not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = DivisionSerializer(division, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': 'Division updated successfully.',
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            'success': False,
            'message': 'Validation failed.',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


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