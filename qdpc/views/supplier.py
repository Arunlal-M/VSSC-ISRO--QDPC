from qdpc.core.modelviewset import BaseModelViewSet
from rest_framework.response import Response
from django.shortcuts import render,redirect
from qdpc_core_models.models.supplier import Suppliers
from product.serializers.supplier_serializer import SuppliersSerializer
from rest_framework import status
from qdpc.core import constants

class SupplierListView(BaseModelViewSet):
    def get(self, request, format=None):
        suppliers = Suppliers.objects.all()
        serializer = SuppliersSerializer(suppliers, many=True)
        context={
            'suppliers':serializer.data
        }
        print(context)
        return render(request, 'supplier.html',context)     
       
    
    def post(self, request, format=None):
        data = {}
        print(request.data)
        is_success = False
        message = constants.SUPPLIER_CREATION_FAILED
        status_code = status.HTTP_400_BAD_REQUEST
        serializer = SuppliersSerializer(data=request.data)

        try:
            if serializer.is_valid():
                serializer.save()
                is_success = True
                status_code = status.HTTP_201_CREATED
                data = serializer.data
                message = constants.SUPPLIER_CREATION_SUCESSFULLY
            else:
                # pass
                is_success = False
                status_code = status.HTTP_400_BAD_REQUEST
                data = serializer.errors
                message = constants.SUPPLIER_CREATION_FAILED


        except Exception as ex:
            is_success = False
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            message = constants.SUPPLIER_CREATION_FAILED

        return self.render_response(data, is_success, message, status_code)


class DeleteSupplierView(BaseModelViewSet):
    """
    View to handle the deletion of a source using the POST method.
    """

    def post(self, request, supplierId, format=None):
        try:
           supplier= Suppliers.objects.get(id=supplierId)
           supplier.delete()
           return Response({
                'success': True,
                'message': constants.SUPPLIER_DELETE_SUCCESSFULLY
            }, status=status.HTTP_200_OK)
        except Suppliers.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Supplier not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  

class EditSupplierView(BaseModelViewSet):
    """
    View to handle editing of source using the PUT method.
    """
    
    def get(self, request, supplierId):
        try:
            suppliers = Suppliers.objects.get(id=supplierId)  # Using filter to allow multiple results
            

            # Create a dictionary to store the data
            data = {
                
                'id': suppliers.id,
                'name': suppliers.name,
                'email': suppliers.email,
                'address': suppliers.address,
            }
            
            return Response({'data': data}, status=status.HTTP_200_OK)  # Return serialized data
        
        except Suppliers.DoesNotExist:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request, supplierId):
            try:
                suppliers = Suppliers.objects.get(id=supplierId)
            except Suppliers.DoesNotExist:
                return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

            serializer = SuppliersSerializer(suppliers, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'success': True,
                    'message': 'Suppliers updated successfully.',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            
            return Response({
                'success': False,
                'message': 'Validation failed.',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
  