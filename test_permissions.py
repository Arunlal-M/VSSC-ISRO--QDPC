#!/usr/bin/env python
"""
Test script to verify the permission system is working correctly
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qdpc.settings')
django.setup()

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from qdpc.core.permissions import get_user_permissions_from_auth_table, convert_permissions_to_page_codes, get_user_page_codes

def test_permission_system():
    """Test the permission system functions"""
    print("Testing Permission System...")
    print("=" * 50)
    
    # Test 1: Get all groups
    print("\n1. Available Groups:")
    groups = Group.objects.all()
    for group in groups:
        print(f"   - {group.name} (ID: {group.id})")
    
    # Test 2: Get all permissions
    print("\n2. Available Permissions:")
    permissions = Permission.objects.all()
    permission_count = permissions.count()
    print(f"   Total permissions: {permission_count}")
    
    # Show first 10 permissions as examples
    for i, perm in enumerate(permissions[:10]):
        print(f"   - {perm.content_type.app_label}.{perm.codename}: {perm.name}")
    
    if permission_count > 10:
        print(f"   ... and {permission_count - 10} more permissions")
    
    # Test 3: Test permission mapping
    print("\n3. Testing Permission to Page Code Mapping:")
    test_permissions = [
        'qdpc_core_models.view_center',
        'qdpc_core_models.add_center',
        'equipment.view_equipment',
        'product.view_product',
        'user.view_user'
    ]
    
    page_codes = convert_permissions_to_page_codes(test_permissions)
    print(f"   Test permissions: {test_permissions}")
    print(f"   Resulting page codes: {page_codes}")
    
    # Test 4: Test with a specific group
    print("\n4. Testing Group Permissions:")
    if groups.exists():
        test_group = groups.first()
        print(f"   Testing with group: {test_group.name}")
        
        # Get group permissions
        group_permissions = test_group.permissions.all()
        print(f"   Group has {group_permissions.count()} permissions")
        
        # Convert to page codes
        if group_permissions.exists():
            perm_strings = [f"{p.content_type.app_label}.{p.codename}" for p in group_permissions]
            page_codes = convert_permissions_to_page_codes(perm_strings)
            print(f"   Permission strings: {perm_strings[:5]}...")  # Show first 5
            print(f"   Accessible pages: {page_codes}")
    
    print("\n" + "=" * 50)
    print("Permission system test completed!")

if __name__ == "__main__":
    test_permission_system()
