from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from qdpc.core.permissions import (
    get_role_based_page_access, 
    get_user_accessible_pages_by_role, 
    has_role_based_page_access, 
    ROLE_PAGE_ACCESS
)

class Command(BaseCommand):
    help = 'Test and validate role-based permissions system'

    def add_arguments(self, parser):
        parser.add_argument(
            '--create-groups',
            action='store_true',
            help='Create missing groups',
        )
        parser.add_argument(
            '--create-test-users',
            action='store_true',
            help='Create test users for each role',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Testing Role-Based Permissions System'))
        self.stdout.write('=' * 60)
        
        # Test 1: Check ROLE_PAGE_ACCESS configuration
        self.test_role_configuration()
        
        # Test 2: Check existing groups
        self.test_existing_groups()
        
        # Test 3: Create missing groups if requested
        if options['create_groups']:
            self.create_missing_groups()
        
        # Test 4: Create test users if requested
        if options['create_test_users']:
            self.create_test_users()
        
        # Test 5: Test permission functions
        self.test_permission_functions()
        
        # Test 6: Test with real users
        self.test_with_real_users()
        
        self.stdout.write(self.style.SUCCESS('\nRole-based permission testing completed!'))

    def test_role_configuration(self):
        self.stdout.write('\n1. Role Configuration:')
        for role, pages in ROLE_PAGE_ACCESS.items():
            page_count = len(pages) if pages != ['ALL'] else 'ALL'
            self.stdout.write(f'   {role}: {page_count} pages - {pages}')

    def test_existing_groups(self):
        self.stdout.write('\n2. Database Groups:')
        groups = Group.objects.all()
        if groups.exists():
            for group in groups:
                user_count = group.user_set.count()
                self.stdout.write(f'   - {group.name} ({user_count} users)')
        else:
            self.stdout.write(self.style.WARNING('   No groups found in database!'))
        
        # Check for missing groups
        required_roles = set(ROLE_PAGE_ACCESS.keys())
        existing_roles = set(g.name for g in groups)
        missing_roles = required_roles - existing_roles
        
        if missing_roles:
            self.stdout.write(self.style.WARNING(f'   Missing roles: {list(missing_roles)}'))
        else:
            self.stdout.write(self.style.SUCCESS('   All required roles exist'))

    def create_missing_groups(self):
        self.stdout.write('\n3. Creating Missing Groups:')
        for role_name in ROLE_PAGE_ACCESS.keys():
            group, created = Group.objects.get_or_create(name=role_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'   ✓ Created group: {role_name}'))
            else:
                self.stdout.write(f'   - Group already exists: {role_name}')

    def create_test_users(self):
        self.stdout.write('\n4. Creating Test Users:')
        for role_name in ROLE_PAGE_ACCESS.keys():
            username = f'test_{role_name.lower()}'
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': f'{username}@test.com',
                    'first_name': f'Test {role_name}',
                    'is_active': True
                }
            )
            
            if created:
                user.set_password('testpass123')
                user.save()
                self.stdout.write(self.style.SUCCESS(f'   ✓ Created user: {username}'))
            else:
                self.stdout.write(f'   - User already exists: {username}')
            
            # Assign to group
            group = Group.objects.get(name=role_name)
            user.groups.add(group)
            self.stdout.write(f'     Added to group: {role_name}')

    def test_permission_functions(self):
        self.stdout.write('\n5. Testing Permission Functions:')
        
        # Test with each role configuration
        for role_name, expected_pages in ROLE_PAGE_ACCESS.items():
            self.stdout.write(f'\n   Testing {role_name} role:')
            
            # Find a user with this role
            try:
                group = Group.objects.get(name=role_name)
                if group.user_set.exists():
                    test_user = group.user_set.first()
                    
                    # Test get_role_based_page_access
                    actual_pages = get_role_based_page_access(test_user)
                    match = actual_pages == expected_pages
                    status = '✓' if match else '✗'
                    self.stdout.write(f'     {status} get_role_based_page_access: {actual_pages}')
                    
                    # Test get_user_accessible_pages_by_role
                    pages_by_role = get_user_accessible_pages_by_role(test_user)
                    self.stdout.write(f'     ✓ get_user_accessible_pages_by_role: {pages_by_role}')
                    
                    # Test specific page access
                    test_pages = ['dashboard', 'equipment', 'reports', 'nonexistent']
                    for page in test_pages:
                        has_access = has_role_based_page_access(test_user, page)
                        expected_access = page in expected_pages or 'ALL' in expected_pages
                        status = '✓' if has_access == expected_access else '✗'
                        self.stdout.write(f'     {status} {page}: {has_access}')
                else:
                    self.stdout.write(f'     - No users found for role {role_name}')
            except Group.DoesNotExist:
                self.stdout.write(f'     - Group {role_name} does not exist')

    def test_with_real_users(self):
        self.stdout.write('\n6. Testing with Real Users:')
        users = User.objects.all()[:5]  # Test with first 5 users
        
        if not users.exists():
            self.stdout.write('   No users found in database')
            return
        
        for user in users:
            self.stdout.write(f'\n   User: {user.username}')
            user_groups = list(user.groups.values_list('name', flat=True))
            self.stdout.write(f'   Groups: {user_groups}')
            self.stdout.write(f'   Superuser: {user.is_superuser}')
            
            try:
                # Test permission functions
                accessible_pages = get_role_based_page_access(user)
                self.stdout.write(f'   Accessible pages: {accessible_pages}')
                
                pages_by_role = get_user_accessible_pages_by_role(user)
                self.stdout.write(f'   Pages by role: {pages_by_role}')
                
                # Test specific pages
                test_pages = ['dashboard', 'equipment', 'product']
                for page in test_pages:
                    has_access = has_role_based_page_access(user, page)
                    self.stdout.write(f'   {page}: {has_access}')
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'   Error testing user {user.username}: {e}'))
