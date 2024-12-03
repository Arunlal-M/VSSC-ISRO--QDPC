from qdpc.core.modelviewset import BaseModelViewSet
from rest_framework.response import Response
from django.shortcuts import render, redirect
from qdpc_core_models.models.product import Product
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





class ProductListView(BaseModelViewSet):

    def get(self, request, format=None):
        
       
       
        product = self.get_all_obj(model_name=Product)
        context = {
            'product':product
        }
        return render(request,'product.html',context)
      
   
    
class ProductAddView(BaseModelViewSet):

    def get(self, request, format=None):

        category= self.get_all_obj(model_name=ProductCategory)
        owner=self.get_all_obj(model_name=Division)
        enduse=self.get_all_obj(model_name=EndUse)
        processingagency=self.get_all_obj(model_name=Division)
        testingagency=self.get_all_obj(model_name=Division)
        components=self.get_all_obj(model_name=ProductComponent)
        rawmaterial=self.get_all_obj(model_name=RawMaterial)
        consumable=self.get_all_obj(model_name=Consumable)
        equipment=self.get_all_obj(model_name=Equipment)
        context={
            'category':category,
             'owner':owner,
             'enduse':enduse,
             'processingagency':processingagency,
             'testingagency': testingagency,
             'components':components,
             'rawmaterial':rawmaterial,
             'consumable':consumable,
             'equipment':equipment,


        }
       
       

        return render(request,'productlist.html',context)
  
    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(is_active=True)
            success = True
            message = 'Product added successfully!'
            data = serializer.data
            status_code = status.HTTP_201_CREATED
        else:
            success = False
            message = 'Product add failed.'
            status_code = status.HTTP_400_BAD_REQUEST
            data = {}
    
        return self.render_response(data, success, message, status_code)
    


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
