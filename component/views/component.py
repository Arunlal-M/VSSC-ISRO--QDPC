from qdpc.core.modelviewset import BaseModelViewSet
from rest_framework import status
from qdpc.core import constants
from django.shortcuts import render, redirect
from qdpc_core_models.models.component import Component
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

class ComponentListFetchView(BaseModelViewSet):
  
     def get(self,request,batch_id=None):

        if batch_id:
            component_data = self.get_component_data(batch_id)
            return Response({'data': component_data}, status=status.HTTP_200_OK)
        else:
            components =Component.objects.values('name').annotate(latest_id=Max('id'))
            
            # Filter the RawMaterial objects to get only the most recent ones
            latest_components = Component.objects.filter(id__in=[com['latest_id'] for com in components])
            
            # Serialize the filtered results
            serializer = ComponentSerializer( latest_components, many=True)
            
            context = {'batches': serializer.data}
           
            return render(request, 'component.html', context)
     def get_component_data(self, batch_id):
    # Fetch the raw material object using the batch_id
        comp = get_object_or_404(Component, id=batch_id)
        
    # Fetch all available options for sources, suppliers, and grades
        all_sources = Sources.objects.all().values('id', 'name')
        all_suppliers = Suppliers.objects.all().values('id', 'name')
        all_grades = Grade.objects.all().values('id', 'name','abbreviation')
        

        components_data = {
            'id': comp.id,
            'name': comp.name,
            'sources': [{'id': source.id, 'name': source.name} for source in comp.sources.all()],
            'suppliers': [{'id': supplier.id, 'name': supplier.name} for supplier in comp.suppliers.all()],
            'grade': [{'id': grade.id, 'name': grade.name,'abbreviation':grade.abbreviation} for grade in comp.grade.all()],                  
            'acceptance_test': [{'id': acceptance_test.id, 'name': acceptance_test.name,'min':acceptance_test.min_value,'max':acceptance_test.max_value, 'unit': str(acceptance_test.unit)} for acceptance_test in comp.acceptance_test.all()],
            'shelf_life_value': comp.shelf_life_value,
            'shelf_life_unit': comp.shelf_life_unit,
            'user_defined_date': comp.user_defined_date,
            'calculate_expiry_date': comp.calculate_expiry_date,
            'all_sources': list(all_sources),  # Include all available sources
            'all_suppliers': list(all_suppliers),  # Include all available suppliers
            'all_grades': list(all_grades),  # Include all available grades
        }

        return components_data

    
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




class ComponentAdd(BaseModelViewSet):
    """ Component List API for qdpc application"""
 
    def get(self, request):
        sources =self.get_all_obj(model_name=Sources)
        suppliers = self.get_all_obj(model_name=Suppliers)
        acceptance_tests = AcceptanceTest.objects.values('name').annotate(latest_id=Max('id'))
        grades=self.get_all_obj(model_name=Grade)
        # Filter the AcceptanceTest objects to get only the most recent ones
        latest_acceptance_tests = AcceptanceTest.objects.filter(id__in=[test['latest_id'] for test in acceptance_tests])
        
        context = {
            'sources': sources,
            'suppliers': suppliers,
            'acceptence_test':latest_acceptance_tests,
            'grades':grades,
        }
        return render(request, 'addcomponent.html',context)
    
    def post(self, request):
        data=request.data
        print(request.data)
        success=False
        message=constants.USERNAME_PASSWORD_EMPTY
        status_code=status.HTTP_403_FORBIDDEN

        try:
            if data:
                success, status_code, data, message = ComponentService.add_component_add(data=data)
                print( success, status_code, data, message,"what i got afer testing")

        except Exception as ex:
            data={}
            success = False
            message = constants.USERNAME_PASSWORD_EMPTY
            status_code = status.HTTP_400_BAD_REQUEST
            
        return self.render_response(data, success, message, status_code)


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
            component = Component.objects.get(id=componentId)
            component.delete()
            return Response({
                'success': True,
                'message': constants.COMPONENT_DELETE_SUCCESSFULLY
            }, status=status.HTTP_200_OK)
        except Component.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Component not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class UpdateComponentStatusView(BaseModelViewSet):
    def post(self, request, componentId, format=None): 
        try:
            component = Component.objects.get(name=componentId)
            new_status = request.data.get('status')  # Get the status directly from request data
            
            
            # Convert to boolean if it's not already
            if isinstance(new_status, str):
                new_status = new_status.lower() == 'true'

            component.is_active = new_status  # Update the product's active status
            component.save()

            return Response({
                'success': True,
                'message': 'Component status updated successfully',
                'is_active': component.is_active
            }, status=status.HTTP_200_OK)
        except Component.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Component not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
       


