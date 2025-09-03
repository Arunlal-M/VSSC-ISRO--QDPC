from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from qdpc.core.permissions import has_page_permission, get_user_page_permissions

@login_required
def debug_user_role(request):
    """Debug view to check user role information and permissions"""
    user = request.user
    
    # Get dynamic page permissions
    user_page_permissions = get_user_page_permissions(user)
    
    # Test specific page access using dynamic permission system
    test_pages = {
        'Dashboard': has_page_permission(user, 'Dashboard', 'view'),
        'Equipment': has_page_permission(user, 'Equipment', 'view'),
        'Raw Material': has_page_permission(user, 'Raw Material', 'view'),
        'Consumable': has_page_permission(user, 'Consumable', 'view'),
        'Component': has_page_permission(user, 'Component', 'view'),
        'Product batch': has_page_permission(user, 'Product batch', 'view'),
        'Process': has_page_permission(user, 'Process', 'view'),
        'Reports': has_page_permission(user, 'Reports', 'view'),
        'Stage Clearance': has_page_permission(user, 'Stage Clearance', 'view'),
        'Acceptance Test': has_page_permission(user, 'Acceptance Test', 'view'),
    }
    
    # Get all possible role information
    debug_info = {
        'username': user.username,
        'is_superuser': user.is_superuser,
        'is_staff': user.is_staff,
        'is_active': user.is_active,
        'has_role_attribute': hasattr(user, 'role'),
        'role_value': getattr(user, 'role', None),
        # Handle role name access more gracefully
        'role_name': None,
        'groups_count': user.groups.count(),
        'groups': list(user.groups.values_list('name', flat=True)),
        'all_permissions': list(user.get_all_permissions()),
        'user_permissions': list(user.user_permissions.values_list('codename', flat=True)),
        'group_permissions': list(user.groups.values_list('permissions__codename', flat=True)),
        
        # Dynamic permission information
        'user_page_permissions': user_page_permissions,
        'user_has_all_access': 'ALL' in user_page_permissions,
        'test_page_access': test_pages,
        'available_groups': list(user.groups.values_list('name', flat=True)),
        'total_page_permissions': len(user_page_permissions)
    }
    
    # Try to get role name safely
    try:
        if user.groups.exists():
            debug_info['role_name'] = user.groups.first().name
        elif hasattr(user, 'role') and user.role:
            debug_info['role_name'] = user.role.name
    except Exception:
        debug_info['role_name'] = 'Error accessing role'
    
    return render(request, 'debug_role.html', {'debug_info': debug_info})
