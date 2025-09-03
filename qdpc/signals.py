from django.db.models.signals import post_save, post_delete, post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.apps import apps
from django.core.management import call_command
import os
from django.conf import settings

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

    # Define model names to manage Django-model permissions for
    model_classes = [
        Equipment,
        RawMaterial,
        ProductCategory,
        Product,
        ProductBatch
    ]

    # Ensure custom action permissions exist for relevant models
    custom_actions = ['approve', 'reject', 'export']
    for model in model_classes:
        try:
            ct = ContentType.objects.get_for_model(model)
            model_name = model._meta.model_name
            for action in custom_actions:
                Permission.objects.get_or_create(
                    content_type=ct,
                    codename=f"{action}_{model_name}",
                    defaults={'name': f"Can {action} {model_name.replace('_', ' ')}"}
                )
        except Exception as e:
            print(f"[Custom Permission Error] {model.__name__}: {e}")

    # Note: We no longer auto-create default groups here. Groups come from Excel seeding.


# Run seeders after migrations complete for this app
@receiver(post_migrate)
def run_seeders_after_migrate(sender, app_config=None, using=None, verbosity=1, **kwargs):
    try:
        # Only run once when the qdpc app finishes migrating
        if not app_config or app_config.name != 'qdpc':
            return

        # Check if seeding has already been done using a database flag
        from django.contrib.auth.models import Group
        from django.core.cache import cache
        
        # Use cache to track if seeding has been done in this session
        seeding_key = 'qdpc_seeding_completed'
        if cache.get(seeding_key):
            if verbosity > 0:
                print("[Seeder] Seeding already completed in this session, skipping")
            return
            
        # Check if groups already exist to avoid duplicate seeding
        if Group.objects.exists():
            if verbosity > 0:
                print("[Seeder] Groups already exist, skipping group reseeding")
            # Mark seeding as completed
            cache.set(seeding_key, True, timeout=3600)  # 1 hour timeout
            return

        # Seed VSSC pages (idempotent)
        try:
            call_command('seed_vssc_pages', verbosity=verbosity)
        except Exception as se:
            print(f"[Seeder] seed_vssc_pages failed: {se}")

        # Only create groups if they don't exist
        try:
            # Create basic auth groups from built-in list
            call_command('reseed_auth_groups', preserve_existing=True, add_permissions=True)
        except Exception as se:
            print(f"[Seeder] reseed_auth_groups failed: {se}")

        # Ensure superusers and Master Admin group have all permissions
        try:
            from django.contrib.auth import get_user_model
            from django.contrib.auth.models import Permission
            User = get_user_model()

            all_perms = Permission.objects.all()

            # Grant all permissions to the Master Admin/Super Admin group
            admin_group, _ = Group.objects.get_or_create(name='Master Admin/Super Admin')
            admin_group.permissions.set(all_perms)

            # Grant all permissions to all superusers
            for su in User.objects.filter(is_superuser=True):
                su.user_permissions.set(all_perms)
        except Exception as pe:
            print(f"[Seeder] grant all perms to superusers failed: {pe}")

        # Mark seeding as completed
        cache.set(seeding_key, True, timeout=3600)  # 1 hour timeout

    except Exception as e:
        print(f"[Seeder] post_migrate hook error: {e}")

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
