from qdpc.core.modelviewset import BaseModelViewSet
from rest_framework.response import Response
from django.shortcuts import render,redirect
from qdpc_core_models.models.equipment import Equipment
from equipment.serializers.equipment_serializer import EquipmentSerializer
from qdpc_core_models.models.division import Division
from rest_framework import status
from qdpc.core import constants



class EquipmentView(BaseModelViewSet):
    def get(self, request, format=None):
        # Fetch all Equipment objects once
        equipment_list = Equipment.objects.all()
        equipment_owner_list = Division.objects.all()
        
        # Pass the queryset to the context
        context = {
            'id':equipment_list,
            'name': equipment_list,
            'equipment_owner': equipment_owner_list,  # Pass only Division instances for the dropdown
            'serial_no': equipment_list,
            'make': equipment_list,
            'last_calibration_date': equipment_list,
            'calibration_validity_duration_type': equipment_list,
            'calibration_validity_duration_value': equipment_list,
            'calibration_due_date': equipment_list,
            'calibration_certificate': equipment_list,
        }

        return render(request, 'equipment-add.html', context)
    
    def post(self, request):
        print(request.data)
        serializer = EquipmentSerializer(data=request.data)
       
        if serializer.is_valid():
            serializer.save()
          
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class EquipmentList(BaseModelViewSet):
    def get(self, request, format=None):
        
        equipment = self.get_all_obj(model_name=Equipment)
        context = {
            'equipment':equipment
        }
        return render(request,'equipment-list.html',context)
      



class DeleteEquipmentView(BaseModelViewSet):
    """
    View to handle the deletion of a center using the POST method.
    """

    def post(self, request, equipId, format=None):
        try:
            equipment = Equipment.objects.get(id=equipId)
            equipment.delete()
            return Response({
                'success': True,
                'message': constants.EQUIPMENT_DELETE_SUCCESSFULLY
            }, status=status.HTTP_200_OK)
        except Equipment.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Equipment not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





    