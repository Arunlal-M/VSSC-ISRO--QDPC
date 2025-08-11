from qdpc.core.modelviewset import BaseModelViewSet
from rest_framework.response import Response
from django.shortcuts import render, redirect
from qdpc_core_models.models.product import Product,Drawing,ProductDocument,ProductDocumentFile
from qdpc_core_models.models.product_category import ProductCategory
from qdpc_core_models.models.division import Division
from qdpc_core_models.models.enduse import EndUse
from qdpc_core_models.models.porcessing_agency import ProcessingAgency
from qdpc_core_models.models.testing_agency import TestingAgency
from qdpc_core_models.models.component import Component
from qdpc_core_models.models.raw_material import RawMaterial
from qdpc_core_models.models.consumable import Consumable
from qdpc_core_models.models.equipment import Equipment
from qdpc_core_models.models.process import Process
from qdpc_core_models.models.acceptance_test import AcceptanceTest
from qdpc_core_models.models.product_acceptence import ProductAcceptanceTest
from qdpc_core_models.models.unit import Unit
from product.serializers.product_serializer import ProductSerializer
from rest_framework import status
from qdpc.core import constants
from qdpc_core_models.models.document_type import DocumentType
import json
import traceback
import sys


class ProductListView(BaseModelViewSet):
    def get(self, request, format=None):
        product_id = request.GET.get('id')
        
        if product_id:
            try:
                # Try to get single product by ID
                product = Product.objects.get(id=int(product_id))
                serilizer=ProductSerializer(product)
                return Response(serilizer.data)            
            except (ValueError, Product.DoesNotExist):
                # Handle invalid ID format or non-existent product
                context = {
                    'error': f"Product with ID {product_id} not found",
                    'product': self.get_all_obj(model_name=Product)
                }
                return render(request, 'product.html', context)
        
        # If no ID specified, return all products
        product = self.get_all_obj(model_name=Product)
        context = {'product': product}
        return render(request, 'product.html', context)
    
class ProductAddView(BaseModelViewSet):

    def get(self, request, format=None):
        category = ProductCategory.objects.all()
        owner = Division.objects.all()
        enduse = EndUse.objects.all()
        processingagency = Division.objects.all()
        testingagency = Division.objects.all()
        components = Component.objects.all()
        rawmaterial = RawMaterial.objects.all()
        consumable = Consumable.objects.all()
        equipment = Equipment.objects.all()
        process = self.get_all_obj(model_name=Process)
        acceptancetest = self.get_all_obj(model_name=AcceptanceTest)
        document_types = DocumentType.objects.all()

        context = {
            'category': category,
            'owner': owner,
            'enduse': enduse,
            'processingagency': processingagency,
            'testingagency': testingagency,
            'components': components,
            'rawmaterial': rawmaterial,
            'consumable': consumable,
            'equipment': equipment,
            'process': process,
            'acceptancetest': acceptancetest,
            'document_types': document_types,
        }

        return render(request, 'productlist.html', context)

    def post(self, request, format=None):        
        serializer = ProductSerializer(data=request.data)
        try:
            if serializer.is_valid():
                validated_data = serializer.validated_data.copy()

                # Set default values
                validated_data['shelf_life_value'] = validated_data.get('shelf_life_value') or 0
                validated_data['batch_size'] = validated_data.get('batch_size') or 0
                validated_data['shelf_life_unit'] = validated_data.get('shelf_life_unit') or 'days'
                validated_data['shelf_life_type'] = validated_data.get('shelf_life_type') or 'tbd'
                validated_data['drawing_applicable'] = validated_data.get('drawing_applicable') or 0

                # Optional FKs
                validated_data['product_owner'] = validated_data.get('product_owner') or None
                validated_data['processing_agencies'] = validated_data.get('processing_agencies') or None
                validated_data['testing_agencies'] = validated_data.get('testing_agencies') or None

                for field in ['components', 'rawmaterial', 'consumable', 'equipment', 'process']:
                    validated_data.pop(field, None)
                validated_data.pop('is_active', None)

                product = Product.objects.create(**validated_data, is_active=True)

                # Set ManyToMany fields
                product.components.set(request.data.getlist('components') or [])
                product.rawmaterial.set(request.data.getlist('raw_material') or [])
                product.consumable.set(request.data.getlist('consumable') or [])
                product.equipment.set(request.data.getlist('equipment') or [])
                product.process.set(request.data.getlist('process') or [])

                # Handle acceptance tests
                if 'acceptance_tests' in request.data:
                    try:
                        acceptance_tests = json.loads(request.data['acceptance_tests'])
                        for test in acceptance_tests:
                            acceptance_test = AcceptanceTest.objects.get(id=test['id'])
                            unit = Unit.objects.get(abbreviation=test['unit_name'])
                            ProductAcceptanceTest.objects.create(
                                product=product,
                                acceptance_test=acceptance_test,
                                min_value=test['min_value'],
                                max_value=test['max_value'],
                                unit=unit
                            )
                    except json.JSONDecodeError:
                        print("Failed to decode acceptance_tests JSON")
                    except AcceptanceTest.DoesNotExist:
                        print(f"AcceptanceTest with id {test['id']} does not exist")

                if validated_data.get('drawing_applicable') == 'yes': 
                    drawings_data = json.loads(request.data.get('drawings', '[]'))
                    for drawing in drawings_data:
                        index = drawing.get('index')
                        file_key = f'drawing_document_{index}'
                        drawing_file = request.FILES.get(file_key)

                        Drawing.objects.create(
                            product=product,
                            drawing_number=drawing.get('drawing_number'),
                            drawing_title=drawing.get('drawing_title'),
                            drawing_status=drawing.get('drawing_status'),
                            drawing_document=drawing_file
                        )                

                    # Handle product documents
                    document_category_id = request.data.get('category')
                    documents_data = request.POST.get('documents')

                    if documents_data:
                        try:
                            documents = json.loads(documents_data)
                            for idx, doc in enumerate(documents):
                                document_instance = ProductDocument.objects.create(
                                    product=product,
                                    product_category_id=doc.get('category'),
                                    title=doc.get('title'),
                                    issue_no=doc.get('issue_no'),
                                    revision_no=doc.get('revision_no'),
                                    release_date=doc.get('release_date'),
                                    approved_by=doc.get('approved_by'),
                                    validity=doc.get('validity') or 0
                                )

                                for file_key, file_obj in request.FILES.items():
                                    if file_key.startswith(f'document_file_{idx}_'):
                                        ProductDocumentFile.objects.create(
                                            document=document_instance,
                                            file=file_obj
                                        )
                        except DocumentType.DoesNotExist:
                            return Response({
                                'success': False,
                                'message': 'Document Category not found'
                            }, status=status.HTTP_404_NOT_FOUND)

                return Response({
                    'success': True,
                    'message': 'Product added successfully!',
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)

            else:
                return Response({
                    'success': False,
                    'message': 'Product add failed.',
                    'data': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(f"Error occurred while adding product: {str(e)}")

            tb = traceback.extract_tb(sys.exc_info()[2])[-1]
            filename = tb.filename
            lineno = tb.lineno
            error_msg = f"An error occurred at {filename}, line {lineno}: {str(e)}"

            return Response({
                'success': False,
                'message': f"An error occurred: {error_msg}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeleteProductView(BaseModelViewSet):
    """
    View to handle the deletion of a source using the POST method.
    """

    def post(self, request, productId, format=None):
        try:
           product= Product.objects.get(name=productId)
           product.delete()
           return Response({
                'success': True,
                'message': constants.PRODUCT_DELETE_SUCCESSFULLY
            }, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Supplier not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
 
 
class UpdateProductStatusView(BaseModelViewSet):
    def post(self, request, productId, format=None): 
        try:
            product = Product.objects.get(name=productId)
            new_status = request.data.get('status')  # Get the status directly from request data
            
            # Convert to boolean if it's not already
            if isinstance(new_status, str):
                new_status = new_status.lower() == 'true'

            product.is_active = new_status  # Update the product's active status
            product.save()

            return Response({
                'success': True,
                'message': 'Product status updated successfully',
                'is_active': product.is_active
            }, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Product not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            
class AddProductDocumentView(BaseModelViewSet):
    def post(self, request, format=None):
        try:
            # Get product ID and document category ID from request data
            product_id = request.data.get('product')
            document_category_id = request.data.get('category')

            # Check if the product and document category are provided
            if not product_id or not document_category_id:
                print(product_id)
                print(document_category_id)
                return Response({
                    'success': False,
                    'message': 'Product and Document Category are required'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Fetch the actual Product and DocumentType objects from the database
            # try:
            #     product = Product.objects.get(name=product_id)  # Uncommented to fetch the Product object
            # except Product.DoesNotExist:
            #     return Response({
            #         'success': False,
            #         'message': 'Product not found'
            #     }, status=status.HTTP_404_NOT_FOUND)

            # try:
            document_category = DocumentType.objects.get(id=document_category_id)
            # except DocumentType.DoesNotExist:
            #     return Response({
            #         'success': False,
            #         'message': 'Document Category not found'
            #     }, status=status.HTTP_404_NOT_FOUND)

            # Create the product document
            document = ProductDocument.objects.create(
                product=product_id,  # Use the actual Product instance
                title=request.data.get('title'),
                document_category=document_category,  # Assign DocumentType instance
                issue_no=request.data.get('issue_no'),
                revision_no=request.data.get('revision_no'),
                release_date=request.data.get('release_date'),
                approved_by=request.data.get('approved_by'),
                document=request.FILES.get('document'),
                validity=request.data.get('validity')
            )

            return Response({
                'success': True,
                'message': 'Product Document added successfully',
                'document_id': document.id
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                'success': False,
                'message': f"An error occurred: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
class ViewProductDetailView(BaseModelViewSet):
    def post(self, request, productId, format=None):
        try:
            product = Product.objects.get(id=productId)
            serializer = ProductSerializer(product)
            data = serializer.data

            # Add FK related names
            data['category'] = {'name': product.category.name if product.category else ''}
            data['product_owner'] = {'name': product.product_owner.name if product.product_owner else ''}
            data['processing_agencies'] = {'name': product.processing_agencies.name if product.processing_agencies else ''}
            data['end_uses'] = {'name': product.end_uses.name if product.end_uses else ''}
            data['testing_agencies'] = {'name': product.testing_agencies.name if product.testing_agencies else ''}

            # Add ManyToMany
            data['components'] = [{'id': c.id, 'name': c.name} for c in product.components.all()]
            data['rawmaterial'] = [{'id': r.id, 'name': r.name} for r in product.rawmaterial.all()]
            data['consumable'] = [{'id': c.id, 'name': c.name} for c in product.consumable.all()]
            data['equipment'] = [{'id': e.id, 'name': e.name} for e in product.equipment.all()]
            data['process'] = [{'id': p.id, 'name': p.process_title} for p in product.process.all()]
            # data['process'] = ['']


            # ✅ Add Drawings
            data['drawings'] = [
            {
                'drawing_number': d.drawing_number,
                'drawing_title': d.drawing_title,
                'drawing_status': d.drawing_status,
                'drawing_document': request.build_absolute_uri(d.drawing_document.url) if d.drawing_document else ''
            }
            for d in product.drawings.all()
        ]


            # ✅ Add Product Documents and their files
            data['documents'] = []
            data['documents'] = [
                {
                    'title': doc.title,
                    'issue_no': doc.issue_no,
                    'revision_no': doc.revision_no,
                    'release_date': doc.release_date,
                    'approved_by': doc.approved_by,
                    'validity': doc.validity,
                    'files': [
                        request.build_absolute_uri(f.file.url)
                        for f in doc.files.all()
                    ]
                }
                for doc in product.documents.all()
            ]


            return Response({
                'success': True,
                'message': "Product data fetched successfully.",
                'data': data
            }, status=status.HTTP_200_OK)

        except Product.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Product not found.'
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            print(f"Error in ViewProductDetailView: {e}")
            tb = traceback.extract_tb(sys.exc_info()[2])[-1]
            filename = tb.filename
            lineno = tb.lineno
            error_msg = f"An error occurred at {filename}, line {lineno}: {str(e)}"
            return Response({
                'success': False,
                'message': error_msg,
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
