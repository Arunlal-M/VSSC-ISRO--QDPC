#!/usr/bin/env python
"""
Comprehensive test script to verify role-based permissions system
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qdpc.settings')
django.setup()

from django.contrib.auth.models import User, Group
from qdpc.core.permissions import (
    get_role_based_page_access, 
    get_user_accessible_pages_by_role, 
    has_role_based_page_access, 
    ROLE_PAGE_ACCESS
)

def test_role_permissions():
    """Test the role-based permission system"""
    print("Testing Role-Based Permission System")
    print("=" * 50)
    
    # Test 1: Check ROLE_PAGE_ACCESS configuration
    print("\n1. Role Configuration:")
    for role, pages in ROLE_PAGE_ACCESS.items():
        print(f"   {role}: {pages}")
    
    # Test 2: Check existing groups in database
    print("\n2. Existing Groups in Database:")
    groups = Group.objects.all()
    if groups.exists():
        for group in groups:
            print(f"   - {group.name} (ID: {group.id})")
    else:
        print("   No groups found in database!")
    
    # Test 3: Check existing users
    print("\n3. Existing Users:")
    users = User.objects.all()[:5]  # Show first 5 users
    for user in users:
        user_groups = list(user.groups.values_list('name', flat=True))
        print(f"   - {user.username} (Groups: {user_groups})")
    
    # Test 4: Test permission functions with different scenarios
    print("\n4. Testing Permission Functions:")
    
    # Create test scenarios
    test_scenarios = [
        {"role": "Admin", "expected_pages": ["ALL"]},
        {"role": "Manager", "expected_pages": ["dashboard", "equipment", "rawmaterial", "consumable", "component", "product", "process", "reports", "stage_clearance", "acceptance_test"]},
        {"role": "Operator", "expected_pages": ["dashboard", "equipment", "rawmaterial", "consumable", "component", "product", "process", "stage_clearance"]},
        {"role": "Viewer", "expected_pages": ["dashboard", "reports"]},
        {"role": "Guest", "expected_pages": ["dashboard"]},
    ]
    
    for scenario in test_scenarios:
        role = scenario["role"]
        expected = scenario["expected_pages"]
        actual = ROLE_PAGE_ACCESS.get(role, [])
        
        status = "✓ PASS" if actual == expected else "✗ FAIL"
        print(f"   {role}: {status}")
        if actual != expected:
            print(f"     Expected: {expected}")
            print(f"     Actual: {actual}")
    
    # Test 5: Test with actual users if they exist
    print("\n5. Testing with Real Users:")
    if users.exists():
        test_user = users.first()
        print(f"   Testing with user: {test_user.username}")
        
        # Test get_role_based_page_access
        accessible_pages = get_role_based_page_access(test_user)
        print(f"   Accessible pages: {accessible_pages}")
        
        # Test get_user_accessible_pages_by_role
        pages_by_role = get_user_accessible_pages_by_role(test_user)
        print(f"   Pages by role: {pages_by_role}")
        
        # Test specific page access
        test_pages = ["dashboard", "equipment", "reports", "nonexistent_page"]
        for page in test_pages:
            has_access = has_role_based_page_access(test_user, page)
            print(f"   Access to '{page}': {has_access}")
    else:
        print("   No users found to test with")
    
    # Test 6: Test superuser access
    print("\n6. Testing Superuser Access:")
    superusers = User.objects.filter(is_superuser=True)
    if superusers.exists():
        superuser = superusers.first()
        print(f"   Testing with superuser: {superuser.username}")
        
        accessible_pages = get_role_based_page_access(superuser)
        print(f"   Superuser accessible pages: {accessible_pages}")
        
        # Test specific page access for superuser
        has_dashboard = has_role_based_page_access(superuser, "dashboard")
        has_equipment = has_role_based_page_access(superuser, "equipment")
        print(f"   Superuser dashboard access: {has_dashboard}")
        print(f"   Superuser equipment access: {has_equipment}")
    else:
        print("   No superusers found")
    
    print("\n" + "=" * 50)
    print("Role-based permission test completed!")

def create_missing_groups():
    """Create missing groups based on ROLE_PAGE_ACCESS"""
    print("\nCreating Missing Groups:")
    print("-" * 30)
    
    for role_name in ROLE_PAGE_ACCESS.keys():
        group, created = Group.objects.get_or_create(name=role_name)
        if created:
            print(f"   ✓ Created group: {role_name}")
        else:
            print(f"   - Group already exists: {role_name}")

if __name__ == "__main__":
    test_role_permissions()
    
    # Ask if user wants to create missing groups
    print("\n" + "=" * 50)
    create_groups = input("Do you want to create missing groups? (y/n): ").lower().strip()
    if create_groups == 'y':
        create_missing_groups()
        print("\nRe-running tests after group creation...")
        test_role_permissions()
