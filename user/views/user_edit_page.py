from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from qdpc.core.modelviewset import BaseModelViewSet
from qdpc_core_models.models.user import User
from qdpc_core_models.models.center import Center
from qdpc_core_models.models.role import Role
from qdpc_core_models.models.user_type import UserType
from qdpc_core_models.models.division import Division
from user.serializers.userupdate_serializer import UserUpdateSerializer
from django.contrib.auth.models import Group


class UserEditPageView(BaseModelViewSet):
    """Full-page user edit similar to Django admin edit page."""

    def _is_super_admin(self, request) -> bool:
        try:
            # Direct superuser flag
            if request.user.is_superuser:
                return True

            # Allowed elevated names
            elevated_names = {
                "SUPER ADMIN",
                "MASTER ADMIN",
                "ADMIN",
                "MASTER ADMIN/SUPER ADMIN",
                "SYSTEM ADMINISTRATOR-1",
                "SYSTEM ADMINISTRATOR-2",
                "SYSTEM ADMINISTRATOR-3",
            }

            # Check Role FK name - handle case where user has no role
            try:
                user_role = getattr(request.user, 'role', None)
                if user_role and hasattr(user_role, 'name'):
                    name = str(user_role.name).upper()
                    if name in elevated_names:
                        return True
            except Exception:
                pass

            # Check Django Group memberships
            try:
                group_names = set(n.upper() for n in request.user.groups.values_list('name', flat=True))
                if any(n in elevated_names for n in group_names):
                    return True
            except Exception:
                pass

            return False
        except Exception:
            return bool(getattr(request.user, 'is_superuser', False))

    def get(self, request, user_id: int):
        is_super_admin = self._is_super_admin(request)
        user = get_object_or_404(User, id=user_id)

        # Build selected id lists to support both FK and M2M role setups
        selected_center_ids = list(user.centre.values_list('id', flat=True))
        selected_division_ids = list(user.divisions.values_list('id', flat=True))
        selected_role_ids = []
        
        print(f"DEBUG: User {user.username} - Checking role assignments")
        
        # Prioritize Django groups over custom roles for display purposes
        try:
            if user.groups.exists():
                group_ids = list(user.groups.values_list('id', flat=True))
                selected_role_ids = group_ids
                print(f"DEBUG: User has groups with IDs: {group_ids}")
                
                # Special handling for "Guest" group - ensure it's properly selected
                guest_group = Group.objects.filter(name='Guest').first()
                if guest_group and guest_group.id in group_ids:
                    print(f"DEBUG: User has Guest group (ID: {guest_group.id})")
                    # Ensure Guest group is first in the list for proper selection
                    if selected_role_ids and selected_role_ids[0] != guest_group.id:
                        selected_role_ids.remove(guest_group.id)
                        selected_role_ids.insert(0, guest_group.id)
                        print(f"DEBUG: Reordered selected_role_ids to prioritize Guest: {selected_role_ids}")
            # Only check custom Role FK if no groups exist
            elif getattr(user, 'role_id', None):
                try:
                    selected_role_ids = [user.role_id]
                    print(f"DEBUG: User has FK role with ID: {selected_role_ids}")
                except Exception as e:
                    print(f"DEBUG: Error checking role FK: {e}")
                    selected_role_ids = []
        except Exception as e:
            print(f"DEBUG: Error checking groups: {e}")
            selected_role_ids = []

        print(f"DEBUG: Final selected_role_ids: {selected_role_ids}")
        
        # Additional debug info for role selection
        print(f"DEBUG: User groups: {list(user.groups.values_list('name', flat=True))}")
        print(f"DEBUG: User role_id: {getattr(user, 'role_id', None)}")
        print(f"DEBUG: User role: {getattr(user, 'role', None)}")
        print(f"DEBUG: all_roles count: {Group.objects.count()}")
        print(f"DEBUG: all_roles names: {list(Group.objects.values_list('name', flat=True))}")
        
        # Check if user has any groups at all
        user_groups = list(user.groups.all())
        print(f"DEBUG: User groups objects: {user_groups}")
        if user_groups:
            print(f"DEBUG: First group ID: {user_groups[0].id}, Name: {user_groups[0].name}")
        else:
            print("DEBUG: User has NO groups assigned!")

        # Set display_role_name for the user (similar to user list view)
        try:
            name = ''
            # First check Django group memberships (this is what most users will have)
            if user.groups.exists():
                group_names = list(user.groups.values_list('name', flat=True))
                name = ", ".join(group_names)
                print(f"DEBUG: User {user.username} has groups: {group_names}")
            # Only check custom Role FK if no groups exist and role is assigned
            elif getattr(user, 'role_id', None) and user.role:
                try:
                    name = user.role.name or ''
                    print(f"DEBUG: User {user.username} has custom role: {name}")
                except Exception:
                    # If role lookup fails, fall back to groups
                    if user.groups.exists():
                        group_names = list(user.groups.values_list('name', flat=True))
                        name = ", ".join(group_names)
                        print(f"DEBUG: User {user.username} fallback to groups: {group_names}")
            # Final fallback
            user.display_role_name = name or 'Guest'
            print(f"DEBUG: User {user.username} display_role_name set to: {user.display_role_name}")
        except Exception as e:
            print(f"DEBUG: Error setting display_role_name for user {user.username}: {e}")
            # If all else fails, try to get groups
            try:
                if user.groups.exists():
                    group_names = list(user.groups.values_list('name', flat=True))
                    user.display_role_name = ", ".join(group_names) or 'Guest'
                    print(f"DEBUG: User {user.username} fallback display_role_name: {user.display_role_name}")
                else:
                    user.display_role_name = 'Guest'
                    print(f"DEBUG: User {user.username} final fallback display_role_name: Guest")
            except Exception as group_e:
                user.display_role_name = 'Guest'
                print(f"DEBUG: User {user.username} error in fallback: {group_e}, display_role_name: Guest")

        context = {
            'target_user': user,
            'all_centers': Center.objects.all(),
            'all_divisions': Division.objects.all(),
            # Use Groups to list all available roles
            'all_roles': Group.objects.all().order_by('name'),
            'all_usertypes': UserType.objects.all(),
            'is_super_admin': is_super_admin,
            'selected_center_ids': selected_center_ids,
            'selected_division_ids': selected_division_ids,
            'selected_role_ids': selected_role_ids,
        }
        return render(request, 'user_edit.html', context)

    def post(self, request, user_id: int):
        # print('ANUMONNNNNNNNNN')
        user = get_object_or_404(User, id=user_id)
        is_super_admin = self._is_super_admin(request)

        # Get the selected group from the role dropdown
        selected_group_id = request.POST.get('role')      
        # Check what Groups are available for the dropdown
        try:
            all_groups = Group.objects.all().order_by('name')           
            # Check if the selected group exists
            if selected_group_id and selected_group_id.strip():
                try:
                    group_id = int(selected_group_id)
                    if group_id > 0:
                        selected_group = Group.objects.get(id=group_id)
                        print(f"DEBUG: Selected group exists: {selected_group.name} (ID: {selected_group.id})")
                        
                        # Update user's groups - clear existing and add new
                        user.groups.clear()
                        user.groups.add(selected_group)
                        print(f"DEBUG: Updated user groups to: {selected_group.name}")
                        
                    else:
                        print("DEBUG: Selected group ID is 0 or negative")
                except (ValueError, Group.DoesNotExist):
                    print(f"DEBUG: Selected group ID {selected_group_id} is invalid or doesn't exist")
                    
        except Exception as e:
            print(f"DEBUG: Error checking groups: {e}")
            import traceback
            print(f"DEBUG: Group check traceback: {traceback.format_exc()}")
        
        # Build payload compatible with serializer
        data = {
            'username': request.POST.get('username', user.username),
            'first_name': request.POST.get('first_name', user.first_name),
            'last_name': request.POST.get('last_name', user.last_name),
            'email': request.POST.get('email', user.email),
            'phone_number': request.POST.get('phone_number', user.phone_number),
            'desired_salutation': request.POST.get('desired_salutation', user.desired_salutation),
            'usertype': request.POST.get('usertype') or (user.usertype.id if user.usertype else None),
            'centre': [int(request.POST.get('centre'))] if request.POST.get('centre') else [],
            'divisions': [int(request.POST.get('divisions'))] if request.POST.get('divisions') else [],
            'is_active': True if request.POST.get('is_active') == 'on' else False,
            'is_staff': True if request.POST.get('is_staff') == 'on' else user.is_staff,
            'is_superuser': True if request.POST.get('is_superuser') == 'on' else user.is_superuser,
            'is_approved': True if request.POST.get('is_approved') == 'on' else user.is_approved,
        }
        
        print(f"DEBUG: Serializer data: {data}")

        try:
            # Try updating user fields directly first to isolate the issue
            print("DEBUG: Anuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu")
            
            # Update basic fields
            user.first_name = data.get('first_name', user.first_name)
            user.last_name = data.get('last_name', user.last_name)
            user.email = data.get('email', user.email)
            user.phone_number = data.get('phone_number', user.phone_number)
            user.desired_salutation = data.get('desired_salutation', user.desired_salutation)
            user.is_active = data.get('is_active', user.is_active)
            user.is_staff = data.get('is_staff', user.is_staff)
            user.is_superuser = data.get('is_superuser', user.is_superuser)
            user.is_approved = data.get('is_approved', user.is_approved)
            
            # Check current user role
            print(f"DEBUG: Current user role: {getattr(user, 'role', None)}")
            print(f"DEBUG: Current user role_id: {getattr(user, 'role_id', None)}")
            # Don't touch the role field at all - let it stay as is
            print("DEBUG: Keeping user.role unchanged to avoid ForeignKey issues")
            
            # Update usertype if provided
            if data.get('usertype'):
                try:
                    usertype = UserType.objects.get(id=data['usertype'])
                    user.usertype = usertype
                    print(f"DEBUG: Updated usertype to: {usertype}")
                except UserType.DoesNotExist:
                    print("DEBUG: UserType not found")
                    pass
            
            print("DEBUG: About to save user instance")
            print(f"DEBUG: User role before save: {getattr(user, 'role', None)}")
            print(f"DEBUG: User role_id before save: {getattr(user, 'role_id', None)}")
            
            try:
                print("DEBUG: About to call user.save()")
                print(f"DEBUG: User.role before save: {getattr(user, 'role', None)}")
                print(f"DEBUG: User.role_id before save: {getattr(user, 'role_id', None)}")
                
                # Try to save with update_fields to avoid role validation
                update_fields = [
                    'first_name', 'last_name', 'email', 'phone_number', 
                    'desired_salutation', 'is_active', 'is_staff', 
                    'is_superuser', 'is_approved'
                ]
                if data.get('usertype'):
                    update_fields.append('usertype')
                
                print(f"DEBUG: Using update_fields: {update_fields}")
                user.save(update_fields=update_fields)
                print(f"DEBUG: User instance saved successfully")
                print(f"DEBUG: User role after save: {getattr(user, 'role', None)}")
                print(f"DEBUG: User role_id after save: {getattr(user, 'role_id', None)}")
            except Exception as save_error:
                print(f"DEBUG: Error during user.save(): {save_error}")
                print(f"DEBUG: Error type: {type(save_error)}")
                import traceback
                print(f"DEBUG: Save error traceback: {traceback.format_exc()}")
                raise
            
            # Update many-to-many fields after saving the user
            print("DEBUG: Updating many-to-many fields")
            if data.get('centre'):
                user.centre.set(data['centre'])
                print(f"DEBUG: Updated centre to: {data['centre']}")
            if data.get('divisions'):
                user.divisions.set(data['divisions'])
                print(f"DEBUG: Updated divisions to: {data['divisions']}")
            
            # Update user groups based on role selection
            print("DEBUG: Starting group update process")
            print(f"DEBUG: Selected group ID: '{selected_group_id}'")
            
            # Check if selected_group_id is a valid non-empty value
            if selected_group_id and str(selected_group_id).strip() and selected_group_id != '' and selected_group_id != '0':
                try:
                    # Convert to int and validate it's not 0
                    group_id = int(selected_group_id)
                    if group_id > 0:
                        print(f"DEBUG: Processing group ID: {group_id}")
                        
                        # Check if the group exists first
                        try:
                            selected_group = Group.objects.get(id=group_id)
                            print(f"DEBUG: Found group: {selected_group.name} (ID: {selected_group.id})")
                        except Group.DoesNotExist:
                            print(f"DEBUG: Group with ID {group_id} does not exist")
                            raise
                        
                        print("DEBUG: About to clear existing groups")
                        # Clear existing groups
                        user.groups.clear()
                        print("DEBUG: Cleared existing groups")
                        
                        print("DEBUG: About to add selected group")
                        # Add the selected group
                        user.groups.add(selected_group)
                        print(f"DEBUG: Added group: {selected_group.name} (ID: {selected_group.id})")
                        
                        print("DEBUG: Group updated successfully")
                            
                except (ValueError, Group.DoesNotExist) as e:
                    print(f"DEBUG: Error processing group selection: {e}")
                    import traceback
                    print(f"DEBUG: Group selection traceback: {traceback.format_exc()}")
                    pass
            else:
                print("DEBUG: No valid group selected, clearing groups")
                # Clear groups if no role selected
                user.groups.clear()
                print("DEBUG: Cleared all groups")
            
            # Show final group status
            final_groups = list(user.groups.values_list('name', flat=True))
            print(f"DEBUG: User groups after update: {final_groups}")
            
            print("DEBUG: Redirecting to user list")
            return HttpResponseRedirect('/user/userlist/?updated=1')
            
        except Exception as e:
            print(f"DEBUG: Exception occurred: {e}")
            print(f"DEBUG: Exception type: {type(e)}")
            import traceback
            print(f"DEBUG: Traceback: {traceback.format_exc()}")
            
            # Re-render with error
            context = {
                'target_user': user,
                'all_centers': Center.objects.all(),
                'all_divisions': Division.objects.all(),
                'all_roles': Group.objects.all(),
                'all_usertypes': UserType.objects.all(),
                'is_super_admin': is_super_admin,
                'errors': {'general': [f'An error occurred: {str(e)}']},
                'form_values': request.POST,
            }
            return render(request, 'user_edit.html', context)


