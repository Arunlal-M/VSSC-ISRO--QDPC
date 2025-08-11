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
class AcceptanceTestAdd(BaseModelViewSet):
    parser_classes = [MultiPartParser, FormParser]

    """ Raw Material List API for qdpc application"""
 
    def get(self, request):
        # raw_material_batch = self.get_all_obj(model_name=RawMaterial)
        units = self.get_all_obj(model_name=Unit)
        context = {
            'units':units
        }
        return render(request, 'acceptance_test.html',context)
    
    def post(self, request):
        # Validate the incoming data using the serializer   
        serializer = AcceptanceTestSerializer(data=request.data)

        if serializer.is_valid():
            acceptance_test = serializer.save()
            success = True
            message = 'Acceptance test added successfully!'
            data = serializer.data
            status_code = status.HTTP_201_CREATED
            notification_message = f"New acceptance test '{acceptance_test.name}' was added."
            create_notification(notification_message)  # Create a notification
        else:
            success = False
            message = 'Validation failed.'
            data = serializer.errors  # 👈 Return validation errors
            status_code = status.HTTP_400_BAD_REQUEST

        return Response({
            'success': success,
            'message': message,
            'data': data
        }, status=status_code)


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