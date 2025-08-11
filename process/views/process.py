from qdpc.core.modelviewset import BaseModelViewSet
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404, redirect
from process.serializers.process_serializer import ProcessStepSerializer,ProcessNewSerializer
from qdpc_core_models.models.process import Process, ProcessStep
from qdpc_core_models.models.product import Product
from qdpc_core_models.models.equipment import Equipment
from qdpc_core_models.models.consumable import Consumable
from qdpc_core_models.models.raw_material import RawMaterial
from qdpc_core_models.models.component import Component
from qdpc_core_models.models.raw_materialbach import RawMaterialBatch
from qdpc_core_models.models.consumablebatch import ConsumableBatch
from qdpc_core_models.models.componentbatch import ComponentBatch
from qdpc_core_models.models.unit import Unit
from rest_framework import status
from qdpc.core import constants
from django.utils.timezone import now


class ProcessListView(BaseModelViewSet):
    template_name = 'process_list.html'

    def get(self, request):
        processes = Process.objects.all()
        return render(request, self.template_name, {'processes': processes})


class ProcessView(BaseModelViewSet):
    template_name = 'process_detail.html'

    def get(self, request, process_title):
        process = ProcessStep.objects.filter(process=process_title)  # Using filter to allow multiple results
        print(process)
        return render(request, self.template_name, {'process': process,'process_title': process_title})


class ProcessCreateView(BaseModelViewSet):
    template_name = 'process_create.html'

    def get(self, request):
        data=request.data
        print(data)
        raw_material_batch = RawMaterialBatch.objects.all()
        equipment = Equipment.objects.all()
        consumable_batch = ConsumableBatch.objects.all()
        component_batch = ComponentBatch.objects.all()
        units = Unit.objects.all()
        today = now().date()

        return render(request, self.template_name, {
            'raw_material_batch': raw_material_batch,
            'consumable_batch': consumable_batch,
            'equipment': equipment,
            'component_batch': component_batch,
            # 'equipment': equipment,
            # 'consumables': consumables,
            # 'component': component,
            'units':units,
            'today': today,
        })

    def post(self, request):
        print(request.data)
        process_title = request.POST.get('process_title')
        if not process_title:
            return render(request, self.template_name, {
                'error': 'Process title is required.',
                'raw_material_batch': RawMaterialBatch.objects.all(),
                'equipment': Equipment.objects.all(),
                'consumable_batch': ConsumableBatch.objects.all(),
                'component_batch': ComponentBatch.objects.all(),
                'units': Unit.objects.all(),
            })

        process, created = Process.objects.get_or_create(process_title=process_title)

        step_counter = 1
        while True:
            step_description = request.POST.get(f'step_{step_counter}_description')
            if not step_description:
                break

            step_date = request.POST.get(f'step_{step_counter}_date')
            rm_status = request.POST.get(f'step_{step_counter}_rm_status')
            equipment_status = request.POST.get(f'step_{step_counter}_equipment_status')
            consumable_status = request.POST.get(f'step_{step_counter}_consumable_status')
            component_status = request.POST.get(f'step_{step_counter}_component_status')
            # step_specifications = request.POST.get(f'step_{step_counter}_specifications')
            # measured_value = request.POST.get(f'step_{step_counter}_measured_value')
            remarks = request.POST.get(f'step_{step_counter}_remarks')
            test_result = request.POST.get(f'step_{step_counter}_test_result')
            specification_result = request.POST.get(f'step_{step_counter}_specification_result')
            process_type = request.POST.get(f'step_{step_counter}_test_type')

            min_value = request.POST.get(f'step_{step_counter}_min_value')
            max_value = request.POST.get(f'step_{step_counter}_max_value')
            
            if process_type != "quantitative":
                min_value = None
                max_value = None

            raw_material_ids = [id for id in request.POST.getlist(f'step_{step_counter}_raw_material_batch[]') if id]
            equipment_ids = [id for id in request.POST.getlist(f'step_{step_counter}_equipment[]') if id]
            consumable_ids = [id for id in request.POST.getlist(f'step_{step_counter}_consumable_batch[]') if id]
            component_ids = [id for id in request.POST.getlist(f'step_{step_counter}_component_batch[]') if id]
            units_ids = [id for id in request.POST.getlist(f'step_{step_counter}_unit[]') if id]

            process_step = ProcessStep.objects.create(
                process=process,
                process_description=step_description,
                process_date=step_date,
                rm_status=rm_status,
                equipment_status=equipment_status,
                consumable_status=consumable_status,
                component_status=component_status,
                # process_step_spec=step_specifications,
                # measured_value_observation=measured_value,
                remarks=remarks,
                min_value=min_value,
                max_value=max_value,
                test_result=test_result,
                specification_result=specification_result,
            )

            if process_step:
                process_step.raw_material_batch.add(*RawMaterialBatch.objects.filter(id__in=raw_material_ids))
                process_step.equipment.add(*Equipment.objects.filter(id__in=equipment_ids))
                process_step.consumable_batch.add(*ConsumableBatch.objects.filter(id__in=consumable_ids))
                process_step.component_batch.add(*ComponentBatch.objects.filter(id__in=component_ids))
                process_step.unit.add(*Unit.objects.filter(id__in=units_ids))
                
            else:
                return render(request, self.template_name, {'error': 'Failed to create process step.'})

            step_counter += 1

        return redirect('process_list')

class EditProcessStepView(BaseModelViewSet):
    """
    View to handle editing of a Process Step using the PUT method.
    """
    
    def get(self, request, process_title, stepId):
        try:
            process = ProcessStep.objects.get(process__process_title=process_title,step_id=stepId)  # Using filter to allow multiple results
            print(process)
              
            # Get all raw materials, equipment, consumables, and components
            all_raw_material_batch = RawMaterialBatch.objects.all()
            all_equipment = Equipment.objects.all()
            all_consumable_batch = ConsumableBatch.objects.all()
            all_component_batch = ComponentBatch.objects.all()
            all_units = Unit.objects.all()
            
            # Get the selected raw materials, equipment, consumables, and components for the current process step
            selected_raw_material_batch = process.raw_material_batch.all()
            selected_equipment = process.equipment.all()
            selected_consumable_batch = process.consumable_batch.all()
            selected_component_batch = process.component_batch.all()
            selected_units = process.unit.all()
            
            # Create a dictionary to store the data
            data = {
                'id': process.id,
                'process_description': process.process_description,
                'rm_status': process.rm_status,
                'equipment_status': process.equipment_status,
                'consumable_status': process.consumable_status,
                'component_status': process.component_status,
                # 'process_step_spec': process.process_step_spec,
                # 'measured_value_observation': process.measured_value_observation,
                'all_raw_material_batch': [{'id': material.id, 'name': material.name} for material in all_raw_material_batch],
                'remarks': process.remarks,
                'min_value': process.min_value,
                'max_value': process.max_value,
                'specification_result': process.specification_result,
                'remarks': process.remarks,
                'all_equipment': [{'id': equip.id, 'name': equip.name} for equip in all_equipment],
                'all_consumable_batch': [{'id': consum.id, 'name': consum.name} for consum in all_consumable_batch],
                'all_component_batch': [{'id': comp.id, 'name': comp.name} for comp in all_component_batch],
                'raw_material_batch': [{'id': material.id, 'name': material.name} for material in selected_raw_material_batch],
                'equipment': [{'id': equip.id, 'name': equip.name} for equip in selected_equipment],
                'consumable_batch': [{'id': consum.id, 'name': consum.name} for consum in selected_consumable_batch],
                'component_batch': [{'id': comp.id, 'name': comp.name} for comp in selected_component_batch],
            }
            
            return Response({'data': data}, status=status.HTTP_200_OK)  # Return serialized data
        
        except ProcessStep.DoesNotExist:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request, process_title, stepId):
            try:
                processstep = ProcessStep.objects.get(process__process_title=process_title, step_id=stepId)
            except ProcessStep.DoesNotExist:
                return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

            serializer = ProcessStepSerializer(processstep, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'success': True,
                    'message': 'Process step updated successfully.',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            
            return Response({
                'success': False,
                'message': 'Validation failed.',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


    
class DeleteProcessStepView(BaseModelViewSet):
    """
    View to handle the deletion of a Process Step using the POST method.
    """

    def post(self, request, stepId,process_title, format=None):
        try:
           step= ProcessStep.objects.get(process__process_title=process_title, step_id=stepId)
           print(step)
           step.delete()
           return Response({
                'success': True,
                'message': constants.PROCESS_STEP_DELETE_SUCCESSFULLY
            }, status=status.HTTP_200_OK)
        except ProcessStep.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Process step not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
            
class ProcessViewSet(BaseModelViewSet):
   
    def get(self,request,productId):
        print(productId)
        processes =Product.objects.filter(id=productId)
        serializer = ProcessNewSerializer(processes, many=True)
        print(serializer.data)
        return Response({
            'status': 'success',
            'processes': serializer.data
        })
  


class ProcessStepViewSet(BaseModelViewSet):
   
     def get(self, request, process_title):
        print("enterd Get")
        print(process_title)
        try:
            process = ProcessStep.objects.filter(process=process_title)  # Using filter to allow multiple results
            print(process)
            serializer = ProcessStepSerializer(process,many=True)
            # Get all raw materials, equipment, consumables, and components
            # all_raw_material_batch = RawMaterialBatch.objects.all()
            # all_equipment = Equipment.objects.all()
            # all_consumable_batch = ConsumableBatch.objects.all()
            # all_component_batch = ComponentBatch.objects.all()
            # all_units = Unit.objects.all()
            
            # # Get the selected raw materials, equipment, consumables, and components for the current process step
            # selected_raw_material_batch = process.raw_material_batch.all()
            # selected_equipment = process.equipment.all()
            # selected_consumable_batch = process.consumable_batch.all()
            # selected_component_batch = process.component_batch.all()
            # selected_units = process.unit.all()
            
            # # Create a dictionary to store the data
            # data = {
            #     'id': process.id,
            #     'process_description': process.process_description,
            #     'rm_status': process.rm_status,
            #     'equipment_status': process.equipment_status,
            #     'consumable_status': process.consumable_status,
            #     'component_status': process.component_status,
            #     # 'process_step_spec': process.process_step_spec,
            #     # 'measured_value_observation': process.measured_value_observation,
            #     'all_raw_material_batch': [{'id': material.id, 'name': material.raw_material.name} for material in all_raw_material_batch],
            #     'remarks': process.remarks,
            #     'min_value': process.min_value,
            #     'max_value': process.max_value,
            #     'specification_result': process.specification_result,
            #     'remarks': process.remarks,
            #     'all_equipment': [{'id': equip.id, 'name': equip.name} for equip in all_equipment],
            #     'all_consumable_batch': [{'id': consum.id, 'name': consum.consumable.name} for consum in all_consumable_batch],
            #     'all_component_batch': [{'id': comp.id, 'name': comp.component.name} for comp in all_component_batch],
            #     'raw_material_batch': [{'id': material.id, 'name': material.raw_material.name} for material in selected_raw_material_batch],
            #     'equipment': [{'id': equip.id, 'name': equip.name} for equip in selected_equipment],
            #     'consumable_batch': [{'id': consum.id, 'name': consum.consumable.name} for consum in selected_consumable_batch],
            #     'component_batch': [{'id': comp.id, 'name': comp.component.name} for comp in selected_component_batch],
            # }
            print(serializer.data)

            
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)  # Return serialized data
        
        except ProcessStep.DoesNotExist:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)