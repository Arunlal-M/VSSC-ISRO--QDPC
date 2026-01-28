#!/usr/bin/env python
"""
Setup script to ensure super admin and administrative roles have all permissions by default.
This script creates default permissions for all administrative roles automatically.
"""

import os
import sys
import django

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qdpc.settings')
django.setup()

from django.contrib.auth.models import Group
from qdpc_core_models.models.page_permission import PagePermission


def setup_admin_permissions():
    """Setup default full permissions for administrative roles"""
    print("Setting up default permissions for administrative roles...")
    
    # Define administrative role names
    admin_roles = [
        'System Administrator',
        'Super Admin', 
        'SYSTEM ADMINISTRATOR',
        'SUPER ADMIN',
        'Master Admin/Super Admin',
        'Roles- System administrator',
        'System Administrator-1',
        'System Administrator-2', 
        'System Administrator-3'
    ]
    
    # Define all pages and their permissions
    pages_permissions = {
        'Dashboard': ['view'],
        'Equipment': ['view', 'add', 'edit', 'delete'],
        'Acceptance test': ['view', 'add', 'edit', 'delete', 'approve', 'reject'],
        'Raw material': ['view', 'add', 'edit', 'delete'],
        'Raw material batch': ['view', 'add', 'edit', 'delete'],
        'Consumable': ['view', 'add', 'edit', 'delete'],
        'Consumable batch': ['view', 'add', 'edit', 'delete'],
        'Component': ['view', 'add', 'edit', 'delete'],
        'Component batch': ['view', 'add', 'edit', 'delete'],
        'Product': ['view', 'add', 'edit', 'delete'],
        'Product batch': ['view', 'add', 'edit', 'delete', 'approve', 'reject'],
        'Process': ['view', 'add', 'edit', 'delete'],
        'Units': ['view', 'add', 'edit', 'delete'],
        'Grade': ['view', 'add', 'edit', 'delete'],
        'Enduse': ['view', 'add', 'edit', 'delete'],
        'Document type': ['view', 'add', 'edit', 'delete'],
        'Center': ['view', 'add', 'edit', 'delete'],
        'Division': ['view', 'add', 'edit', 'delete'],
        'Source': ['view', 'add', 'edit', 'delete'],
        'Supplier': ['view', 'add', 'edit', 'delete'],
        'User management': ['view', 'add', 'edit', 'delete'],
        'Reports': ['view', 'add'],
        'Stage clearance': ['view', 'add', 'edit', 'delete'],
        'QAR report': ['view', 'add'],
        'Role management': ['view', 'add', 'edit', 'delete'],
        'Permission management': ['view', 'edit']
    }
    
    created_count = 0
    updated_count = 0
    
    for role_name in admin_roles:
        print(f"\nProcessing role: {role_name}")
        
        # Get or create the group
        group, group_created = Group.objects.get_or_create(name=role_name)
        
        if group_created:
            print(f'  ✓ Created group: {role_name}')
        else:
            print(f'  → Group exists: {role_name}')
        
        # Set permissions for this group
        for page_name, actions in pages_permissions.items():
            for action in actions:
                permission, created = PagePermission.objects.get_or_create(
                    group=group,
                    page_name=page_name,
                    action=action,
                    defaults={'is_allowed': True}
                )
                
                if created:
                    created_count += 1
                    print(f'    ✓ Created: {page_name} - {action}')
                elif not permission.is_allowed:
                    permission.is_allowed = True
                    permission.save()
                    updated_count += 1
                    print(f'    ✓ Enabled: {page_name} - {action}')
    
    print(f'\n{"="*60}')
    print('SETUP COMPLETE')
    print(f'{"="*60}')
    print(f'Created {created_count} new permissions')
    print(f'Updated {updated_count} existing permissions')
    
    # Summary of administrative roles
    print(f'\n{"="*60}')
    print('ADMINISTRATIVE ROLES WITH FULL PERMISSIONS:')
    print(f'{"="*60}')
    
    for role_name in admin_roles:
        try:
            group = Group.objects.get(name=role_name)
            perm_count = PagePermission.objects.filter(group=group, is_allowed=True).count()
            print(f'{role_name}: {perm_count} permissions')
        except Group.DoesNotExist:
            print(f'{role_name}: Group not found')
    
    print(f'\n✅ All administrative roles now have full permissions by default!')
    print('Users in these roles will have access to all features regardless of checkbox settings.')
    
    return created_count, updated_count


def verify_admin_access():
    """Verify that admin roles have proper access"""
    print(f'\n{"="*60}')
    print('VERIFICATION: Admin Role Access')
    print(f'{"="*60}')
    
    from qdpc.core.permissions import has_page_permission
    from django.contrib.auth.models import User
    
    # Test with a sample admin user if exists
    admin_users = User.objects.filter(groups__name__in=[
        'System Administrator', 'Super Admin'
    ]).distinct()[:3]
    
    test_permissions = [
        ('Product batch', 'view'),
        ('Product batch', 'add'),
        ('Product batch', 'edit'),
        ('Product batch', 'delete'),
        ('Product batch', 'approve'),
        ('Equipment', 'view'),
        ('Equipment', 'add'),
        ('Acceptance test', 'view'),
        ('Acceptance test', 'add'),
    ]
    
    for user in admin_users:
        print(f'\nTesting user: {user.username}')
        print(f'Groups: {", ".join([g.name for g in user.groups.all()])}')
        
        for page_name, action in test_permissions:
            has_perm = has_page_permission(user, page_name, action)
            status = '✓' if has_perm else '✗'
            print(f'  {status} {page_name} - {action}')
    
    if not admin_users:
        print('No admin users found for testing.')
        print('Create users and assign them to administrative groups to test.')


if __name__ == '__main__':
    try:
        created, updated = setup_admin_permissions()
        verify_admin_access()
        
        print(f'\n{"="*60}')
        print('NEXT STEPS:')
        print(f'{"="*60}')
        print('1. Assign users to administrative groups')
        print('2. Test login with admin users')
        print('3. Verify all buttons and menus are visible')
        print('4. Regular users still controlled by permission checkboxes')
        
    except Exception as e:
        print(f'Error: {str(e)}')
        import traceback
        traceback.print_exc()
