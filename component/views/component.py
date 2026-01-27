from qdpc.core.modelviewset import BaseModelViewSet
from rest_framework import status
from qdpc.core import constants
from django.shortcuts import render, redirect
from qdpc_core_models.models.component import Component,ComponentDocument
from component.serializers.component_serializer import ComponentSerializer
from component.services.component_service import ComponentService
from qdpc_core_models.models.supplier import Suppliers
from qdpc_core_models.models.acceptance_test import AcceptanceTest
from qdpc_core_models.models.source import Sources
from qdpc_core_models.models.supplier import Suppliers
from qdpc_core_models.models.source import Sources
from django.shortcuts import get_object_or_404
from rest_framework.response import Response  
from django.db.models import Max
from qdpc_core_models.models.grade import Grade
from qdpc_core_models.models.document_type import DocumentType
from component.serializers.comptestdataserializer import CompTestDataSerializer
from django.contrib.contenttypes.models import ContentType
from consumable.serializers.consumable_list_serializer import PreCertificationSerializer
from qdpc_core_models.models.division import Division
from qdpc.services.notification_service import NotificationService
import json
import logging

# Set up logging
logger = logging.getLogger(__name__)

class ComponentListFetchView(BaseModelViewSet):
  
     def get(self,request,batch_id=None):
        try:
            if batch_id:
                component_data = self.get_component_data(batch_id)
                return Response({'data': component_data}, status=status.HTTP_200_OK)
            else:
                components =Component.objects.values('name').annotate(latest_id=Max('id'))
                
                # Filter the Component objects to get only the most recent ones
                latest_components = Component.objects.filter(id__in=[com['latest_id'] for com in components])
                
                # Serialize the filtered results
                serializer = ComponentSerializer( latest_components, many=True)
                
                context = {'batches': serializer.data}
               
                return render(request, 'component.html', context)
        except Exception as e:
            logger.error(f"Error in ComponentListFetchView.get: {str(e)}")
            return Response({
                'success': False,
                'message': 'Failed to fetch component data'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
     def get_component_data(self, batch_id):
        try:
            # Fetch the component object using the batch_id
            comp = get_object_or_404(Component, id=batch_id)
            
            # Fetch all available options for sources, suppliers, and grades
            all_sources = Sources.objects.all().values('id', 'name')
            all_suppliers = Suppliers.objects.all().values('id', 'name')
            all_grades = Grade.objects.all().values('id', 'name','abbreviation')
            all_acceptance = AcceptanceTest.objects.all().values('id', 'name')

            components_data = {
                'id': comp.id,
                'name': comp.name,
                'sources': [{'id': source.id, 'name': source.name} for source in comp.sources.all()],
                'suppliers': [{'id': supplier.id, 'name': supplier.name} for supplier in comp.suppliers.all()],
                'grade': [{'id': grade.id, 'name': grade.name,'abbreviation':grade.abbreviation} for grade in comp.grade.all()],                  
                'acceptance_test': [{'id': acceptance_test.id, 'name': acceptance_test.name,'min':acceptance_test.min_value,'max':acceptance_test.max_value, 'unit': str(acceptance_test.unit)} for acceptance_test in comp.acceptance_test.all()],
                'shelf_life_type': comp.shelf_life_type,
                'shelf_life_value': comp.shelf_life_value,
                'shelf_life_unit': comp.shelf_life_unit,
                'user_defined_date': comp.user_defined_date,
                'calculate_expiry_date': comp.calculate_expiry_date,
                'all_sources': list(all_sources),  # Include all available sources
                'all_suppliers': list(all_suppliers),  # Include all available suppliers
                'all_grades': list(all_grades),  # Include all available grades
                'all_acceptance' : list(all_acceptance),
            }

            return components_data
        except Exception as e:
            logger.error(f"Error in get_component_data: {str(e)}")
            raise

    
     def put(self, request, batch_id):
        try:
            component = Component.objects.get(id=batch_id)
        except Component.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Component not found'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = ComponentSerializer(component, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                serializer.save()
                
                # Create notification for successful component update
                try:
                    NotificationService.create_entity_notification(
                        entity_type='component',
                        entity_id=component.id,
                        entity_name=component.name,
                        notification_type='update',
                        created_by=request.user
                    )
                    logger.info(f"Update notification created successfully for component {component.name}")
                except Exception as notif_error:
                    logger.error(f"Update notification creation failed: {notif_error}")
                    # Don't fail the operation for notification issues
                
                return Response({
                    'success': True,
                    'message': 'Component updated successfully',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            except Exception as e:
                logger.error(f"Error saving component: {str(e)}")
                return Response({
                    'success': False,
                    'message': 'Failed to save component changes'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({
            'success': False,
            'message': 'Validation failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)




class ComponentAdd(BaseModelViewSet):
    """ Component List API for qdpc application"""
 
    def get(self, request):
        sources =self.get_all_obj(model_name=Sources)
        suppliers = self.get_all_obj(model_name=Suppliers)
        acceptance_tests = AcceptanceTest.objects.values('name').annotate(latest_id=Max('id'))
        grades=self.get_all_obj(model_name=Grade)
        # Filter the AcceptanceTest objects to get only the most recent ones
        latest_acceptance_tests = AcceptanceTest.objects.filter(id__in=[test['latest_id'] for test in acceptance_tests])
        document_types = DocumentType.objects.all()  # Add this line to fetch document types
        owner = Division.objects.all()
        context = {
            'sources': sources,
            'suppliers': suppliers,
            'acceptence_test':latest_acceptance_tests,
            'grades':grades,
            'document_types': document_types,  # Pass document types to the template
            'owner': owner,  # Pass document types to the template
        }
        return render(request, 'addcomponent.html',context)
    def post(self, request):
        data = request.data.copy()
        files = request.FILES
        logger.info(f"Creating component with data: {data.get('name', 'Unknown')}")
        logger.debug(f"FILES: {files}")
        logger.debug(f"DATA: {data}")

        # Safely extract test_data
        test_data_raw = data.get('test_data', '[]')
        try:
            test_data = json.loads(test_data_raw)
            logger.debug(f"Successfully parsed test_data: {len(test_data)} items")
        except Exception as e:
            logger.error(f"Failed to parse test_data: {e}")
            test_data = []

        # ✅ Extract acceptance_test ids and inject into data
        acceptance_test_ids = []
        for item in test_data:
            test_id = item.get('acceptance_test_id')
            if test_id and test_id not in acceptance_test_ids:
                acceptance_test_ids.append(test_id)
        data.setlist('acceptance_test', acceptance_test_ids)

        # Convert to proper types
        precertification = data.get('precertified', 'false')
        precertification = precertification.lower() == 'true' if isinstance(precertification, str) else False

        success = False
        message = "Something went wrong"
        status_code = status.HTTP_400_BAD_REQUEST
        response_data = {}

        try:
            if data:
                # Call service to add component
                success, status_code, component_data, message = ComponentService.add_component_add(data=data)
                logger.info(f"Component creation response: {success}, {status_code}, {component_data}, {message}")

                if success:
                    component_id = component_data.get('id')
                    logger.info(f"Component created successfully with ID: {component_id}")

                    # Create notification for successful component creation
                    try:
                        created_component = Component.objects.get(id=component_id)
                        NotificationService.create_entity_notification(
                            entity_type='component',
                            entity_id=created_component.id,
                            entity_name=created_component.name,
                            notification_type='create',
                            created_by=request.user
                        )
                        logger.info(f"Notification created successfully for component: {created_component.name}")
                    except Exception as notif_error:
                        logger.error(f"Notification creation failed for component {component_id}: {notif_error}")
                        # Don't fail the operation for notification issues

                    # Attach component_id to each test data item
                    for item in test_data:
                        item['component_id'] = component_id

                    # ✅ Save test data
                    if test_data:
                        serializer = CompTestDataSerializer(data=test_data, many=True)
                        if serializer.is_valid():
                            serializer.save()
                            logger.info(f"Test data saved successfully for component {component_id}")
                            
                            # Create notification for test data creation
                            try:
                                NotificationService.create_entity_notification(
                                    entity_type='component_test_data',
                                    entity_id=component_id,
                                    entity_name=f"Test data for {created_component.name}",
                                    notification_type='create',
                                    created_by=request.user
                                )
                                logger.info(f"Test data notification created successfully for component {component_id}")
                            except Exception as notif_error:
                                logger.error(f"Test data notification creation failed for component {component_id}: {notif_error}")
                        else:
                            logger.error(f"Test data validation failed for component {component_id}: {serializer.errors}")
                            return Response({
                                'success': False,
                                'message': 'Test data validation failed',
                                'errors': serializer.errors
                            }, status=status.HTTP_400_BAD_REQUEST)

                    # ✅ Save PreCertification
                    if precertification:
                        logger.info(f"Processing PreCertification for component {component_id}")

                        def get_val(key):
                            val = data.getlist(key)
                            return val[0] if val else None

                        precert_data = {
                            'content_type': ContentType.objects.get(model='component').id,
                            'object_id': component_id,
                            'certified_by': get_val('certified_by'),
                            'certificate_reference_no': get_val('certificate_ref'),
                            'certificate_issue_date': get_val('issue_date'),
                            'certificate_valid_till': get_val('valid_till'),
                            'certificate_file': files.get('certificate_file'),
                            'certificate_disposition': get_val('certificate_disposition') or 'CLEARED',
                        }

                        logger.debug(f"PreCertification Data: {precert_data}")

                        precert_serializer = PreCertificationSerializer(data=precert_data)
                        if precert_serializer.is_valid():
                            precert_serializer.save()
                            logger.info(f"PreCertification saved successfully for component {component_id}")
                            
                            # Create notification for pre-certification creation
                            try:
                                NotificationService.create_entity_notification(
                                    entity_type='component_precertification',
                                    entity_id=component_id,
                                    entity_name=f"Pre-certification for {created_component.name}",
                                    notification_type='create',
                                    created_by=request.user
                                )
                                logger.info(f"Pre-certification notification created successfully for component {component_id}")
                            except Exception as notif_error:
                                logger.error(f"Pre-certification notification creation failed for component {component_id}: {notif_error}")
                        else:
                            logger.error(f"PreCertification serializer errors for component {component_id}: {precert_serializer.errors}")
                            return Response({
                                'success': False,
                                'message': 'PreCertification validation failed',
                                'errors': precert_serializer.errors
                            }, status=status.HTTP_400_BAD_REQUEST)

                    response_data = component_data
                    message = "Component created successfully"
                    status_code = status.HTTP_201_CREATED
                else:
                    # Create notification for failed component creation
                    try:
                        NotificationService.create_entity_notification(
                            entity_type='component',
                            entity_id=None,
                            entity_name=data.get('name', 'Unknown'),
                            notification_type='create_failed',
                            created_by=request.user
                        )
                        logger.info(f"Failure notification created successfully for component: {data.get('name', 'Unknown')}")
                    except Exception as notif_error:
                        logger.error(f"Failure notification creation failed for component {data.get('name', 'Unknown')}: {notif_error}")

        except Exception as ex:
            logger.error(f"Exception in component creation: {ex}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            message = str(ex)
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        return self.render_response(
            response_data if success else {},
            success,
            message,
            status_code
        )

class ComponentDetailView(BaseModelViewSet):
    """
    View to handle detailed raw material operations, including fetching, listing, and adding raw materials.
    """

    def get(self, request,batch_id=None):
        if batch_id:
            sources = self.get_all_obj(model_name=Sources)
            suppliers = self.get_all_obj(model_name=Suppliers)
            acceptance_tests = AcceptanceTest.objects.values('name').annotate(latest_id=Max('id'))
            grades=self.get_all_obj(model_name=Grade)
            # Filter the AcceptanceTest objects to get only the most recent ones
            latest_acceptance_tests = AcceptanceTest.objects.filter(id__in=[test['latest_id'] for test in acceptance_tests])
            
            # Fetch detailed information for a specific raw material by batch_id
            component = get_object_or_404(Component, id=batch_id)
        
        # Get all raw materials with the same name
            components_with_same_name = Component.objects.filter(name=component.name)
            # latest_raw_materials = RawMaterial.objects.filter(id__in=[rm['latest_id'] for rm in raw_materials])
            serializer = ComponentSerializer(components_with_same_name, many=True)

            context = {
                'sources': sources,
                'suppliers': suppliers,
                'acceptence_test': latest_acceptance_tests,
                'batches': serializer.data,
                'grades':grades,
            }
            return render(request, 'component_detailed_view.html', context)
        # else:
        #     # If no batch_id is provided, render the form for adding raw materials with a list of existing materials
        #     sources = self.get_all_obj(model_name=Sources)
        #     suppliers = self.get_all_obj(model_name=Suppliers)
        #     acceptance_tests = AcceptanceTest.objects.values('name').annotate(latest_id=Max('id'))
            
        #     # Filter the AcceptanceTest objects to get only the most recent ones
        #     latest_acceptance_tests = AcceptanceTest.objects.filter(id__in=[test['latest_id'] for test in acceptance_tests])
            
        #     # Get the most recent raw materials
        #     raw_material = get_object_or_404(RawMaterial, id=9)
        
        # # Get all raw materials with the same name
        #     raw_materials_with_same_name = RawMaterial.objects.filter(name=raw_material.name)
        #     # latest_raw_materials = RawMaterial.objects.filter(id__in=[rm['latest_id'] for rm in raw_materials])
        #     serializer = RawMaterialSerializer(raw_materials_with_same_name, many=True)

        #     context = {
        #         'sources': sources,
        #         'suppliers': suppliers,
        #         'acceptence_test': latest_acceptance_tests,
        #         'batches': serializer.data
        #     }
        #     return render(request, 'raw_detailed_view.html', context)

    def get_component_data(self, batch_id):
        # Fetch the raw material object using the batch_id
        component = get_object_or_404(Component, id=batch_id)
        
        # Get all components with the same name
        components_with_same_name = Component.objects.filter(name=component.name)
        
        # Create a list to hold data for all components with the same name
        components_data = []
        
        # Loop through each raw material and prepare the data
        for comp in components_with_same_name:
            logger.debug(f"Raw Material ID: {comp.id} has {comp.acceptance_test.count()} acceptance tests.")
            
            comp_data = {
                'id': comp.id,
                'name': comp.name,
                'sources': [{'id': source.id, 'name': source.name} for source in comp.sources.all()],
                'suppliers': [{'id': supplier.id, 'name': supplier.name} for supplier in comp.suppliers.all()],
                'grades': [{'id': grad.id, 'name': grad.name} for grad in comp.grade.all()],               
                'acceptance_test': [{'id': acceptance_test.id, 'name': acceptance_test.name} for acceptance_test in comp.acceptance_test.all()],
                'shelf_life_value': comp.shelf_life_value,
                'shelf_life_unit': comp.shelf_life_unit,
                'user_defined_date':comp.user_defined_date,
                'calculate_expiry_date': comp.calculate_expiry_date,
            }
            components_data.append(comp_data)

        return components_data

    def post(self, request):
        data = request.data
        logger.debug(f"Request data: {data}")
        success = False
        message = constants.USERNAME_PASSWORD_EMPTY
        status_code = status.HTTP_403_FORBIDDEN

        try:
            if data:
                success, status_code, data, message = ComponentService.add_component_add(data=data)
                logger.debug(f"Response: success={success}, status_code={status_code}, data={data}, message={message}")

        except Exception as ex:
            logger.error(f"Error occurred: {ex}")
            data = {}
            success = False
            message = constants.USERNAME_PASSWORD_EMPTY
            status_code = status.HTTP_400_BAD_REQUEST

        return self.render_response(data, success, message, status_code)

    def put(self, request, batch_id):
        try:
            component = Component.objects.get(id=batch_id)
        except Component.DoesNotExist:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ComponentSerializer(component, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class DeleteComponentView(BaseModelViewSet):
    """
    View to handle the deletion of a source using the POST method.
    """

    def post(self, request, componentId, format=None):
        try:
            logger.info(f"Attempting to delete component with ID: {componentId}")
            component = Component.objects.get(id=componentId)
            component_name = component.name  # Store name before deletion
            component.delete()
            logger.info(f"Successfully deleted component: {component_name}")
            
            # Create notification for successful component deletion
            try:
                NotificationService.create_entity_notification(
                    entity_type='component',
                    entity_id=componentId,
                    entity_name=component_name,
                    notification_type='delete',
                    created_by=request.user
                )
                logger.info(f"Delete notification created successfully for component: {component_name}")
            except Exception as notif_error:
                logger.error(f"Delete notification creation failed for component {component_name}: {notif_error}")
                # Don't fail the operation for notification issues
            
            return Response({
                'success': True,
                'message': constants.COMPONENT_DELETE_SUCCESSFULLY
            }, status=status.HTTP_200_OK)
        except Component.DoesNotExist:
            logger.warning(f"Attempted to delete non-existent component with ID: {componentId}")
            return Response({
                'success': False,
                'message': 'Component not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error deleting component with ID {componentId}: {str(e)}")
            return Response({
                'success': False,
                'message': 'An error occurred while deleting the component.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class UpdateComponentStatusView(BaseModelViewSet):
    def post(self, request, componentId, format=None): 
        try:
            logger.info(f"Attempting to update status for component: {componentId}")
            component = Component.objects.get(name=componentId)
            new_status = request.data.get('status')  # Get the status directly from request data
            
            # Convert to boolean if it's not already
            if isinstance(new_status, str):
                new_status = new_status.lower() == 'true'

            old_status = component.is_active
            component.is_active = new_status  # Update the product's active status
            component.save()
            
            status_text = 'activated' if new_status else 'deactivated'
            logger.info(f"Successfully updated component {component.name} status from {old_status} to {new_status}")
            
            # Create notification for successful component status update
            try:
                NotificationService.create_entity_notification(
                    entity_type='component',
                    entity_id=component.id,
                    entity_name=component.name,
                    notification_type='status_update',
                    created_by=request.user
                )
                logger.info(f"Status update notification created successfully for component {component.name} - {status_text}")
            except Exception as notif_error:
                logger.error(f"Status update notification creation failed for component {component.name}: {notif_error}")
                # Don't fail the operation for notification issues

            return Response({
                'success': True,
                'message': f'Component status updated successfully to {status_text}',
                'is_active': component.is_active
            }, status=status.HTTP_200_OK)
        except Component.DoesNotExist:
            logger.warning(f"Attempted to update status for non-existent component: {componentId}")
            return Response({
                'success': False,
                'message': 'Component not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error updating status for component {componentId}: {str(e)}")
            return Response({
                'success': False,
                'message': 'An error occurred while updating the component status.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
       

class AddComponentDocumentView(BaseModelViewSet):
    def post(self, request, format=None):
        try:
            component_id = request.data.get('component')
            category_id = request.data.get('category')  # Get the category ID

            if not component_id or not category_id:
                logger.warning("Component document creation failed: Missing component or category")
                return Response({
                    'success': False,
                    'message': 'Component and category are required'
                }, status=status.HTTP_400_BAD_REQUEST)

            try:
                category = DocumentType.objects.get(id=category_id)
            except DocumentType.DoesNotExist:
                logger.warning(f"Document type not found with ID: {category_id}")
                return Response({
                    'success': False,
                    'message': 'Document category not found'
                }, status=status.HTTP_404_NOT_FOUND)

            # Create the document
            document = ComponentDocument.objects.create(
                component=component_id,
                title=request.data.get('title'),
                category=category,  # Assign the DocumentType instance here
                issue_no=request.data.get('issue_no'),
                revision_no=request.data.get('revision_no'),
                release_date=request.data.get('release_date'),
                approved_by=request.data.get('approved_by'),
                document=request.FILES.get('document'),
                validity=request.data.get('validity')
            )
            
            logger.info(f"Component document created successfully: {document.title}")

            # Create notification for successful document addition
            try:
                NotificationService.create_entity_notification(
                    entity_type='component_document',
                    entity_id=document.id,
                    entity_name=f"Document: {document.title} for Component {component_id}",
                    notification_type='create',
                    created_by=request.user
                )
                logger.info(f"Document notification created successfully for component {component_id}")
            except Exception as notif_error:
                logger.error(f"Document notification creation failed for component {component_id}: {notif_error}")
                # Don't fail the operation for notification issues

            return Response({
                'success': True,
                'message': 'Component Document added successfully',
                'document_id': document.id
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Error creating component document: {str(e)}")
            return Response({
                'success': False,
                'message': 'An error occurred while creating the component document.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ComponentByid(BaseModelViewSet):
    def get(self, request, material_id):
        batches = Component.objects.filter(id=material_id)
        serializer = ComponentSerializer(batches, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)