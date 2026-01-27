from rest_framework import status
from qdpc.core import constants
from rest_framework.response import Response
# from qdpc.services.rawmaterial_service import RawMaterialService
from qdpc.core.modelviewset import BaseModelViewSet
from django.shortcuts import render, redirect
from qdpc_core_models.models.raw_materialbach import RawMaterialBatch
from qdpc_core_models.models.unit import Unit
from qdpc_core_models.models.acceptance_test import AcceptanceTest
from product.serializers.acceptence_test_serializer import AcceptanceTestSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Max
from urllib.parse import unquote
from qdpc.notifications import create_notification
from django.http import JsonResponse
import json

class AcceptanceTestAdd(BaseModelViewSet):
    parser_classes = [MultiPartParser, FormParser]

    """ Raw Material List API for qdpc application"""
 
    def get(self, request):
        # raw_material_batch = self.get_all_obj(model_name=RawMaterial)
        units = self.get_all_obj(model_name=Unit)
        context = {
            'units':units
        }
        return render(request, 'acceptance_test_add.html',context)
    
    def post(self, request):
        try:
            # Get form data
            name = request.POST.get('name')
            test_type = request.POST.get('test_type')
            min_value = request.POST.get('min_value')
            max_value = request.POST.get('max_value')
            unit_id = request.POST.get('unit')
            reevaluation_frequency_value = request.POST.get('reevaluation_frequency_value')
            reevaluation_frequency_unit = request.POST.get('reevaluation_frequency_unit')
            test_result = request.POST.get('test_result')
            specification_result = request.POST.get('specification_result')
            
            # Validate required fields
            if not name or not test_type or not reevaluation_frequency_value or not reevaluation_frequency_unit:
                return JsonResponse({
                    'success': False,
                    'message': 'Required fields are missing'
                }, status=400)
            
            # Convert numeric values
            try:
                min_value = int(min_value) if min_value else None
                max_value = int(max_value) if max_value else None
                reevaluation_frequency_value = int(reevaluation_frequency_value)
            except ValueError:
                return JsonResponse({
                    'success': False,
                    'message': 'Invalid numeric values'
                }, status=400)
            
            # Create acceptance test
            acceptance_test = AcceptanceTest.objects.create(
                name=name,
                test_type=test_type,
                min_value=min_value,
                max_value=max_value,
                unit_id=unit_id if unit_id else None,
                reevaluation_frequency_value=reevaluation_frequency_value,
                reevaluation_frequency_unit=reevaluation_frequency_unit,
                test_result=test_result,
                specification_result=specification_result
            )
            
            # Create notification
            notification_message = f"New acceptance test '{acceptance_test.name}' was added."
            create_notification(notification_message)
            
            return JsonResponse({
                'success': True,
                'message': 'Acceptance test created successfully!',
                'data': {
                    'id': acceptance_test.id,
                    'name': acceptance_test.name
                }
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error creating acceptance test: {str(e)}'
            }, status=500)


class AcceptanceTestList(BaseModelViewSet):
    """ Raw Material Acceptance Test List API """

    def get(self, request):
        # Extract the ID from query parameters (if provided)
        test_id = request.GET.get('id', None)

        if test_id:
            print("Entered test id")
            # If an ID is provided, filter directly by that ID
            latest_tests = AcceptanceTest.objects.filter(id=test_id)
            test_serializer = AcceptanceTestSerializer(latest_tests, many=True)

            context = {
                'acceptance_tests': test_serializer.data,
            }
            print("context",context)
            return Response(context)
            
        else:
            # Get the most recent entry for each AcceptanceTest based on the name
            acceptance_tests = AcceptanceTest.objects.values('name').annotate(latest_id=Max('id'))
            
            # Filter the AcceptanceTest objects to get only the most recent ones
            latest_tests = AcceptanceTest.objects.filter(id__in=[test['latest_id'] for test in acceptance_tests])

        # Serialize the filtered results
        test_serializer = AcceptanceTestSerializer(latest_tests, many=True)

        context = {
            'acceptance_tests': test_serializer.data,
        }
        print(context)
        return render(request, 'rmtest-list.html', context)


class DeleteAcceptanceView(BaseModelViewSet):
    """
    View to handle the deletion of a source using the POST method.
    """

    def post(self, request, acceptancetestId, format=None):
        print(f"Deleting acceptance test with ID: {acceptancetestId}")  # Debugging

        try:
            decoded_acceptancetestId = unquote(acceptancetestId)  # Decode URL-encoded string
            acceptancetest = AcceptanceTest.objects.get(name=decoded_acceptancetestId)
            acceptancetest.delete()
            return Response({
                'success': True,
                'message': constants.ACCEPTANCETEST_DELETE_SUCCESSFULLY
            }, status=status.HTTP_200_OK)
        except AcceptanceTest.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Acceptancetest not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
class ViewAcceptanceTestDetailView(BaseModelViewSet):
    """View to handle viewing of acceptance test details using POST method."""
    
    def post(self, request, acceptanceTestId, format=None):
        try:
            acceptance_test = AcceptanceTest.objects.get(id=acceptanceTestId)
            serializer = AcceptanceTestSerializer(acceptance_test)
            data = serializer.data
            
            # Add unit name if exists
            if acceptance_test.unit:
                data['unit_name'] = acceptance_test.unit.name
            
            return Response({
                'success': True,
                'message': "Acceptance test data fetched successfully.",
                'data': data
            }, status=status.HTTP_200_OK)
            
        except AcceptanceTest.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Acceptance test not found.'
            }, status=status.HTTP_404_NOT_FOUND)
            
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)