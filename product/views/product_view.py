from qdpc.core.modelviewset import BaseModelViewSet
from rest_framework.response import Response
from django.shortcuts import render, redirect
from qdpc_core_models.models.product import Product,ProductDocument
from qdpc_core_models.models.product_category import ProductCategory
from qdpc_core_models.models.division import Division
from qdpc_core_models.models.enduse import EndUse
from qdpc_core_models.models.porcessing_agency import ProcessingAgency
from qdpc_core_models.models.testing_agency import TestingAgency
from qdpc_core_models.models.product_component import ProductComponent
from qdpc_core_models.models.raw_material import RawMaterial
from qdpc_core_models.models.consumable import Consumable
from qdpc_core_models.models.equipment import Equipment

from product.serializers.product_serializer import ProductSerializer
from rest_framework import status
from qdpc.core import constants
from qdpc_core_models.models.document_type import DocumentType





class ProductListView(BaseModelViewSet):

    def get(self, request, format=None):
        
       
       
        product = self.get_all_obj(model_name=Product)
        context = {
            'product':product
        }
        return render(request,'product.html',context)
      
   
    
class ProductAddView(BaseModelViewSet):

    def get(self, request, format=None):
        category = self.get_all_obj(model_name=ProductCategory)
        owner = self.get_all_obj(model_name=Division)
        enduse = self.get_all_obj(model_name=EndUse)
        processingagency = self.get_all_obj(model_name=Division)
        testingagency = self.get_all_obj(model_name=Division)
        components = self.get_all_obj(model_name=ProductComponent)
        rawmaterial = self.get_all_obj(model_name=RawMaterial)
        consumable = self.get_all_obj(model_name=Consumable)
        equipment = self.get_all_obj(model_name=Equipment)
        document_types = DocumentType.objects.all()  # Add this line to fetch document types

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
            'document_types': document_types,  # Pass document types to the template
        }

        return render(request, 'productlist.html', context)

    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data)
        try:
            if serializer.is_valid():
                # Saving product instance with validation
                product = serializer.save(is_active=True)

                # Handle file upload and document association if needed
                document_category_id = request.data.get('category')
                document = request.FILES.get('document')

                if document_category_id and document:
                    try:
                        document_category = DocumentType.objects.get(id=document_category_id)
                        ProductDocument.objects.create(
                            product=product,
                            title=request.data.get('title'),
                            document_category=document_category,
                            issue_no=request.data.get('issue_no'),
                            revision_no=request.data.get('revision_no'),
                            release_date=request.data.get('release_date'),
                            approved_by=request.data.get('approved_by'),
                            document=document,
                            validity=request.data.get('validity')
                        )
                    except DocumentType.DoesNotExist:
                        return Response({
                            'success': False,
                            'message': 'Document Category not found'
                        }, status=status.HTTP_404_NOT_FOUND)

                success = True
                message = 'Product added successfully!'
                data = serializer.data
                status_code = status.HTTP_201_CREATED
            else:
                success = False
                message = 'Product add failed.'
                data = serializer.errors
                status_code = status.HTTP_400_BAD_REQUEST

            return self.render_response(data, success, message, status_code)

        except Exception as e:
            # Debugging: Log error and return meaningful message
            print(f"Error occurred while adding product: {str(e)}")
            return Response({
                'success': False,
                'message': f"An error occurred: {str(e)}"
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
