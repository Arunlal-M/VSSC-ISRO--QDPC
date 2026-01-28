from django.contrib.auth.models import Group
from qdpc_core_models.models.role import Role
from qdpc.core.permissions import (
    get_user_page_permissions,
    has_page_permission,
    get_user_accessible_pages
)


def get_default_permissions():
    return {
        'user_page_permissions': {},
        'user_accessible_pages': [],
        'user_has_all_access': False,
        'user_role_name': None,
        'user_group_names': [],
        'can_access_dashboard': False,
        'can_access_equipment': False,
        'can_access_acceptance_test': False,
        'can_access_raw_material': False,
        'can_access_raw_material_batch': False,
        'can_access_consumable': False,
        'can_access_consumable_batch': False,
        'can_access_component': False,
        'can_access_component_batch': False,
        'can_access_product': False,
        'can_access_product_batch': False,
        'can_access_process': False,
        'can_access_units': False,
        'can_access_grade': False,
        'can_access_enduse': False,
        'can_access_document_type': False,
        'can_access_center': False,
        'can_access_division': False,
        'can_access_source': False,
        'can_access_supplier': False,
        'can_access_user_management': False,
        'can_access_reports': False,
        'can_access_stage_clearance': False,
        'can_access_qar_report': False,
        'can_access_role_management': False,
        'can_access_permission_management': False,
    }


def get_admin_permissions():
    """Return full permissions for super admin and administrative roles"""
    return {
        'user_page_permissions': {'ALL': ['view', 'add', 'edit', 'delete', 'approve', 'reject']},
        'user_accessible_pages': ['ALL'],
        'user_has_all_access': True,
        
        # Dashboard access
        'can_access_dashboard': True,
        
        # Equipment permissions
        'can_access_equipment': True,
        'can_add_equipment': True,
        'can_edit_equipment': True,
        'can_delete_equipment': True,
        
        # Acceptance Test permissions
        'can_access_acceptance_test': True,
        'can_add_acceptance_test': True,
        'can_edit_acceptance_test': True,
        'can_delete_acceptance_test': True,
        'can_approve_acceptance_test': True,
        'can_reject_acceptance_test': True,
        
        # Raw Material permissions
        'can_access_raw_material': True,
        'can_add_raw_material': True,
        'can_edit_raw_material': True,
        'can_delete_raw_material': True,
        
        # Raw Material Batch permissions
        'can_access_raw_material_batch': True,
        'can_add_raw_material_batch': True,
        'can_edit_raw_material_batch': True,
        'can_delete_raw_material_batch': True,
        
        # Consumable permissions
        'can_access_consumable': True,
        'can_add_consumable': True,
        'can_edit_consumable': True,
        'can_delete_consumable': True,
        
        # Consumable Batch permissions
        'can_access_consumable_batch': True,
        'can_add_consumable_batch': True,
        'can_edit_consumable_batch': True,
        'can_delete_consumable_batch': True,
        
        # Component permissions
        'can_access_component': True,
        'can_add_component': True,
        'can_edit_component': True,
        'can_delete_component': True,
        
        # Component Batch permissions
        'can_access_component_batch': True,
        'can_add_component_batch': True,
        'can_edit_component_batch': True,
        'can_delete_component_batch': True,
        
        # Product permissions
        'can_access_product': True,
        'can_add_product': True,
        'can_edit_product': True,
        'can_delete_product': True,
        
        # Product Batch permissions
        'can_access_product_batch': True,
        'can_add_product_batch': True,
        'can_edit_product_batch': True,
        'can_delete_product_batch': True,
        'can_approve_product_batch': True,
        'can_reject_product_batch': True,
        
        # Process permissions
        'can_access_process': True,
        'can_add_process': True,
        'can_edit_process': True,
        'can_delete_process': True,
        
        # Miscellaneous permissions
        'can_access_units': True,
        'can_add_units': True,
        'can_edit_units': True,
        'can_delete_units': True,
        
        'can_access_grade': True,
        'can_add_grade': True,
        'can_edit_grade': True,
        'can_delete_grade': True,
        
        'can_access_enduse': True,
        'can_add_enduse': True,
        'can_edit_enduse': True,
        'can_delete_enduse': True,
        
        'can_access_document_type': True,
        'can_add_document_type': True,
        'can_edit_document_type': True,
        'can_delete_document_type': True,
        
        'can_access_center': True,
        'can_add_center': True,
        'can_edit_center': True,
        'can_delete_center': True,
        
        'can_access_division': True,
        'can_add_division': True,
        'can_edit_division': True,
        'can_delete_division': True,
        
        'can_access_source': True,
        'can_add_source': True,
        'can_edit_source': True,
        'can_delete_source': True,
        
        'can_access_supplier': True,
        'can_add_supplier': True,
        'can_edit_supplier': True,
        'can_delete_supplier': True,
        
        # User Management permissions
        'can_access_user_management': True,
        'can_add_user_management': True,
        'can_edit_user_management': True,
        'can_delete_user_management': True,
        
        # Report permissions
        'can_access_reports': True,
        'can_generate_reports': True,
        
        'can_access_stage_clearance': True,
        'can_add_stage_clearance': True,
        'can_edit_stage_clearance': True,
        'can_delete_stage_clearance': True,
        
        'can_access_qar_report': True,
        'can_generate_qar_report': True,
        
        # Role Management permissions
        'can_access_role_management': True,
        'can_add_role_management': True,
        'can_edit_role_management': True,
        'can_delete_role_management': True,
        
        # Permission Management permissions
        'can_access_permission_management': True,
        'can_edit_permission_management': True,
    }


def user_permissions(request):
    """Context processor to provide user permissions to all templates"""
    if not request.user.is_authenticated:
        return get_default_permissions()

    # Super users and admin roles have all permissions by default
    if request.user.is_superuser:
        return get_admin_permissions()
    
    # Check if user belongs to administrative roles
    admin_group_names = {
        'System Administrator', 'Super Admin', 'SYSTEM ADMINISTRATOR', 'SUPER ADMIN',
        'Master Admin/Super Admin', 'Roles- System administrator',
        'System Administrator-1', 'System Administrator-2', 'System Administrator-3'
    }
    
    user_groups = request.user.groups.all()
    if user_groups.filter(name__in=admin_group_names).exists():
        return get_admin_permissions()

    # Get all page permissions using PagePermission model only
    user_page_permissions = get_user_page_permissions(request.user)
    user_accessible_pages = get_user_accessible_pages(request.user)

    # Build permission flags for templates
    permissions = {
        # Dashboard access
        'can_access_dashboard': has_page_permission(request.user, 'Dashboard', 'view'),
        
        # Equipment permissions
        'can_access_equipment': has_page_permission(request.user, 'Equipment', 'view'),
        'can_add_equipment': has_page_permission(request.user, 'Equipment', 'add'),
        'can_edit_equipment': has_page_permission(request.user, 'Equipment', 'edit'),
        'can_delete_equipment': has_page_permission(request.user, 'Equipment', 'delete'),
        
        # Acceptance Test permissions
        'can_access_acceptance_test': has_page_permission(request.user, 'Acceptance test', 'view'),
        'can_add_acceptance_test': has_page_permission(request.user, 'Acceptance test', 'add'),
        'can_edit_acceptance_test': has_page_permission(request.user, 'Acceptance test', 'edit'),
        'can_delete_acceptance_test': has_page_permission(request.user, 'Acceptance test', 'delete'),
        'can_approve_acceptance_test': has_page_permission(request.user, 'Acceptance test', 'approve'),
        'can_reject_acceptance_test': has_page_permission(request.user, 'Acceptance test', 'reject'),
        
        # Raw Material permissions
        'can_access_raw_material': has_page_permission(request.user, 'Raw material', 'view'),
        'can_add_raw_material': has_page_permission(request.user, 'Raw material', 'add'),
        'can_edit_raw_material': has_page_permission(request.user, 'Raw material', 'edit'),
        'can_delete_raw_material': has_page_permission(request.user, 'Raw material', 'delete'),
        
        # Raw Material Batch permissions
        'can_access_raw_material_batch': has_page_permission(request.user, 'Raw material batch', 'view'),
        'can_add_raw_material_batch': has_page_permission(request.user, 'Raw material batch', 'add'),
        'can_edit_raw_material_batch': has_page_permission(request.user, 'Raw material batch', 'edit'),
        'can_delete_raw_material_batch': has_page_permission(request.user, 'Raw material batch', 'delete'),
        
        # Consumable permissions
        'can_access_consumable': has_page_permission(request.user, 'Consumable', 'view'),
        'can_add_consumable': has_page_permission(request.user, 'Consumable', 'add'),
        'can_edit_consumable': has_page_permission(request.user, 'Consumable', 'edit'),
        'can_delete_consumable': has_page_permission(request.user, 'Consumable', 'delete'),
        
        # Consumable Batch permissions
        'can_access_consumable_batch': has_page_permission(request.user, 'Consumable batch', 'view'),
        'can_add_consumable_batch': has_page_permission(request.user, 'Consumable batch', 'add'),
        'can_edit_consumable_batch': has_page_permission(request.user, 'Consumable batch', 'edit'),
        'can_delete_consumable_batch': has_page_permission(request.user, 'Consumable batch', 'delete'),
        
        # Component permissions
        'can_access_component': has_page_permission(request.user, 'Component', 'view'),
        'can_add_component': has_page_permission(request.user, 'Component', 'add'),
        'can_edit_component': has_page_permission(request.user, 'Component', 'edit'),
        'can_delete_component': has_page_permission(request.user, 'Component', 'delete'),
        
        # Component Batch permissions
        'can_access_component_batch': has_page_permission(request.user, 'Component batch', 'view'),
        'can_add_component_batch': has_page_permission(request.user, 'Component batch', 'add'),
        'can_edit_component_batch': has_page_permission(request.user, 'Component batch', 'edit'),
        'can_delete_component_batch': has_page_permission(request.user, 'Component batch', 'delete'),
        
        # Product permissions
        'can_access_product': has_page_permission(request.user, 'Product', 'view'),
        'can_add_product': has_page_permission(request.user, 'Product', 'add'),
        'can_edit_product': has_page_permission(request.user, 'Product', 'edit'),
        'can_delete_product': has_page_permission(request.user, 'Product', 'delete'),
        
        # Product Batch permissions - Fixed page name consistency
        'can_access_product_batch': has_page_permission(request.user, 'Product batch', 'view'),
        'can_add_product_batch': has_page_permission(request.user, 'Product batch', 'add'),
        'can_edit_product_batch': has_page_permission(request.user, 'Product batch', 'edit'),
        'can_delete_product_batch': has_page_permission(request.user, 'Product batch', 'delete'),
        'can_approve_product_batch': has_page_permission(request.user, 'Product batch', 'approve'),
        'can_reject_product_batch': has_page_permission(request.user, 'Product batch', 'reject'),
        
        # Process permissions
        'can_access_process': has_page_permission(request.user, 'Process', 'view'),
        'can_add_process': has_page_permission(request.user, 'Process', 'add'),
        'can_edit_process': has_page_permission(request.user, 'Process', 'edit'),
        'can_delete_process': has_page_permission(request.user, 'Process', 'delete'),
        
        # Miscellaneous permissions
        'can_access_units': has_page_permission(request.user, 'Units', 'view'),
        'can_add_units': has_page_permission(request.user, 'Units', 'add'),
        'can_edit_units': has_page_permission(request.user, 'Units', 'edit'),
        'can_delete_units': has_page_permission(request.user, 'Units', 'delete'),
        
        'can_access_grade': has_page_permission(request.user, 'Grade', 'view'),
        'can_add_grade': has_page_permission(request.user, 'Grade', 'add'),
        'can_edit_grade': has_page_permission(request.user, 'Grade', 'edit'),
        'can_delete_grade': has_page_permission(request.user, 'Grade', 'delete'),
        
        'can_access_enduse': has_page_permission(request.user, 'Enduse', 'view'),
        'can_add_enduse': has_page_permission(request.user, 'Enduse', 'add'),
        'can_edit_enduse': has_page_permission(request.user, 'Enduse', 'edit'),
        'can_delete_enduse': has_page_permission(request.user, 'Enduse', 'delete'),
        
        'can_access_document_type': has_page_permission(request.user, 'Document type', 'view'),
        'can_add_document_type': has_page_permission(request.user, 'Document type', 'add'),
        'can_edit_document_type': has_page_permission(request.user, 'Document type', 'edit'),
        'can_delete_document_type': has_page_permission(request.user, 'Document type', 'delete'),
        
        'can_access_center': has_page_permission(request.user, 'Center', 'view'),
        'can_add_center': has_page_permission(request.user, 'Center', 'add'),
        'can_edit_center': has_page_permission(request.user, 'Center', 'edit'),
        'can_delete_center': has_page_permission(request.user, 'Center', 'delete'),
        
        'can_access_division': has_page_permission(request.user, 'Division', 'view'),
        'can_add_division': has_page_permission(request.user, 'Division', 'add'),
        'can_edit_division': has_page_permission(request.user, 'Division', 'edit'),
        'can_delete_division': has_page_permission(request.user, 'Division', 'delete'),
        
        'can_access_source': has_page_permission(request.user, 'Source', 'view'),
        'can_add_source': has_page_permission(request.user, 'Source', 'add'),
        'can_edit_source': has_page_permission(request.user, 'Source', 'edit'),
        'can_delete_source': has_page_permission(request.user, 'Source', 'delete'),
        
        'can_access_supplier': has_page_permission(request.user, 'Supplier', 'view'),
        'can_add_supplier': has_page_permission(request.user, 'Supplier', 'add'),
        'can_edit_supplier': has_page_permission(request.user, 'Supplier', 'edit'),
        'can_delete_supplier': has_page_permission(request.user, 'Supplier', 'delete'),
        
        # User Management permissions
        'can_access_user_management': has_page_permission(request.user, 'User management', 'view'),
        'can_add_user_management': has_page_permission(request.user, 'User management', 'add'),
        'can_edit_user_management': has_page_permission(request.user, 'User management', 'edit'),
        'can_delete_user_management': has_page_permission(request.user, 'User management', 'delete'),
        
        # Report permissions
        'can_access_reports': has_page_permission(request.user, 'Reports', 'view'),
        'can_generate_reports': has_page_permission(request.user, 'Reports', 'add'),
        
        'can_access_stage_clearance': has_page_permission(request.user, 'Stage clearance', 'view'),
        'can_add_stage_clearance': has_page_permission(request.user, 'Stage clearance', 'add'),
        'can_edit_stage_clearance': has_page_permission(request.user, 'Stage clearance', 'edit'),
        'can_delete_stage_clearance': has_page_permission(request.user, 'Stage clearance', 'delete'),
        
        'can_access_qar_report': has_page_permission(request.user, 'QAR report', 'view'),
        'can_generate_qar_report': has_page_permission(request.user, 'QAR report', 'add'),
        
        # Role Management permissions
        'can_access_role_management': has_page_permission(request.user, 'Role management', 'view'),
        'can_add_role_management': has_page_permission(request.user, 'Role management', 'add'),
        'can_edit_role_management': has_page_permission(request.user, 'Role management', 'edit'),
        'can_delete_role_management': has_page_permission(request.user, 'Role management', 'delete'),
        
        # Permission Management permissions
        'can_access_permission_management': has_page_permission(request.user, 'Permission management', 'view'),
        'can_edit_permission_management': has_page_permission(request.user, 'Permission management', 'edit'),
        
        # Additional context
        'user_page_permissions': user_page_permissions,
        'user_accessible_pages': user_accessible_pages,
    }
    
    return permissions


def user_context(request):
    """Context processor to provide user role and group information to all templates"""
    context = {}
    
    if request.user.is_authenticated:
        # Get user role information
        user_role_name = None
        user_group_names = []
        
        try:
            # First check if user has a custom role assigned
            if hasattr(request.user, 'role') and request.user.role:
                user_role_name = request.user.role.name
            # Then check Django groups (this is what most users will have)
            elif request.user.groups.exists():
                user_group_names = list(request.user.groups.values_list('name', flat=True))
                # Use the first group as the primary role
                if user_group_names:
                    user_role_name = user_group_names[0]
        except Exception as e:
            user_role_name = None
            user_group_names = []
        
        # Get all page permissions using PagePermission model only
        user_page_permissions = get_user_page_permissions(request.user)
        user_accessible_pages = get_user_accessible_pages(request.user)
        
        context.update({
            'user_role_name': user_role_name,
            'user_group_names': user_group_names,
            'user_page_permissions': user_page_permissions,
            'user_accessible_pages': user_accessible_pages,
            'user_has_all_access': request.user.is_superuser,
        })
    
    return context
