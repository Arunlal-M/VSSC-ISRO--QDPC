# views.py
from qdpc.core.modelviewset import BaseModelViewSet
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.http import JsonResponse
from rest_framework import status
from django.views import View
from qdpc_core_models.models.document_type import DocumentType
from product.serializers.document_type_serializer import DocumentTypeSerializer
from qdpc.core import constants


class DocumentTypeView(BaseModelViewSet):
    def get(self, request, format=None):
        documenttype = DocumentType.objects.all()
        serializer = DocumentTypeSerializer(documenttype, many=True)
        context={
            'documenttype': serializer.data,
        }
        print(context)
        return render(request, 'document_type.html',context)     
       
    
    def post(self, request, format=None):
        data = {}
        is_success = False
        message = constants.DOCUMENT_CREATION_FAILED
        status_code = status.HTTP_400_BAD_REQUEST
        serializer = DocumentTypeSerializer(data=request.data)

        try:
            if serializer.is_valid():
                serializer.save()
                is_success = True
                status_code = status.HTTP_201_CREATED
                data = serializer.data
                message = constants.DOCUMENT_CREATION_SUCESSFULLY
            else:
                # pass
                is_success = False
                status_code = status.HTTP_400_BAD_REQUEST
                data = serializer.errors
                message = constants.DOCUMENT_CREATION_FAILED


        except Exception as ex:
            is_success = False
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            message = constants.DOCUMENT_CREATION_FAILED

        return self.render_response(data, is_success, message, status_code)


class DeleteDocumentTypeView(BaseModelViewSet):
    """
    View to handle the deletion of a source using the POST method.
    """

    def post(self, request, documenttypeId, format=None):
        try:
           grades= DocumentType.objects.get(id=documenttypeId)
           grades.delete()
           return Response({
                'success': True,
                'message': constants.DOCUMENT_DELETE_SUCCESSFULLY
            }, status=status.HTTP_200_OK)
        except DocumentType.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Document Type not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

class EditDocumentTypeView(BaseModelViewSet):
    """
    View to handle editing of documenttype using the PUT method.
    """
    
    def get(self, request, documenttypeId):
        try:
            documenttype = DocumentType.objects.get(id=documenttypeId)  # Using filter to allow multiple results
            

            # Create a dictionary to store the data
            data = {
                
                'id': documenttype.id,
                'name': documenttype.name,
                
                
            }
            
            return Response({'data': data}, status=status.HTTP_200_OK)  # Return serialized data
        
        except DocumentType.DoesNotExist:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request, documenttypeId):
            try:
                documenttype = DocumentType.objects.get(id=documenttypeId)
            except DocumentType.DoesNotExist:
                return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

            serializer = DocumentTypeSerializer(documenttype, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'success': True,
                    'message': 'DocumentType updated successfully.',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            
            return Response({
                'success': False,
                'message': 'Validation failed.',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)   