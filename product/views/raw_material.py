from qdpc.core.modelviewset import BaseModelViewSet
from rest_framework import status
from qdpc.core import constants
from django.shortcuts import render, redirect
from qdpc_core_models.models.raw_material import RawMaterial, RawMaterialDocument
from product.serializers.RawMaterialSerializer import RawMaterialSerializer
from product.services.raw_material_service import RawmaterialService
from qdpc_core_models.models.supplier import Suppliers
from qdpc_core_models.models.acceptance_test import AcceptanceTest
from qdpc_core_models.models.source import Sources
from qdpc_core_models.models.supplier import Suppliers
from qdpc_core_models.models.source import Sources
from django.shortcuts import get_object_or_404
from rest_framework.response import Response  
from django.db.models import Max
from qdpc_core_models.models.grade import Grade

class RawMatrialListFetchView(BaseModelViewSet):
  
    def get(self,request,batch_id=None):

        if batch_id:
            raw_material_data = self.get_raw_material_data(batch_id)
            return Response({'data': raw_material_data}, status=status.HTTP_200_OK)
        else:
            raw_materials = RawMaterial.objects.values('name').annotate(latest_id=Max('id'))
            
            # Filter the RawMaterial objects to get only the most recent ones
            latest_raw_materials = RawMaterial.objects.filter(id__in=[rm['latest_id'] for rm in raw_materials])
            
            # Serialize the filtered results
            serializer = RawMaterialSerializer(latest_raw_materials, many=True)
            
            context = {'batches': serializer.data}
           
            return render(request, 'material.html', context)
    def get_raw_material_data(self, batch_id):
    # Fetch the raw material object using the batch_id
        material = get_object_or_404(RawMaterial, id=batch_id)
        
    # Fetch all available options for sources, suppliers, and grades
        all_sources = Sources.objects.all().values('id', 'name')
        all_suppliers = Suppliers.objects.all().values('id', 'name')
        all_grades = Grade.objects.all().values('id', 'name','abbreviation')
        all_acceptance = AcceptanceTest.objects.all().values('id', 'name')
        
        raw_materials_data = {
            'id': material.id,
            'name': material.name,
            'sources': [{'id': source.id, 'name': source.name} for source in material.sources.all()],
            'suppliers': [{'id': supplier.id, 'name': supplier.name} for supplier in material.suppliers.all()],
            'grade': [{'id': grade.id, 'name': grade.name,'abbreviation':grade.abbreviation} for grade in material.grade.all()],                  
            'acceptance_test': [{'id': acceptance_test.id, 'name': acceptance_test.name,'min':acceptance_test.min_value,'max':acceptance_test.max_value, 'unit': str(acceptance_test.unit)} for acceptance_test in material.acceptance_test.all()],
            'shelf_life_type': material.shelf_life_type,
            'shelf_life_value': material.shelf_life_value,
            'shelf_life_unit': material.shelf_life_unit,
            'user_defined_date': material.user_defined_date,
            'calculate_expiry_date': material.calculate_expiry_date,
            'all_sources': list(all_sources),  # Include all available sources
            'all_suppliers': list(all_suppliers),  # Include all available suppliers
            'all_grades': list(all_grades),  # Include all available grades
            'all_acceptance' : list(all_acceptance),
        }

        return raw_materials_data

    
    def put(self, request, batch_id):
        try:
            raw_material = RawMaterial.objects.get(id=batch_id)
        except RawMaterial.DoesNotExist:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = RawMaterialSerializer(raw_material, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class RawMaterialAdd(BaseModelViewSet):
    """ Raw Material List API for qdpc application"""
 
    def get(self, request):
        sources =self.get_all_obj(model_name=Sources)
        suppliers = self.get_all_obj(model_name=Suppliers)
        acceptance_tests = AcceptanceTest.objects.values('name').annotate(latest_id=Max('id'))
        grades = self.get_all_obj(model_name=Grade)
        # Filter the AcceptanceTest objects to get only the most recent ones
        latest_acceptance_tests = AcceptanceTest.objects.filter(id__in=[test['latest_id'] for test in acceptance_tests])
        
        context = {
            'sources': sources,
            'suppliers': suppliers,
            'acceptence_test':latest_acceptance_tests,
            'grades' : grades,
        }
        return render(request, 'addmaterial.html',context)
    
    def post(self, request):
        data=request.data
        print(request.data)
        success=False
        message=constants.USERNAME_PASSWORD_EMPTY
        status_code=status.HTTP_403_FORBIDDEN

        try:
            if data:
                success, status_code, data, message = RawmaterialService.add_rawmaterial_add(data=data)
                print( success, status_code, data, message,"what i got afer testing")

        except Exception as ex:
            data={}
            success = False
            message = constants.USERNAME_PASSWORD_EMPTY
            status_code = status.HTTP_400_BAD_REQUEST
            
        return self.render_response(data, success, message, status_code)


class RawmatrialDetailView(BaseModelViewSet):
    """
    View to handle detailed raw material operations, including fetching, listing, and adding raw materials.
    """

    def get(self, request,batch_id=None):
        if batch_id:
            sources = self.get_all_obj(model_name=Sources)
            suppliers = self.get_all_obj(model_name=Suppliers)
            acceptance_tests = AcceptanceTest.objects.values('name').annotate(latest_id=Max('id'))
            grades = self.get_all_obj(model_name=Grade)
            # Filter the AcceptanceTest objects to get only the most recent ones
            latest_acceptance_tests = AcceptanceTest.objects.filter(id__in=[test['latest_id'] for test in acceptance_tests])
            
            # Fetch detailed information for a specific raw material by batch_id
            raw_material = get_object_or_404(RawMaterial, id=batch_id)
        
        # Get all raw materials with the same name
            raw_materials_with_same_name = RawMaterial.objects.filter(name=raw_material.name)
            # latest_raw_materials = RawMaterial.objects.filter(id__in=[rm['latest_id'] for rm in raw_materials])
            serializer = RawMaterialSerializer(raw_materials_with_same_name, many=True)

            context = {
                'sources': sources,
                'suppliers': suppliers,
                'acceptence_test': latest_acceptance_tests,
                'batches': serializer.data,
                'grades' : grades,
            }
            return render(request, 'raw_detailed_view.html', context)
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

    def get_raw_material_data(self, batch_id):
        # Fetch the raw material object using the batch_id
        raw_material = get_object_or_404(RawMaterial, id=batch_id)
        
        # Get all raw materials with the same name
        raw_materials_with_same_name = RawMaterial.objects.filter(name=raw_material.name)
        
        # Create a list to hold data for all raw materials with the same name
        raw_materials_data = []
        
        # Loop through each raw material and prepare the data
        for material in raw_materials_with_same_name:
            logger.debug(f"Raw Material ID: {material.id} has {material.acceptance_test.count()} acceptance tests.")
            
            material_data = {
                'id': material.id,
                'name': material.name,
                'sources': [{'id': source.id, 'name': source.name} for source in material.sources.all()],
                'suppliers': [{'id': supplier.id, 'name': supplier.name} for supplier in material.suppliers.all()],
                'grade': [{'id': grade.id, 'name': grade.name} for grade in material.grade.all()],                    'shelf_life_value': material.shelf_life_value,
                'shelf_life_unit': material.shelf_life_unit,
                'user_defined_date': material.user_defined_date,
                'calculate_expiry_date': material.calculate_expiry_date,
            }
            raw_materials_data.append(material_data)

        return raw_materials_data

    def post(self, request):
        data = request.data
        logger.debug(f"Request data: {data}")
        success = False
        message = constants.USERNAME_PASSWORD_EMPTY
        status_code = status.HTTP_403_FORBIDDEN

        try:
            if data:
                success, status_code, data, message = RawmaterialService.add_rawmaterial_add(data=data)
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
            raw_material = RawMaterial.objects.get(id=batch_id)
        except RawMaterial.DoesNotExist:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = RawMaterialSerializer(raw_material, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteRawMatrialView(BaseModelViewSet):
    """
    View to handle the deletion of a Raw Material using the POST method.
    """

    def post(self, request, rawId, format=None):
        try:
           raw_material= RawMaterial.objects.get(id=rawId)
           raw_material.delete()
           return Response({
                'success': True,
                'message': constants.RAWMATERIAL_DELETE_SUCCESSFULLY
            }, status=status.HTTP_200_OK)
        except RawMaterial.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Raw Material not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
            

class UpdateRawmaterialStatusView(BaseModelViewSet):
    def post(self, request, rawId, format=None): 
        try:
            raw_material = RawMaterial.objects.get(name=rawId)
            new_status = request.data.get('status')  # Get the status directly from request data
            
            # Convert to boolean if it's not already
            if isinstance(new_status, str):
                new_status = new_status.lower() == 'true'

            raw_material.is_active = new_status  # Update the product's active status
            raw_material.save()

            return Response({
                'success': True,
                'message': 'Rawmaterial status updated successfully',
                'is_active': raw_material.is_active
            }, status=status.HTTP_200_OK)
        except RawMaterial.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Rawmaterial not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
class AddRawMaterialDocumentView(BaseModelViewSet):
    def post(self, request, format=None):
        try:
            raw_material_id = request.data.get('raw_material')
            if not raw_material_id:
                return Response({
                    'success': False,
                    'message': 'Raw Material is required'
                }, status=status.HTTP_400_BAD_REQUEST)

            # try:
            #     raw_material = RawMaterial.objects.get(name=raw_material_id)
            # except RawMaterial.DoesNotExist:
            #     return Response({
            #         'success': False,
            #         'message': 'Raw Material not found'
            #     }, status=status.HTTP_404_NOT_FOUND)

            # Create the document
            document = RawMaterialDocument.objects.create(
                raw_material=raw_material_id,
                title=request.data.get('title'),
                category=request.data.get('category'),
                issue_no=request.data.get('issue_no'),
                revision_no=request.data.get('revision_no'),
                release_date=request.data.get('release_date'),
                approved_by=request.data.get('approved_by'),
                document=request.FILES.get('document'),
                validity=request.data.get('validity')
            )

            return Response({
                'success': True,
                'message': 'Raw Material Document added successfully',
                'document_id': document.id
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                'success': False,
                'message': f"An error occurred: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)