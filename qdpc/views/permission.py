from qdpc.core.modelviewset import BaseModelViewSet  # Import APIView from Django REST framework
from rest_framework.response import Response  # Import Response to send HTTP responses
from django.contrib.auth.models import Permission, Group  # Import Permission and Group models
from rest_framework.permissions import IsAuthenticated  # Import permission class to ensure user is authenticated
from rest_framework import status  # Import status to handle HTTP status codes
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

 


class GroupPermissionListView(BaseModelViewSet):  # Create a class for the API view to list permissions by group
    permission_classes = [IsAuthenticated]  # Set permission to allow only authenticated users

    def get(self, request, group_id):  # Define the GET method for retrieving permissions by group ID
        try:
            # Only Superusers or SUPER ADMIN role can manage roles
            is_super = request.user.is_superuser or (getattr(request.user, 'role', None) and str(request.user.role.name).upper() in {"SUPER ADMIN", "MASTER ADMIN"})
            if not is_super:
                return render(request, 'group_permissions.html', {"error": "Unauthorized"}, status=403)
            group = Group.objects.get(id=group_id)  # Retrieve the group by its ID
            
            # Get all available permissions from Django
            all_permissions = Permission.objects.all().order_by('content_type__app_label', 'content_type__model', 'codename')
            
            # Get existing permissions for this group
            group_permissions = group.permissions.all()
            
            # Group permissions by content type for better organization
            permissions_by_type = {}
            for perm in all_permissions:
                app_label = perm.content_type.app_label
                model = perm.content_type.model
                key = f"{app_label}.{model}"
                
                if key not in permissions_by_type:
                    permissions_by_type[key] = {
                        'app_label': app_label,
                        'model': model,
                        'permissions': []
                    }
                
                permissions_by_type[key]['permissions'].append({
                    'id': perm.id,
                    'name': perm.name,
                    'codename': perm.codename,
                    'is_assigned': perm in group_permissions
                })
            
            context = {
                'group': group,
                'permissions_by_type': permissions_by_type,
                'group_permissions': group_permissions,
            }
            return render(request, 'group_permissions.html', context)
        except Group.DoesNotExist:  # Handle case where the group does not exist
            return Response({"error": "Group not found."}, status=status.HTTP_404_NOT_FOUND)  # Return a 404 error if the group is not found


    @csrf_exempt
    def post(self, request, group_id):
        group = get_object_or_404(Group, pk=group_id)
        is_super = request.user.is_superuser or (getattr(request.user, 'role', None) and str(request.user.role.name).upper() in {"SUPER ADMIN", "MASTER ADMIN"})
        if not is_super:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            # Get selected permission IDs from the form
            selected_permission_ids = request.POST.getlist('permissions')
            
            # Convert to Permission objects
            selected_permissions = Permission.objects.filter(id__in=selected_permission_ids)
            
            # Update group permissions
            group.permissions.set(selected_permissions)
            
            messages.success(request, f'Permissions updated for group "{group.name}"!')
            return redirect('group-permission-list', group_id=group_id)
            
        except Exception as e:
            messages.error(request, f'Error updating permissions: {str(e)}')
            return redirect('group-permission-list', group_id=group_id) 
            
    # DELETE method to remove the group
    def delete(self, request, group_id):
        try:
            group = get_object_or_404(Group, pk=group_id)  # Fetch the group or return 404
            group.delete()  # Delete the group from the database
            return Response({'message': 'Group deleted successfully!'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

