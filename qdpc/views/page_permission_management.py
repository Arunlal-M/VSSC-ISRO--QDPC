from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
import json

from qdpc.models.page_permission import Page, PagePermission
from qdpc.core.decorators import require_admin_permission


def is_admin_user(user):
    """Check if user is admin or has role management access"""
    from qdpc.core.permissions import has_page_permission
    return user.is_superuser or has_page_permission(user, 'Groups', 'view')


@login_required
@require_admin_permission()
def page_permission_dashboard(request):
    """Dashboard showing all pages and user's role permissions"""
    
    # Get pages from database or use default structure
    try:
        pages_by_section = Page.get_pages_by_section()
    except:
        # Fallback to hardcoded structure if database is not ready
        pages_by_section = get_default_vssc_pages()
    
    # Get user's groups and permissions
    user_groups = request.user.groups.all()
    user_permissions = set()
    
    for group in user_groups:
        group_permissions = group.permissions.all()
        for perm in group_permissions:
            user_permissions.add(f"{perm.content_type.app_label}.{perm.content_type.model}.{perm.codename}")
    
    # Check page access based on user permissions
    for section_name, pages in pages_by_section.items():
        for page in pages:
            if hasattr(page, 'has_access'):
                continue
            page.has_access = check_page_access(page, user_permissions)
            page.permission_level = get_permission_level(page, user_permissions)
    
    context = {
        'pages_by_section': pages_by_section,
        'user_groups': user_groups,
        'user_permissions': user_permissions,
    }
    
    return render(request, 'page_permission_management/dashboard.html', context)


@login_required
@require_admin_permission()
def manage_page_permissions(request):
    """Main page permission management interface"""
    
    groups = Group.objects.all().order_by('name')
    pages_by_section = Page.get_pages_by_section()
    
    # Get existing permissions for all groups
    group_permissions = {}
    for group in groups:
        group_permissions[group.id] = {}
        for section_name, pages in pages_by_section.items():
            for page in pages:
                group_permissions[group.id][page.name] = {}
                for perm_type, _ in PagePermission.PERMISSION_TYPES:
                    group_permissions[group.id][page.name][perm_type] = PagePermission.has_permission(
                        group, page.name, perm_type
                    )


    
    context = {
        'groups': groups,
        'pages_by_section': pages_by_section,
        'group_permissions': group_permissions,
        'permission_types': PagePermission.PERMISSION_TYPES,
    }
    
    return render(request, 'page_permission_management/manage_permissions.html', context)


@login_required
@require_admin_permission()
def group_page_permissions(request, group_id):
    """Manage page permissions for a specific group"""
    
    group = get_object_or_404(Group, id=group_id)
    pages_by_section = Page.get_pages_by_section()
    
    # Get existing permissions for this group
    group_permissions = {}
    for section_name, pages in pages_by_section.items():
        for page in pages:
            group_permissions[page.name] = {}
            for perm_type, _ in PagePermission.PERMISSION_TYPES:
                group_permissions[page.name][perm_type] = PagePermission.has_permission(
                    group, page.name, perm_type
                )


    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Clear existing permissions for this group
                PagePermission.objects.filter(group=group).delete()
                
                # Create new permissions based on form data
                for page_name, permissions in request.POST.items():
                    if page_name.startswith('permission_'):
                        # Extract page name and permission type from form field name
                        # Format: permission_page_name_permission_type
                        parts = page_name.split('_', 2)
                        if len(parts) == 3:
                            _, page_name, perm_type = parts
                            
                            # Find the page object
                            page = None
                            for section_pages in pages_by_section.values():
                                for p in section_pages:
                                    if p.name == page_name:
                                        page = p
                                        break
                                if page:
                                    break
                            
                            if page and perm_type in [pt[0] for pt in PagePermission.PERMISSION_TYPES]:
                                PagePermission.objects.create(
                                    group=group,
                                    page_name=page.name,
                                    page_url=page.url,
                                    permission_type=perm_type,
                                    is_active=True
                                )
                
                messages.success(request, f'Page permissions updated successfully for group "{group.name}"!')
                return redirect('manage-page-permissions')
                
        except Exception as e:
            messages.error(request, f'Error updating permissions: {str(e)}')
    
    context = {
        'group': group,
        'pages_by_section': pages_by_section,
        'group_permissions': group_permissions,
        'permission_types': PagePermission.PERMISSION_TYPES,
    }
    
    return render(request, 'page_permission_management/group_permissions.html', context)


@csrf_exempt
def update_page_permission(request):
    """AJAX endpoint to update a single page permission"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            group_id = data.get('group_id')
            page_name = data.get('page_name')
            permission_type = data.get('permission_type')
            enabled = data.get('enabled')
            
            if not all([group_id, page_name, permission_type, enabled is not None]):
                return JsonResponse({'status': 'error', 'message': 'Missing required parameters'})
            
            group = get_object_or_404(Group, id=group_id)
            
            if enabled:
                # Create or update permission
                PagePermission.objects.update_or_create(
                    group=group,
                    page_name=page_name,
                    permission_type=permission_type,
                    defaults={'is_active': True}
                )
            else:
                # Remove permission
                PagePermission.objects.filter(
                    group=group,
                    page_name=page_name,
                    permission_type=permission_type
                ).delete()
            
            return JsonResponse({'status': 'success', 'message': 'Permission updated'})
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def check_page_access(page, user_permissions):
    """Check if user has access to a specific page based on permissions"""
    
    # Define permission mappings for each page
    page_permissions = {
        'Dashboard': ['auth.view_user', 'qdpc_core_models.view_product'],
        'Equipments': ['equipment.view_equipment'],
        'Acceptance Test': ['qdpc_core_models.view_acceptancetest'],
        'Rawmaterial': ['qdpc_core_models.view_rawmaterial'],
        'Rawmaterial Batch': ['qdpc_core_models.view_rawmaterialbatch'],
        'Consumable': ['consumable.view_consumable'],
        'Consumable Batch': ['consumable.view_consumablebatch'],
        'Component': ['component.view_component'],
        'Component Batch': ['component.view_componentbatch'],
        'Process': ['process.view_process'],
        'Product': ['qdpc_core_models.view_product'],
        'Product Batch': ['qdpc_core_models.view_productbatch'],
        'Units': ['qdpc_core_models.view_unit'],
        'Grade': ['qdpc_core_models.view_grade'],
        'Enduse': ['qdpc_core_models.view_enduse'],
        'Document Type': ['qdpc_core_models.view_documenttype'],
        'Center': ['qdpc_core_models.view_center'],
        'Division': ['qdpc_core_models.view_division'],
        'Source': ['qdpc_core_models.view_source'],
        'Supplier': ['qdpc_core_models.view_supplier'],
        'Users': ['user.view_user'],
        'Process Log-Sheet': ['qdpc_core_models.view_processlog'],
        'Stage Clearance': ['stage_clearance.view_stageclearance'],
        'Q.A.R-Report': ['qdpc_core_models.view_qarreport'],
        'Groups': ['auth.view_group'],
    }
    
    required_permissions = page_permissions.get(page.name, [])
    
    # Check if user has any of the required permissions
    for perm in required_permissions:
        if perm in user_permissions:
            return True
    
    return False


def get_permission_level(page, user_permissions):
    """Get the permission level for a page (view, add, edit, delete)"""
    
    page_name = page.name
    base_model = get_base_model_name(page_name)
    
    if not base_model:
        return 'no_access'
    
    # Check different permission levels
    view_perm = f"{base_model}.view_{base_model.lower()}"
    add_perm = f"{base_model}.add_{base_model.lower()}"
    change_perm = f"{base_model}.change_{base_model.lower()}"
    delete_perm = f"{base_model}.delete_{base_model.lower()}"
    
    if delete_perm in user_permissions:
        return 'full_access'
    elif change_perm in user_permissions:
        return 'edit_access'
    elif add_perm in user_permissions:
        return 'add_access'
    elif view_perm in user_permissions:
        return 'view_access'
    else:
        return 'no_access'


def get_base_model_name(page_name):
    """Get the base model name for permission checking"""
    
    model_mapping = {
        'Dashboard': 'qdpc_core_models',
        'Equipments': 'equipment',
        'Acceptance Test': 'qdpc_core_models',
        'Rawmaterial': 'qdpc_core_models',
        'Rawmaterial Batch': 'qdpc_core_models',
        'Consumable': 'consumable',
        'Consumable Batch': 'consumable',
        'Component': 'component',
        'Component Batch': 'component',
        'Process': 'process',
        'Product': 'qdpc_core_models',
        'Product Batch': 'qdpc_core_models',
        'Units': 'qdpc_core_models',
        'Grade': 'qdpc_core_models',
        'Enduse': 'qdpc_core_models',
        'Document Type': 'qdpc_core_models',
        'Center': 'qdpc_core_models',
        'Division': 'qdpc_core_models',
        'Source': 'qdpc_core_models',
        'Supplier': 'qdpc_core_models',
        'Users': 'user',
        'Process Log-Sheet': 'qdpc_core_models',
        'Stage Clearance': 'stage_clearance',
        'Q.A.R-Report': 'qdpc_core_models',
        'Groups': 'auth',
    }
    
    return model_mapping.get(page_name, 'qdpc_core_models')


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
