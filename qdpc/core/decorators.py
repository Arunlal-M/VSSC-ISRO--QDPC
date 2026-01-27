from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.http import JsonResponse
from qdpc.core.permissions import has_page_permission


def require_page_permission(page_name, permission_type='view', redirect_url='user-dashboard'):
    """
    Decorator to check if user has specific page permission
    Based on PagePermission model and dashboard checkbox selections only
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, 'You must be logged in to access this page.')
                return redirect('login')
            
            if not has_page_permission(request.user, page_name, permission_type):
                # Check if it's an AJAX request
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'error': 'Permission denied'}, status=403)
                
                messages.error(request, f'You do not have permission to {permission_type} {page_name}.')
                return redirect(redirect_url)
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def require_admin_permission(redirect_url='user-dashboard'):
    """
    Decorator to check if user has admin/role management permissions
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, 'You must be logged in to access this page.')
                return redirect('login')
            
            # Check if user is superuser or has Groups management permission
            if not (request.user.is_superuser or has_page_permission(request.user, 'Groups', 'view')):
                messages.error(request, 'You do not have permission to access this page.')
                return redirect(redirect_url)
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
