from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from qdpc.core.decorators import require_admin_permission
from django.contrib.auth.models import Group
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
import json

from qdpc.models.page_permission import Page, PagePermission
from qdpc_core_models.models.role import Role


def is_admin_user(user):
    """Check if user is admin or has role management access"""
    from qdpc.core.permissions import has_page_permission
    return user.is_superuser or has_page_permission(user, 'Groups', 'view')


@login_required
@require_admin_permission()
def unified_permission_dashboard(request):
    """Main dashboard for unified permission management"""
    
    # Get all roles (using the Role model which extends Group)
    roles = Role.objects.all().order_by('name')
    
    # Get pages organized by section
    try:
        pages_by_section = Page.get_pages_by_section()
    except:
        # Fallback to default structure if database is not ready
        pages_by_section = get_default_vssc_pages()
    
    # Get existing permissions for all groups
    group_permissions = {}
    for role in roles:
        group_permissions[role.id] = {}
        for section_name, pages in pages_by_section.items():
            for page in pages:
                group_permissions[role.id][page.name] = {}
                for perm_type, _ in PagePermission.PERMISSION_TYPES:
                    group_permissions[role.id][page.name][perm_type] = PagePermission.has_permission(
                        role, page.name, perm_type
                    )
    
    context = {
        'roles': roles,
        'pages_by_section': pages_by_section,
        'group_permissions': group_permissions,
        'permission_types': PagePermission.PERMISSION_TYPES,
    }
    
    return render(request, 'page_permission_management/unified_permissions.html', context)


@login_required
def bulk_update_permissions(request):
    """Bulk update permissions for multiple roles and pages"""
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Get all form data
                form_data = request.POST
                
                # Process each permission field
                for field_name, value in form_data.items():
                    if field_name.startswith('permission_'):
                        # Format: permission_role_id_page_name_permission_type
                        parts = field_name.split('_', 3)
                        if len(parts) == 4:
                            _, role_id, page_name, perm_type = parts
                            
                            # Find the role and page
                            try:
                                role = Role.objects.get(id=role_id)
                                
                                # Create or update the permission
                                PagePermission.objects.update_or_create(
                                    group=role,
                                    page_name=page_name,
                                    permission_type=perm_type,
                                    defaults={
                                        'page_url': get_page_url(page_name),
                                        'is_active': True
                                    }
                                )
                                
                            except Role.DoesNotExist:
                                continue
                
                messages.success(request, 'All permissions updated successfully!')
                return JsonResponse({'status': 'success', 'message': 'Permissions updated'})
                
        except Exception as e:
            messages.error(request, f'Error updating permissions: {str(e)}')
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


@login_required
@require_admin_permission()
def role_permission_summary(request):
    """Show a summary of permissions for each role"""
    
    roles = Role.objects.all().order_by('name')
    pages_by_section = Page.get_pages_by_section()
    
    # Get permission summary for each role
    role_summaries = {}
    for role in roles:
        role_summaries[role] = {
            'total_permissions': 0,
            'pages_with_permissions': 0,
            'permission_breakdown': {},
            'page_permissions': {}
        }
        
        # Get all permissions for this role
        permissions = PagePermission.objects.filter(group=role, is_active=True)
        
        for perm in permissions:
            role_summaries[role]['total_permissions'] += 1
            
            if perm.page_name not in role_summaries[role]['page_permissions']:
                role_summaries[role]['page_permissions'][perm.page_name] = []
                role_summaries[role]['pages_with_permissions'] += 1
            
            role_summaries[role]['page_permissions'][perm.page_name].append(perm.permission_type)
            
            if perm.permission_type not in role_summaries[role]['permission_breakdown']:
                role_summaries[role]['permission_breakdown'][perm.permission_type] = 0
            role_summaries[role]['permission_breakdown'][perm.permission_type] += 1
    
    context = {
        'roles': roles,
        'pages_by_section': pages_by_section,
        'role_summaries': role_summaries,
        'permission_types': PagePermission.PERMISSION_TYPES,
    }
    
    return render(request, 'page_permission_management/role_summary.html', context)


@login_required
def page_permission_summary(request):
    """Show a summary of permissions for each page"""
    
    pages_by_section = Page.get_pages_by_section()
    roles = Role.objects.all().order_by('name')
    
    # Get permission summary for each page
    page_summaries = {}
    for section_name, pages in pages_by_section.items():
        for page in pages:
            page_summaries[page.name] = {
                'section': section_name,
                'url': page.url,
                'total_permissions': 0,
                'roles_with_permissions': 0,
                'permission_breakdown': {},
                'role_permissions': {}
            }
            
            # Get all permissions for this page
            permissions = PagePermission.objects.filter(page_name=page.name, is_active=True)
            
            for perm in permissions:
                page_summaries[page.name]['total_permissions'] += 1
                
                if perm.group.name not in page_summaries[page.name]['role_permissions']:
                    page_summaries[page.name]['role_permissions'][perm.group.name] = []
                    page_summaries[page.name]['roles_with_permissions'] += 1
                
                page_summaries[page.name]['role_permissions'][perm.group.name].append(perm.permission_type)
                
                if perm.permission_type not in page_summaries[page.name]['permission_breakdown']:
                    page_summaries[page.name]['permission_breakdown'][perm.permission_type] = 0
                page_summaries[page.name]['permission_breakdown'][perm.permission_type] += 1
    
    context = {
        'pages_by_section': pages_by_section,
        'roles': roles,
        'page_summaries': page_summaries,
        'permission_types': PagePermission.PERMISSION_TYPES,
    }
    
    return render(request, 'page_permission_management/page_summary.html', context)


def get_page_url(page_name):
    """Get URL for a page name"""
    # Default URL mapping
    url_mapping = {
        'Dashboard': 'user-dashboard',
        'Equipments': 'equipment-list',
        'Acceptance Test': 'acceptance-test-list',
        'Rawmaterial': 'raw-material',
        'Rawmaterial Batch': 'raw-material-batch-fetch',
        'Consumable': 'consumable-list',
        'Consumable Batch': 'consumable-batch-fetch',
        'Component': 'component-list',
        'Component Batch': 'component-batch-fetch',
        'Process': 'process_list',
        'Product': 'product-home',
        'Product Batch': 'product-batch-list',
        'Units': 'unit-list',
        'Grade': 'grade-list',
        'Enduse': 'enduse-list',
        'Document Type': 'documenttype-list',
        'Center': 'center-list',
        'Division': 'division-list',
        'Source': 'source-list',
        'Supplier': 'supplier-list',
        'Users': 'user-list',
        'Process Log-Sheet': '#',
        'Stage Clearance': 'clearance',
        'Q.A.R-Report': '#',
        'Groups': 'group-list',
    }
    
    return url_mapping.get(page_name, '#')

def get_default_vssc_pages():
    """Fallback function to get default VSSC page structure"""
    return {
        'Pages': [
            {'id': 1, 'name': 'Dashboard', 'url': 'user-dashboard', 'icon': 'home'},
        ],
        'Product Data Management': [
            {'id': 2, 'name': 'Equipments', 'url': 'equipment-list', 'icon': 'tool'},
            {'id': 3, 'name': 'Acceptance Test', 'url': 'acceptance-test-list', 'icon': 'check-circle'},
            {'id': 4, 'name': 'Rawmaterial', 'url': 'raw-material', 'icon': 'package'},
            {'id': 5, 'name': 'Rawmaterial Batch', 'url': 'raw-material-batch-fetch', 'icon': 'layers'},
            {'id': 6, 'name': 'Consumable', 'url': 'consumable-list', 'icon': 'box'},
            {'id': 7, 'name': 'Consumable Batch', 'url': 'consumable-batch-fetch', 'icon': 'archive'},
            {'id': 8, 'name': 'Component', 'url': 'component-list', 'icon': 'cpu'},
            {'id': 9, 'name': 'Component Batch', 'url': 'component-batch-fetch', 'icon': 'hard-drive'},
            {'id': 10, 'name': 'Process', 'url': 'process_list', 'icon': 'settings'},
            {'id': 11, 'name': 'Product', 'url': 'product-home', 'icon': 'shopping-bag'},
            {'id': 12, 'name': 'Product Batch', 'url': 'product-batch-list', 'icon': 'shopping-cart'},
        ],
        'Miscellaneous Data Management': [
            {'id': 13, 'name': 'Units', 'url': 'unit-list', 'icon': 'hash'},
            {'id': 14, 'name': 'Grade', 'url': 'grade-list', 'icon': 'star'},
            {'id': 15, 'name': 'Enduse', 'url': 'enduse-list', 'icon': 'target'},
            {'id': 16, 'name': 'Document Type', 'url': 'documenttype-list', 'icon': 'file-text'},
            {'id': 17, 'name': 'Center', 'url': 'center-list', 'icon': 'map-pin'},
            {'id': 18, 'name': 'Division', 'url': 'division-list', 'icon': 'git-branch'},
            {'id': 19, 'name': 'Source', 'url': 'source-list', 'icon': 'external-link'},
            {'id': 20, 'name': 'Supplier', 'url': 'supplier-list', 'icon': 'truck'},
        ],
        'User Management': [
            {'id': 21, 'name': 'Users', 'url': 'user-list', 'icon': 'users'},
        ],
        'Report Generation': [
            {'id': 22, 'name': 'Process Log-Sheet', 'url': '#', 'icon': 'clipboard'},
            {'id': 23, 'name': 'Stage Clearance', 'url': 'clearance', 'icon': 'unlock'},
            {'id': 24, 'name': 'Q.A.R-Report', 'url': '#', 'icon': 'file-text'},
        ],
        'Roles Management': [
            {'id': 25, 'name': 'Groups', 'url': 'group-list', 'icon': 'users'},
        ]
    }
