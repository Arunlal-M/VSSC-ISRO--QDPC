import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qdpc.settings')
django.setup()

from django.contrib.auth.models import User, Group
from qdpc.core.permissions import ROLE_PAGE_ACCESS, get_role_based_page_access, has_role_based_page_access

print("=== ROLE-BASED PERMISSIONS VALIDATION ===\n")

# 1. Check role configuration
print("1. ROLE CONFIGURATION:")
for role, pages in ROLE_PAGE_ACCESS.items():
    print(f"   {role}: {pages}")

# 2. Check database groups
print(f"\n2. DATABASE STATE:")
print(f"   Total groups: {Group.objects.count()}")
print(f"   Total users: {User.objects.count()}")

groups = Group.objects.all()
for group in groups:
    print(f"   Group: {group.name} ({group.user_set.count()} users)")

# 3. Create missing groups
print(f"\n3. CREATING MISSING GROUPS:")
for role_name in ROLE_PAGE_ACCESS.keys():
    group, created = Group.objects.get_or_create(name=role_name)
    print(f"   {role_name}: {'Created' if created else 'Already exists'}")

# 4. Test permission functions
print(f"\n4. TESTING PERMISSION FUNCTIONS:")

# Create a test user if none exist
if not User.objects.exists():
    test_user = User.objects.create_user('testuser', 'test@example.com', 'password')
    admin_group = Group.objects.get(name='Admin')
    test_user.groups.add(admin_group)
    print("   Created test user with Admin role")
else:
    test_user = User.objects.first()

print(f"   Testing with user: {test_user.username}")
print(f"   User groups: {[g.name for g in test_user.groups.all()]}")

# Test functions
try:
    pages = get_role_based_page_access(test_user)
    print(f"   get_role_based_page_access: {pages}")
    
    # Test specific page access
    test_pages = ['dashboard', 'equipment', 'reports', 'invalid_page']
    for page in test_pages:
        access = has_role_based_page_access(test_user, page)
        print(f"   {page}: {access}")
        
except Exception as e:
    print(f"   ERROR: {e}")

# 5. Test each role
print(f"\n5. TESTING ALL ROLES:")
for role_name in ROLE_PAGE_ACCESS.keys():
    try:
        group = Group.objects.get(name=role_name)
        if group.user_set.exists():
            user = group.user_set.first()
            pages = get_role_based_page_access(user)
            expected = ROLE_PAGE_ACCESS[role_name]
            status = "✓" if pages == expected else "✗"
            print(f"   {role_name}: {status} Got {pages}, Expected {expected}")
        else:
            print(f"   {role_name}: No users assigned")
    except Group.DoesNotExist:
        print(f"   {role_name}: Group not found")

print(f"\n=== VALIDATION COMPLETE ===")
