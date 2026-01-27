from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from qdpc_core_models.models import User
from qdpc_core_models.models.productBatch import ProductBatchs
from qdpc_core_models.models.product import Product
from product.services.approval_service import ProductBatchApprovalService


class Command(BaseCommand):
    help = 'Test the product batch approval permissions system'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='Username to test permissions for')
        parser.add_argument('--create-test-batch', action='store_true', help='Create a test product batch')

    def handle(self, *args, **options):
        self.stdout.write('Testing Product Batch Approval Permissions System...')
        
        # Create test product if it doesn't exist
        from qdpc_core_models.models.product_category import ProductCategory
        from qdpc_core_models.models.division import Division
        
        # Get first available category and division
        category = ProductCategory.objects.first()
        division = Division.objects.first()
        
        if not category or not division:
            self.stdout.write(self.style.ERROR('No ProductCategory or Division found. Please create them first.'))
            return
        
        product, created = Product.objects.get_or_create(
            name='Test Product for Approval',
            defaults={
                'category': category,
                'product_owner': division
            }
        )
        if created:
            self.stdout.write(f'Created test product: {product.name}')
        
        # Create test batch if requested
        if options['create_test_batch']:
            batch, created = ProductBatchs.objects.get_or_create(
                batch_id='TEST-BATCH-001',
                defaults={
                    'product': product,
                    'manufacturing_start': '2025-01-01',
                    'manufacturing_end': '2025-01-31',
                    'status': 'pending'
                }
            )
            if created:
                self.stdout.write(f'Created test batch: {batch.batch_id}')
        else:
            # Get existing batch or create one
            batch = ProductBatchs.objects.filter(status='pending').first()
            if not batch:
                batch = ProductBatchs.objects.create(
                    batch_id='TEST-BATCH-001',
                    product=product,
                    manufacturing_start='2025-01-01',
                    manufacturing_end='2025-01-31',
                    status='pending'
                )
                self.stdout.write(f'Created test batch: {batch.batch_id}')
        
        # Test specific user if provided
        if options['username']:
            try:
                user = User.objects.get(username=options['username'])
                self.test_user_permissions(user, batch)
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'User {options["username"]} not found'))
                return
        
        # Test all users with different roles
        self.stdout.write('\n' + '='*60)
        self.stdout.write('Testing All Users with Different Roles')
        self.stdout.write('='*60)
        
        # Test superuser
        superuser = User.objects.filter(is_superuser=True).first()
        if superuser:
            self.test_user_permissions(superuser, batch)
        
        # Test users with different roles
        test_roles = [
            'Division Head SDA',
            'Section Head SDA', 
            'Engineer SDA',
            'Division Head QA',
            'Section Head QA',
            'Engineer QA',
            'Division Head QC',
            'Section Head QC',
            'Engineer QC'
        ]
        
        for role_name in test_roles:
            try:
                group = Group.objects.get(name=role_name)
                users = group.user_set.all()[:1]  # Get first user in group
                if users:
                    self.test_user_permissions(users[0], batch)
                else:
                    self.stdout.write(f'{role_name}: No users in group')
            except Group.DoesNotExist:
                self.stdout.write(f'{role_name}: Group not found')
        
        self.stdout.write('\n' + '='*60)
        self.stdout.write('Permission Testing Complete!')
        self.stdout.write('='*60)

    def test_user_permissions(self, user, batch):
        """Test approval permissions for a specific user"""
        self.stdout.write(f'\n--- Testing User: {user.username} ---')
        
        # Get user groups
        user_groups = [group.name for group in user.groups.all()]
        self.stdout.write(f'Groups: {", ".join(user_groups) if user_groups else "No groups"}')
        
        # Test approval permissions
        can_approve, message = ProductBatchApprovalService.can_approve_product_batch(user, batch)
        self.stdout.write(f'Can Approve: {"✅ YES" if can_approve else "❌ NO"}')
        self.stdout.write(f'Message: {message}')
        
        # Get comprehensive permissions
        permissions = ProductBatchApprovalService.get_user_approval_permissions(user)
        self.stdout.write(f'Approval Level: {permissions.get("approval_level", "none")}')
        self.stdout.write(f'Explanation: {permissions.get("explanation", "No explanation")}')
        
        # Test with different batch statuses
        original_status = batch.status
        
        # Test with approved batch
        batch.status = 'approved'
        batch.save()
        can_approve_approved, message_approved = ProductBatchApprovalService.can_approve_product_batch(user, batch)
        self.stdout.write(f'Can Approve Approved Batch: {"✅ YES" if can_approve_approved else "❌ NO"}')
        
        # Test with rejected batch
        batch.status = 'rejected'
        batch.save()
        can_approve_rejected, message_rejected = ProductBatchApprovalService.can_approve_product_batch(user, batch)
        self.stdout.write(f'Can Approve Rejected Batch: {"✅ YES" if can_approve_rejected else "❌ NO"}')
        
        # Restore original status
        batch.status = original_status
        batch.save()
        
        self.stdout.write('-' * 40)
