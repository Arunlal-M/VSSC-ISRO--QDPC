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
        return render(request, self.template_name, {'process': process})


# class ProcessCreateView(BaseModelViewSet):
#     template_name = 'process_create.html'

#     def get(self, request):
#         raw_materials = RawMaterial.objects.all()
#         equipment = Equipment.objects.all()
#         consumables = Consumable.objects.all()
#         return render(request, self.template_name, {
#             'raw_materials': raw_materials,
#             'equipment': equipment,
#             'consumables': consumables,
#         })

#     def post(self, request):
#         process_title = request.POST.get('process_title')
#         process_description = request.POST.get('process_description')
#         process_date = request.POST.get('process_date')

#         process = Process.objects.create(
#             process_title=process_title,
#             process_description=process_description,
#             process_date=process_date
#         )

#         # Create initial step if provided
#         raw_material_ids = request.POST.getlist('raw_material')
#         equipment_ids = request.POST.getlist('equipment')
#         process_step_spec = request.POST.get('process_step_spec')
#         measured_value_observation = request.POST.get('measured_value_observation')

#         if process_step_spec and measured_value_observation:
#             step = ProcessStep.objects.create(
#                 process=process,
#                 process_step_spec=process_step_spec,
#                 measured_value_observation=measured_value_observation
#             )
#             step.raw_material.set(raw_material_ids)
#             step.equipment.set(equipment_ids)

#         return redirect('process_list')

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

        return render(request, self.template_name, {
            'raw_materials_with_status': raw_materials_with_status,
            'consumables_with_status': consumables_with_status,
            'equipment_with_status': equipment_with_status,
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
    def put(self, request, batch_id):
        try:
            processstep = ProcessStep.objects.get(id=batch_id)
        except ProcessStep.DoesNotExist:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProcessStepSerializer(processstep, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    
class DeleteProcessStepView(BaseModelViewSet):
    """
    View to handle the deletion of a Process Step using the POST method.
    """

    def post(self, request, rawId, format=None):
        try:
           step= ProcessStep.objects.get(id=rawId)
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
            
