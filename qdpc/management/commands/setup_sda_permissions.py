from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from qdpc_core_models.models.productBatch import ProductBatchs


class Command(BaseCommand):
    help = 'Set up SDA user permissions for product batch management'

    def handle(self, *args, **options):
        try:
            # Get or create the Division Head SDA group
            sda_group, created = Group.objects.get_or_create(name='Division Head SDA')
            if created:
                self.stdout.write(
                    self.style.SUCCESS('Created Division Head SDA group')
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS('Division Head SDA group already exists')
                )

            # Get the content type for ProductBatchs
            content_type = ContentType.objects.get_for_model(ProductBatchs)
            
            # Get all available permissions for ProductBatchs
            permissions = Permission.objects.filter(content_type=content_type)
            
            # Add all permissions to the SDA group
            for permission in permissions:
                sda_group.permissions.add(permission)
                self.stdout.write(
                    f'Added permission: {permission.name}'
                )

            # Also check for product app permissions if they exist
            try:
                product_content_type = ContentType.objects.get(
                    app_label='product',
                    model='productbatch'
                )
                product_permissions = Permission.objects.filter(
                    content_type=product_content_type
                )
                
                for permission in product_permissions:
                    sda_group.permissions.add(permission)
                    self.stdout.write(
                        f'Added product permission: {permission.name}'
                    )
            except ContentType.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING('Product app content type not found')
                )

            self.stdout.write(
                self.style.SUCCESS(
                    'Successfully set up SDA permissions for product batch management'
                )
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error setting up permissions: {str(e)}')
            )
