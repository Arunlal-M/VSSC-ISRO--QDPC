from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """Get item from dictionary by key"""
    if dictionary and isinstance(dictionary, dict):
        return dictionary.get(key, {})
    return {}


@register.filter
def has_permission(user, permission_name):
    """Check if user has a specific permission"""
    if user and user.is_authenticated:
        return user.has_perm(permission_name)
    return False


@register.filter
def can_access_page(user, page_name):
    """Check if user can access a specific page"""
    if user and user.is_authenticated:
        # Check if user is superuser
        if user.is_superuser:
            return True
        
        # Check user's groups for page permissions
        for group in user.groups.all():
            try:
                from qdpc.models.page_permission import PagePermission
                if PagePermission.objects.filter(
                    group=group,
                    page_name=page_name,
                    permission_type='view',
                    is_active=True
                ).exists():
                    return True
            except:
                pass
        
        # Fallback to Django permissions
        return user.has_perm('auth.view_group')
    
    return False
