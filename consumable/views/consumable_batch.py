from qdpc.core.modelviewset import BaseModelViewSet
from rest_framework import status
from qdpc.core import constants
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404, render, redirect
from qdpc_core_models.models.consumablebatch import ConsumableBatch
from qdpc_core_models.models.consumable import Consumable
from qdpc_core_models.models.unit import Unit
from consumable.serializers.consumable_batch_serializer import ConsumableBatchDetailedSerializer, ConsumableBatchSerializer
from consumable.serializers.consumable_acceptance_test_seraizler import ConsumableAcceptanceTestSerializer
from qdpc_core_models.models.acceptance_test import AcceptanceTest
from consumable.services.consumable_service import ConsumableService
from datetime import datetime, timedelta
from urllib.parse import unquote
from qdpc_core_models.models.consumableGradeAcceptance import ConsumableGradeAcceptanceTest
from qdpc.services.notification_service import NotificationService



class ConsumableBatchFetchView(BaseModelViewSet):
  

    def get(self,request,pk=None):
        if pk:
            data={}
            success = False
            message = constants.CONSUMABLE_BATCH_FAILD
            status_code = status.HTTP_403_FORBIDDEN
            try:
                success, status_code, data, message = ConsumableService.get_consumable_batch_list(pk=None)
                context = {'batches':data}
                return render(request,'consumable_batchlist.html',context)

            except Exception as ex:
                success = False
                message = constants.CONSUMABLE_BATCH_FAILD
                status_code = status.HTTP_400_BAD_REQUEST
                
                return self.render_response(data,success, message, status_code)
        else:
            consumable_batches =self.get_all_obj(model_name=ConsumableBatch)
            serializer = ConsumableBatchSerializer(consumable_batches, many=True)
            context = {'batches': serializer.data}

           
        return render(request,'consumable_batchlist.html',context)
    
   
class ConsumableBatchEditView(BaseModelViewSet):

    def get(self, request, batch_id):
        try:
            # Fetch the consumable_batch batch by ID
            consumable_batch = ConsumableBatch.objects.get(batch_id=batch_id)
            serializer = ConsumableBatchSerializer(consumable_batch)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        except ConsumableBatch.DoesNotExist:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, batch_id):
        try:
            print("////////////////////////////////////Received data:", request.data)  # Debugging
            decoded_batch_id = unquote(batch_id)  # Decode URL-encoded string
            consumable_batch = ConsumableBatch.objects.get(batch_id=decoded_batch_id)
        except ConsumableBatch.DoesNotExist:
            return Response({'isSuccess': False,'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        
        print("////////////////////////////////////Received data:", request.data)  # Debugging
        
        serializer = ConsumableBatchSerializer(consumable_batch, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            
            # Create notification for successful batch update
            try:
                NotificationService.create_entity_notification(
                    entity_type='consumable_batch',
                    entity_id=consumable_batch.id,
                    entity_name=f"Batch {consumable_batch.batch_id} for {consumable_batch.consumable.name}",
                    notification_type='update',
                    created_by=request.user
                )
                print("Batch update notification created successfully")
            except Exception as notif_error:
                print(f"Batch update notification failed: {notif_error}")
                # Don't fail the operation for notification issues
            
            return Response({'isSuccess': True, 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'isSuccess': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ConsumableBatchAddView(BaseModelViewSet):

    def get(self,request):
        grade_name = request.GET.get("grade_name")
        consumable_name = request.GET.get("consumable_name")
        
        # If AJAX request for acceptance tests by grade/raw_material
        if grade_name and consumable_name:
            print("Grade Name:", grade_name)
            print("Consumable Name:", consumable_name)
            tests = ConsumableGradeAcceptanceTest.objects.filter(
                consumable__name=consumable_name,
                grade__name=grade_name
            )
            result = [
                {
                    "id": test.acceptance_test.id,
                    "name": test.acceptance_test.name,
                    "min": test.min_value,
                    "max": test.max_value,
                    "unit": test.unit_name,
                }
                for test in tests
            ]
            return Response({"tests": result})

        consumables =self.get_all_obj(model_name=Consumable)
        units = self.get_all_obj(model_name=Unit)
        acceptance_test =self.get_all_obj(model_name=AcceptanceTest)
        consumables_with_expiry = []
        for consumable in consumables:
            expiry_date = None
            if consumable.shelf_life_value and consumable.shelf_life_unit:
                expiry_date = consumable.calculate_expiry_date  # Ensure the property is use
            consumables_with_expiry.append({
                'id': consumable.id,
                'name': consumable.name,
                'grade': consumable.grade,
                'shelf_life_value': consumable.shelf_life_value,
                'shelf_life_unit': consumable.shelf_life_unit,
                'expiry_date': expiry_date,  # Pass expiry date to template
                
            })
        context = {
            'consumables': consumables_with_expiry,
            'units': units,
            'acceptance' : acceptance_test

        }

        return render(request,'consumable_batch.html',context)
    
    # def post(self, request):
    #     success=False
    #     message=constants.CONSUMABLE_BATCH_FAILD
    #     status_code=status.HTTP_403_FORBIDDEN
    #     data=request.data
      
    #     try:
    #         if data:
    #             success, status_code, data, message = ConsumableService.add_consumable_bach_add(data=data)
           
    #     except Exception as ex:
    #         success = False
    #         message = constants.CONSUMABLE_BATCH_FAILD
    #         status_code = status.HTTP_400_BAD_REQUEST
            
    #     return self.render_response(data, success, message, status_code)

    def post(self, request):
        success=False
        message=constants.CONSUMABLE_BATCH_FAILD
        status_code=status.HTTP_403_FORBIDDEN
        data=request.data
        
        try:
            # Validate required fields
            consumable_id = data.get("consumable")
            batch_id = data.get("batch_id")
            procurement_date = data.get("procurement_date")
            batch_size_value = data.get("batch_size_value")
            batch_size_unit = data.get("batch_size_unit")
            packing_details = data.get("packing_details")

            if not all([consumable_id, batch_id, procurement_date, batch_size_value, batch_size_unit, packing_details]):
                raise ValueError("All required fields must be provided.")

            # Validate consumable exists
            consumable = Consumable.objects.filter(id=consumable_id).first()
            if not consumable:
                raise ValueError(f"Consumable with ID {consumable_id} not found.")

            # Validate unit exists
            unit = Unit.objects.filter(id=batch_size_unit).first()
            if not unit:
                raise ValueError(f"Unit with ID {batch_size_unit} not found.")

            # Validate procurement date
            try:
                procurement_date = datetime.strptime(procurement_date, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("Invalid procurement date format. Use YYYY-MM-DD.")

            # Validate batch size value
            try:
                batch_size_value = float(batch_size_value)
                if batch_size_value <= 0:
                    raise ValueError("Batch size value must be greater than zero.")
            except (ValueError, TypeError):
                raise ValueError("Batch size value must be a valid number.")

            # Calculate expiry date if not provided
            expiry_date = data.get("expiry_date")
            if not expiry_date and consumable.shelf_life_value and consumable.shelf_life_unit:
                if consumable.shelf_life_unit == "days":
                    expiry_date = procurement_date + timedelta(days=consumable.shelf_life_value)
                elif consumable.shelf_life_unit == "months":
                    expiry_date = procurement_date + timedelta(days=consumable.shelf_life_value * 30)
                elif consumable.shelf_life_unit == "years":
                    expiry_date = procurement_date + timedelta(days=consumable.shelf_life_value * 365)

            # Prepare data for service
            batch_data = {
                'consumable': consumable_id,
                'batch_id': batch_id,
                'procurement_date': procurement_date,
                'batch_size_value': batch_size_value,
                'batch_size_unit': batch_size_unit,
                'packing_details': packing_details,
                'expiry_date': expiry_date or procurement_date,
                'status': 'available'
            }

            print("DEBUG - Data Before Service Call:", batch_data)

            # Call the service to add the batch
            success, status_code, response_data, message = ConsumableService.add_consumable_bach_add(data=batch_data)
            
            # Create notification for successful batch creation
            if success:
                try:
                    NotificationService.create_entity_notification(
                        entity_type='consumable_batch',
                        entity_id=response_data.get('id') if response_data else None,
                        entity_name=f"Batch {batch_id} for {consumable.name}",
                        notification_type='create',
                        created_by=request.user
                    )
                    print("Batch creation notification created successfully")
                except Exception as notif_error:
                    print(f"Batch creation notification failed: {notif_error}")
                    # Don't fail the operation for notification issues
            
        except ValueError as ve:
            print(f"Validation error: {ve}")
            success = False
            message = str(ve)
            status_code = status.HTTP_400_BAD_REQUEST
        except Exception as ex:
            print(f"Unexpected error: {ex}")
            success = False
            message = f"Unexpected error: {str(ex)}"
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            
        return self.render_response(response_data if success else {}, success, message, status_code)



class ConsumableBatchAcceptenceTest(BaseModelViewSet):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        print(request.data, "Received request data")

        consumable_id = request.data.get('consumable')
        batch_id = request.data.get('batch_id')
        sources_id = request.data.get('sources')
        suppliers_id = request.data.get('suppliers')
        grade_id = request.data.get('grade')

        data = []
        index = 0
        while f'acceptance_tests[{index}][id]' in request.data:
            test_data = {
                'batch_id': batch_id,
                'consumable': consumable_id,
                'acceptance_test': request.data.get(f'acceptance_tests[{index}][id]'),
                'test_value': request.data.get(f'acceptance_tests[{index}][test_value]'),
                'sources': sources_id,
                'suppliers': suppliers_id,
                'grade': grade_id,
                'min_value': request.data.get(f'acceptance_tests[{index}][min_value]'),
                'max_value': request.data.get(f'acceptance_tests[{index}][max_value]'),
                'file': request.FILES.get(f'acceptance_tests[{index}][file]'),
                'status': request.data.get(f'acceptance_tests[{index}][status]'),
                'remark': request.data.get(f'acceptance_tests[{index}][remark]'),
                'created_by': request.data.get(f'acceptance_tests[{index}][created_by]', 'user')
            }
            data.append(test_data)
            index += 1

        print(data, "Processed test data")

        serializer = ConsumableAcceptanceTestSerializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            
            # Create notification for successful acceptance test creation
            try:
                NotificationService.create_entity_notification(
                    entity_type='consumable_acceptance_test',
                    entity_id=batch_id,
                    entity_name=f"Acceptance tests for batch {batch_id}",
                    notification_type='create',
                    created_by=request.user
                )
                print("Acceptance test notification created successfully")
            except Exception as notif_error:
                print(f"Acceptance test notification failed: {notif_error}")
                # Don't fail the operation for notification issues
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("Validation errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ConsumableBatchDetailView(BaseModelViewSet):
    """
    View to handle detailed list of batchlist.
    """

    def get(self, request, batch_id):
        batch = get_object_or_404(ConsumableBatch, batch_id=batch_id)
        serializer = ConsumableBatchDetailedSerializer(batch)
        return render(request, 'consumable_batch_detail_view.html', {'batch_detail': serializer.data})
    

class DeleteConsumableBatchView(BaseModelViewSet):
    """
    View to handle the deletion of a source using the POST method.
    """

    def post(self, request, conbatchId, format=None):
        try:

            decoded_conbatchId = unquote(conbatchId)  # Decode URL-encoded string
            consumablebatch = ConsumableBatch.objects.get(batch_id=decoded_conbatchId)
            batch_info = f"Batch {consumablebatch.batch_id} for {consumablebatch.consumable.name}"  # Store info before deletion

            consumablebatch.delete()
            
            # Create notification for successful batch deletion
            try:
                NotificationService.create_entity_notification(
                    entity_type='consumable_batch',
                    entity_id=None,  # Already deleted
                    entity_name=batch_info,
                    notification_type='delete',
                    created_by=request.user
                )
                print("Batch deletion notification created successfully")
            except Exception as notif_error:
                print(f"Batch deletion notification failed: {notif_error}")
                # Don't fail the operation for notification issues
            
            return Response({
                'success': True,
                'message': constants.CONSUMABLE_BATCH_DELETE_SUCCESSFULLY
            }, status=status.HTTP_200_OK)
        except ConsumableBatch.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Consumable Batch not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)       
        

class ViewConsumableBatchDetailView(BaseModelViewSet):
    """
    View to handle viewing of raw material batch details using POST method.
    """
    def post(self, request, batchId, format=None):
        try:
            batch = ConsumableBatch.objects.get(batch_id=batchId)
            serializer = ConsumableBatchSerializer(batch)
            data = serializer.data
            
            return Response({
                'success': True,
                'message': "Consumable batch data fetched successfully.",
                'data': data
            }, status=status.HTTP_200_OK)
        except ConsumableBatch.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Consumable batch not found.'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ConsumableBatchesByMaterial(BaseModelViewSet):
    def get(self, request, material_id):
        batches = ConsumableBatch.objects.filter(consumable_id=material_id)
        serializer = ConsumableBatchSerializer(batches, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)