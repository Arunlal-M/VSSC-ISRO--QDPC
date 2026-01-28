from django.contrib.auth.models import Group
from qdpc.models.page_permission import PagePermission
from qdpc.core.permissions import has_page_permission

class ProductBatchPermissionService:
    """SINGLE SOURCE OF TRUTH for Product Batch permissions using PagePermission system"""
    
    # Define the exact page name as it appears in your permission dashboard
    PAGE_NAME = 'Product batch'  # Note: lowercase 'b' as shown in dashboard
    
    @staticmethod
    def check_user_permission(user, permission_type):
        """
        Check if user has a specific permission for Product Batch
        Uses the centralized has_page_permission function
        
        Args:
            user: Django user object
            permission_type: 'view', 'add', 'edit', 'delete', 'approve'
        
        Returns:
            bool: True if user has permission, False otherwise
        """
        return has_page_permission(user, ProductBatchPermissionService.PAGE_NAME, permission_type)
    
    @staticmethod
    def get_user_permissions(user):
        """
        Get all permissions for a user for Product Batch
        Uses the centralized permission system
        
        Returns:
            dict: Dictionary with permission types as keys and boolean values
        """
        return {
            'view': has_page_permission(user, ProductBatchPermissionService.PAGE_NAME, 'view'),
            'add': has_page_permission(user, ProductBatchPermissionService.PAGE_NAME, 'add'),
            'edit': has_page_permission(user, ProductBatchPermissionService.PAGE_NAME, 'edit'),
            'delete': has_page_permission(user, ProductBatchPermissionService.PAGE_NAME, 'delete'),
            'approve': has_page_permission(user, ProductBatchPermissionService.PAGE_NAME, 'approve')
        }
    
    @staticmethod
    def debug_user_permissions(user):
        """
        Debug function to show what permissions a user has
        
        Returns:
            str: Debug information about user permissions
        """
        if not user.is_authenticated:
            return "User not authenticated"
            
        debug_info = f"User: {user.username}\n"
        debug_info += f"Superuser: {user.is_superuser}\n"
        debug_info += f"Groups: {[g.name for g in user.groups.all()]}\n\n"
        
        if user.is_superuser:
            debug_info += "Superuser - has all permissions\n"
            return debug_info
            
        # Check PagePermission records
        user_groups = user.groups.all()
        debug_info += f"PagePermission Records for '{ProductBatchPermissionService.PAGE_NAME}':\n"
        
        for group in user_groups:
            debug_info += f"\nGroup: {group.name}\n"
            group_permissions = PagePermission.objects.filter(
                group=group,
                page_name=ProductBatchPermissionService.PAGE_NAME,
                is_active=True
            )
            
            if group_permissions.exists():
                for perm in group_permissions:
                    debug_info += f"  - {perm.permission_type}: {perm.is_active}\n"
            else:
                debug_info += f"  - No '{ProductBatchPermissionService.PAGE_NAME}' permissions found\n"
                
        # Check what permissions this user actually has
        actual_permissions = ProductBatchPermissionService.get_user_permissions(user)
        debug_info += f"\nFinal Permissions:\n"
        for perm_type, has_perm in actual_permissions.items():
            debug_info += f"  - {perm_type}: {has_perm}\n"
            
        return debug_info
    
    @staticmethod
    def get_page_permission_context(user):
        """
        Get the complete permission context for templates
        
        Returns:
            dict: Complete permission context for templates
        """
        if not user.is_authenticated:
            return {
                'can_access_product_batch': False,
                'can_add_product_batch': False,
                'can_edit_product_batch': False,
                'can_delete_product_batch': False,
                'can_approve_product_batch': False,
            }
        
        # Get permissions from PagePermission system
        user_permissions = ProductBatchPermissionService.get_user_permissions(user)
        
        return {
            'can_access_product_batch': user.is_superuser or user_permissions['view'],
            'can_add_product_batch': user.is_superuser or user_permissions['add'],
            'can_edit_product_batch': user.is_superuser or user_permissions['edit'],
            'can_delete_product_batch': user.is_superuser or user_permissions['delete'],
            'can_approve_product_batch': user.is_superuser or user_permissions['approve'],
        }
