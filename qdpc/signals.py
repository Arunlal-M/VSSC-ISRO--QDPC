from django.db.models.signals import post_save, post_delete, post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.apps import apps

from qdpc_core_models.models.equipment import Equipment
from qdpc_core_models.models.raw_material import RawMaterial
from qdpc_core_models.models.product import Product
from qdpc_core_models.models.product_category import ProductCategory
from qdpc_core_models.models.product_batchlist import ProductBatch

from .views.activity_logger import log_activity
from authentication.middleware import get_current_user


@receiver(post_migrate)
def create_default_roles_and_permissions(sender, **kwargs):
    if not apps.is_installed('qdpc'):
        return

    # Step 1: Create default roles (groups)
    default_roles = ['GUEST', 'ADMIN', 'QA', 'QC', 'SDA', 'INDUSTRY']
    
    # Step 2: Define model names to manage permissions for
    model_classes = [
        Equipment,
        RawMaterial,
        ProductCategory,
        Product,
        ProductBatch
    ]

    for role_name in default_roles:
        group, _ = Group.objects.get_or_create(name=role_name)

        for model in model_classes:
            try:
                content_type = ContentType.objects.get_for_model(model)
                permissions = Permission.objects.filter(content_type=content_type)

                model_name = model._meta.model_name

                if role_name == 'ADMIN':
                    group.permissions.add(*permissions)

                elif role_name in ['QA', 'QC', 'SDA']:
                    allowed = permissions.filter(codename__in=[
                        f'view_{model_name}', f'change_{model_name}'
                    ])
                    group.permissions.add(*allowed)

                elif role_name in ['GUEST', 'INDUSTRY']:
                    view_perm = permissions.filter(codename=f'view_{model_name}')
                    group.permissions.add(*view_perm)

            except Exception as e:
                print(f"[Permission Error] {model.__name__}: {e}")


# Equipment logging
@receiver(post_save, sender=Equipment)
def log_equipment_create_update(sender, instance, created, **kwargs):
    user = get_current_user()
    action = 'create' if created else 'update'
    log_activity(user, instance, action)

@receiver(post_delete, sender=Equipment)
def log_equipment_delete(sender, instance, **kwargs):
    user = get_current_user()
    log_activity(user, instance, 'delete')


# RawMaterial logging
@receiver(post_save, sender=RawMaterial)
def log_rawmaterial_create_update(sender, instance, created, **kwargs):
    user = get_current_user()
    action = 'create' if created else 'update'
    log_activity(user, instance, action)

@receiver(post_delete, sender=RawMaterial)
def log_rawmaterial_delete(sender, instance, **kwargs):
    user = get_current_user()
    log_activity(user, instance, 'delete')
