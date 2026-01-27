from rest_framework import status
from qdpc.core import constants
from qdpc.services.user_service import UserService
from qdpc.core.modelviewset import BaseModelViewSet
from django.shortcuts import render, redirect
from qdpc_core_models.models.user import User
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from qdpc_core_models.models.center import Center
from qdpc_core_models.models.role import Role
from qdpc_core_models.models.user_type import UserType
from qdpc_core_models.models.division import Division
from user.serializers.userupdate_serializer import UserUpdateSerializer
from qdpc_core_models.models.rolemeta import RoleMeta
from django.contrib.auth.models import Group
class UserFetch(BaseModelViewSet):
    authentication_classes = [TokenAuthentication]
    """ User List API for qdpc application"""

    def post(self, request):
        data=request.query_params
        success = False
        message = constants.USER_FETCH_FAILED
        status_code = status.HTTP_403_FORBIDDEN
        try:
            success, status_code, data, message =UserService.get_user_list(data)
        except Exception as ex:
            success = False
            message = constants.USER_FETCH_FAILED
            status_code = status.HTTP_400_BAD_REQUEST
            
        return self.render_response(data, success, message, status_code)




class UserListView(BaseModelViewSet):
    """""user list api to fetch all the user to user list"""
   
    def get(self, request, user_id=None):
        if user_id:
            user_data = self.get_user_data(user_id)
            print(user_data)

            all_divisions = self.get_all_obj(model_name=Division)
            # Use groups instead of roles to avoid the "Role matching query does not exist" error
            all_groups = Group.objects.all()
            all_centres=self.get_all_obj(model_name=Center)
            all_usertypes=self.get_all_obj(model_name=UserType)
           
            # all_roles = 
            user_data['all_divisions'] = [{'id': division.id, 'name': division.name} for division in all_divisions]
            user_data['all_centres'] = [{'id': centre.id, 'name': centre.name} for centre in all_centres]
            user_data['all_roles'] = [{'id': group.id, 'name': group.name} for group in all_groups]
            user_data['all_usertypes'] = [{'id': usertype.id, 'name': usertype.name} for usertype in all_usertypes]
            return Response({'data': user_data}, status=status.HTTP_200_OK)
        
        else:
            users = User.objects.all()
            groups = Group.objects.all()
            # Attach display_role_name to each user; fallback to Group(s) or 'Guest'
            for u in users:
                try:
                    name = ''
                    # First check Django group memberships (this is what most users will have)
                    if u.groups.exists():
                        group_names = list(u.groups.values_list('name', flat=True))
                        name = ", ".join(group_names)
                    # Only check custom Role FK if no groups exist and role is assigned
                    elif getattr(u, 'role_id', None) and u.role:
                        try:
                            name = u.role.name or ''
                        except Exception:
                            # If role lookup fails, fall back to groups
                            if u.groups.exists():
                                group_names = list(u.groups.values_list('name', flat=True))
                                name = ", ".join(group_names)
                    # Final fallback
                    u.display_role_name = name or 'Guest'
                except Exception:
                    # If all else fails, try to get groups
                    try:
                        if u.groups.exists():
                            group_names = list(u.groups.values_list('name', flat=True))
                            u.display_role_name = ", ".join(group_names) or 'Guest'
                        else:
                            u.display_role_name = 'Guest'
                    except Exception:
                        u.display_role_name = 'Guest'
            default_roles = list(
                RoleMeta.objects.select_related('group')
                .filter(is_default=True)
                .order_by('group__name')
                .values('group__name', 'page_codes')
            )
            # Determine if current user is super admin
            user_role_name = None
            try:
                # Check groups first (this is what most users will have)
                if request.user.groups.exists():
                    group_names = [group.name.upper() for group in request.user.groups.all()]
                    user_role_name = group_names[0] if group_names else None
                    is_super_admin = request.user.is_superuser or any(name in {"SUPER ADMIN", "MASTER ADMIN"} for name in group_names)
                # Only check custom role if no groups exist
                elif hasattr(request.user, 'role') and request.user.role:
                    try:
                        role_name = str(request.user.role.name).upper()
                        user_role_name = role_name
                        is_super_admin = request.user.is_superuser or role_name in {"SUPER ADMIN", "MASTER ADMIN"}
                    except Exception:
                        # If role lookup fails, fall back to groups
                        if request.user.groups.exists():
                            group_names = [group.name.upper() for group in request.user.groups.all()]
                            user_role_name = group_names[0] if group_names else None
                            is_super_admin = request.user.is_superuser or any(name in {"SUPER ADMIN", "MASTER ADMIN"} for name in group_names)
                        else:
                            is_super_admin = request.user.is_superuser
                else:
                    is_super_admin = request.user.is_superuser
            except Exception:
                is_super_admin = request.user.is_superuser

            context = {
                'users': users,
                'all_roles': [{'id': g.id, 'name': g.name} for g in groups],
                'default_roles': default_roles,
                'is_super_admin': is_super_admin,
            }

            return render(request, 'usernewone.html', context)

    def get_user_data(self, user_id):
        user = get_object_or_404(User, id=user_id)
        # Build role selection compatible with Group-based roles
        if getattr(user, 'role_id', None):
            selected_role_ids = [user.role_id]
            print("selected_role_ids",selected_role_ids)
        else:
            selected_role_ids = list(user.groups.values_list('id', flat=True))
            print("selected_group_ids",selected_role_ids)

        user_data = {
            'userid':user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone_number': user.phone_number,
            'desired_salutation': user.desired_salutation,
            'centre': [centre.id for centre in user.centre.all()],
            'divisions': [division.id for division in user.divisions.all()],
            'role': selected_role_ids,
            'usertype': user.usertype.id if user.usertype else None,
            'is_active': user.is_active,
            'is_staff': user.is_staff,
            'is_approved': user.is_approved,
            'is_superuser': user.is_superuser,
        }

        print("user data",selected_role_ids)
        return user_data
    

    

    def put(self, request, user_id):
        data = {}
        success = False
        message = "Invalid data"
        status_code = status.HTTP_400_BAD_REQUEST
        
        try:
            # Super admin only
            can_change_role = False
            try:
                if getattr(request.user, 'is_superuser', False):
                    can_change_role = True
                # Check groups first (this is what most users will have)
                elif request.user.groups.exists():
                    group_names = [group.name.upper() for group in request.user.groups.all()]
                    if any(name in {"SUPER ADMIN", "MASTER ADMIN"} for name in group_names):
                        can_change_role = True
                # Only check custom role if no groups exist
                elif hasattr(request.user, 'role') and request.user.role:
                    try:
                        role_name = str(request.user.role.name).upper()
                        if role_name in {"SUPER ADMIN", "MASTER ADMIN"}:
                            can_change_role = True
                    except Exception:
                        # If role lookup fails, fall back to groups
                        if request.user.groups.exists():
                            group_names = [group.name.upper() for group in request.user.groups.all()]
                            if any(name in {"SUPER ADMIN", "MASTER ADMIN"} for name in group_names):
                                can_change_role = True
            except Exception:
                can_change_role = getattr(request.user, 'is_superuser', False)

            print(user_id,"user id which is passed")
            user = User.objects.get(id=user_id)
            print(user,"The user i am doing put operation")
            serializer = UserUpdateSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                if not can_change_role:
                    # Strip privileged fields; allow role only if permitted
                    for key in ['role', 'is_superuser', 'is_staff', 'is_approved']:
                        if key in serializer.validated_data:
                            serializer.validated_data.pop(key, None)
                print("serilaizer is valid")
                instance = serializer.save()
                data = serializer.data
                print(data,"What i got data")
                success = True
                message = "User updated successfully"
                status_code = status.HTTP_200_OK
            else:
                data = serializer.errors
        except User.DoesNotExist:
            message = "User not found"
            status_code = status.HTTP_404_NOT_FOUND

        return self.render_response(data,success, message, status_code)


    # def update_user_role(self, request, user_id):
        
    #     try:
    #         user = User.objects.get(id=user_id)
    #         roles = request.data.get('roles', [])  # Get selected roles from request
    #         user.role.set(roles)  # Assign selected roles to the user
    #         user.save()
    #         return self.render_response({}, True, "Role updated successfully", status.HTTP_200_OK)
    #     except User.DoesNotExist:
    #         return self.render_response({}, False, "User not found", status.HTTP_404_NOT_FOUND)

class UserProfileView(BaseModelViewSet):
    def get(self,request,format=None):
        users = User.objects.all()
        # Use groups instead of roles to avoid the "Role matching query does not exist" error
        all_groups = Group.objects.all()
        context = {
            "users":users,
           "all_roles": all_groups  # Keep the key name for backward compatibility
        }
        return render(request, 'index.html', context)
