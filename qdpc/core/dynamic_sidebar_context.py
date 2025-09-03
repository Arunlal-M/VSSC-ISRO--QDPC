from qdpc.models.page_permission import PagePermission




def dynamic_sidebar_context(request):
    """
    Context processor to provide dynamic sidebar permissions based on database PagePermission records
    This is the single source of truth for sidebar permissions - no hardcoded roles
    """
    context = {}
    
    if request.user.is_authenticated:
        # Get user's groups
        user_groups = request.user.groups.all()

        # Superadmin: full access to everything (but still check database first)
        is_superuser = request.user.is_superuser

        # For all other users, check database PagePermission records
        # This is the ONLY way permissions are determined - no hardcoded roles
        
        context.update({
            # Dashboard access (everyone gets dashboard)
            'can_access_dashboard': True,
            
            # Product Data Management
            'can_access_equipment': is_superuser or check_page_permission(user_groups, 'Equipments', 'view'),
            'can_access_acceptance_test': is_superuser or check_page_permission(user_groups, 'Acceptance Test', 'view'),
            'can_access_raw_material': is_superuser or check_page_permission(user_groups, 'Rawmaterial', 'view'),
            'can_access_raw_material_batch': is_superuser or check_page_permission(user_groups, 'Rawmaterial Batch', 'view'),
            'can_access_consumable': is_superuser or check_page_permission(user_groups, 'Consumable', 'view'),
            'can_access_consumable_batch': is_superuser or check_page_permission(user_groups, 'Consumable Batch', 'view'),
            'can_access_component': is_superuser or check_page_permission(user_groups, 'Component', 'view'),
            'can_access_component_batch': is_superuser or check_page_permission(user_groups, 'Component Batch', 'view'),
            'can_access_process': is_superuser or check_page_permission(user_groups, 'Process', 'view'),
            'can_access_product': is_superuser or check_page_permission(user_groups, 'Product', 'view'),
            'can_access_product_batch': is_superuser or check_page_permission(user_groups, 'Product Batch', 'view'),
            
            # Miscellaneous Data Management
            'can_access_units': is_superuser or check_page_permission(user_groups, 'Units', 'view'),
            'can_access_grade': is_superuser or check_page_permission(user_groups, 'Grade', 'view'),
            'can_access_enduse': is_superuser or check_page_permission(user_groups, 'Enduse', 'view'),
            'can_access_document_type': is_superuser or check_page_permission(user_groups, 'Document Type', 'view'),
            'can_access_center': is_superuser or check_page_permission(user_groups, 'Center', 'view'),
            'can_access_division': is_superuser or check_page_permission(user_groups, 'Division', 'view'),
            'can_access_source': is_superuser or check_page_permission(user_groups, 'Source', 'view'),
            'can_access_supplier': is_superuser or check_page_permission(user_groups, 'Supplier', 'view'),
            
            # User Management
            'can_access_user_management': is_superuser or check_page_permission(user_groups, 'Users', 'view'),
            
            # Report Generation
            'can_access_reports': is_superuser or check_page_permission(user_groups, 'Process Log-Sheet', 'view'),
            'can_access_stage_clearance': is_superuser or check_page_permission(user_groups, 'Stage Clearance', 'view'),
            'can_access_qar_report': is_superuser or check_page_permission(user_groups, 'Q.A.R-Report', 'view'),
            
            # Role Management
            'can_access_role_management': is_superuser or check_page_permission(user_groups, 'Groups', 'view'),
            
            # Additional permission checks for specific actions
            'can_add_equipment': is_superuser or check_page_permission(user_groups, 'Equipments', 'add'),
            'can_edit_equipment': is_superuser or check_page_permission(user_groups, 'Equipments', 'edit'),
            'can_delete_equipment': is_superuser or check_page_permission(user_groups, 'Equipments', 'delete'),
            
            'can_add_raw_material': is_superuser or check_page_permission(user_groups, 'Rawmaterial', 'add'),
            'can_edit_raw_material': is_superuser or check_page_permission(user_groups, 'Rawmaterial', 'edit'),
            'can_delete_raw_material': is_superuser or check_page_permission(user_groups, 'Rawmaterial', 'delete'),
            
            'can_add_consumable': is_superuser or check_page_permission(user_groups, 'Consumable', 'add'),
            'can_edit_consumable': is_superuser or check_page_permission(user_groups, 'Consumable', 'edit'),
            'can_delete_consumable': is_superuser or check_page_permission(user_groups, 'Consumable', 'delete'),
            
            'can_add_component': is_superuser or check_page_permission(user_groups, 'Component', 'add'),
            'can_edit_component': is_superuser or check_page_permission(user_groups, 'Component', 'edit'),
            'can_delete_component': is_superuser or check_page_permission(user_groups, 'Component', 'delete'),
            
            'can_add_process': is_superuser or check_page_permission(user_groups, 'Process', 'add'),
            'can_edit_process': is_superuser or check_page_permission(user_groups, 'Process', 'edit'),
            'can_delete_process': is_superuser or check_page_permission(user_groups, 'Process', 'delete'),
            
            'can_add_product': is_superuser or check_page_permission(user_groups, 'Product', 'add'),
            'can_edit_product': is_superuser or check_page_permission(user_groups, 'Product', 'edit'),
            'can_delete_product': is_superuser or check_page_permission(user_groups, 'Product', 'delete'),
            
            # User's groups for display
            'user_groups': user_groups,
        })
        
    else:
        # For anonymous users, set all permissions to False
        context.update({
            'can_access_dashboard': False,
            'can_access_equipment': False,
            'can_access_acceptance_test': False,
            'can_access_raw_material': False,
            'can_access_raw_material_batch': False,
            'can_access_consumable': False,
            'can_access_consumable_batch': False,
            'can_access_component': False,
            'can_access_component_batch': False,
            'can_access_process': False,
            'can_access_product': False,
            'can_access_product_batch': False,
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
            'user_groups': [],
        })
    
    return context


def check_page_permission(user_groups, page_name, permission_type):
    """
    Check if any of the user's groups have a specific permission for a page
    This is the ONLY way permissions are checked - from database PagePermission records
    """
    if not user_groups:
        return False
    
    # Check if any group has the required PagePermission (custom table)
    for group in user_groups:
        if PagePermission.objects.filter(
            group=group,
            page_name=page_name,
            permission_type=permission_type,
            is_active=True
        ).exists():
            return True

    return False
