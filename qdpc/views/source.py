from qdpc.core.modelviewset import BaseModelViewSet
from rest_framework.response import Response
from django.shortcuts import render,redirect
from qdpc_core_models.models.source import Sources
from product.serializers.source_serializer import SourcesSerializer
from rest_framework import status
from qdpc.core import constants

class SourceListView(BaseModelViewSet):
    def get(self, request, format=None):
        sources = Sources.objects.all()
        serializer = SourcesSerializer(sources, many=True)
        context={
            'sources':serializer.data
        }

        return render(request, 'source.html', context) 
       
    
    def post(self, request, format=None):
        data = {}
        print(request.data)
        is_success = False
        message = constants.SOURCE_CREATION_FAILED
        status_code = status.HTTP_400_BAD_REQUEST
        serializer = SourcesSerializer(data=request.data)


        try:
            if serializer.is_valid():
                print("it is valid")
                serializer.save()
                is_success = True
                status_code = status.HTTP_201_CREATED
                data = serializer.data
                message = constants.SOURCE_CREATION_SUCESSFULLY

            else:
                # pass
                print("not valid")
                is_success = False
                status_code = status.HTTP_400_BAD_REQUEST
                data = serializer.errors
                message = constants.SOURCE_CREATION_FAILED


        except Exception as ex:
            is_success = False
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            message = constants.SOURCE_CREATION_FAILED

        return self.render_response(data, is_success, message, status_code)
    
class DeleteSourceView(BaseModelViewSet):
    """
    View to handle the deletion of a source using the POST method.
    """

    def post(self, request, sourceId, format=None):
        try:
            source = Sources.objects.get(id=sourceId)
            source.delete()
            return Response({
                'success': True,
                'message': constants.SOURCE_DELETE_SUCCESSFULLY
            }, status=status.HTTP_200_OK)
        except Sources.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Source not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    