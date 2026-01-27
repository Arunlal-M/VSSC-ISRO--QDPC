from django.core.management.base import BaseCommand
from permission_system.models import Page, PermissionRole as Role, RolePagePermission


class Command(BaseCommand):
    help = 'Initialize the role and permission system with default pages and roles'

    def handle(self, *args, **options):
        self.stdout.write('Initializing Role and Permission System...')
        
        # Create default pages
        self.create_default_pages()
        
        # Create default roles
        self.create_default_roles()
        
        # Set up default permissions
        self.setup_default_permissions()
        
        self.stdout.write(self.style.SUCCESS('Role and Permission System initialized successfully!'))

    def create_default_pages(self):
        """Create default system pages"""
        self.stdout.write('Creating default pages...')
        
        default_pages = [
            (1, 'Dashboard', 'user-dashboard', 'home'),
            (2, 'Equipments', 'equipment-list', 'tool'),
            (3, 'Acceptance Test', 'acceptance-test-list', 'check-circle'),
            (4, 'Rawmaterial', 'rawmaterial-list', 'package'),
            (5, 'Rawmaterial Batch', 'rawmaterial-batch-list', 'layers'),
            (6, 'Consumable', 'consumable-list', 'box'),
            (7, 'Consumable Batch', 'consumable-batch-list', 'archive'),
            (8, 'Component', 'component-list', 'cpu'),
            (9, 'Component Batch', 'component-batch-list', 'hard-drive'),
            (10, 'Process', 'process-list', 'settings'),
            (11, 'Product', 'product-list', 'shopping-bag'),
            (12, 'Product Batch', 'product-batch-list', 'shopping-cart'),
            (13, 'Units', 'unit-list', 'hash'),
            (14, 'Grade', 'grade-list', 'star'),
            (15, 'Enduse', 'enduse-list', 'target'),
            (16, 'Document Type', 'documenttype-list', 'file-text'),
            (17, 'Center', 'center-list', 'map-pin'),
            (18, 'Division', 'division-list', 'git-branch'),
            (19, 'Source', 'source-list', 'external-link'),
            (20, 'Supplier', 'supplier-list', 'truck'),
            (21, 'Users', 'user-list', 'users'),
            (22, 'Process Log-Sheet', '#', 'clipboard'),
            (23, 'Stage Clearance', 'clearance', 'unlock'),
            (24, 'Q.A.R-Report', '#', 'file-text'),
            (25, 'Groups', 'group-list', 'users'),
            (26, 'Roles Management', 'role-permission-dashboard', 'shield'),
        ]
        
        for page_number, page_name, url_name, icon in default_pages:
            page, created = Page.objects.get_or_create(
                page_number=page_number,
                defaults={
                    'page_name': page_name,
                    'url_name': url_name,
                    'icon': icon,
                    'description': f'Access to {page_name} functionality',
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(f'  ✓ Created page: {page_name}')
            else:
                self.stdout.write(f'  - Page already exists: {page_name}')

    def create_default_roles(self):
        """Create default system roles"""
        self.stdout.write('Creating default roles...')
        
        default_roles = [
            ('Super Admin', 'admin', 'Full system access with all permissions'),
            ('Admin', 'admin', 'Administrative access to most system functions'),
            ('Manager', 'manager', 'Management level access to assigned modules'),
            ('Supervisor', 'supervisor', 'Supervisory access with approval capabilities'),
            ('Staff', 'staff', 'Standard user access to assigned modules'),
            ('Guest', 'guest', 'Limited read-only access to basic information'),
        ]
        
        for role_name, role_type, description in default_roles:
            role, created = Role.objects.get_or_create(
                name=role_name,
                defaults={
                    'role_type': role_type,
                    'description': description,
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(f'  ✓ Created role: {role_name}')
            else:
                self.stdout.write(f'  - Role already exists: {role_name}')

    def setup_default_permissions(self):
        """Set up default permissions for roles"""
        self.stdout.write('Setting up default permissions...')
        
        # Get all pages and roles
        pages = Page.objects.all()
        super_admin = Role.objects.get(name='Super Admin')
        admin = Role.objects.get(name='Admin')
        manager = Role.objects.get(name='Manager')
        supervisor = Role.objects.get(name='Supervisor')
        staff = Role.objects.get(name='Staff')
        guest = Role.objects.get(name='Guest')
        
        # Super Admin - Full access to everything
        for page in pages:
            permission, created = RolePagePermission.objects.get_or_create(
                role=super_admin,
                page=page,
                defaults={
                    'can_view': True,
                    'can_add': True,
                    'can_edit': True,
                    'can_delete': True,
                    'can_approve': True,
                }
            )
            if created:
                self.stdout.write(f'  ✓ Super Admin permissions for {page.page_name}')
        
        # Admin - Most access except user management
        admin_restricted_pages = ['Roles Management']
        for page in pages:
            if page.page_name not in admin_restricted_pages:
                permission, created = RolePagePermission.objects.get_or_create(
                    role=admin,
                    page=page,
                    defaults={
                        'can_view': True,
                        'can_add': True,
                        'can_edit': True,
                        'can_delete': False,  # Limited delete access
                        'can_approve': True,
                    }
                )
                if created:
                    self.stdout.write(f'  ✓ Admin permissions for {page.page_name}')
        
        # Manager - Access to core business functions
        manager_pages = [
            'Dashboard', 'Product', 'Product Batch', 'Rawmaterial', 'Rawmaterial Batch',
            'Consumable', 'Consumable Batch', 'Component', 'Component Batch',
            'Process', 'Acceptance Test', 'Stage Clearance', 'Q.A.R-Report'
        ]
        for page in pages:
            if page.page_name in manager_pages:
                permission, created = RolePagePermission.objects.get_or_create(
                    role=manager,
                    page=page,
                    defaults={
                        'can_view': True,
                        'can_add': True,
                        'can_edit': True,
                        'can_delete': False,
                        'can_approve': True,
                    }
                )
                if created:
                    self.stdout.write(f'  ✓ Manager permissions for {page.page_name}')
        
        # Supervisor - Similar to manager but with more approval capabilities
        supervisor_pages = manager_pages + ['Users', 'Groups']
        for page in pages:
            if page.page_name in supervisor_pages:
                permission, created = RolePagePermission.objects.get_or_create(
                    role=supervisor,
                    page=page,
                    defaults={
                        'can_view': True,
                        'can_add': page.page_name not in ['Users', 'Groups'],
                        'can_edit': page.page_name not in ['Users', 'Groups'],
                        'can_delete': False,
                        'can_approve': True,
                    }
                )
                if created:
                    self.stdout.write(f'  ✓ Supervisor permissions for {page.page_name}')
        
        # Staff - Basic operational access
        staff_pages = [
            'Dashboard', 'Product', 'Rawmaterial', 'Consumable', 'Component',
            'Process', 'Acceptance Test', 'Units', 'Grade', 'Enduse'
        ]
        for page in pages:
            if page.page_name in staff_pages:
                permission, created = RolePagePermission.objects.get_or_create(
                    role=staff,
                    page=page,
                    defaults={
                        'can_view': True,
                        'can_add': page.page_name == 'Acceptance Test',
                        'can_edit': page.page_name == 'Acceptance Test',
                        'can_delete': False,
                        'can_approve': False,
                    }
                )
                if created:
                    self.stdout.write(f'  ✓ Staff permissions for {page.page_name}')
        
        # Guest - Read-only access to basic pages
        guest_pages = ['Dashboard', 'Product', 'Rawmaterial', 'Consumable', 'Component']
        for page in pages:
            if page.page_name in guest_pages:
                permission, created = RolePagePermission.objects.get_or_create(
                    role=guest,
                    page=page,
                    defaults={
                        'can_view': True,
                        'can_add': False,
                        'can_edit': False,
                        'can_delete': False,
                        'can_approve': False,
                    }
                )
                if created:
                    self.stdout.write(f'  ✓ Guest permissions for {page.page_name}')
        
        self.stdout.write('Default permissions setup completed!')
