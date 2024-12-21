from qdpc.core.modelviewset import BaseModelViewSet
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404, redirect
from process.serializers.process_serializer import ProcessStepSerializer
from qdpc_core_models.models.process import Process, ProcessStep
from qdpc_core_models.models.equipment import Equipment
from qdpc_core_models.models.consumable import Consumable
from qdpc_core_models.models.raw_material import RawMaterial
from qdpc_core_models.models.component import Component
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
        raw_materials = RawMaterial.objects.all()
        equipment = Equipment.objects.all()
        consumables = Consumable.objects.all()
        component = Component.objects.all()
        today = now().date()

        # Add expiry status to each raw material
        raw_materials_with_status = [
            {
                'material': material,
                'is_expired': material.calculate_expiry_date < today
            }
            for material in raw_materials
        ]
        consumables_with_status = [
            {
                'consum': consum,
                'is_expired': consum.calculate_expiry_date < today
            }
            for consum in consumables
        ]
        equipment_with_status = [
            {
                'equip': equip,
                'is_expired': equip.calibration_due_date < today
            }
            for equip in equipment
        ]
        component_with_status = [
            {
                'comp': comp,
                'is_expired': comp.calculate_expiry_date < today
            }
            for comp in component
        ]

        return render(request, self.template_name, {
            'raw_materials_with_status': raw_materials_with_status,
            'consumables_with_status': consumables_with_status,
            'equipment_with_status': equipment_with_status,
            'component_with_status': component_with_status,
            'equipment': equipment,
            'consumables': consumables,
            'component': component,
            'today': today,
        })

    def post(self, request):
        print(request.data)
        # Process-level data
        process_title = request.POST.get('process_title')
        if not process_title:
            return render(request, self.template_name, {
                'error': 'Process title is required.',
                'raw_materials': RawMaterial.objects.all(),
                'equipment': Equipment.objects.all(),
                'consumables': Consumable.objects.all(),
                'component': Component.objects.all(),
                
            })

        process, created = Process.objects.get_or_create(process_title=process_title)

        # Handle dynamically added steps
        step_counter = 1
        while True:
            # Fetch step-specific data
            step_description = request.POST.get(f'step_{step_counter}_description')
            if not step_description:
                break  # Exit loop if no more steps are provided

            step_date = request.POST.get(f'step_{step_counter}_date')
            rm_status = request.POST.get(f'step_{step_counter}_rm_status')
            equipment_status = request.POST.get(f'step_{step_counter}_equipment_status')
            step_specifications = request.POST.get(f'step_{step_counter}_specifications')
            measured_value = request.POST.get(f'step_{step_counter}_measured_value')
            remarks = request.POST.get(f'step_{step_counter}_remarks')

            # Many-to-Many relationships
            raw_material_ids = request.POST.getlist(f'step_{step_counter}_raw_material[]')
            equipment_ids = request.POST.getlist(f'step_{step_counter}_equipment[]')
            consumable_ids = request.POST.getlist(f'step_{step_counter}_consumable[]')
            component_ids = request.POST.getlist(f'step_{step_counter}_component[]')

            # Create a new step
            process_step = ProcessStep.objects.create(
                process=process,
                process_description=step_description,
                process_date=step_date,
                rm_status=rm_status,
                equipment_status=equipment_status,
                process_step_spec=step_specifications,
                measured_value_observation=measured_value,
                remarks=remarks,
            )

            # Add Many-to-Many relationships
            process_step.raw_material.add(*RawMaterial.objects.filter(id__in=raw_material_ids))
            process_step.equipment.add(*Equipment.objects.filter(id__in=equipment_ids))
            process_step.consumable.add(*Consumable.objects.filter(id__in=consumable_ids))
            process_step.component.add(*Component.objects.filter(id__in=component_ids))

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
            all_raw_materials = RawMaterial.objects.all()
            all_equipment = Equipment.objects.all()
            all_consumables = Consumable.objects.all()
            all_components = Component.objects.all()
            
            # Get the selected raw materials, equipment, consumables, and components for the current process step
            selected_raw_materials = process.raw_material.all()
            selected_equipment = process.equipment.all()
            selected_consumables = process.consumable.all()
            selected_components = process.component.all()
            
            # Create a dictionary to store the data
            data = {
                'id': process.id,
                'process_description': process.process_description,
                'rm_status': process.rm_status,
                'equipment_status': process.equipment_status,
                'process_step_spec': process.process_step_spec,
                'measured_value_observation': process.measured_value_observation,
                'remarks': process.remarks,
                'all_raw_materials': [{'id': material.id, 'name': material.name} for material in all_raw_materials],
                'all_equipment': [{'id': equip.id, 'name': equip.name} for equip in all_equipment],
                'all_consumables': [{'id': consum.id, 'name': consum.name} for consum in all_consumables],
                'all_components': [{'id': comp.id, 'name': comp.name} for comp in all_components],
                'raw_materials': [{'id': material.id, 'name': material.name} for material in selected_raw_materials],
                'equipment': [{'id': equip.id, 'name': equip.name} for equip in selected_equipment],
                'consumables': [{'id': consum.id, 'name': consum.name} for consum in selected_consumables],
                'components': [{'id': comp.id, 'name': comp.name} for comp in selected_components],
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
            
