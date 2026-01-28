#!/usr/bin/env python
"""
Test script to debug permission checking logic
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qdpc.settings')
django.setup()

from qdpc_core_models.models import User
from qdpc.models.page_permission import PagePermission

def test_permission_logic():
    """Test the permission checking logic step by step"""
    print("=== Testing Permission Logic Step by Step ===\n")
    
    # 1. Get the super admin user
    try:
        user = User.objects.get(username='superadmin')
        print(f"1. User: {user.username}")
        print(f"   ID: {user.id}")
        print(f"   is_superuser: {user.is_superuser}")
        print(f"   Groups: {[g.name for g in user.groups.all()]}")
    except User.DoesNotExist:
        print("❌ User 'superadmin' not found!")
        return
    
    print()
    
    # 2. Test the ProductBatchPermissionService
    print("2. Testing ProductBatchPermissionService:")
    try:
        from product.services.permission_service import ProductBatchPermissionService
        
        # Test get_user_permissions
        user_permissions = ProductBatchPermissionService.get_user_permissions(user)
        print(f"   get_user_permissions result: {user_permissions}")
        
        # Test get_page_permission_context
        page_context = ProductBatchPermissionService.get_page_permission_context(user)
        print(f"   get_page_permission_context result: {page_context}")
        
    except Exception as e:
        print(f"   ❌ Error with ProductBatchPermissionService: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    
    # 3. Test direct PagePermission queries (fallback logic)
    print("3. Testing Direct PagePermission Queries (Fallback Logic):")
    try:
        user_groups = user.groups.all()
        print(f"   User groups: {[g.name for g in user_groups]}")
        
        # Check if user has any groups with Product batch permissions
        has_permissions = PagePermission.objects.filter(
            group__in=user_groups,
            page_name='Product batch',
            is_active=True
        ).exists()
        print(f"   Has any Product batch permissions: {has_permissions}")
        
        if has_permissions:
            # Check each permission type
            add_perm = PagePermission.objects.filter(
                group__in=user_groups,
                page_name='Product batch',
                permission_type='add',
                is_active=True
            ).exists()
            edit_perm = PagePermission.objects.filter(
                group__in=user_groups,
                page_name='Product batch',
                permission_type='edit',
                is_active=True
            ).exists()
            delete_perm = PagePermission.objects.filter(
                group__in=user_groups,
                page_name='Product batch',
                permission_type='delete',
                is_active=True
            ).exists()
            approve_perm = PagePermission.objects.filter(
                group__in=user_groups,
                page_name='Product batch',
                permission_type='approve',
                is_active=True
            ).exists()
            
            print(f"   Individual permissions:")
            print(f"     - add: {add_perm}")
            print(f"     - edit: {edit_perm}")
            print(f"     - delete: {delete_perm}")
            print(f"     - approve: {approve_perm}")
            
            # Create the page_permissions dict like the view does
            page_permissions = {
                'can_access_product_batch': True,
                'can_add_product_batch': add_perm,
                'can_edit_product_batch': edit_perm,
                'can_delete_product_batch': delete_perm,
                'can_approve_product_batch': approve_perm,
            }
            print(f"   Final page_permissions dict: {page_permissions}")
            
        else:
            print("   ❌ No Product batch permissions found!")
            
    except Exception as e:
        print(f"   ❌ Error with direct PagePermission queries: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    
    # 4. Test the exact query that should work
    print("4. Testing Exact Query for Edit Permission:")
    try:
        edit_permissions = PagePermission.objects.filter(
            group__in=user.groups.all(),
            page_name='Product batch',
            permission_type='edit',
            is_active=True
        )
        print(f"   Raw edit permissions query result: {edit_permissions}")
        print(f"   Count: {edit_permissions.count()}")
        if edit_permissions.exists():
            for perm in edit_permissions:
                print(f"     - Group: {perm.group.name}, Type: {perm.permission_type}, Active: {perm.is_active}")
        
    except Exception as e:
        print(f"   ❌ Error with edit permission query: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n=== Test Complete ===")

if __name__ == '__main__':
    test_permission_logic()
