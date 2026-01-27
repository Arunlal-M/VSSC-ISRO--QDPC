# Dynamic permission system based on PagePermission model only

# Page name mapping for consistent naming across the application
PAGE_NAME_MAPPING = {
    'Dashboard': 'Dashboard',
    'Equipments': 'Equipments', 
    'Acceptance Test': 'Acceptance Test',
    'Rawmaterial': 'Rawmaterial',
    'Rawmaterial Batch': 'Rawmaterial Batch',
    'Consumable': 'Consumable',
    'Consumable Batch': 'Consumable Batch',
    'Component': 'Component',
    'Component Batch': 'Component Batch',
    'Process': 'Process',
    'Product': 'Product',
    'Product Batch': 'Product Batch',
    'Units': 'Units',
    'Grade': 'Grade',
    'Enduse': 'Enduse',
    'Document Type': 'Document Type',
    'Center': 'Center',
    'Division': 'Division',
    'Source': 'Source',
    'Supplier': 'Supplier',
    'Users': 'Users',
    'Process Log-Sheet': 'Process Log-Sheet',
    'Stage Clearance': 'Stage Clearance',
    'Q.A.R-Report': 'Q.A.R-Report',
    'Groups': 'Groups',
}

def get_user_page_permissions(user):
    """Get user's page permissions using the PagePermission system"""
    if not user.is_authenticated:
        return {}
    
    # Super users have access to everything
    if user.is_superuser:
        return {'ALL': {'view', 'add', 'edit', 'delete', 'approve', 'reject'}}
    
    # System Administrator and Super Admin roles have full access
    user_groups = user.groups.all()
    admin_group_names = {
        'System Administrator', 'Super Admin', 'SYSTEM ADMINISTRATOR', 'SUPER ADMIN',
        'Master Admin/Super Admin', 'Roles- System administrator',
        'System Administrator-1', 'System Administrator-2', 'System Administrator-3'
    }
    if user_groups.filter(name__in=admin_group_names).exists():
        return {'ALL': {'view', 'add', 'edit', 'delete', 'approve', 'reject'}}
    
    from qdpc.models.page_permission import PagePermission
    
    user_permissions = {}
    
    # Get all groups the user belongs to
    for group in user_groups:
        # Get all page permissions for this group
        page_perms = PagePermission.objects.filter(group=group, is_active=True)
        
        for perm in page_perms:
            if perm.page_name not in user_permissions:
                user_permissions[perm.page_name] = set()
            user_permissions[perm.page_name].add(perm.permission_type)
    
    return user_permissions

def has_page_permission(user, page_name, permission_type='view'):
    """Check if user has a specific permission for a page using PagePermission system"""
    if not user.is_authenticated:
        return False
    
    # Super users have access to everything
    if user.is_superuser:
        return True
    
    # System Administrator and Super Admin roles have full access
    user_groups = user.groups.all()
    admin_group_names = {
        'System Administrator', 'Super Admin', 'SYSTEM ADMINISTRATOR', 'SUPER ADMIN',
        'Master Admin/Super Admin', 'Roles- System administrator',
        'System Administrator-1', 'System Administrator-2', 'System Administrator-3'
    }
    if user_groups.filter(name__in=admin_group_names).exists():
        return True
    
    from qdpc.models.page_permission import PagePermission
    
    # Check if any of user's groups have this permission
    return PagePermission.objects.filter(
        group__in=user_groups,
        page_name=page_name,
        permission_type=permission_type,
        is_active=True
    ).exists()

def get_user_accessible_pages(user):
    """Get list of pages user can access using PagePermission system"""
    if not user.is_authenticated:
        return []
    
    # Super users have access to everything
    if user.is_superuser:
        return ['ALL']
    
    # System Administrator and Super Admin roles have full access
    user_groups = user.groups.all()
    admin_group_names = {
        'System Administrator', 'Super Admin', 'SYSTEM ADMINISTRATOR', 'SUPER ADMIN',
        'Master Admin/Super Admin', 'Roles- System administrator',
        'System Administrator-1', 'System Administrator-2', 'System Administrator-3'
    }
    if user_groups.filter(name__in=admin_group_names).exists():
        return ['ALL']
    
    from qdpc.models.page_permission import PagePermission
    
    # Get unique page names from user's permissions
    pages = PagePermission.objects.filter(
        group__in=user_groups,
        is_active=True
    ).values_list('page_name', flat=True).distinct()
    
    return list(pages)

def has_page_access(user, page_name):
    """Check if user has any access to a page (backward compatibility)"""
    return has_page_permission(user, page_name, 'view')
