from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from qdpc.core.modelviewset import BaseModelViewSet
from qdpc_core_models.models.product_batchlist import ProductBatch
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
from qdpc_core_models.models.productBatch import *
from django.views import View
import json
from product.models import DynamicTable, DynamicTableRow
from django.db import models
from django.core.paginator import Paginator


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
                serializer = ProcessSerilalizers(related_processes, many=True)
                return Response(serializer.data)
            except Product.DoesNotExist:
                return Response({'error': 'Product not found'}, status=404)
        return Response({'error': 'Product ID is required'}, status=400)


class ProductBatchFetchView(BaseModelViewSet):
    def get(self, request, pk=None):
        data = {}
        success = False
        message = constants.USER_FETCH_FAILED
        status_code = status.HTTP_403_FORBIDDEN

        if pk:
            try:
                success, status_code, data, message = ProductService.get_product_batch_detail(pk)
                context = {'batches': data}
                return render(request, 'product_batchlist.html', context)
            except Exception as ex:
                return self.render_response(data, success, message, status.HTTP_400_BAD_REQUEST)
        else:
            try:
                # Get basic parameters
                page_number = request.GET.get('page', 1)
                page_size = 25
                
                # Get product batches
                batches = ProductBatchs.objects.all().order_by('-created_at')
                
                # Basic pagination
                paginator = Paginator(batches, page_size)
                page_obj = paginator.get_page(page_number)
                
                # Load proper approval permissions for the user
                try:
                    from product.services.approval_service import ProductBatchApprovalService
                    approval_permissions = ProductBatchApprovalService.get_user_approval_permissions(request.user)
                except Exception as e:
                    # Fallback permissions based on user groups and Django permissions
                    approval_permissions = {
                        'user_roles': [group.name for group in request.user.groups.all()],
                        'approval_level': 'user',
                        'can_approve_product_batch': request.user.has_perm('qdpc_core_models.approve_productbatch') or request.user.is_superuser,
                        'can_reject_product_batch': request.user.has_perm('qdpc_core_models.reject_productbatch') or request.user.is_superuser,
                        'explanation': 'Permissions loaded from user groups and Django permissions'
                    }
                
                context = {
                    'batches': page_obj,
                    'approval_permissions': approval_permissions,
                    'page_obj': page_obj,
                    'is_paginated': paginator.num_pages > 1,
                    'page_range': paginator.get_elided_page_range(page_obj.number, on_each_side=2, on_ends=1),
                    'search_query': '',
                    'status_filter': '',
                    'total_count': paginator.count,
                    'status_choices': ProductBatchs.STATUS_CHOICES
                }
                

                
                return render(request, 'product_batchlist.html', context)
                
            except Exception as e:
                print(f"DEBUG: Error in ProductBatchFetchView: {e}")
                import traceback
                traceback.print_exc()
                # Return a simple error context
                context = {
                    'batches': [],
                    'approval_permissions': {
                        'user_roles': [],
                        'approval_level': 'none',
                        'can_approve_product_batch': False,
                        'can_reject_product_batch': False,
                        'explanation': f'Error loading data: {str(e)}'
                    },
                    'page_obj': None,
                    'is_paginated': False,
                    'page_range': [],
                    'search_query': '',
                    'status_filter': '',
                    'total_count': 0,
                    'status_choices': ProductBatchs.STATUS_CHOICES
                }
                return render(request, 'product_batchlist.html', context)


class ProductBatchQARReportView(BaseModelViewSet):
    """View for downloading QAR (Quality Assurance Report) for approved product batches"""
    
    def get(self, request, batch_id):
        try:
            # Get the product batch
            batch = ProductBatchs.objects.get(id=batch_id)
            
            # Check if batch is approved
            if batch.status != 'approved':
                return Response({
                    'error': 'QAR Report can only be generated for approved batches'
                }, status=400)
            
            # Check if user has permission to download QAR reports
            if not (request.user.has_perm('qdpc_core_models.view_productbatch') or 
                   request.user.has_perm('product.view_productbatch') or 
                   request.user.is_superuser):
                return Response({
                    'error': 'You do not have permission to download QAR reports'
                }, status=403)
            
            # Generate QAR report content
            from django.http import HttpResponse
            
            # Create a simple text report (you can enhance this to generate PDF or other formats)
            report_content = f"""
QUALITY ASSURANCE REPORT
========================

Product Batch ID: {batch.batch_id}
Product: {batch.product.name if batch.product else 'N/A'}
Manufacturing Start: {batch.manufacturing_start}
Manufacturing End: {batch.manufacturing_end}
Status: {batch.status}
Approved By: {batch.qa_approved_by.username if batch.qa_approved_by else 'N/A'}
Approval Date: {batch.qa_approval_date.strftime('%Y-%m-%d %H:%M') if batch.qa_approval_date else 'N/A'}

Approval Remarks: {batch.approval_remarks if batch.approval_remarks else 'None'}

This document certifies that the product batch has been approved by Quality Assurance and meets all required standards.

Generated on: {now().strftime('%Y-%m-%d %H:%M:%S')}
            """.strip()
            
            # Create the HTTP response
            response = HttpResponse(content_type='text/plain')
            response['Content-Disposition'] = f'attachment; filename="QAR_Report_Batch_{batch.batch_id}.txt"'
            response.write(report_content)
            
            return response
            
        except ProductBatchs.DoesNotExist:
            return Response({
                'error': 'Product batch not found'
            }, status=404)
        except Exception as e:
            return Response({
                'error': f'Error generating QAR report: {str(e)}'
            }, status=500)


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

            # Raw Materials                     
            for raw_json in request.POST.getlist('raw_materials[]'):
                try:
                    raw_data = json.loads(raw_json)
                    raw_id = raw_data.get('raw_material_id')
                    batch_id = raw_data.get('batch_id')

                    if raw_id and batch_id:
                        try:
                            batch_instance = RawMaterialBatch.objects.get(pk=batch_id)
                        except RawMaterialBatch.DoesNotExist:
                            continue 
                        ProductBatchRawMaterial.objects.create(
                            product_batch=product_batch,
                            raw_material_id=raw_id,
                            batch=batch_instance, 
                            status='status'
                        )
                except (json.JSONDecodeError, KeyError, TypeError):
                    continue

            # Components
            for comp_json in data.getlist('components[]'):
                try:
                    comp_data = json.loads(comp_json)
                    ProductBatchComponent.objects.create(
                        product_batch=product_batch,
                        component_id=comp_data['component_id'],
                        batch=comp_data['batch_id'],
                        status=""
                    )
                except Exception as e:
                    return Response({
                        'success': False,
                        'error': f"Component save failed: {str(e)}"
                    }, status=status.HTTP_400_BAD_REQUEST)

            # Consumables
            for con_json in data.getlist('consumables[]'):
                try:
                    con_data = json.loads(con_json)
                    ProductBatchConsumable.objects.create(
                        product_batch=product_batch,
                        consumable_id=con_data['consumable_id'],
                        batch=con_data['batch_id'],
                        status=con_data['status']
                    )
                except Exception as e:
                    return Response({
                        'success': False,
                        'error': f"Consumable save failed: {str(e)}"
                    }, status=status.HTTP_400_BAD_REQUEST)

            # Drawings
            for draw_id in data.getlist('drawings[]'):
                ProductBatchDrawing.objects.create(
                    product_batch=product_batch,
                    drawing_id=draw_id
                )

            # Processes
            for proc_id in data.getlist('processes[]'):
                ProductBatchProcess.objects.create(
                    product_batch=product_batch,
                    process_id=proc_id
                )

            # Equipment
            for eq_id in data.getlist('equipment[]'):
                ProductBatchEquipment.objects.create(
                    product_batch=product_batch,
                    equipment_id=eq_id
                )

            # Product Acceptance Tests
            test_ids = request.POST.getlist('acceptance_tests[]')
            print("Received Test IDs:", test_ids) 
            for test_id in data.getlist('acceptance_tests[]'):               
                ProductBatchAcceptanceTest.objects.create(
                    product_batch=product_batch,
                    acceptance_test_id=test_id,
                    result=request.POST.get(f'result_{test_id}'),
                    date_of_test=request.POST.get(f'date_{test_id}') or None,
                    remarks=request.POST.get(f'remark_{test_id}'),
                    report=files.get(f'report_{test_id}')
                )

            # Raw material acceptance tests
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
                    print(f"Error saving raw acceptance test at index {index}:", e)

                index += 1
            
            save_dynamic_tables(request, product_batch.id)    
            return Response({'message': 'Product batch created successfully.'}, status=status.HTTP_201_CREATED)

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

        return Response({'success': True})
    return Response({'error': 'Invalid request'}, status=400)


class ProductBatchDetailView(BaseModelViewSet):
    def get(self, request, batch_id):
        print("Product batch hit")
        try:
            batch = ProductBatch.objects.get(id=batch_id)
        except ProductBatch.DoesNotExist:
            return Response({"error": "Product batch not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductBatchDetailedSerializer(batch)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductBatchDeleteView(APIView):
    def post(self, request, pk):
        try:
            batch = get_object_or_404(ProductBatchs, pk=pk)

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
        
        # Debug: Check if there are any processes and process steps
        print(f"DEBUG: Found {processes.count()} processes for this batch")
        
        for process_batch in processes:
            process = process_batch.process
            print(f"DEBUG: Processing process: {process.process_title} (ID: {process.id})")
            
            # Get all process steps for this process
            process_steps = ProcessStep.objects.filter(process=process).order_by('step_id')
            print(f"DEBUG: Found {process_steps.count()} process steps for process {process.process_title}")
            
            # Debug: Print each step
            for step in process_steps:
                print(f"DEBUG: Step {step.step_id}: {step.process_description}")
            
            process_data = {
                'process': process,
                'steps': process_steps
            }
            process_steps_data.append(process_data)
        
        # Debug: Check all processes and steps in the system
        all_processes = Process.objects.all()
        print(f"DEBUG: Total processes in system: {all_processes.count()}")
        for proc in all_processes:
            steps = ProcessStep.objects.filter(process=proc)
            print(f"DEBUG: Process '{proc.process_title}' has {steps.count()} steps")

        return render(request, 'prductbatchview.html', {
            'batch': batch,
            'raw_materials': raw_materials,
            'components': components,
            'consumables': consumables,
            'processes': processes,
            'process_steps_data': process_steps_data,
            'drawings': drawings,
            'equipment': equipment,
            'acceptance_tests': tests,
        })


class ProductBatchApproveView(APIView):
    def post(self, request, pk):
        """Approve a product batch - only accessible by QA roles"""
        try:
            # Check if user has QA role
            user_groups = request.user.groups.all()
            qa_roles = [
                'Division Head QA',
                'Section Head QA', 
                'Engineer QA',
                'Technical/Scientific staff QA'
            ]
            
            user_has_qa_role = any(group.name in qa_roles for group in user_groups)
            
            if not user_has_qa_role:
                return Response({
                    'success': False,
                    'message': 'Access denied. Only QA roles can approve product batches.'
                }, status=status.HTTP_403_FORBIDDEN)
            
            # Get the product batch
            try:
                batch = ProductBatchs.objects.get(id=pk)
            except ProductBatchs.DoesNotExist:
                return Response({
                    'success': False,
                    'message': 'Product batch not found.'
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Check if batch is already approved
            if hasattr(batch, 'status') and batch.status == 'approved':
                return Response({
                    'success': False,
                    'message': 'Product batch is already approved.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Approve the batch
            if hasattr(batch, 'status'):
                batch.status = 'approved'
            if hasattr(batch, 'qa_approval_date'):
                batch.qa_approval_date = now()
            if hasattr(batch, 'qa_approved_by'):
                batch.qa_approved_by = request.user
            
            batch.save()
            
            return Response({
                'success': True,
                'message': 'Product batch approved successfully.',
                'batch_id': batch.batch_id
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error approving batch: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductBatchQAApprovalView(BaseModelViewSet):
    """QA Approval page for product batches - readonly view with approve/reject actions"""
    
    def get(self, request, batch_id):
        """Display the QA approval page with readonly batch details"""
        try:
            # Check if user has QA role
            user_groups = request.user.groups.all()
            qa_roles = [
                'Division Head QA',
                'Section Head QA', 
                'Engineer QA',
                'Technical/Scientific staff QA'
            ]
            
            user_has_qa_role = any(group.name in qa_roles for group in user_groups)
            
            if not user_has_qa_role:
                return Response({
                    'success': False,
                    'message': 'Access denied. Only QA roles can access this page.'
                }, status=status.HTTP_403_FORBIDDEN)
            
            # Get the product batch with all related data
            try:
                batch = ProductBatchs.objects.select_related('product').get(id=batch_id)
            except ProductBatchs.DoesNotExist:
                return Response({
                    'success': False,
                    'message': 'Product batch not found.'
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Check if batch is already processed
            if hasattr(batch, 'status') and batch.status in ['approved', 'rejected']:
                return Response({
                    'success': False,
                    'message': f'Product batch is already {batch.status}.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Get related data for display
            raw_materials = batch.productbatchrawmaterial_set.select_related('raw_material').all()
            components = batch.productbatchcomponent_set.select_related('component').all()
            consumables = batch.productbatchconsumable_set.select_related('consumable').all()
            processes = batch.productbatchprocess_set.select_related('process').all()
            drawings = batch.productbatchdrawing_set.select_related('drawing').all()
            equipment = batch.productbatchequipment_set.select_related('equipment').all()
            tests = batch.productbatchacceptancetest_set.select_related('acceptance_test').all()
            
            context = {
                'batch': batch,
                'raw_materials': raw_materials,
                'components': components,
                'consumables': consumables,
                'processes': processes,
                'drawings': drawings,
                'equipment': equipment,
                'acceptance_tests': tests,
                'user_role': request.user.groups.first().name if request.user.groups.exists() else None
            }
            
            return render(request, 'product_batch_qa_approval.html', context)
            
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error loading batch: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request, batch_id):
        """Handle approve/reject action with remarks"""
        try:
            # Check if user has QA role
            user_groups = request.user.groups.all()
            qa_roles = [
                'Division Head QA',
                'Section Head QA', 
                'Engineer QA',
                'Technical/Scientific staff QA'
            ]
            
            user_has_qa_role = any(group.name in qa_roles for group in user_groups)
            
            if not user_has_qa_role:
                return Response({
                    'success': False,
                    'message': 'Access denied. Only QA roles can approve/reject product batches.'
                }, status=status.HTTP_403_FORBIDDEN)
            
            # Get the product batch
            try:
                batch = ProductBatchs.objects.get(id=batch_id)
            except ProductBatchs.DoesNotExist:
                return Response({
                    'success': False,
                    'message': 'Product batch not found.'
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Check if batch is already processed
            if hasattr(batch, 'status') and batch.status in ['approved', 'rejected']:
                return Response({
                    'success': False,
                    'message': f'Product batch is already {batch.status}.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Get action and remarks from request
            action = request.data.get('action')  # 'approve' or 'reject'
            remarks = request.data.get('remarks', '')
            
            if action not in ['approve', 'reject']:
                return Response({
                    'success': False,
                    'message': 'Invalid action. Must be "approve" or "reject".'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Update batch status and store approval/rejection data
            if hasattr(batch, 'status'):
                batch.status = action
            if hasattr(batch, 'qa_approval_date'):
                batch.qa_approval_date = now()
            if hasattr(batch, 'qa_approved_by'):
                batch.qa_approved_by = request.user
            if hasattr(batch, 'rejection_reason') and action == 'rejected':
                batch.rejection_reason = remarks
            
            batch.save()
            
            # Store approval/rejection record in database
            # You can create a separate model for this if needed
            # For now, we'll use the existing fields
            
            return Response({
                'success': True,
                'message': f'Product batch {action}d successfully.',
                'batch_id': batch.batch_id,
                'action': action,
                'remarks': remarks,
                'qa_user': request.user.username,
                'qa_date': now().isoformat()
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error processing batch: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SubmitToSectionView(APIView):
    """Handle submission from Engineer QA and Technical/Scientific staff QA to Section Head QA"""
    
    def post(self, request, batch_id):
        try:
            # Check if user has appropriate role
            user_groups = request.user.groups.all()
            user_role = user_groups.first().name if user_groups.exists() else None
            
            if user_role not in ['Engineer QA', 'Technical/Scientific staff QA']:
                return Response({
                    'success': False,
                    'message': 'Access denied. Only Engineer QA and Technical/Scientific staff QA can submit to Section Head.'
                }, status=status.HTTP_403_FORBIDDEN)
            
            # Get the product batch
            try:
                batch = ProductBatchs.objects.get(id=batch_id)
            except ProductBatchs.DoesNotExist:
                return Response({
                    'success': False,
                    'message': 'Product batch not found.'
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Update batch with submission details
            batch.submitted_by_role = user_role
            batch.submitted_by_user = request.user
            batch.submitted_date = now()
            batch.save()
            
            return Response({
                'success': True,
                'message': f'Product batch submitted to Section Head QA successfully.',
                'batch_id': batch.batch_id,
                'submitted_by': request.user.username,
                'submitted_role': user_role,
                'submitted_date': now().isoformat()
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error submitting batch: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SubmitToDivisionView(APIView):
    """Handle submission from Section Head QA to Division Head QA"""
    
    def post(self, request, batch_id):
        try:
            # Check if user has Section Head QA role
            user_groups = request.user.groups.all()
            user_role = user_groups.first().name if user_groups.exists() else None
            
            if user_role != 'Section Head QA':
                return Response({
                    'success': False,
                    'message': 'Access denied. Only Section Head QA can submit to Division Head QA.'
                }, status=status.HTTP_403_FORBIDDEN)
            
            # Get the product batch
            try:
                batch = ProductBatchs.objects.get(id=batch_id)
            except ProductBatchs.DoesNotExist:
                return Response({
                    'success': False,
                    'message': 'Product batch not found.'
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Update batch with submission details
            batch.submitted_by_role = user_role
            batch.submitted_by_user = request.user
            batch.submitted_date = now()
            batch.save()
            
            return Response({
                'success': True,
                'message': f'Product batch submitted to Division Head QA successfully.',
                'batch_id': batch.batch_id,
                'submitted_by': request.user.username,
                'submitted_role': user_role,
                'submitted_date': now().isoformat()
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error submitting batch: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RejectBatchView(APIView):
    """Handle rejection from Section Head QA to Engineer QA and Technical/Scientific staff QA"""
    
    def post(self, request, batch_id):
        try:
            # Check if user has Section Head QA role
            user_groups = request.user.groups.all()
            user_role = user_groups.first().name if user_groups.exists() else None
            
            if user_role != 'Section Head QA':
                return Response({
                    'success': False,
                    'message': 'Access denied. Only Section Head QA can reject batches.'
                }, status=status.HTTP_403_FORBIDDEN)
            
            # Get the product batch
            try:
                batch = ProductBatchs.objects.get(id=batch_id)
            except ProductBatchs.DoesNotExist:
                return Response({
                    'success': False,
                    'message': 'Product batch not found.'
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Get rejection remarks
            remarks = request.data.get('remarks', '')
            if not remarks:
                return Response({
                    'success': False,
                    'message': 'Rejection remarks are required.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Update batch with rejection details
            batch.status = 'rejected'
            batch.rejection_reason = remarks
            batch.qa_approval_date = now()
            batch.qa_approved_by = request.user
            batch.save()
            
            return Response({
                'success': True,
                'message': f'Product batch rejected successfully.',
                'batch_id': batch.batch_id,
                'rejected_by': request.user.username,
                'rejection_reason': remarks,
                'rejection_date': now().isoformat()
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error rejecting batch: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
