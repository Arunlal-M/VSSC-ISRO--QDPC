from qdpc.core.modelviewset import BaseModelViewSet  # Import APIView from Django REST framework
from rest_framework.response import Response  # Import Response to send HTTP responses
from django.contrib.auth.models import Permission, Group  # Import Permission and Group models
from rest_framework.permissions import IsAuthenticated  # Import permission class to ensure user is authenticated
from rest_framework import status  # Import status to handle HTTP status codes
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt


class GroupPermissionListView(BaseModelViewSet):  # Create a class for the API view to list permissions by group
    permission_classes = [IsAuthenticated]  # Set permission to allow only authenticated users

    def get(self, request, group_id):  # Define the GET method for retrieving permissions by group ID
        try:
            group = Group.objects.get(id=group_id)  # Retrieve the group by its ID
            permissions = Permission.objects.all()  # Get all permissions from the database
            group_permissions = group.permissions.all()  # Get all permissions associated with the group
            
            available_permissions = [{"id": permission.id, "name": permission.name} for permission in permissions if permission not in group_permissions]  # List permissions not in group
            chosen_permissions = [{"id": permission.id, "name": permission.name} for permission in group_permissions]  # List permissions in group
            
            context ={
                'group': group,
                'permissions': permissions,
                'available_permissions' : available_permissions,
                'chosen_permissions' : chosen_permissions,
                
            }
            return render(request, 'group_permissions.html', context)
        except Group.DoesNotExist:  # Handle case where the group does not exist
            return Response({"error": "Group not found."}, status=status.HTTP_404_NOT_FOUND)  # Return a 404 error if the group is not found


    @csrf_exempt
    def post(self, request, group_id):
            group = get_object_or_404(Group, pk=group_id)
            permission_ids = request.data.get('permissions', [])  

            try:
                # Convert permission IDs to Permission objects
                new_permissions = Permission.objects.filter(id__in=permission_ids)

                # Update group permissions
                group.permissions.set(new_permissions) 
                return Response({'message': 'Permissions updated successfully!'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
            
    # DELETE method to remove the group
    def delete(self, request, group_id):
        try:
            group = get_object_or_404(Group, pk=group_id)  # Fetch the group or return 404
            group.delete()  # Delete the group from the database
            return Response({'message': 'Group deleted successfully!'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

