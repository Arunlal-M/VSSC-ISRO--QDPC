from qdpc.core.modelviewset import BaseModelViewSet
from rest_framework import status
from qdpc.core import constants
from django.shortcuts import render, redirect
from qdpc_core_models.models.consumable import Consumable,ConsumableDocument,PreCertification, PendingAction, OtherRemark
from qdpc_core_models.models.division import Division
from consumable.serializers.consumable_list_serializer import ConsumableSerializer,PreCertificationSerializer
from consumable.services.consumable_service import ConsumableService
from qdpc_core_models.models.supplier import Suppliers
from qdpc_core_models.models.acceptance_test import AcceptanceTest
from qdpc_core_models.models.source import Sources
from qdpc_core_models.models.supplier import Suppliers
from qdpc_core_models.models.source import Sources
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from rest_framework.response import Response  
from django.db.models import Max
from qdpc_core_models.models.grade import Grade
from qdpc_core_models.models.document_type import DocumentType
from django.core.exceptions import ObjectDoesNotExist
from consumable.serializers.consumtestdataserializer import ConsumTestDataSerializer
from django.contrib.contenttypes.models import ContentType


class ConsumableListFetchView(BaseModelViewSet):
  
     def get(self,request,batch_id=None):

        if batch_id:
            consumable_data = self.get_consumable_data(batch_id)
            return Response({'data': consumable_data}, status=status.HTTP_200_OK)
        else:
            consumables =Consumable.objects.values('name').annotate(latest_id=Max('id'))
            
            # Filter the RawMaterial objects to get only the most recent ones
            latest_consumables = Consumable.objects.filter(id__in=[con['latest_id'] for con in consumables])
            
            # Serialize the filtered results
            serializer = ConsumableSerializer( latest_consumables, many=True)
            
            context = {'batches': serializer.data}
           
            return render(request, 'consumable.html', context)
     def get_consumable_data(self, batch_id):
    # Fetch the raw material object using the batch_id
        consum = get_object_or_404(Consumable, id=batch_id)
        
    # Fetch all available options for sources, suppliers, and grades
        all_sources = Sources.objects.all().values('id', 'name')
        all_suppliers = Suppliers.objects.all().values('id', 'name')
        all_grades = Grade.objects.all().values('id', 'name','abbreviation')
        all_acceptance = AcceptanceTest.objects.all().values('id', 'name')


        consumables_data = {
            'id': consum.id,
            'name': consum.name,
            'sources': [{'id': source.id, 'name': source.name} for source in consum.sources.all()],
            'suppliers': [{'id': supplier.id, 'name': supplier.name} for supplier in consum.suppliers.all()],
            'grade': [{'id': grade.id, 'name': grade.name,'abbreviation':grade.abbreviation} for grade in consum.grade.all()],                  
            'acceptance_test': [{'id': acceptance_test.id, 'name': acceptance_test.name,'min':acceptance_test.min_value,'max':acceptance_test.max_value, 'unit': str(acceptance_test.unit)} for acceptance_test in consum.acceptance_test.all()],
            'shelf_life_type': consum.shelf_life_type,
            'shelf_life_value': consum.shelf_life_value,
            'shelf_life_unit': consum.shelf_life_unit,
            'user_defined_date': consum.user_defined_date,
            'calculate_expiry_date': consum.calculate_expiry_date,
            'all_sources': list(all_sources),  # Include all available sources
            'all_suppliers': list(all_suppliers),  # Include all available suppliers
            'all_grades': list(all_grades),  # Include all available grades
            'all_acceptance' : list(all_acceptance),
        }

        return consumables_data

    
     def put(self, request, batch_id):
        try:
            consumable = Consumable.objects.get(id=batch_id)
        except Consumable.DoesNotExist:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ConsumableSerializer(consumable, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class ConsumableAdd(BaseModelViewSet):
    # parser_classes = (MultiPartParser, FormParser)  # Important for file uploads
    # """ Consumabl List API for qdpc application"""
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
        return render(request, 'addconsumable.html',context)

    def post(self, request):
        data = request.data.copy()  # Ensure we have a mutable copy
        files = request.FILES
        print(files, "this is my file")
        print("Request Data:", data)

        # Ensure test_data is parsed properly
        test_data = data.get('test_data', [])
        if isinstance(test_data, str):
            import json
            try:
                test_data = json.loads(test_data)
            except Exception as e:
                print("Failed to parse test_data:", e)
                test_data = []
                
# ✅ Extract acceptance_test ids and inject into data
        acceptance_test_ids = []
        for item in test_data:
            test_id = item.get('acceptance_test_id')
            if test_id and test_id not in acceptance_test_ids:
                acceptance_test_ids.append(test_id)
        data.setlist('acceptance_test', acceptance_test_ids)      
        # Convert string to boolean
        precertification = str(data.get('precertified', 'false')).lower() == 'true'

        success = False
        message = "Something went wrong"
        status_code = status.HTTP_400_BAD_REQUEST
        response_data = {}

        try:
            if data:
                # Add consumable
                success, status_code, response_data, message = ConsumableService.add_consumable_add(data=data)
                print(success, status_code, response_data, message, "what I got after testing")

                if success:
                    print("Consumable created successfully")
                    consumable_id = response_data.get('id')

                    # Attach consumable_id to each test data item
                    for item in test_data:
                        item['consumable_id'] = consumable_id

                    # ✅ Save test data
                    if test_data:
                        serializer = ConsumTestDataSerializer(data=test_data, many=True)
                        if serializer.is_valid():
                            serializer.save()
                            print("Test data saved successfully")
                        else:
                            return Response({
                                'message': 'Test data validation failed',
                                'errors': serializer.errors
                            }, status=status.HTTP_400_BAD_REQUEST)

                    # ✅ Save PreCertification if applicable
                    if precertification:
                        print("Enter PreCertification")

                        precert_data = {
                
                            'content_type': ContentType.objects.get(model='consumable').id,
                            'object_id': consumable_id,
                            'certified_by': data.get('certified_by'),
                            'certificate_reference_no': data.get('certificate_ref'),
                            'certificate_issue_date': data.get('issue_date'),
                            'certificate_valid_till': data.get('valid_till'),
                            'certificate_file': request.FILES.get('certificate_file'),
                            'certificate_disposition': data.get('certificate_disposition', 'CLEARED'),
                        }
                        precert_serializer = PreCertificationSerializer(data=precert_data)
                        if precert_serializer.is_valid():
                            precert_serializer.save()
                            print("PreCertification saved successfully")
                        else:
                            print("PreCertification serializer errors:", precert_serializer.errors)
                            return Response({
                                'message': 'PreCertification validation failed',
                                'errors': precert_serializer.errors
                            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as ex:
            print("Exception occurred:", ex)
            success = False
            message = str(ex)
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        return self.render_response(response_data if success else {}, success, message, status_code)

class ConsumableDetailView(BaseModelViewSet):
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
            consumable = get_object_or_404(Consumable, id=batch_id)
        
        # Get all raw materials with the same name
            consumables_with_same_name = Consumable.objects.filter(name=consumable.name)
            # latest_raw_materials = RawMaterial.objects.filter(id__in=[rm['latest_id'] for rm in raw_materials])
            serializer = ConsumableSerializer(consumables_with_same_name, many=True)

            context = {
                'sources': sources,
                'suppliers': suppliers,
                'acceptence_test': latest_acceptance_tests,
                'batches': serializer.data,
                'grades':grades,
            }
            return render(request, 'consumable_detailed_view.html', context)
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

    def get_consumable_data(self, batch_id):
        # Fetch the raw material object using the batch_id
        consumable = get_object_or_404(Consumable, id=batch_id)
        
        # Get all consumables with the same name
        consumables_with_same_name = Consumable.objects.filter(name=consumable.name)
        
        # Create a list to hold data for all consumables with the same name
        consumables_data = []
        
        # Loop through each raw material and prepare the data
        for consum in consumables_with_same_name:
            logger.debug(f"Raw Material ID: {consum.id} has {consum.acceptance_test.count()} acceptance tests.")
            
            consum_data = {
                'id': consum.id,
                'name': consum.name,
                'sources': [{'id': source.id, 'name': source.name} for source in consum.sources.all()],
                'suppliers': [{'id': supplier.id, 'name': supplier.name} for supplier in consum.suppliers.all()],
                'grades': [{'id': grad.id, 'name': grad.name} for grad in consum.grade.all()],               
                # 'acceptance_test': [{'id': acceptance_test.id, 'name': acceptance_test.name} for acceptance_test in consum.acceptance_test.all()],
                # 'shelf_life_value': consum.shelf_life_value,
                'shelf_life_unit': consum.shelf_life_unit,
                'user_defined_date': consum.user_defined_date,
                'calculate_expiry_date': consum.calculate_expiry_date,
            }
            consumables_data.append(consum_data)

        return consumables_data

    def post(self, request):
        data = request.data
        logger.debug(f"Request data: {data}")
        success = False
        message = constants.USERNAME_PASSWORD_EMPTY
        status_code = status.HTTP_403_FORBIDDEN

        try:
            if data:
                success, status_code, data, message = ConsumableService.add_consumable_add(data=data)
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
            consumable = Consumable.objects.get(id=batch_id)
        except Consumable.DoesNotExist:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ConsumableSerializer(consumable, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class ViewConsumableDetailView(BaseModelViewSet):
    """
    View to handle viewing of consumable details using POST method.
    """
    def post(self, request, consumableId, format=None):
        try:
            consumable = Consumable.objects.get(id=consumableId)
            serializer = ConsumableSerializer(consumable)
            data = serializer.data

            data['sources'] = [{'id': s.id, 'name': s.name} for s in consumable.sources.all()]
            data['suppliers'] = [{'id': s.id, 'name': s.name} for s in consumable.suppliers.all()]
            data['grades'] = [{'id': g.id, 'name': g.name} for g in consumable.grade.all()]
            data['acceptance_test'] = [{'id': a.id, 'name': a.name} for a in consumable.acceptance_test.all()]

            return Response({
                'success': True,
                'message': "Consumable data fetched successfully.",
                'data': data
            }, status=status.HTTP_200_OK)

        except Consumable.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Consumable not found.'
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeleteConsumableView(BaseModelViewSet):
    """
    View to handle the deletion of a source using the POST method.
    """

    def post(self, request, consumableId, format=None):
        try:
            consumable = Consumable.objects.get(id=consumableId)
            consumable.delete()
            return Response({
                'success': True,
                'message': constants.CONSUMABLE_DELETE_SUCCESSFULLY
            }, status=status.HTTP_200_OK)
        except Consumable.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Consumable not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class UpdateConsumableStatusView(BaseModelViewSet):
    def post(self, request, consumableId, format=None): 
        try:
            consumable = Consumable.objects.get(name=consumableId)
            new_status = request.data.get('status')  # Get the status directly from request data
            
            
            # Convert to boolean if it's not already
            if isinstance(new_status, str):
                new_status = new_status.lower() == 'true'

            consumable.is_active = new_status  # Update the product's active status
            consumable.save()

            return Response({
                'success': True,
                'message': 'Consumable status updated successfully',
                'is_active': consumable.is_active
            }, status=status.HTTP_200_OK)
        except Consumable.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Consumable not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
       

class AddConsumableDocumentView(BaseModelViewSet):
    def post(self, request, format=None):
        try:
            consumable_id = request.data.get('consumable')
            category_id = request.data.get('category')  # Get the category ID

            if not consumable_id or not category_id:
                return Response({
                    'success': False,
                    'message': 'Consumable is required'
                }, status=status.HTTP_400_BAD_REQUEST)

            # try:
            #     consumable = Consumable.objects.get(name=consumable_id)
            # except Consumable.DoesNotExist:
            #     return Response({
            #         'success': False,
            #         'message': 'Consumable not found'
            #     }, status=status.HTTP_404_NOT_FOUND)
            category = DocumentType.objects.get(id=category_id)

            # Create the document
            document = ConsumableDocument.objects.create(
                consumable=consumable_id,
                title=request.data.get('title'),
                category=category,  # Assign the DocumentType instance here
                issue_no=request.data.get('issue_no'),
                revision_no=request.data.get('revision_no'),
                release_date=request.data.get('release_date'),
                approved_by=request.data.get('approved_by'),
                document=request.FILES.get('document'),
                validity=request.data.get('validity')
            )

            return Response({
                'success': True,
                'message': 'Consumable Document added successfully',
                'document_id': document.id
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                'success': False,
                'message': f"An error occurred: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# class AddConsumablePreCertificationView(BaseModelViewSet):

#     def get(self, request):
#         owner = Division.objects.all()

#         context = {
#             'owner': owner,
#         }

#         return render(request, 'addconsumable.html', context)


#     def post(self, request, format=None):
#         try:
#             consumable_id = request.data.get('consumable')
#             certified_by_id = request.data.get('certified_by')
#             certificate_reference_no = request.data.get('certificate_reference_no')
#             certificate_issue_date = request.data.get('certificate_issue_date')
#             certificate_valid_till = request.data.get('certificate_valid_till')
#             certificate_file = request.FILES.get('certificate_file')
#             certificate_disposition = request.data.get('certificate_disposition')
#             pending_actions = request.data.getlist('pending_actions', [])
#             other_remarks = request.data.getlist('other_remarks', [])

#             if not consumable_id or not certified_by_id:
#                 return Response({
#                     'success': False,
#                     'message': 'Consumable and Certified By fields are required'
#                 }, status=status.HTTP_400_BAD_REQUEST)

#             try:
#                 consumable = Consumable.objects.get(id=consumable_id)
#                 certified_by = Division.objects.get(id=certified_by_id)
#             except ObjectDoesNotExist:
#                 return Response({
#                     'success': False,
#                     'message': 'Consumable or Certified By entity not found'
#                 }, status=status.HTTP_404_NOT_FOUND)

#             pre_certification = PreCertification.objects.create(
#                 raw_material=consumable,
#                 certified_by=certified_by,
#                 certificate_reference_no=certificate_reference_no,
#                 certificate_issue_date=certificate_issue_date,
#                 certificate_valid_till=certificate_valid_till,
#                 certificate_file=certificate_file,
#                 certificate_disposition=certificate_disposition
#             )

#             for action in pending_actions:
#                 PendingAction.objects.create(certification=pre_certification, action_detail=action)

#             for remark in other_remarks:
#                 OtherRemark.objects.create(certification=pre_certification, remark_detail=remark)

#             return Response({
#                 'success': True,
#                 'message': 'Pre-Certification added successfully',
#                 'certification_id': pre_certification.id
#             }, status=status.HTTP_201_CREATED)
        
#         except Exception as e:
#             return Response({
#                 'success': False,
#                 'message': f"An error occurred: {str(e)}"
#             }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ConsumableByid(BaseModelViewSet):
    def get(self, request, material_id):
        print("material_id",material_id)
        
        batches = Consumable.objects.filter(id=material_id)
        serializer = ConsumableSerializer(batches, many=True)
        print("serializer",serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)