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
import os
import json
import traceback
import sys
from django.conf import settings


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
        # Pre-validate form data to catch common issues
        def validate_form_data(data):
            """Validate form data before serialization"""
            errors = []
            
            # Check for placeholder text in select fields
            select_fields = ['components', 'raw_material', 'consumable', 'equipment', 'process']
            for field in select_fields:
                field_data = data.getlist(field) if hasattr(data, 'getlist') else data.get(field, [])
                if isinstance(field_data, list):
                    for item in field_data:
                        if item and isinstance(item, str) and item.startswith('Choose'):
                            errors.append(f"Please select a valid {field.replace('_', ' ')} instead of '{item}'")
            
            # Check for empty required fields
            required_fields = ['name', 'category', 'product_owner']
            for field in required_fields:
                if not data.get(field):
                    errors.append(f"{field.replace('_', ' ').title()} is required")
            
            return errors
        
        # Validate form data first
        validation_errors = validate_form_data(request.data)
        if validation_errors:
            return Response({
                'success': False,
                'message': 'Validation failed',
                'data': validation_errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
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

                # Set ManyToMany fields with proper filtering
                def clean_many_to_many_data(data_list):
                    """Filter out empty strings and placeholder text from many-to-many data"""
                    if not data_list:
                        return []
                    return [item for item in data_list if item and item.strip() and not item.startswith('Choose')]
                
                product.components.set(clean_many_to_many_data(request.data.getlist('components')))
                product.rawmaterial.set(clean_many_to_many_data(request.data.getlist('raw_material')))
                product.consumable.set(clean_many_to_many_data(request.data.getlist('consumable')))
                product.equipment.set(clean_many_to_many_data(request.data.getlist('equipment')))
                product.process.set(clean_many_to_many_data(request.data.getlist('process')))

                # Handle acceptance tests
                if 'acceptance_tests' in request.data:
                    try:
                        acceptance_tests = json.loads(request.data['acceptance_tests'])
                        for test in acceptance_tests:
                            # Validate test data before processing
                            if not test.get('id') or not test.get('unit_name'):
                                print(f"Skipping invalid acceptance test: {test}")
                                continue
                                
                            try:
                                acceptance_test = AcceptanceTest.objects.get(id=test['id'])
                                unit = Unit.objects.get(abbreviation=test['unit_name'])
                                ProductAcceptanceTest.objects.create(
                                    product=product,
                                    acceptance_test=acceptance_test,
                                    min_value=test.get('min_value'),
                                    max_value=test.get('max_value'),
                                    unit=unit
                                )
                            except AcceptanceTest.DoesNotExist:
                                print(f"AcceptanceTest with id {test['id']} does not exist")
                            except Unit.DoesNotExist:
                                print(f"Unit with abbreviation {test['unit_name']} does not exist")
                            except Exception as e:
                                print(f"Error creating ProductAcceptanceTest: {e}")
                    except json.JSONDecodeError:
                        print("Failed to decode acceptance_tests JSON")
                    except Exception as e:
                        print(f"Unexpected error processing acceptance tests: {e}")

                if validated_data.get('drawing_applicable') == 'yes': 
                    try:
                        drawings_data = json.loads(request.data.get('drawings', '[]'))
                        for drawing in drawings_data:
                            # Validate drawing data
                            if not drawing.get('drawing_number') or not drawing.get('drawing_title'):
                                print(f"Skipping invalid drawing: {drawing}")
                                continue
                                
                            index = drawing.get('index')
                            file_key = f'drawing_document_{index}'
                            drawing_file = request.FILES.get(file_key)

                            try:
                                Drawing.objects.create(
                                    product=product,
                                    drawing_number=drawing.get('drawing_number'),
                                    drawing_title=drawing.get('drawing_title'),
                                    drawing_status=drawing.get('drawing_status'),
                                    drawing_document=drawing_file
                                )
                            except Exception as e:
                                print(f"Error creating Drawing: {e}")
                    except json.JSONDecodeError:
                        print("Failed to decode drawings JSON")
                    except Exception as e:
                        print(f"Unexpected error processing drawings: {e}")                

                    # Handle product documents
                    document_category_id = request.data.get('category')
                    documents_data = request.POST.get('documents')

                    if documents_data:
                        try:
                            documents = json.loads(documents_data)
                            for idx, doc in enumerate(documents):
                                # Validate document data
                                if not doc.get('title') or not doc.get('category'):
                                    print(f"Skipping invalid document: {doc}")
                                    continue
                                
                                try:
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
                                            try:
                                                ProductDocumentFile.objects.create(
                                                    document=document_instance,
                                                    file=file_obj
                                                )
                                            except Exception as e:
                                                print(f"Error creating ProductDocumentFile: {e}")
                                except Exception as e:
                                    print(f"Error creating ProductDocument: {e}")
                        except json.JSONDecodeError:
                            print("Failed to decode documents JSON")
                        except Exception as e:
                            print(f"Unexpected error processing documents: {e}")

                return Response({
                    'success': True,
                    'message': 'Product added successfully!',
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)

            else:
                # Provide more user-friendly error messages
                error_messages = []
                for field, errors in serializer.errors.items():
                    if field == 'non_field_errors':
                        error_messages.extend(errors)
                    else:
                        field_name = field.replace('_', ' ').title()
                        for error in errors:
                            error_messages.append(f"{field_name}: {error}")
                
                return Response({
                    'success': False,
                    'message': 'Product add failed. Please check the following errors:',
                    'data': error_messages
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(f"Error occurred while adding product: {str(e)}")
            
            # Provide user-friendly error message
            if "Field 'id' expected a number but got" in str(e):
                error_message = "Invalid selection detected. Please ensure all dropdown fields have valid selections."
            elif "does not exist" in str(e):
                error_message = "One or more selected items no longer exist. Please refresh and try again."
            else:
                error_message = "An unexpected error occurred while adding the product. Please try again."

            return Response({
                'success': False,
                'message': error_message,
                'debug_info': str(e) if settings.DEBUG else None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeleteProductView(BaseModelViewSet):
    """Delete a product by ID using POST."""

    def post(self, request, productId, format=None):
        try:
            product = Product.objects.get(id=int(productId))
            product.delete()
            return Response({
                'success': True,
                'message': constants.PRODUCT_DELETE_SUCCESSFULLY
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
 
 
class UpdateProductStatusView(BaseModelViewSet):
    def post(self, request, productId, format=None):
        try:
            product = Product.objects.get(id=int(productId))
            new_status = request.data.get('status')

            if isinstance(new_status, str):
                new_status = new_status.lower() == 'true'

            product.is_active = bool(new_status)
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

class ProductUpdateView(BaseModelViewSet):
    """Edit a product by ID (GET renders form, POST updates)."""

    def get(self, request, productId, format=None):
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
            'product_id': productId,
        }

        return render(request, 'product_edit.html', context)

    def post(self, request, productId, format=None):
        try:
            product = Product.objects.get(id=int(productId))

            # Make a mutable copy and sanitize inputs
            incoming_data = request.data.copy()

            # If shelf life is not duration-based, don't validate value/unit
            shelf_type = incoming_data.get('shelf_life_type')
            if shelf_type in ['not_applicable', 'tbd', '', None]:
                incoming_data.pop('shelf_life_value', None)
                incoming_data.pop('shelf_life_unit', None)
            else:
                # Normalize empty strings to None for numeric
                if incoming_data.get('shelf_life_value') in ['', 'null', 'undefined', None]:
                    incoming_data['shelf_life_value'] = None

            # Drop empty optional fields to avoid overriding
            for key in ['specific_use', 'processing_agencies', 'testing_agencies', 'end_uses']:
                if incoming_data.get(key) in ['', 'null', 'undefined', None]:
                    incoming_data.pop(key, None)

            serializer = ProductSerializer(product, data=incoming_data, partial=True)
            if serializer.is_valid():
                validated_data = serializer.validated_data.copy()

                # Defaults and optional FKs
                if 'shelf_life_type' in validated_data and validated_data['shelf_life_type'] in ['not_applicable', 'tbd']:
                    validated_data['shelf_life_value'] = None
                    validated_data['shelf_life_unit'] = None

                for field in ['components', 'rawmaterial', 'consumable', 'equipment', 'process']:
                    validated_data.pop(field, None)

                # Save simple fields
                for attr, value in serializer.validated_data.items():
                    if attr not in ['components', 'rawmaterial', 'consumable', 'equipment', 'process', 'drawings']:
                        setattr(product, attr, value)
                product.save()

                # Update M2M fields only if keys are present in request
                if hasattr(request, 'POST') or hasattr(request, 'data'):
                    qd = getattr(request, 'POST', None) or request.data
                    if 'components' in qd:
                        product.components.set(qd.getlist('components'))
                    if 'raw_material' in qd:
                        product.rawmaterial.set(qd.getlist('raw_material'))
                    if 'consumable' in qd:
                        product.consumable.set(qd.getlist('consumable'))
                    if 'equipment' in qd:
                        product.equipment.set(qd.getlist('equipment'))
                    if 'process' in qd:
                        product.process.set(qd.getlist('process'))

                # Update drawings if provided
                if 'drawings' in request.data or 'drawings' in incoming_data:
                    try:
                        drawings_data = json.loads(incoming_data.get('drawings', '[]'))
                        product.drawings.all().delete()
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
                    except json.JSONDecodeError:
                        pass

                # Update documents if provided
                documents_json = request.POST.get('documents') or incoming_data.get('documents')
                if documents_json:
                    try:
                        documents_data = json.loads(documents_json)
                        # Remove existing and recreate from payload
                        product.documents.all().delete()
                        for idx, doc in enumerate(documents_data):
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

                            # Attach uploaded files following key pattern document_file_{idx}_<n>
                            for file_key, file_obj in request.FILES.items():
                                if file_key.startswith(f'document_file_{idx}_'):
                                    ProductDocumentFile.objects.create(
                                        document=document_instance,
                                        file=file_obj
                                    )
                    except json.JSONDecodeError:
                        pass

                return Response({
                    'success': True,
                    'message': 'Product updated successfully',
                }, status=status.HTTP_200_OK)

            return Response({
                'success': False,
                'message': 'Validation failed',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
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
            data['category'] = {
                'id': product.category.id if product.category else None,
                'name': product.category.name if product.category else ''
            }
            data['product_owner'] = {
                'id': product.product_owner.id if product.product_owner else None,
                'name': product.product_owner.name if product.product_owner else ''
            }
            data['processing_agencies'] = {
                'id': product.processing_agencies.id if product.processing_agencies else None,
                'name': product.processing_agencies.name if product.processing_agencies else ''
            }
            data['end_uses'] = {
                'id': product.end_uses.id if product.end_uses else None,
                'name': product.end_uses.name if product.end_uses else ''
            }
            data['testing_agencies'] = {
                'id': product.testing_agencies.id if product.testing_agencies else None,
                'name': product.testing_agencies.name if product.testing_agencies else ''
            }

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


            # ✅ Add Product Documents and their files (with URLs and names)
            documents_payload = []
            for doc in product.documents.all():
                files_payload = []
                for f in doc.files.all():
                    try:
                        file_url = request.build_absolute_uri(f.file.url) if f.file else ''
                        file_name = os.path.basename(f.file.name) if f.file else ''
                    except Exception:
                        file_url = ''
                        file_name = ''
                    files_payload.append({
                        'file_url': file_url,
                        'file_name': file_name,
                    })

                documents_payload.append({
                    'title': doc.title,
                    'category': doc.product_category.name if getattr(doc, 'product_category', None) else '',
                    'category_id': doc.product_category.id if getattr(doc, 'product_category', None) else None,
                    'issue_no': doc.issue_no,
                    'revision_no': doc.revision_no,
                    'release_date': doc.release_date,
                    'approved_by': doc.approved_by,
                    'validity': doc.validity,
                    'files': files_payload,
                })

            data['documents'] = documents_payload


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
