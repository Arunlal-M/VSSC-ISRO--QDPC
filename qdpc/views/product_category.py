# views.py
from qdpc.core.modelviewset import BaseModelViewSet
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.http import JsonResponse
from rest_framework import status
from django.views import View
from qdpc_core_models.models.product_category import ProductCategory
from product.serializers.product_category_serializer import ProductCategorySerializer
from qdpc.core import constants


class ProductCategoryView(BaseModelViewSet):
    def get(self, request, format=None):
        productcategory = ProductCategory.objects.all()
        serializer = ProductCategorySerializer(productcategory, many=True)
        context={
            'productcategory': serializer.data,
        }
        print(context)
        return render(request, 'product_category.html',context)     
       
    
    def post(self, request, format=None):
        data = {}
        is_success = False
        message = constants.PRODUCT_CATEGORY_CREATION_FAILED
        status_code = status.HTTP_400_BAD_REQUEST
        serializer = ProductCategorySerializer(data=request.data)

        try:
            if serializer.is_valid():
                serializer.save()
                is_success = True
                status_code = status.HTTP_201_CREATED
                data = serializer.data
                message = constants.PRODUCT_CATEGORY_CREATION_SUCESSFULLY
            else:
                # pass
                is_success = False
                status_code = status.HTTP_400_BAD_REQUEST
                data = serializer.errors
                message = constants.PRODUCT_CATEGORY_CREATION_FAILED


        except Exception as ex:
            is_success = False
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            message = constants.PRODUCT_CATEGORY_CREATION_FAILED

        return self.render_response(data, is_success, message, status_code)


class DeleteProductCategoryView(BaseModelViewSet):
    """
    View to handle the deletion of a source using the POST method.
    """

    def post(self, request, productcategoryId, format=None):
        try:
           productcategory= ProductCategory.objects.get(id=productcategoryId)
           productcategory.delete()
           return Response({
                'success': True,
                'message': constants.PRODUCT_CATEGORY_DELETE_SUCCESSFULLY
            }, status=status.HTTP_200_OK)
        except ProductCategory.DoesNotExist:
            return Response({
                'success': False,
                'message': 'ProductCategory not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    

class EditProductCategoryView(BaseModelViewSet):
    """
    View to handle editing of ProductCategory using the PUT method.
    """
    
    def get(self, request, productcategoryId):
        try:
            productcategory = ProductCategory.objects.get(id=productcategoryId)  # Using filter to allow multiple results
            

            # Create a dictionary to store the data
            data = {
                
                'id': productcategory.id,
                'name': productcategory.name,
                
                
            }
            
            return Response({'data': data}, status=status.HTTP_200_OK)  # Return serialized data
        
        except ProductCategory.DoesNotExist:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request, productcategoryId):
            try:
                productcategory = ProductCategory.objects.get(id=productcategoryId)
            except ProductCategory.DoesNotExist:
                return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

            serializer = ProductCategorySerializer(productcategory, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'success': True,
                    'message': 'ProductCategory updated successfully.',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            
            return Response({
                'success': False,
                'message': 'Validation failed.',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
                     