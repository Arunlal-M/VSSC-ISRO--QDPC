from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render,redirect
from rest_framework import status
from qdpc_core_models.models.center import Center
from qdpc_core_models.models.user_type import UserType
from qdpc_core_models.models.division import Division
from qdpc.core import constants
from qdpc.core.modelviewset import BaseModelViewSet
from product.serializers.div_center_serializers import CenterSerializer


class CenterListView(BaseModelViewSet):
    def get(self, request, format=None):
        centers = Center.objects.all()
        user_types = self.get_all_obj(UserType)
        serializer = CenterSerializer(centers, many=True)
        context = {
            'centers': serializer.data,
            'user_types': user_types
        }
        print(context)
        return render(request, 'center.html', context)

    def post(self, request, format=None):
        # Extract relevant data from request
        data = {
            'name': request.data.get('center_name'),
            'user_type': request.data.get('user_type'),
        }
        serializer = CenterSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            success = True
            status_code = status.HTTP_201_CREATED
            data = serializer.data
            message = constants.SOURCE_CREATION_SUCESSFULLY
        else:
            success = False
            status_code = status.HTTP_400_BAD_REQUEST
            data = serializer.errors
            message = constants.SOURCE_CREATION_FAILED
        return self.render_response(data,success, message, status_code)

    



class DeleteCenterView(BaseModelViewSet):
    """
    View to handle the deletion of a center using the POST method.
    """

    def post(self, request, centerId, format=None):
        try:
            center = Center.objects.get(id=centerId)
            center.delete()
            return Response({
                'success': True,
                'message': constants.CENTER_DELETE_SUCCESSFULLY
            }, status=status.HTTP_200_OK)
        except Center.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Center not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            

class EditCenterView(BaseModelViewSet):
    """
    View to handle editing of a Center using the PUT method and support division retrieval by center.
    """

    def get(self, request, centerId=None, user_type=None):
        """
        Handle retrieval of center data by centerId or filter center by user_type.
        """
        try:
            if centerId is not None:
                # Retrieve a specific division by ID
                center = Center.objects.get(id=centerId)
                all_usertype = UserType.objects.all()

                # Create a response data object for the division
                data = {
                    'id': center.id,
                    'name': center.name,
                    'user_type': {
                        'id': center.user_type.id,
                        'name': center.user_type.name
                    },
                    'all_usertype': [{'id': user_type.id, 'name': user_type.name} for user_type in all_usertype],
                }
                return Response({'data': data}, status=status.HTTP_200_OK)

            elif user_type is not None:
                # Filter center by usertype 
                centers = Center.objects.filter(user_type=user_type)
                serializer = CenterSerializer(centers, many=True)
                return Response({'centers': serializer.data}, status=status.HTTP_200_OK)

            else:
                return Response({'message': 'Invalid parameters.'}, status=status.HTTP_400_BAD_REQUEST)

        except Center.DoesNotExist:
            return Response({'detail': 'Center not found.'}, status=status.HTTP_404_NOT_FOUND)
        except UserType.DoesNotExist:
            return Response({'detail': 'UserType not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, centerId):
        """
        Handle editing a Center by its ID.
        """
        try:
            center = Center.objects.get(id=centerId)
        except Center.DoesNotExist:
            return Response({'detail': 'Center not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CenterSerializer(center, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': 'Center updated successfully.',
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            'success': False,
            'message': 'Validation failed.',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)