from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from qdpc.core.modelviewset import BaseModelViewSet
from qdpc.core.decorators import require_page_permission
from qdpc_core_models.models.product_batchlist import ProductBatch
from qdpc_core_models.models.productBatch import ProductBatchs, ProductBatchRawMaterial, ProductBatchComponent, ProductBatchConsumable, ProductBatchProcess, ProductBatchDrawing, ProductBatchEquipment, ProductBatchAcceptanceTest, RawmaterialAcceptenceTest
from qdpc_core_models.models.raw_material import RawMaterial
from qdpc_core_models.models.raw_materialbach import RawMaterialBatch
from qdpc_core_models.models.consumable import Consumable
from qdpc_core_models.models.consumablebatch import ConsumableBatch
from qdpc_core_models.models.product import Product
from qdpc_core_models.models.component import Component
from qdpc_core_models.models.componentbatch import ComponentBatch
from qdpc_core_models.models.process import Process, ProcessStep
from qdpc_core_models.models.unit import Unit
from product.serializers.product_batch_serializer import ProductBatchDetailedSerializer
from qdpc.core import constants
from product.services.product_service import ProductService
from qdpc_core_models.models.product_category import ProductCategory
from product.serializers.RawMaterialSerializer import *
from rest_framework.views import APIView
from qdpc_core_models.models.product import Drawing
from django.utils.timezone import now
from qdpc_core_models.models.equipment import *
from qdpc_core_models.models.product_acceptence import ProductAcceptanceTest
# Removed conflicting import - using ProductBatch from product_batchlist instead
from django.views import View
import json
from product.models import DynamicTable, DynamicTableRow
from django.http import JsonResponse
from django.urls import reverse
from django.contrib import messages
from qdpc.services.notification_service import NotificationService


class ConsumableWithBatchesAPIView(APIView):
    def get(self, request):
        product_id = request.GET.get('product_id')
        
        if product_id:
            try:
                product = Product.objects.get(id=product_id)
                consumables = product.consumable.filter(is_active=True)
            except Product.DoesNotExist:
                return Response({'error': 'Product not found'}, status=404)
        else:
            consumables = Consumable.objects.none()

        serializer = ConsumableWithBatchesSerializer(consumables, many=True)
        return Response(serializer.data)


class ComponentBatchListView(APIView):
    def get(self, request):  
        product_id = request.GET.get('product_id')
        if product_id:
            try:
                product = Product.objects.get(id=product_id)
                components = product.components.all()  
            except Product.DoesNotExist:
                return Response({'error': 'Product not found'}, status=404)
        else:
            components = Component.objects.none()  
        serializer = ComponentWithBatchesSerializer(components, many=True)
        return Response(serializer.data)


class RawMaterialBatchListView(APIView):
    def get(self, request):
        product_id = request.GET.get('product_id')
        raw_material_id = request.GET.get('raw_material_id')

        if not product_id:
            return Response({'error': 'product_id is required'}, status=400)

        try:
            product = Product.objects.get(id=product_id)
            raw_materials = product.rawmaterial.all()
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=404)

        raw_materials_data = RawMaterialWithBatchesSerializer(raw_materials, many=True).data

        return Response({
            'raw_materials': raw_materials_data,
        })


class RawMaterialAcceptanceTestListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        raw_material_id = request.GET.get('raw_material_id')
        if not raw_material_id:
            return Response({'error': 'Missing raw_material_id'}, status=status.HTTP_400_BAD_REQUEST)

        tests = RawMaterialAcceptanceTest.objects.filter(raw_material_id=raw_material_id)
        if not tests.exists():
            return Response({'error': 'No tests found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = RawMaterialAcceptanceTestSerializer(tests, many=True, context={'request': request})
        raw_material_info = serializer.data[0] 

        formatted_tests = []
        for item in serializer.data:
            formatted_tests.append({
                'file': item['file'],
                'test_id': item['id'],
                'test_name': item['acceptance_test_name'],
                'test_type': 'Qualitative' if item['test_value'] and item['test_value'].isalpha() else 'Quantitative',
                'test_value': item['test_value'],
                'result_remark': item['remark'],
                'unit': '',
                'test_date': now().date().isoformat(),
                'validity_date': '',
            })
        return Response({
            'raw_material_name': raw_material_info['raw_material_name'],
            'batch': raw_material_info['batch_id'],
            'grade_name': raw_material_info['grade_name'],
            'sources_name': raw_material_info['sources_name'],
            'suppliers_name': raw_material_info['suppliers_name'],
            'tests': formatted_tests
        }, status=status.HTTP_200_OK)


class DrawingListByProductAPIView(APIView):
    def get(self, request):
        product_id = request.GET.get('product_id')
        if product_id:
            try:
                product = Product.objects.get(id=product_id)
                drawings = product.drawings.all()
            except Product.DoesNotExist:
                return Response({'error': 'Product not found'}, status=404)
        else:
            drawings = Drawing.objects.none()
        
        serializer = DrawingSerializer(drawings, many=True)
        return Response(serializer.data)


class ProductEquipmentsApiView(APIView):
    def get(self, request):
        product_id = request.GET.get('product_id')
        if not product_id:
            return Response({'error': 'Product ID is required', 'equipment': []}, status=400)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found', 'equipment': []}, status=404)

        related_equipment = product.equipment.all()
        serializer = EquipmentSerializer(related_equipment, many=True)
        equipment_data = serializer.data

        for equipment in equipment_data:
            equipment_id = equipment['id']
            docs = EquipmentDocument.objects.filter(equipment_id=equipment_id)
            equipment['documents'] = [{
                'id': doc.id,
                'title': doc.title,
                'documentFile': str(doc.documentfile)
            } for doc in docs]

        return Response({'equipment': equipment_data}, status=200)


class ProductAcceptanceTestApiView(APIView):
    def get(self, request):
        product_id = request.GET.get('product_id')

        if not product_id:
            return Response({'error': 'product_id is required'}, status=400)
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=404)
        tests = ProductAcceptanceTest.objects.filter(product=product)       

        serializer = ProductAcceptanceTestSerializer(tests, many=True)
        return Response(serializer.data)


class RawMaterialProcessListAPIView(APIView):
    def get(self, request):
        product_id = request.GET.get('product_id')
        if product_id:
            try:
                product = Product.objects.get(id=product_id)
                related_processes = product.process.all()
                
                # Get detailed process data including steps
                process_data = []
                for process in related_processes:
                    try:
                        # Get all process steps for this process
                        process_steps = ProcessStep.objects.filter(process=process).order_by('step_id')
                        
                        process_info = {
                            'id': process.id,
                            'process_title': process.process_title,
                            'steps': []
                        }
                        
                        for step in process_steps:
                            try:
                                step_data = {
                                    'step_id': step.step_id,
                                    'process_description': step.process_description,
                                    'process_date': step.process_date.strftime('%Y-%m-%d') if step.process_date else None,
                                    'process_type': step.process_type,
                                    'rm_status': step.rm_status,
                                    'equipment_status': step.equipment_status,
                                    'consumable_status': step.consumable_status,
                                    'component_status': step.component_status,
                                    'min_value': step.min_value,
                                    'max_value': step.max_value,
                                    'test_result': step.test_result,
                                    'specification_result': step.specification_result,
                                    'remarks': step.remarks,
                                    'raw_materials': [],
                                    'equipment': [],
                                    'consumables': [],
                                    'components': []
                                }
                                
                                # Get related ManyToMany data with error handling
                                try:
                                    if hasattr(step, 'raw_material_batch'):
                                        raw_materials = []
                                        for rm in step.raw_material_batch.all():
                                            try:
                                                if hasattr(rm, 'raw_material') and rm.raw_material:
                                                    raw_materials.append({
                                                        'id': rm.id, 
                                                        'name': rm.raw_material.name
                                                    })
                                                else:
                                                    raw_materials.append({
                                                        'id': rm.id, 
                                                        'name': f'Batch {getattr(rm, "batch_id", "Unknown")}'
                                                    })
                                            except Exception as e:
                                                print(f"Error processing raw material: {e}")
                                                raw_materials.append({
                                                    'id': rm.id, 
                                                    'name': 'Unknown Material'
                                                })
                                        step_data['raw_materials'] = raw_materials
                                except Exception as e:
                                    print(f"Error accessing raw_material_batch: {e}")
                                    step_data['raw_materials'] = []
                                
                                try:
                                    if hasattr(step, 'equipment'):
                                        step_data['equipment'] = [
                                            {'id': eq.id, 'name': eq.name} 
                                            for eq in step.equipment.all()
                                        ]
                                except Exception as e:
                                    print(f"Error accessing equipment: {e}")
                                    step_data['equipment'] = []
                                
                                try:
                                    if hasattr(step, 'consumable_batch'):
                                        consumables = []
                                        for cons in step.consumable_batch.all():
                                            try:
                                                if hasattr(cons, 'consumable') and cons.consumable:
                                                    consumables.append({
                                                        'id': cons.id, 
                                                        'name': cons.consumable.name
                                                    })
                                                else:
                                                    consumables.append({
                                                        'id': cons.id, 
                                                        'name': f'Batch {getattr(cons, "batch_id", "Unknown")}'
                                                    })
                                            except Exception as e:
                                                print(f"Error processing consumable: {e}")
                                                consumables.append({
                                                    'id': cons.id, 
                                                    'name': 'Unknown Consumable'
                                                })
                                        step_data['consumables'] = consumables
                                except Exception as e:
                                    print(f"Error accessing consumable_batch: {e}")
                                    step_data['consumables'] = []
                                
                                try:
                                    if hasattr(step, 'component_batch'):
                                        components = []
                                        for comp in step.component_batch.all():
                                            try:
                                                if hasattr(comp, 'component') and comp.component:
                                                    components.append({
                                                        'id': comp.id, 
                                                        'name': comp.component.name
                                                    })
                                                else:
                                                    components.append({
                                                        'id': comp.id, 
                                                        'name': f'Batch {getattr(comp, "batch_id", "Unknown")}'
                                                    })
                                            except Exception as e:
                                                print(f"Error processing component: {e}")
                                                components.append({
                                                    'id': comp.id, 
                                                    'name': 'Unknown Component'
                                                })
                                        step_data['components'] = components
                                except Exception as e:
                                    print(f"Error accessing component_batch: {e}")
                                    step_data['components'] = []
                                
                                process_info['steps'].append(step_data)
                            except Exception as e:
                                print(f"Error processing step {step.step_id}: {e}")
                                continue
                        
                        process_data.append(process_info)
                    except Exception as e:
                        print(f"Error processing process {process.process_title}: {e}")
                        continue

                return Response(process_data)
            except Product.DoesNotExist:
                return Response({'error': 'Product not found'}, status=404)
        return Response({'error': 'Product ID is required'}, status=400)


@method_decorator(login_required, name='dispatch')
class ProductBatchFetchView(BaseModelViewSet):
    def get(self, request, pk=None):
        data = {}
        success = False
        message = constants.USER_FETCH_FAILED
        status_code = status.HTTP_403_FORBIDDEN

        if pk:
            try:
                success, status_code, data, message = ProductService.get_product_batch_detail(pk)
                
                # Get PagePermission variables for Product Batch using unified permission service
                page_permissions = {}
                if request.user.is_authenticated:
                    try:
                        from product.services.permission_service import ProductBatchPermissionService
                        
                        # Get unified permission context
                        page_permissions = ProductBatchPermissionService.get_page_permission_context(request.user)
                        

                        
                    except Exception as e:
                        print(f"Error getting page permissions: {e}")
                        # Fallback to checking PagePermission directly from database
                        try:
                            from qdpc.models.page_permission import PagePermission
                            user_groups = request.user.groups.all()
                            
                            # Check if user has any groups with Product batch permissions
                            has_permissions = PagePermission.objects.filter(
                                group__in=user_groups,
                                page_name='Product batch',
                                is_active=True
                            ).exists()
                            

                            
                            if has_permissions:
                                # User has some permissions, check each type
                                add_perm = PagePermission.objects.filter(
                                    group__in=user_groups,
                                    page_name='Product batch',
                                    permission_type='add',
                                    is_active=True
                                ).exists()
                                edit_perm = PagePermission.objects.filter(
                                    group__in=user_groups,
                                    page_name='Product batch',
                                    permission_type='edit',
                                    is_active=True
                                ).exists()
                                delete_perm = PagePermission.objects.filter(
                                    group__in=user_groups,
                                    page_name='Product batch',
                                    permission_type='delete',
                                    is_active=True
                                ).exists()
                                approve_perm = PagePermission.objects.filter(
                                    group__in=user_groups,
                                    page_name='Product batch',
                                    permission_type='approve',
                                    is_active=True
                                ).exists()
                                

                                
                                page_permissions = {
                                    'can_access_product_batch': True,
                                    'can_add_product_batch': add_perm,
                                    'can_delete_product_batch': delete_perm,
                                    'can_edit_product_batch': edit_perm,
                                    'can_approve_product_batch': approve_perm,
                                }
                            else:
                                # No permissions found, default to view only
                                page_permissions = {
                                    'can_access_product_batch': True,
                                    'can_add_product_batch': False,
                                    'can_edit_product_batch': False,
                                    'can_delete_product_batch': False,
                                    'can_approve_product_batch': False,
                                }
                        except Exception as db_error:
                            print(f"Error checking PagePermission directly: {db_error}")
                            # Final fallback - allow basic access
                            page_permissions = {
                                'can_access_product_batch': True,
                                'can_add_product_batch': False,
                                'can_edit_product_batch': False,
                                'can_delete_product_batch': False,
                                'can_approve_product_batch': False,
                            }
                
                context = {
                    'batches': data,
                    'total_count': len(data) if isinstance(data, list) else 1,
                    **page_permissions  # Unpack page permissions into context
                }
                return render(request, 'product_batchlist.html', context)
            except Exception as ex:
                return self.render_response(data, success, message, status.HTTP_400_BAD_REQUEST)
        else:
            batches = ProductBatchs.objects.select_related('product').all().order_by('-created_at')
            
            # Get user approval permissions
            approval_permissions = {}
            if request.user.is_authenticated:
                try:
                    from product.services.approval_service import ProductBatchApprovalService
                    approval_permissions = ProductBatchApprovalService.get_user_approval_permissions(request.user)
                except Exception as e:
                    print(f"Error getting approval permissions: {e}")
                    approval_permissions = {
                        'can_approve_product_batch': False,
                        'can_reject_product_batch': False,
                        'user_roles': [],
                        'approval_level': 'none',
                        'explanation': 'Error loading permissions'
                    }
            
            # Get PagePermission variables for Product Batch using unified permission service
            page_permissions = {}
            if request.user.is_authenticated:
                try:
                    from product.services.permission_service import ProductBatchPermissionService
                    
                    # Get unified permission context
                    page_permissions = ProductBatchPermissionService.get_page_permission_context(request.user)
                    
                    
                    
                except Exception as e:
                    print(f"Error getting page permissions: {e}")
                    # Fallback to checking PagePermission directly from database
                    try:
                        from qdpc.models.page_permission import PagePermission
                        user_groups = request.user.groups.all()
                        
                        # Check if user has any groups with Product batch permissions
                        has_permissions = PagePermission.objects.filter(
                            group__in=user_groups,
                            page_name='Product batch',
                            is_active=True
                        ).exists()
                        

                        
                        if has_permissions:
                            # User has some permissions, check each type
                            add_perm = PagePermission.objects.filter(
                                group__in=user_groups,
                                page_name='Product batch',
                                permission_type='add',
                                is_active=True
                            ).exists()
                            edit_perm = PagePermission.objects.filter(
                                group__in=user_groups,
                                page_name='Product batch',
                                permission_type='edit',
                                is_active=True
                            ).exists()
                            delete_perm = PagePermission.objects.filter(
                                group__in=user_groups,
                                page_name='Product batch',
                                permission_type='delete',
                                is_active=True
                            ).exists()
                            approve_perm = PagePermission.objects.filter(
                                group__in=user_groups,
                                page_name='Product batch',
                                permission_type='approve',
                                is_active=True
                            ).exists()
                            

                            
                            page_permissions = {
                                'can_access_product_batch': True,
                                'can_add_product_batch': add_perm,
                                'can_edit_product_batch': edit_perm,
                                'can_delete_product_batch': delete_perm,
                                'can_approve_product_batch': approve_perm,
                            }
                        else:
                            # No permissions found, default to view only
                            page_permissions = {
                                'can_access_product_batch': True,
                                'can_add_product_batch': False,
                                'can_edit_product_batch': False,
                                'can_delete_product_batch': False,
                                'can_approve_product_batch': False,
                            }
                    except Exception as db_error:
                        print(f"Error checking PagePermission directly: {db_error}")
                        # Final fallback - allow basic access
                        page_permissions = {
                            'can_access_product_batch': True,
                            'can_add_product_batch': False,
                            'can_edit_product_batch': False,
                            'can_delete_product_batch': False,
                            'can_approve_product_batch': False,
                        }
            
            context = {
                'batches': batches,
                'total_count': batches.count(),
                'approval_permissions': approval_permissions,
                **page_permissions  # Unpack page permissions into context
            }
            return render(request, 'product_batchlist.html', context)


@method_decorator(login_required, name='dispatch')
class ProductBatchAddView(BaseModelViewSet):
    def get(self, request):
        rawmaterial = RawMaterial.objects.all()
        consumable = self.get_all_obj(model_name=Consumable)
        component = Component.objects.all()
        product = self.get_all_obj(model_name=Product)
        units = self.get_all_obj(model_name=Unit)
        category = ProductCategory.objects.all()     
        processes = Process.objects.all()      
        drawings = Drawing.objects.all()        
        
        context = {
            'products': product,
            'raw_material': rawmaterial,
            'consumable': consumable,
            'component': component,
            'units': units,
            'processes': processes,
            'drawings': drawings
        }
        return render(request, 'productbatch_add.html', context)

    def post(self, request):
        data = request.POST
        files = request.FILES
        try:
            # Create Product Batch
            product_batch = ProductBatchs.objects.create(
                batch_id=data.get('batch_id'),
                unit=data.get('unit'),
                product_id=data.get('product'),
                manufacturing_start=data.get('manufacturing_start'),
                manufacturing_end=data.get('manufacturing_end')
            )
            
            # Create notification for product batch creation
            notifications = NotificationService.create_entity_notification(
                entity_type='product_batch',
                entity_id=product_batch.id,
                entity_name=f"Batch {product_batch.batch_id or product_batch.unit}",
                notification_type='create',
                created_by=request.user
            )

            # Raw Materials - Handle both JSON and form data
            raw_materials = request.POST.getlist('raw_materials[]') or request.POST.getlist('raw_material[]')
            for raw_data in raw_materials:
                try:
                    if isinstance(raw_data, str) and raw_data.startswith('{'):
                        # JSON format
                        raw_info = json.loads(raw_data)
                        raw_id = raw_info.get('raw_material_id')
                        batch_id = raw_info.get('batch_id')
                    else:
                        # Form data format
                        raw_id = raw_data
                        batch_id = None
                    
                    if raw_id:
                        try:
                            if batch_id:
                                batch_instance = RawMaterialBatch.objects.get(pk=batch_id)
                            else:
                                # Create or get a default batch if none specified
                                batch_instance = None
                            
                            raw_material_batch = ProductBatchRawMaterial.objects.create(
                                product_batch=product_batch,
                                raw_material_id=raw_id,
                                batch=batch_instance, 
                                status='active'
                            )
                            
                            # Create notification for raw material addition
                            try:
                                NotificationService.create_entity_notification(
                                    entity_type='raw_material',
                                    entity_id=raw_material_batch.id,
                                    entity_name=f"Raw Material added to Batch {product_batch.batch_id or product_batch.unit}",
                                    notification_type='create',
                                    created_by=request.user
                                )
                            except Exception as notif_error:
                                print(f"Notification creation failed: {notif_error}")
                                
                        except RawMaterialBatch.DoesNotExist:
                            print(f"Raw material batch {batch_id} not found")
                            continue
                        except Exception as rm_error:
                            print(f"Error creating raw material batch: {rm_error}")
                            continue
                            
                except (json.JSONDecodeError, KeyError, TypeError, ValueError) as e:
                    print(f"Error processing raw material data: {e}")
                    continue

            # Components - Handle both JSON and form data
            components = request.POST.getlist('components[]') or request.POST.getlist('component[]')
            for comp_data in components:
                try:
                    if isinstance(comp_data, str) and comp_data.startswith('{'):
                        # JSON format
                        comp_info = json.loads(comp_data)
                        comp_id = comp_info.get('component_id')
                        batch_id = comp_info.get('batch_id')
                    else:
                        # Form data format
                        comp_id = comp_data
                        batch_id = None
                    
                    if comp_id:
                        try:
                            if batch_id:
                                batch_instance = ComponentBatch.objects.get(pk=batch_id)
                            else:
                                batch_instance = None
                                
                            ProductBatchComponent.objects.create(
                                product_batch=product_batch,
                                component_id=comp_id,
                                batch=batch_instance,
                                status="active"
                            )
                        except ComponentBatch.DoesNotExist:
                            print(f"Component batch {batch_id} not found")
                            continue
                        except Exception as comp_error:
                            print(f"Error creating component batch: {comp_error}")
                            continue
                            
                except (json.JSONDecodeError, KeyError, TypeError, ValueError) as e:
                    print(f"Error processing component data: {e}")
                    continue

            # Consumables - Handle both JSON and form data
            consumables = request.POST.getlist('consumables[]') or request.POST.getlist('consumable[]')
            for cons_data in consumables:
                try:
                    if isinstance(cons_data, str) and cons_data.startswith('{'):
                        # JSON format
                        cons_info = json.loads(cons_data)
                        cons_id = cons_info.get('consumable_id')
                        batch_id = cons_info.get('batch_id')
                        status_val = cons_info.get('status', 'active')
                    else:
                        # Form data format
                        cons_id = cons_data
                        batch_id = None
                        status_val = 'active'
                    
                    if cons_id:
                        try:
                            if batch_id:
                                batch_instance = ConsumableBatch.objects.get(pk=batch_id)
                            else:
                                batch_instance = None
                                
                            ProductBatchConsumable.objects.create(
                                product_batch=product_batch,
                                consumable_id=cons_id,
                                batch=batch_instance,
                                status=status_val
                            )
                        except ConsumableBatch.DoesNotExist:
                            print(f"Consumable batch {batch_id} not found")
                            continue
                        except Exception as cons_error:
                            print(f"Error creating consumable batch: {cons_error}")
                            continue
                            
                except (json.JSONDecodeError, KeyError, TypeError, ValueError) as e:
                    print(f"Error processing consumable data: {e}")
                    continue

            # Drawings - Handle form data properly
            drawings = request.POST.getlist('drawings[]') or request.POST.getlist('drawing_title[]')
            for i, draw_data in enumerate(drawings):
                try:
                    if draw_data:  # Only create if there's actual data
                        # Get related drawing data
                        drawing_titles = request.POST.getlist('drawing_title[]')
                        drawing_numbers = request.POST.getlist('drawing_number[]')
                        drawing_statuses = request.POST.getlist('drawing_status[]')
                        
                        if i < len(drawing_titles) and drawing_titles[i]:
                            ProductBatchDrawing.objects.create(
                                product_batch=product_batch,
                                drawing_title=drawing_titles[i] if i < len(drawing_titles) else '',
                                drawing_number=drawing_numbers[i] if i < len(drawing_numbers) else '',
                                status=drawing_statuses[i] if i < len(drawing_statuses) else 'active'
                            )
                except Exception as draw_error:
                    print(f"Error creating drawing: {draw_error}")
                    continue

            # Processes - Handle form data properly
            processes = request.POST.getlist('processes[]') or request.POST.getlist('process[]')
            for proc_id in processes:
                try:
                    if proc_id:
                        ProductBatchProcess.objects.create(
                            product_batch=product_batch,
                            process_id=proc_id
                        )
                except Exception as proc_error:
                    print(f"Error creating process: {proc_error}")
                    continue

            # Equipment - Handle form data properly
            equipment_list = request.POST.getlist('equipment[]')
            for eq_id in equipment_list:
                try:
                    if eq_id:
                        ProductBatchEquipment.objects.create(
                            product_batch=product_batch,
                            equipment_id=eq_id
                        )
                except Exception as eq_error:
                    print(f"Error creating equipment: {eq_error}")
                    continue

            # Product Acceptance Tests - Handle form data properly
            test_ids = request.POST.getlist('acceptance_tests[]') 
            for test_id in test_ids:
                try:
                    if test_id:
                        ProductBatchAcceptanceTest.objects.create(
                            product_batch=product_batch,
                            acceptance_test_id=test_id,
                            result=request.POST.get(f'result_{test_id}', ''),
                            date_of_test=request.POST.get(f'date_{test_id}') or None,
                            remarks=request.POST.get(f'remark_{test_id}', ''),
                            report=files.get(f'report_{test_id}')
                        )
                except Exception as test_error:
                    print(f"Error creating acceptance test: {test_error}")
                    continue

            # Raw material acceptance tests - Handle form data properly
            index = 0
            while True:
                raw_material_key = f'raw_acceptance[{index}][raw_material_id]'
                test_id_key = f'raw_acceptance[{index}][acceptance_test_id]'

                raw_material_id = request.POST.get(raw_material_key)
                test_id = request.POST.get(test_id_key)

                if not raw_material_id or not test_id:
                    break

                try:
                    RawmaterialAcceptenceTest.objects.create(
                        product_batch=product_batch,
                        raw_material_id=raw_material_id,
                        acceptance_test_id=test_id
                    )
                except Exception as e:
                    print(f"Error saving raw acceptance test at index {index}: {e}")

                index += 1
            
            # Save dynamic tables with error handling
            try:
                save_dynamic_tables(request, product_batch.id)
            except Exception as dt_error:
                print(f"Error saving dynamic tables: {dt_error}")
                
            return Response({
                'success': True,
                'message': 'Product batch created successfully.',
                'batch_id': product_batch.id
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


def save_dynamic_tables(request, product_batch_id):
    if request.method == 'POST':
        batch = get_object_or_404(ProductBatchs, id=product_batch_id)
        post_data = request.POST

        # Get indexes of all tables
        table_keys = [key for key in post_data if key.startswith('tables[') and key.endswith('][title]')]
        table_indexes = sorted(set(k.split('[')[1].split(']')[0] for k in table_keys))

        for index in table_indexes:
            table_title = post_data.get(f'tables[{index}][title]', '').strip()
            if not table_title:
                continue

            # Extract column names
            columns = []
            col_i = 0
            while True:
                key = f'tables[{index}][columns][{col_i}][name]'
                if key in post_data:
                    col_name = post_data.get(key).strip()
                    columns.append(col_name)
                    col_i += 1
                else:
                    break

            # Save the table with its columns
            dynamic_table = DynamicTable.objects.create(
                product_batch=batch,
                title=table_title,
                columns=columns
            )

            # Now save the row data
            max_rows = 0
            for i in range(len(columns)):
                data_list = post_data.getlist(f'tables[{index}][columns][{i}][data][]')
                max_rows = max(max_rows, len(data_list))

            for row_index in range(max_rows):
                row_data = {}
                for col_index in range(len(columns)):
                    values = post_data.getlist(f'tables[{index}][columns][{col_index}][data][]')
                    row_data[str(col_index)] = values[row_index] if row_index < len(values) else ""
                DynamicTableRow.objects.create(table=dynamic_table, data=row_data)

        # Return success response with notification info
        return Response({
            'success': True,
            'message': 'Product batch created successfully!',
            'batch_id': product_batch.id,
            'batch_name': f"Batch {product_batch.batch_id or product_batch.unit}",
            'notifications_created': len(notifications) if notifications else 0,
            'redirect_url': reverse('product-batch-list')
        })
    return Response({'error': 'Invalid request'}, status=400)


@method_decorator(login_required, name='dispatch')
class ProductBatchDetailView(BaseModelViewSet):
    def get(self, request, batch_id):
        print("Product batch hit")
        try:
            batch = ProductBatch.objects.get(id=batch_id)
        except ProductBatch.DoesNotExist:
            return Response({"error": "Product batch not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductBatchDetailedSerializer(batch)
        return Response(serializer.data, status=status.HTTP_200_OK)


@method_decorator(login_required, name='dispatch')
class ProductBatchDeleteView(APIView):
    def post(self, request, pk):
        try:
            batch = get_object_or_404(ProductBatchs, pk=pk)
            batch_name = f"Batch {batch.batch_id or batch.unit}"
            
            # Create notification for product batch deletion
            NotificationService.create_entity_notification(
                entity_type='product_batch',
                entity_id=batch.id,
                entity_name=batch_name,
                notification_type='delete',
                created_by=request.user
            )

            # Delete related records manually
            ProductBatchRawMaterial.objects.filter(product_batch=batch).delete()
            ProductBatchComponent.objects.filter(product_batch=batch).delete()
            ProductBatchConsumable.objects.filter(product_batch=batch).delete()
            ProductBatchDrawing.objects.filter(product_batch=batch).delete()
            ProductBatchProcess.objects.filter(product_batch=batch).delete()
            ProductBatchEquipment.objects.filter(product_batch=batch).delete()
            ProductBatchAcceptanceTest.objects.filter(product_batch=batch).delete()

            # Delete the batch itself
            batch.delete()

            return Response({'success': True}, status=200)
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=500)


@method_decorator(login_required, name='dispatch')
class SingleProductBatchReportView(View):
    def get(self, request, pk):
        product_batch = get_object_or_404(ProductBatchs.objects.select_related('product'), pk=pk)
        product = product_batch.product
        related_processes = product.process.all()
        raw_materials = product.rawmaterial.all()
        
        product_tests = ProductBatchAcceptanceTest.objects.filter(product_batch=product_batch).select_related('acceptance_test')
        product_test_table = []
        for idx, test in enumerate(product_tests, start=1):
            product_test_table.append({
                'sl_no': idx,
                'batch_no': product_batch.batch_id,
                'parameter': test.acceptance_test.name if test.acceptance_test else '',
                'result': test.result,
                'test_date': test.date_of_test.strftime('%Y-%m-%d') if test.date_of_test else '',
            })

        processess = ProcessSerilalizers(related_processes, many=True)
        
        raw_material_ids = raw_materials.values_list('id', flat=True)
        tests = RawMaterialAcceptanceTest.objects.filter(raw_material_id__in=raw_material_ids)
        test_serializer = RawMaterialAcceptanceTestSerializer(tests, many=True, context={'request': request})
        serialized_tests = test_serializer.data

        rawmaterial_tests_map = {}
        for test in serialized_tests:
            rid = test['raw_material']
            if rid not in rawmaterial_tests_map:
                rawmaterial_tests_map[rid] = []
            rawmaterial_tests_map[rid].append({
                'parameter': test['acceptance_test_name'],
                'specification': test.get('test_value', ''),
                'result': test.get('remark', ''),
                'test_date': now().date().isoformat(),
            })

        # Link to raw material batches
        batch_raw_materials = ProductBatchRawMaterial.objects.filter(
            product_batch=product_batch
        ).select_related('raw_material', 'batch')

        # Final formatted structure for template
        rawmaterial_tests_final = []
        for item in batch_raw_materials:
            rid = item.raw_material.id
            test_data = rawmaterial_tests_map.get(rid, [])
            rawmaterial_tests_final.append({
                'raw_material_name': item.raw_material.name,
                'batch_no': item.batch.batch_id,
                'expiry_date': item.batch.expiry_date.strftime('%Y-%m-%d') if item.batch.expiry_date else None,
                'tests': test_data
            })

        processess = ProcessSerilalizers(related_processes, many=True)

        return render(request, 'report.html', {
            'batch': product_batch,
            'processes': processess.data,
            'rawmaterial_section': rawmaterial_tests_final,
            'product_tests': product_test_table,
            'processing_agency_name': product.processing_agencies.name if product.processing_agencies else None,
            'processing_agency_center': product.processing_agencies.center.name if product.processing_agencies else None
        })


@method_decorator(login_required, name='dispatch')
class SingleProductBatchView(View):
    def get(self, request, pk):      
        batch = get_object_or_404(ProductBatchs.objects.select_related('product'), pk=pk)

        # Fetch all related objects
        raw_materials = batch.productbatchrawmaterial_set.select_related('raw_material').all()
        components = batch.productbatchcomponent_set.select_related('component').all()
        consumables = batch.productbatchconsumable_set.select_related('consumable').all()
        processes = batch.productbatchprocess_set.select_related('process').all()
        drawings = batch.productbatchdrawing_set.select_related('drawing').all()
        equipment = batch.productbatchequipment_set.select_related('equipment').all()
        tests = batch.productbatchacceptancetest_set.select_related('acceptance_test').all()

        # Fetch detailed process steps for each process
        process_steps_data = []
        
        for process_batch in processes:
            process = process_batch.process
            
            # Get all process steps for this process
            process_steps = ProcessStep.objects.filter(process=process).order_by('step_id')
            
            process_data = {
                'process': process,
                'steps': process_steps
            }
            process_steps_data.append(process_data)
        


        # Fetch dynamic tables data
        dynamic_tables = []
        try:
            from product.models import DynamicTable, DynamicTableRow
            tables = DynamicTable.objects.filter(product_batch=batch)
            for table in tables:
                rows = DynamicTableRow.objects.filter(table=table)
                table_data = {
                    'title': table.title,
                    'columns': table.columns,
                    'rows': [row.data for row in rows]
                }
                dynamic_tables.append(table_data)
        except Exception as e:
            dynamic_tables = []

        from django.utils import timezone
        
        return render(request, 'product_batch_view.html', {
            'batch': batch,
            'raw_materials': raw_materials,
            'components': components,
            'consumables': consumables,
            'processes': processes,
            'process_steps_data': process_steps_data,
            'drawings': drawings,
            'equipment': equipment,
            'acceptance_tests': tests,
            'dynamic_tables': dynamic_tables,
            'today': timezone.now().date(),
        })


@method_decorator(login_required, name='dispatch')
class ProductBatchEditView(View):
    def get(self, request, pk):
        try:
            # Get the product batch
            batch = get_object_or_404(ProductBatchs.objects.select_related('product'), pk=pk)
            
            # Get all products for the form
            products = Product.objects.all()
            
            # Fetch all related objects (same as SingleProductBatchView)
            raw_materials = batch.productbatchrawmaterial_set.select_related('raw_material').all()
            components = batch.productbatchcomponent_set.select_related('component').all()
            consumables = batch.productbatchconsumable_set.select_related('consumable').all()
            processes = batch.productbatchprocess_set.select_related('process').all()
            drawings = batch.productbatchdrawing_set.select_related('drawing').all()
            equipment = batch.productbatchequipment_set.select_related('equipment').all()
            acceptance_tests = batch.productbatchacceptancetest_set.select_related('acceptance_test').all()
            
            # Fetch detailed process steps for each process
            process_steps_data = []
            for process_batch in processes:
                process = process_batch.process
                process_steps = ProcessStep.objects.filter(process=process).order_by('step_id')
                process_data = {
                    'process': process,
                    'steps': process_steps
                }
                process_steps_data.append(process_data)
            
            # Get dropdown lists for form options
            raw_materials_list = RawMaterial.objects.all()
            components_list = Component.objects.all()
            consumables_list = Consumable.objects.all()
            processes_list = Process.objects.all()
            equipment_list = Equipment.objects.all()
            acceptance_tests_list = AcceptanceTest.objects.all()
            
           
            
            # Fetch dynamic tables data
            dynamic_tables = []
            try:
                from product.models import DynamicTable, DynamicTableRow
                tables = DynamicTable.objects.filter(product_batch=batch)
                for table in tables:
                    rows = DynamicTableRow.objects.filter(table=table)
                    table_data = {
                        'title': table.title,
                        'columns': table.columns,
                        'rows': [row.data for row in rows]
                    }
                    dynamic_tables.append(table_data)
            except Exception as e:
                dynamic_tables = []
            
            context = {
                'batch': batch,
                'products': products,
                'raw_materials': raw_materials,
                'components': components,
                'consumables': consumables,
                'processes': processes,
                'process_steps_data': process_steps_data,
                'drawings': drawings,
                'equipment': equipment,
                'acceptance_tests': acceptance_tests,
                'raw_materials_list': raw_materials_list,
                'components_list': components_list,
                'consumables_list': consumables_list,
                'processes_list': processes_list,
                'equipment_list': equipment_list,
                'acceptance_tests_list': acceptance_tests_list,
                'dynamic_tables': dynamic_tables,
            }
            
           
            
            return render(request, 'product_batch_edit.html', context)
            
        except Exception as e:

            messages.error(request, f'Error loading batch: {str(e)}')
            # Don't redirect on error, show the error in context
            return render(request, 'product_batch_edit.html', {
                'error': str(e),
                'batch': None,
                'products': Product.objects.all(),
                'raw_materials_list': RawMaterial.objects.all(),
                'components_list': Component.objects.all(),
                'consumables_list': Consumable.objects.all(),
                'processes_list': Process.objects.all(),
                'equipment_list': Equipment.objects.all(),
                'acceptance_tests_list': AcceptanceTest.objects.all(),
            })
    
    def post(self, request, pk):
        try:
            
            # Get the product batch
            batch = get_object_or_404(ProductBatchs.objects.select_related('product'), pk=pk)

            
            # Validate required fields
            required_fields = ['product', 'manufacturing_start', 'manufacturing_end']
            missing_fields = []
            
            for field in required_fields:
                if not request.POST.get(field):
                    missing_fields.append(field)
            
            if missing_fields:
                error_msg = f'Missing required fields: {", ".join(missing_fields)}'

                messages.error(request, error_msg)
                return redirect('product-batch-edit', pk=pk)
            
            # Update basic batch fields
      
            
            if request.POST.get('batch_id'):
                batch.batch_id = request.POST.get('batch_id')
            if request.POST.get('unit_id'):
                batch.unit = request.POST.get('unit_id')
            if request.POST.get('product'):
                batch.product_id = request.POST.get('product')
            if request.POST.get('manufacturing_start'):
                batch.manufacturing_start = request.POST.get('manufacturing_start')
            if request.POST.get('manufacturing_end'):
                batch.manufacturing_end = request.POST.get('manufacturing_end')
            if request.POST.get('status'):
                batch.status = request.POST.get('status')
            
            # Save the batch
            batch.save()
            
            # Create notification for product batch update
            NotificationService.create_entity_notification(
                entity_type='product_batch',
                entity_id=batch.id,
                entity_name=f"Batch {batch.batch_id or batch.unit}",
                notification_type='update',
                created_by=request.user
            )
            
            messages.success(request, 'Product batch updated successfully!')

            return redirect('product-batch-view', pk=batch.id)
            
        except Exception as e:
            messages.error(request, f'Error updating batch: {str(e)}')
            return redirect('product-batch-edit', pk=pk)
    
    def update_related_data(self, request, batch):
        """Update all related data for the product batch"""
        from django.db import transaction
        
        try:
            with transaction.atomic():
                # Update Raw Materials
                self.update_raw_materials(request, batch)
                
                # Update Components
                self.update_components(request, batch)
                
                # Update Consumables
                self.update_consumables(request, batch)
                
                # Update Processes
                self.update_processes(request, batch)
                
                # Update Equipment
                self.update_equipment(request, batch)
                
                # Update Acceptance Tests
                self.update_acceptance_tests(request, batch)
                
                # Update Drawings
                self.update_drawings(request, batch)
                
        except Exception as e:
            raise e
    
    def update_raw_materials(self, request, batch):
        """Update raw materials for the batch"""
        raw_materials = request.POST.getlist('raw_material[]')
        
        # Don't clear existing if no new data provided
        if not raw_materials or all(not rm for rm in raw_materials):
            return
            
        # Clear existing raw materials only if we have new data
        batch.productbatchrawmaterial_set.all().delete()
        
        batch_ids = request.POST.getlist('raw_material_batch_id[]')
        statuses = request.POST.getlist('raw_material_status[]')
        
        for i, raw_material_id in enumerate(raw_materials):
            if raw_material_id:
                try:
                    raw_material = RawMaterial.objects.get(id=raw_material_id)
                    batch_id = batch_ids[i] if i < len(batch_ids) else ''
                    status = statuses[i] if i < len(statuses) else 'active'
                    
                    # Get or create raw material batch
                    raw_batch, created = RawMaterialBatch.objects.get_or_create(
                        raw_material=raw_material,
                        batch_id=batch_id,
                        defaults={'status': status}
                    )
                    
                    # Create product batch raw material relationship
                    ProductBatchRawMaterial.objects.create(
                        product_batch=batch,
                        raw_material=raw_material,
                        batch=raw_batch,
                        status=status
                    )
                except Exception as e:
                    pass
    
    def update_components(self, request, batch):
        """Update components for the batch"""
        components = request.POST.getlist('component[]')
        
        # Don't clear existing if no new data provided
        if not components or all(not comp for comp in components):
            return
            
        # Clear existing components only if we have new data
        batch.productbatchcomponent_set.all().delete()
        
        batch_ids = request.POST.getlist('component_batch_id[]')
        statuses = request.POST.getlist('component_status[]')
        
        for i, component_id in enumerate(components):
            if component_id:
                try:
                    component = Component.objects.get(id=component_id)
                    batch_id = batch_ids[i] if i < len(batch_ids) else ''
                    status = statuses[i] if i < len(statuses) else 'active'
                    
                    # Get or create component batch
                    comp_batch, created = ComponentBatch.objects.get_or_create(
                        component=component,
                        batch_id=batch_id,
                        defaults={'status': status}
                    )
                    
                    # Create product batch component relationship
                    ProductBatchComponent.objects.create(
                        product_batch=batch,
                        component=component,
                        batch=comp_batch,
                        status=status
                    )
                except Exception as e:
                    pass
    
    def update_consumables(self, request, batch):
        """Update consumables for the batch"""
        consumables = request.POST.getlist('consumable[]')
        
        # Don't clear existing if no new data provided
        if not consumables or all(not cons for cons in consumables):
            return
            
        # Clear existing consumables only if we have new data
        batch.productbatchconsumable_set.all().delete()
        
        batch_ids = request.POST.getlist('consumable_batch_id[]')
        statuses = request.POST.getlist('consumable_status[]')
        
        for i, consumable_id in enumerate(consumables):
            if consumable_id:
                try:
                    consumable = Consumable.objects.get(id=consumable_id)
                    batch_id = batch_ids[i] if i < len(batch_ids) else ''
                    status = statuses[i] if i < len(statuses) else 'active'
                    
                    # Get or create consumable batch
                    cons_batch, created = ConsumableBatch.objects.get_or_create(
                        consumable=consumable,
                        batch_id=batch_id,
                        defaults={'status': status}
                    )
                    
                    # Create product batch consumable relationship
                    ProductBatchConsumable.objects.create(
                        product_batch=batch,
                        consumable=consumable,
                        batch=cons_batch,
                        status=status
                    )
                except Exception as e:
                    pass
    
    def update_processes(self, request, batch):
        """Update processes for the batch"""
        processes = request.POST.getlist('process[]')
        
        # Don't clear existing if no new data provided
        if not processes or all(not proc for proc in processes):
            return
            
        # Clear existing processes only if we have new data
        batch.productbatchprocess_set.all().delete()
        
        step_ids = request.POST.getlist('step_id[]')
        descriptions = request.POST.getlist('process_description[]')
        dates = request.POST.getlist('process_date[]')
        
        for i, process_id in enumerate(processes):
            if process_id:
                try:
                    process = Process.objects.get(id=process_id)
                    step_id = step_ids[i] if i < len(step_ids) else 1
                    description = descriptions[i] if i < len(descriptions) else ''
                    date = dates[i] if i < len(dates) else None
                    
                    # Create product batch process relationship
                    ProductBatchProcess.objects.create(
                        product_batch=batch,
                        process=process,
                        step_id=step_id,
                        description=description,
                        date=date
                    )
                except Exception as e:
                    pass
    
    def update_equipment(self, request, batch):
        """Update equipment for the batch"""
        equipment_ids = request.POST.getlist('equipment[]')
        
        # Don't clear existing if no new data provided
        if not equipment_ids or all(not eq for eq in equipment_ids):
            return
            
        # Clear existing equipment only if we have new data
        batch.productbatchequipment_set.all().delete()
        
        for equipment_id in equipment_ids:
            if equipment_id:
                try:
                    equipment = Equipment.objects.get(id=equipment_id)
                    
                    # Create product batch equipment relationship
                    ProductBatchEquipment.objects.create(
                        product_batch=batch,
                        equipment=equipment
                    )
                except Exception as e:
                    pass
    
    def update_acceptance_tests(self, request, batch):
        """Update acceptance tests for the batch"""
        test_ids = request.POST.getlist('acceptance_test[]')
        
        # Don't clear existing if no new data provided
        if not test_ids or all(not test for test in test_ids):
            return
            
        # Clear existing acceptance tests only if we have new data
        batch.productbatchacceptancetest_set.all().delete()
        
        specifications = request.POST.getlist('test_specification[]')
        results = request.POST.getlist('test_result[]')
        dates = request.POST.getlist('test_date[]')
        remarks = request.POST.getlist('test_remarks[]')
        
        for i, test_id in enumerate(test_ids):
            if test_id:
                try:
                    test = AcceptanceTest.objects.get(id=test_id)
                    specification = specifications[i] if i < len(specifications) else ''
                    result = results[i] if i < len(results) else 'pending'
                    date = dates[i] if i < len(dates) else None
                    remark = remarks[i] if i < len(remarks) else ''
                    
                    # Create product batch acceptance test relationship
                    ProductBatchAcceptanceTest.objects.create(
                        product_batch=batch,
                        acceptance_test=test,
                        specification=specification,
                        result=result,
                        test_date=date,
                        remarks=remark
                    )
                except Exception as e:
                    pass
    
    def update_drawings(self, request, batch):
        """Update drawings for the batch"""
        drawing_titles = request.POST.getlist('drawing_title[]')
        
        # Don't clear existing if no new data provided
        if not drawing_titles or all(not title for title in drawing_titles):
            return
            
        # Clear existing drawings only if we have new data
        batch.productbatchdrawing_set.all().delete()
        
        drawing_numbers = request.POST.getlist('drawing_number[]')
        drawing_statuses = request.POST.getlist('drawing_status[]')
        
        for i, title in enumerate(drawing_titles):
            if title:
                try:
                    number = drawing_numbers[i] if i < len(drawing_numbers) else ''
                    status = drawing_statuses[i] if i < len(drawing_statuses) else 'active'
                    
                    # Get or create drawing
                    from qdpc_core_models.models.drawing import Drawing
                    drawing, created = Drawing.objects.get_or_create(
                        drawing_title=title,
                        drawing_number=number,
                        defaults={'drawing_status': status}
                    )
                    
                    # Create product batch drawing relationship
                    ProductBatchDrawing.objects.create(
                        product_batch=batch,
                        drawing=drawing
                    )
                except Exception as e:
                    pass


class ProductBatchApproveView(View):
    def post(self, request, pk):
        try:
            from product.services.approval_service import ProductBatchApprovalService
            
            # Check if user is authenticated
            if not request.user.is_authenticated:
                return JsonResponse({'success': False, 'message': 'Please log in to approve batches.'}, status=401)
            
            # Get the product batch
            batch = get_object_or_404(ProductBatchs, pk=pk)
            
            # Get approval remarks from request
            approval_remarks = request.POST.get('approval_remarks', '')
            
            # Use the approval service to check permissions and approve
            success, message = ProductBatchApprovalService.approve_batch(request.user, batch, approval_remarks)
            
            if success:
                return JsonResponse({
                    'success': True, 
                    'message': message,
                    'batch_status': batch.status,
                    'approved_by': request.user.username,
                    'approval_date': batch.qa_approval_date.isoformat() if batch.qa_approval_date else None,
                    'approval_remarks': batch.approval_remarks
                })
            else:
                return JsonResponse({'success': False, 'message': message}, status=403)
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error approving batch: {str(e)}'}, status=500)


class ProductBatchRejectView(View):
    def post(self, request, pk):
        try:
            from product.services.approval_service import ProductBatchApprovalService
            
            # Check if user is authenticated
            if not request.user.is_authenticated:
                return JsonResponse({'success': False, 'message': 'Please log in to reject batches.'}, status=401)
            
            # Get the product batch
            batch = get_object_or_404(ProductBatchs, pk=pk)
            
            # Get rejection reason from request
            rejection_reason = request.POST.get('rejection_reason', 'No reason provided')
            
            # Use the approval service to check permissions and reject
            success, message = ProductBatchApprovalService.reject_batch(request.user, batch, rejection_reason)
            
            if success:
                return JsonResponse({
                    'success': True, 
                    'message': message,
                    'batch_status': batch.status,
                    'rejected_by': request.user.username,
                    'rejection_date': batch.qa_approval_date.isoformat() if batch.qa_approval_date else None,
                    'rejection_reason': rejection_reason
                })
            else:
                return JsonResponse({'success': False, 'message': message}, status=403)
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error rejecting batch: {str(e)}'}, status=500)
