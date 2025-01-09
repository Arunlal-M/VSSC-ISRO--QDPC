from qdpc.core.modelviewset import BaseModelViewSet
from rest_framework.permissions import IsAdminUser 
from qdpc_core_models.models.user import User
from rest_framework.response import Response
from django.contrib.auth.models import  Group
from qdpc_core_models.models.role import Role
from rest_framework import status
from qdpc.core import constants
from user.serializers.userlist_serializer import UpdateUserStatusSerializer






class UserApprovalView(BaseModelViewSet):
    "user approval api to approva specific roles to a user"
   
     # Ensure only admins can access this endpoint

    def post(self, request, user_id):
        try:
            print(request.data)
            user = User.objects.get(id=user_id)
            roles = request.data.get('roles')  # Get the list of roles from the request

            # Check if there are any roles provided
            if roles:
                # Assign only the first role to the user
                # first_role_id = roles[0]  # Get the first role ID
                user.role.clear()  # Clear existing roles
                user.role.add(roles)  # Assign the first role to the user

            # group_name = 'ApprovedGroup'  # Replace with your actual group name
            # group, created = Group.objects.get_or_create(name=group_name)
            # role, created = Role.objects.get_or_create(name=group_name)
            # user.groups.add(group)

            # Set the user's status to active
            user.is_active = True
            user.is_approved = True
            user.is_staff = True
            user.save()

            success = True
            message = constants.APPROVED_SUCESS 
            status_code = 200

            return self.render_response(data={}, success=success, message=message, status=status_code)

        except User.DoesNotExist:
            return Response({'detail': 'User  not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Add user to a specific group
       



class UpdateUserStatusView(BaseModelViewSet):
    def post(self, request, *args, **kwargs):
        serializer = UpdateUserStatusSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data['id']
            is_active = serializer.validated_data['is_active']
            
            try:
                user = User.objects.get(id=user_id)
                user.is_active = is_active
                user.save()
                return Response({'success': True}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'success': False, 'error': 'User  not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
class RejectUserView(BaseModelViewSet):   
    """
    View to handle the rejection of a user using the POST method.
    """

    def post(self, request, user_id, format=None):
        try:
            user = User.objects.get(id=user_id)
            user.delete()

            return Response({
                'success': True,
                'message': constants.USER_REJECT_SUCCESSFULLY  # Adjust your success message
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({
                'success': False,
                'message': 'User  not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)