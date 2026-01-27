from django import template
from django.contrib.auth.models import Group
from qdpc.models.page_permission import PagePermission

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """Get item from dictionary by key"""
    if dictionary is None:
        return {}
    return dictionary.get(key, {})


@register.filter
def has_page_permission(user, permission_string):
    """Check if user has a specific page permission
    
    Usage: {{ user|has_page_permission:"page_name:permission_type" }}
    Example: {{ user|has_page_permission:"Product Batch:edit" }}
    """
    if not user or not user.is_authenticated:
        return False
    
    # Super users have access to everything
    if user.is_superuser:
        return True
    
    try:
        page_name, permission_type = permission_string.split(':', 1)
    except ValueError:
        return False
    
    # Check if any of user's groups have this permission
    return PagePermission.objects.filter(
        group__in=user.groups.all(),
        page_name=page_name.strip(),
        permission_type=permission_type.strip(),
        is_active=True
    ).exists()


@register.filter
def can_view_page(user, page_name):
    """Check if user can view a specific page"""
    return has_page_permission(user, f"{page_name}:view")


@register.filter
def can_add_to_page(user, page_name):
    """Check if user can add items to a specific page"""
    return has_page_permission(user, f"{page_name}:add")


@register.filter
def can_edit_page(user, page_name):
    """Check if user can edit items on a specific page"""
    return has_page_permission(user, f"{page_name}:edit")


@register.filter
def can_delete_from_page(user, page_name):
    """Check if user can delete items from a specific page"""
    return has_page_permission(user, f"{page_name}:delete")


@register.filter
def can_approve_page(user, page_name):
    """Check if user can approve items on a specific page"""
    return has_page_permission(user, f"{page_name}:approve")


@register.filter
def can_reject_page(user, page_name):
    """Check if user can reject items on a specific page"""
    return has_page_permission(user, f"{page_name}:reject")


@register.simple_tag
def get_user_page_permissions(user):
    """Get all page permissions for a user
    
    Returns: {
        'page_name': ['view', 'edit', 'approve'],
        'another_page': ['view', 'add']
    }
    """
    if not user or not user.is_authenticated:
        return {}
    
    # Super users have access to everything
    if user.is_superuser:
        return {'ALL': ['view', 'add', 'edit', 'delete', 'approve', 'reject']}
    
    user_permissions = {}
    
    # Get all groups the user belongs to
    user_groups = user.groups.all()
    
    for group in user_groups:
        # Get all page permissions for this group
        page_perms = PagePermission.objects.filter(group=group, is_active=True)
        
        for perm in page_perms:
            if perm.page_name not in user_permissions:
                user_permissions[perm.page_name] = set()
            user_permissions[perm.page_name].add(perm.permission_type)
    
    # Convert sets to lists for template use
    return {page: list(perms) for page, perms in user_permissions.items()}


@register.simple_tag
def get_user_accessible_pages(user):
    """Get list of pages user can access"""
    if not user or not user.is_authenticated:
        return []
    
    # Super users have access to everything
    if user.is_superuser:
        return ['ALL']
    
    # Get unique page names from user's permissions
    pages = PagePermission.objects.filter(
        group__in=user.groups.all(),
        is_active=True
    ).values_list('page_name', flat=True).distinct()
    
    return list(pages)


@register.simple_tag
def get_role_page_permissions(role, page_name):
    """Get all permissions for a specific role and page"""
    if not role or not page_name:
        return []
    
    permissions = PagePermission.objects.filter(
        group=role,
        page_name=page_name,
        is_active=True
    ).values_list('permission_type', flat=True)
    
    return list(permissions)


@register.simple_tag
def get_page_permission_count(role, page_name):
    """Get count of permissions for a specific role and page"""
    if not role or not page_name:
        return 0
    
    return PagePermission.objects.filter(
        group=role,
        page_name=page_name,
        is_active=True
    ).count()


@register.simple_tag
def get_role_total_permissions(role):
    """Get total count of permissions for a role"""
    if not role:
        return 0
    
    return PagePermission.objects.filter(
        group=role,
        is_active=True
    ).count()


@register.simple_tag
def get_page_total_permissions(page_name):
    """Get total count of permissions for a page"""
    if not page_name:
        return 0
    
    return PagePermission.objects.filter(
        page_name=page_name,
        is_active=True
    ).count()


@register.filter
def permission_badge_class(permission_type):
    """Get Bootstrap badge class for permission type"""
    badge_classes = {
        'view': 'bg-primary',
        'add': 'bg-success',
        'edit': 'bg-warning',
        'delete': 'bg-danger',
        'approve': 'bg-info',
        'reject': 'bg-secondary'
    }
    return badge_classes.get(permission_type, 'bg-secondary')


@register.filter
def permission_icon(permission_type):
    """Get FontAwesome icon for permission type"""
    icon_mapping = {
        'view': 'fas fa-eye',
        'add': 'fas fa-plus',
        'edit': 'fas fa-edit',
        'delete': 'fas fa-trash',
        'approve': 'fas fa-check',
        'reject': 'fas fa-times'
    }
    return icon_mapping.get(permission_type, 'fas fa-question')
