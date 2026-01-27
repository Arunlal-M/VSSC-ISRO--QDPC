from django import template
from django.contrib.auth.models import Group
from qdpc.models.page_permission import PagePermission

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """Get item from dictionary by key"""
    return dictionary.get(key)


@register.filter
def can_access_page(user, page_name):
    """Check if user can access a specific page based on their group permissions"""
    if not user.is_authenticated:
        return False
    
    # Check if user is superuser
    if user.is_superuser:
        return True
    
    # Check user's groups for page permissions
    user_groups = user.groups.all()
    for group in user_groups:
        if PagePermission.objects.filter(
            group=group,
            page_name=page_name,
            permission_type='view',
            is_active=True
        ).exists():
            return True
    
    return False


@register.filter
def has_page_permission(user, page_name, permission_type):
    """Check if user has a specific permission type for a page"""
    if not user.is_authenticated:
        return False
    
    # Check if user is superuser
    if user.is_superuser:
        return True
    
    # Check user's groups for specific permission
    user_groups = user.groups.all()
    for group in user_groups:
        if PagePermission.objects.filter(
            group=group,
            page_name=page_name,
            permission_type=permission_type,
            is_active=True
        ).exists():
            return True
    
    return False


@register.simple_tag
def get_user_page_permissions(user, page_name):
    """Get all permissions a user has for a specific page"""
    if not user.is_authenticated:
        return []
    
    permissions = []
    user_groups = user.groups.all()
    
    for group in user_groups:
        group_permissions = PagePermission.objects.filter(
            group=group,
            page_name=page_name,
            is_active=True
        )
        for perm in group_permissions:
            permissions.append(perm.permission_type)
    
    return list(set(permissions))  # Remove duplicates
