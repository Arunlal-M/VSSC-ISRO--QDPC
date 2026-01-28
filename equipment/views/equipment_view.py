from qdpc.core.modelviewset import BaseModelViewSet
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from qdpc_core_models.models.equipment import Equipment, EquipmentDocument
from equipment.serializers.equipment_serializer import EquipmentSerializer
from qdpc_core_models.models.division import Division
from rest_framework import status
from qdpc.core import constants
from qdpc_core_models.models.document_type import DocumentType
from django.utils.dateparse import parse_date
from django.db import IntegrityError
from qdpc.services.notification_service import NotificationService



   
class EquipmentView(BaseModelViewSet)   :
    def get(self, request, equipId=None, format=None):
        if equipId:
            equipment_data = self.get_equipment_data(equipId)
            return Response({'data': equipment_data}, status=status.HTTP_200_OK)
        else:
            equipment_list = Equipment.objects.all()
            equipment_owner_list = Division.objects.all()
            document_types = DocumentType.objects.all()

            context = {
                'id': equipment_list,
                'name': equipment_list,
                'equipment_owner': equipment_owner_list,
                'serial_no': equipment_list,
                'make': equipment_list,
                'last_calibration_date': equipment_list,
                'calibration_validity_duration_type': equipment_list,
                'calibration_validity_duration_value': equipment_list,
                'calibration_due_date': equipment_list,
                'calibration_certificate': equipment_list,
                'document_types': document_types,
            }

            return render(request, 'equipment-add.html', context)

    def post(self, request):
        name = request.POST.get('name')
        serial_no = request.POST.get('serial_no')
        make = request.POST.get('make')
        last_calibration_date_str = request.POST.get('last_calibration_date')
        last_calibration_date = parse_date(last_calibration_date_str) if last_calibration_date_str else None
        calibration_validity_duration_type = request.POST.get('calibration_validity_duration_type')
        calibration_validity_duration_value = request.POST.get('calibration_validity_duration_value')
        equipment_owner_id = request.POST.get('equipment_owner')

        errors = []

        if not name:
            errors.append("Equipment name is required.")
        if not serial_no:
            errors.append("Serial number is required.")
        if not make:
            errors.append("Make is required.")
        if not last_calibration_date:
            errors.append("Valid calibration date is required.")
        if not calibration_validity_duration_type:
            errors.append("Calibration validity duration type is required.")
        if not calibration_validity_duration_value or not calibration_validity_duration_value.isdigit():
            errors.append("Calibration validity value must be a positive number.")
        elif int(calibration_validity_duration_value) <= 0:
            errors.append("Calibration validity value must be greater than 0.")
        if not equipment_owner_id:
            errors.append("Equipment owner is required.")

        # Validate calibration date is not in the future
        if last_calibration_date:
            from django.utils import timezone
            today = timezone.now().date()
            if last_calibration_date > today:
                errors.append("Calibration date cannot be in the future.")

        if errors:
            # Check if it's an AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return Response({
                    'success': False,
                    'message': 'Validation failed',
                    'errors': errors
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Regular form submission - render page with errors
                return render(request, 'equipment-add.html', {
                    'errors': errors,
                    'data': request.POST,
                })

        try:
            equipment = Equipment.objects.create(
                name=name,
                serial_no=serial_no,
                make=make,
                last_calibration_date=last_calibration_date,
                calibration_validity_duration_type=calibration_validity_duration_type,
                calibration_validity_duration_value=int(calibration_validity_duration_value),
                equipment_owner_id=equipment_owner_id,
            )

            document = request.FILES.get('documentFile')
            document_title = request.POST.get('title')
            release_date = request.POST.get('release_date')
            approved_by = request.POST.get('approved_by')

            if document:
                EquipmentDocument.objects.create(
                    equipment=equipment,
                    documentfile=document,
                    title=document_title,
                    release_date=parse_date(release_date) if release_date else None,
                    approved_by=approved_by
                )

            # Create notification for equipment creation
            try:
                NotificationService.create_entity_notification(
                    entity_type='equipment',
                    entity_id=equipment.id,
                    entity_name=f"Equipment {equipment.name}",
                    notification_type='create',
                    created_by=request.user
                )
            except Exception:
                # Don't fail the equipment creation if notification fails
                pass

            # Check if it's an AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return Response({
                    'success': True,
                    'message': 'Equipment created successfully',
                    'equipment_id': equipment.id,
                    'equipment_name': equipment.name
                }, status=status.HTTP_201_CREATED)
            else:
                # Regular form submission - redirect to list
                return redirect('equipment-list')

        except IntegrityError:
            error_message = "Equipment with this serial number already exists."
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return Response({
                    'success': False,
                    'message': error_message,
                    'errors': ['Serial number must be unique']
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                errors.append(error_message)
                return render(request, 'equipment-add.html', {
                    'errors': errors,
                    'data': request.POST,
                })
        except Exception as e:
            error_message = f"An error occurred while creating equipment: {str(e)}"
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return Response({
                    'success': False,
                    'message': error_message,
                    'errors': [str(e)]
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                errors.append(error_message)
                return render(request, 'equipment-add.html', {
                    'errors': errors,
                    'data': request.POST,
                })

    def put(self, request, equipId):
        try:
            equipment = Equipment.objects.get(id=equipId)
        except Equipment.DoesNotExist:
            return Response({'detail': 'Equipment not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = EquipmentSerializer(equipment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            
            # Create notification for equipment update
            try:
                NotificationService.create_entity_notification(
                    entity_type='equipment',
                    entity_id=equipId,
                    entity_name=f"Equipment {equipment.name}",
                    notification_type='update',
                    created_by=request.user
                )
            except Exception:
                # Don't fail the equipment update if notification fails
                pass
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_equipment_data(self, equipId):
        equipment = get_object_or_404(Equipment, id=equipId)
        all_divisions = Division.objects.all().values('id', 'name')
        
        equipment_data = {
            'id': equipment.id,
            'name': equipment.name,
            'serial_no': equipment.serial_no,
            'make': equipment.make,
            'last_calibration_date': equipment.last_calibration_date,
            'calibration_validity_duration_type': equipment.calibration_validity_duration_type,
            'calibration_validity_duration_value': equipment.calibration_validity_duration_value,
            'calibration_due_date': equipment.calibration_due_date,
            'calibration_certificate': equipment.calibration_certificate,
            'equipment_owner': equipment.equipment_owner.id if equipment.equipment_owner else None,
            'all_divisions': list(all_divisions),
        }

        return equipment_data


class EquipmentList(BaseModelViewSet):
    def get(self, request, format=None):
        equipment = self.get_all_obj(model_name=Equipment)
        context = {
            'equipment': equipment
        }
        return render(request, 'equipment-list.html', context)


class DeleteEquipmentView(BaseModelViewSet):
    """View to handle the deletion of equipment using the POST method."""

    def post(self, request, equipId, format=None):
        try:
            equipment = Equipment.objects.get(id=equipId)
            
            # Create notification for equipment deletion
            try:
                NotificationService.create_entity_notification(
                    entity_type='equipment',
                    entity_id=equipId,
                    entity_name=f"Equipment {equipment.name}",
                    notification_type='delete',
                    created_by=request.user
                )
            except Exception:
                # Don't fail the equipment deletion if notification fails
                pass
            
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
                'message': f'An error occurred while deleting equipment: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AddEquipmentDocumentView(BaseModelViewSet):
    def post(self, request, format=None):
        try:
            equipment_id = request.data.get('equipment')

            if not equipment_id:
                return Response({
                    'success': False,
                    'message': 'Equipment is required'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Create the document
            document = EquipmentDocument.objects.create(
                equipment=equipment_id,
                title=request.data.get('title'),
                release_date=request.data.get('release_date'),
                approved_by=request.data.get('approved_by'),
                document=request.FILES.get('document'),
            )

            return Response({
                'success': True,
                'message': 'Equipment Document added successfully',
                'document_id': document.id
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'An error occurred while adding document: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ViewEquipmentDetailView(BaseModelViewSet):
    """View to handle viewing of equipment details using POST method."""

    def post(self, request, equipId, format=None):
        try:
            equipment = Equipment.objects.get(id=equipId)
            serializer = EquipmentSerializer(equipment)
            data = serializer.data

            data['equipment_owner'] = equipment.equipment_owner.name if equipment.equipment_owner else "Not Assigned"
            return Response({
                'success': True,
                'message': "Equipment data fetched successfully.",
                'data': data
            }, status=status.HTTP_200_OK)

        except Equipment.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Equipment not found.'
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({
                'success': False,
                'message': f'An error occurred while fetching equipment details: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
