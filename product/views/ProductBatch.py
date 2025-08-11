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
from qdpc_core_models.models.process import Process
from qdpc_core_models.models.unit import Unit
# from product.serializers.product_batch_serializer import ProductBatchDetailedSerializer
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
# from .models import *


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
            consumables = Consumable.objects.none()  # or all() if you want default

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
    
class ProductTestSerilizerAPIview(APIView):
    def get(self,request):
        product_id = request.GET.get('product_id')
        if product_id:
            try:
                 product = Product.objects.get(id=product_id)
                 ProductTestserilizer=product.ProductAcceptanceTest.all()
            except product.DoesNotExist:
                return Response
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

        # If raw_material_id provided, fetch test results for that material
    


        return Response({
            'raw_materials': raw_materials_data,
            # 'acceptance_tests': test_data
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
                'file':item['file'],
                'test_id': item['id'],
                'test_name': item['acceptance_test_name'],
                'test_type': 'Qualitative' if item['test_value'] and item['test_value'].isalpha() else 'Quantitative',
                'test_value': item['test_value'],
                'result_remark': item['remark'],
                'unit': '',  # Optional: add unit if needed
                'test_date': now().date().isoformat(),
                'validity_date': '',  # Optional: calculate
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
                drawings = product.drawings.all()  # from related_name
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

        # Serialize equipment
        serializer = EquipmentSerializer(related_equipment, many=True)
        equipment_data = serializer.data

        # Attach document paths
        for equipment in equipment_data:
            equipment_id = equipment['id']
            docs = EquipmentDocument.objects.filter(equipment_id=equipment_id)
            equipment['documents'] = [{
                'id': doc.id,
                'name': doc.title,
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

# all process   
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
            batches = ProductBatchs.objects.select_related('product').all().order_by('-created_at')
            context = {'batches': batches}
            return render(request, 'product_batchlist.html', context)


class ProductBatchAddView(BaseModelViewSet):
    """
    View to add a new product batch.
    """

    def get(self, request):
        # Fetch related data for form dropdowns
        rawmaterial = RawMaterial.objects.all()
        consumable = Consumable.objects.all()
        consumable = self.get_all_obj(model_name=Consumable)
        component = Component.objects.all()
        product=self.get_all_obj(model_name=Product)
        units = self.get_all_obj(model_name=Unit)
        category = ProductCategory.objects.all()     
        processes = Process.objects.all()      
        drawings = Drawing.objects.all()        
        process = self.get_all_obj(model_name=Process) 
        context = {
            'products': product,
            'raw_material': rawmaterial,
            'consumable': consumable,
            'component': component,
            'units': units,
            'processes':processes,
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
                    continue  # Skip malformed entries



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
                    result = request.POST.get(f'result_{test_id}'),
                    date_of_test = request.POST.get(f'date_{test_id}')or None,
                    remarks = request.POST.get(f'remark_{test_id}'),
                    report=files.get(f'report_{test_id}')
                )
            # rawmaterial           

            index = 0
            while True:
                raw_material_key = f'raw_acceptance[{index}][raw_material_id]'
                test_id_key = f'raw_acceptance[{index}][acceptance_test_id]'

                raw_material_id = request.POST.get(raw_material_key)
                test_id = request.POST.get(test_id_key)

                if not raw_material_id or not test_id:
                    break  # Stop if key not found (end of list)

                try:
                    RawmaterialAcceptenceTest.objects.create(
                        product_batch=product_batch,
                        raw_material_id=raw_material_id,
                        acceptance_test_id=test_id
                    )

                   
                except Exception as e:
                    print(f"Error saving raw acceptance test at index {index}:", e)
                    # You could log or collect error details here

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
        print("PRoduct batch hit")
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
        # product_tests = ProductAcceptanceTest.objects.filter(product=product)
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
                'test_date': now().date().isoformat(),  # If dynamic date needed, change here
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
            'rawmaterial_section': rawmaterial_tests_final,  # For table rendering
            'product_tests': product_test_table,  # ✅ Pass this to template

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
        raw_materials = batch.productbatchrawmaterial_set.select_related('raw_material').all()

       
        return render(request, 'prductbatchview.html', {
            'batch': batch,
            'raw_materials': raw_materials,
            'components': components,
            'consumables': consumables,
            'processes': processes,
            'drawings': drawings,
            'equipment': equipment,
            'acceptance_tests': tests,
            # 'rawmaterial_tests': rawmaterial_tests_data,

        })