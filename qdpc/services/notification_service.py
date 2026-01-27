from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from qdpc_core_models.models.notification import Notification
from qdpc.core.permissions import has_page_permission


class NotificationService:
    """Service to handle notification creation and management"""
    
    @staticmethod
    def get_users_with_permission(entity_type, permission_type='view'):
        """Get users who have permission to view specific entity type"""
        # Map entity types to page names
        entity_to_page_map = {
            'product_batch': 'Product batch',
            'raw_material': 'Raw material',
            'component': 'Component',
            'consumable': 'Consumable',
            'equipment': 'Equipment',
            'acceptance_test': 'Acceptance test',
            'process': 'Process',
            'user': 'Users',
        }
        
        page_name = entity_to_page_map.get(entity_type, entity_type)
        users_with_permission = []
        
        # Get all active users using the custom User model
        User = get_user_model()
        all_users = User.objects.filter(is_active=True)
        
        for user in all_users:
            if has_page_permission(user, page_name, permission_type):
                users_with_permission.append(user)
        
        return users_with_permission
    
    @staticmethod
    def create_entity_notification(entity_type, entity_id, entity_name, 
                                 notification_type, created_by=None):
        """Create notification for entity operations (create, update, delete)"""
        
        try:
            # Get users who have permission to view this entity type
            users = NotificationService.get_users_with_permission(entity_type, 'view')
            
            # Also add the creator to the notification list for immediate feedback
            if created_by and created_by not in users:
                users.append(created_by)
            
            # Create notification title and message
            action_map = {
                'create': 'created',
                'update': 'updated', 
                'delete': 'deleted',
                'approve': 'approved',
                'reject': 'rejected'
            }
            
            action = action_map.get(notification_type, notification_type)
            title = f"{entity_type.replace('_', ' ').title()} {action.title()}"
            
            if created_by:
                message = f"{entity_name} was {action} by {created_by.get_full_name() or created_by.username}"
            else:
                message = f"{entity_name} was {action}"
            
            # Create notifications for all users with permission
            notifications = Notification.create_notification(
                users=users,
                title=title,
                message=message,
                notification_type=notification_type,
                entity_type=entity_type,
                entity_id=entity_id,
                entity_name=entity_name,
                created_by=created_by
            )
            
            return notifications
            
        except Exception as e:
            # Log the error but don't break the main functionality
            print(f"Error creating notification: {e}")
            return []
    
    @staticmethod
    def notify_product_batch_created(batch, created_by=None):
        """Create notification for product batch creation"""
        try:
            # Get users who have permission to view product batches
            users = NotificationService.get_users_with_permission('product_batch', 'view')
            
            # Also add the creator to the notification list for immediate feedback
            if created_by and created_by not in users:
                users.append(created_by)
            
            # Create descriptive title and message
            title = f"New Product Batch Created"
            message = f"Product Batch #{batch.id} for {batch.product.name} has been created"
            
            if created_by:
                message += f" by {created_by.get_full_name() or created_by.username}"
            
            # Add batch details to message
            if hasattr(batch, 'batch_size') and batch.batch_size:
                message += f" with quantity {batch.batch_size}"
            
            if hasattr(batch, 'production_date'):
                message += f" (Production Date: {batch.production_date.strftime('%Y-%m-%d')})"
            
            # Create notifications for all users with permission
            notifications = Notification.create_notification(
                users=users,
                title=title,
                message=message,
                notification_type='create',
                entity_type='product_batch',
                entity_id=batch.id,
                entity_name=f"Product Batch #{batch.id} - {batch.product.name}",
                created_by=created_by
            )
            
            return notifications
            
        except Exception as e:
            # Log the error but don't break the main functionality
            print(f"Error creating product batch notification: {e}")
            return []
    
    @staticmethod
    def notify_product_batch_updated(batch, updated_by=None):
        """Create notification for product batch update"""
        try:
            # Get users who have permission to view product batches
            users = NotificationService.get_users_with_permission('product_batch', 'view')
            
            # Also add the updater to the notification list for immediate feedback
            if updated_by and updated_by not in users:
                users.append(updated_by)
            
            # Create descriptive title and message
            title = f"Product Batch Updated"
            message = f"Product Batch #{batch.id} for {batch.product.name} has been updated"
            
            if updated_by:
                message += f" by {updated_by.get_full_name() or updated_by.username}"
            
            # Add batch details to message
            if hasattr(batch, 'batch_size') and batch.batch_size:
                message += f" with quantity {batch.batch_size}"
            
            if hasattr(batch, 'production_date'):
                message += f" (Production Date: {batch.production_date.strftime('%Y-%m-%d')})"
            
            # Create notifications for all users with permission
            notifications = Notification.create_notification(
                users=users,
                title=title,
                message=message,
                notification_type='update',
                entity_type='product_batch',
                entity_id=batch.id,
                entity_name=f"Product Batch #{batch.id} - {batch.product.name}",
                created_by=updated_by
                )
            
            return notifications
            
        except Exception as e:
            # Log the error but don't break the main functionality
            print(f"Error creating product batch update notification: {e}")
            return []
    
    @staticmethod
    def notify_product_batch_deleted(batch_id, batch_name, deleted_by=None):
        """Create notification for product batch deletion"""
        return NotificationService.create_entity_notification(
            entity_type='product_batch',
            entity_id=batch_id,
            entity_name=batch_name,
            notification_type='delete',
            created_by=deleted_by
        )
    
    @staticmethod
    def notify_acceptance_test_created(test, created_by=None):
        """Create notification for acceptance test creation"""
        return NotificationService.create_entity_notification(
            entity_type='acceptance_test',
            entity_id=test.id,
            entity_name=test.name,
            notification_type='create',
            created_by=created_by
        )
    
    @staticmethod
    def notify_acceptance_test_deleted(test_id, test_name, deleted_by=None):
        """Create notification for acceptance test deletion"""
        return NotificationService.create_entity_notification(
            entity_type='acceptance_test',
            entity_id=test_id,
            entity_name=test_name,
            notification_type='delete',
            created_by=deleted_by
        )
    
    @staticmethod
    def notify_raw_material_batch_created(batch, created_by=None):
        """Create notification for raw material batch creation"""
        try:
            # Get users who have permission to view raw materials
            users = NotificationService.get_users_with_permission('raw_material', 'view')
            
            # Also add the creator to the notification list for immediate feedback
            if created_by and created_by not in users:
                users.append(created_by)
            
            # Create descriptive title and message
            title = f"New Raw Material Batch Created"
            message = f"Raw Material Batch #{batch.batch_id} for {batch.raw_material.name} has been created"
            
            if created_by:
                message += f" by {created_by.get_full_name() or created_by.username}"
            
            # Add batch details to message
            if hasattr(batch, 'batch_size_value') and hasattr(batch, 'batch_size_unit'):
                message += f" with quantity {batch.batch_size_value} {batch.batch_size_unit.name if hasattr(batch.batch_size_unit, 'name') else batch.batch_size_unit}"
            
            if hasattr(batch, 'procurement_date'):
                message += f" (Procured: {batch.procurement_date.strftime('%Y-%m-%d')})"
            
            # Create notifications for all users with permission
            notifications = Notification.create_notification(
                users=users,
                title=title,
                message=message,
                notification_type='create',
                entity_type='raw_material',
                entity_id=batch.id,
                entity_name=f"Raw Material Batch #{batch.batch_id} - {batch.raw_material.name}",
                created_by=created_by
            )
            
            return notifications
            
        except Exception as e:
            # Log the error but don't break the main functionality
            print(f"Error creating raw material batch notification: {e}")
            return []
    
    @staticmethod
    def notify_raw_material_batch_updated(batch, updated_by=None):
        """Create notification for raw material batch update"""
        try:
            # Get users who have permission to view raw materials
            users = NotificationService.get_users_with_permission('raw_material', 'view')
            
            # Also add the updater to the notification list for immediate feedback
            if updated_by and updated_by not in users:
                users.append(updated_by)
            
            # Create descriptive title and message
            title = f"Raw Material Batch Updated"
            message = f"Raw Material Batch #{batch.batch_id} for {batch.raw_material.name} has been updated"
            
            if updated_by:
                message += f" by {updated_by.get_full_name() or updated_by.username}"
            
            # Add batch details to message
            if hasattr(batch, 'batch_size_value') and hasattr(batch, 'batch_size_unit'):
                message += f" with quantity {batch.batch_size_value} {batch.batch_size_unit.name if hasattr(batch.batch_size_unit, 'name') else batch.batch_size_unit}"
            
            if hasattr(batch, 'procurement_date'):
                message += f" (Procured: {batch.procurement_date.strftime('%Y-%m-%d')})"
            
            # Create notifications for all users with permission
            notifications = Notification.create_notification(
                users=users,
                title=title,
                message=message,
                notification_type='update',
                entity_type='raw_material',
                entity_id=batch.id,
                entity_name=f"Raw Material Batch #{batch.batch_id} - {batch.raw_material.name}",
                created_by=updated_by
            )
            
            return notifications
            
        except Exception as e:
            # Log the error but don't break the main functionality
            print(f"Error creating raw material batch update notification: {e}")
            return []
    
    @staticmethod
    def notify_consumable_batch_created(batch, created_by=None):
        """Create notification for consumable batch creation"""
        try:
            # Get users who have permission to view consumables
            users = NotificationService.get_users_with_permission('consumable', 'view')
            
            # Also add the creator to the notification list for immediate feedback
            if created_by and created_by not in users:
                users.append(created_by)
            
            # Create descriptive title and message
            title = f"New Consumable Batch Created"
            message = f"Consumable Batch #{batch.batch_id} for {batch.consumable.name} has been created"
            
            if created_by:
                message += f" by {created_by.get_full_name() or created_by.username}"
            
            # Add batch details to message
            if hasattr(batch, 'batch_size_value') and hasattr(batch, 'batch_size_unit'):
                message += f" with quantity {batch.batch_size_value} {batch.batch_size_unit.name if hasattr(batch.batch_size_unit, 'name') else batch.batch_size_unit}"
            
            if hasattr(batch, 'procurement_date'):
                message += f" (Procured: {batch.procurement_date.strftime('%Y-%m-%d')})"
            
            # Create notifications for all users with permission
            notifications = Notification.create_notification(
                users=users,
                title=title,
                message=message,
                notification_type='create',
                entity_type='consumable',
                entity_id=batch.id,
                entity_name=f"Consumable Batch #{batch.batch_id} - {batch.consumable.name}",
                created_by=created_by
            )
            
            return notifications
            
        except Exception as e:
            # Log the error but don't break the main functionality
            print(f"Error creating consumable batch notification: {e}")
            return []
    
    @staticmethod
    def notify_consumable_batch_updated(batch, updated_by=None):
        """Create notification for consumable batch update"""
        try:
            # Get users who have permission to view consumables
            users = NotificationService.get_users_with_permission('consumable', 'view')
            
            # Also add the updater to the notification list for immediate feedback
            if updated_by and updated_by not in users:
                users.append(updated_by)
            
            # Create descriptive title and message
            title = f"Consumable Batch Updated"
            message = f"Consumable Batch #{batch.batch_id} for {batch.consumable.name} has been updated"
            
            if updated_by:
                message += f" by {updated_by.get_full_name() or updated_by.username}"
            
            # Add batch details to message
            if hasattr(batch, 'batch_size_value') and hasattr(batch, 'batch_size_unit'):
                message += f" with quantity {batch.batch_size_value} {batch.batch_size_unit.name if hasattr(batch.batch_size_unit, 'name') else batch.batch_size_unit}"
            
            if hasattr(batch, 'procurement_date'):
                message += f" (Procured: {batch.procurement_date.strftime('%Y-%m-%d')})"
            
            # Create notifications for all users with permission
            notifications = Notification.create_notification(
                users=users,
                title=title,
                message=message,
                notification_type='update',
                entity_type='consumable',
                entity_id=batch.id,
                entity_name=f"Consumable Batch #{batch.batch_id} - {batch.consumable.name}",
                created_by=updated_by
            )
            
            return notifications
            
        except Exception as e:
            # Log the error but don't break the main functionality
            print(f"Error creating consumable batch update notification: {e}")
            return []
    
    @staticmethod
    def notify_component_batch_created(batch, created_by=None):
        """Create notification for component batch creation"""
        try:
            # Get users who have permission to view components
            users = NotificationService.get_users_with_permission('component', 'view')
            
            # Also add the creator to the notification list for immediate feedback
            if created_by and created_by not in users:
                users.append(created_by)
            
            # Create descriptive title and message
            title = f"New Component Batch Created"
            message = f"Component Batch #{batch.batch_id} for {batch.component.name} has been created"
            
            if created_by:
                message += f" by {created_by.get_full_name() or created_by.username}"
            
            # Add batch details to message
            if hasattr(batch, 'batch_size_value') and hasattr(batch, 'batch_size_unit'):
                message += f" with quantity {batch.batch_size_value} {batch.batch_size_unit.name if hasattr(batch.batch_size_unit, 'name') else batch.batch_size_unit}"
            
            if hasattr(batch, 'procurement_date'):
                message += f" (Procured: {batch.procurement_date.strftime('%Y-%m-%d')})"
            
            # Create notifications for all users with permission
            notifications = Notification.create_notification(
                users=users,
                title=title,
                message=message,
                notification_type='create',
                entity_type='component',
                entity_id=batch.id,
                entity_name=f"Component Batch #{batch.batch_id} - {batch.component.name}",
                created_by=created_by
            )
            
            return notifications
            
        except Exception as e:
            # Log the error but don't break the main functionality
            print(f"Error creating component batch notification: {e}")
            return []
    
    @staticmethod
    def notify_component_batch_updated(batch, updated_by=None):
        """Create notification for component batch update"""
        try:
            # Get users who have permission to view components
            users = NotificationService.get_users_with_permission('component', 'view')
            
            # Also add the updater to the notification list for immediate feedback
            if updated_by and updated_by not in users:
                users.append(updated_by)
            
            # Create descriptive title and message
            title = f"Component Batch Updated"
            message = f"Component Batch #{batch.batch_id} for {batch.component.name} has been updated"
            
            if updated_by:
                message += f" by {updated_by.get_full_name() or updated_by.username}"
            
            # Add batch details to message
            if hasattr(batch, 'batch_size_value') and hasattr(batch, 'batch_size_unit'):
                message += f" with quantity {batch.batch_size_value} {batch.batch_size_unit.name if hasattr(batch.batch_size_unit, 'name') else batch.batch_size_unit}"
            
            if hasattr(batch, 'procurement_date'):
                message += f" (Procured: {batch.procurement_date.strftime('%Y-%m-%d')})"
            
            # Create notifications for all users with permission
            notifications = Notification.create_notification(
                users=users,
                title=title,
                message=message,
                notification_type='update',
                entity_type='component',
                entity_id=batch.id,
                entity_name=f"Component Batch #{batch.batch_id} - {batch.component.name}",
                created_by=updated_by
            )
            
            return notifications
            
        except Exception as e:
            # Log the error but don't break the main functionality
            print(f"Error creating component batch update notification: {e}")
            return []
    
    @staticmethod
    def get_user_notifications(user, limit=10, unread_only=False):
        """Get notifications for a specific user"""
        queryset = Notification.objects.filter(user=user)
        
        if unread_only:
            queryset = queryset.filter(is_read=False)
        
        return queryset.order_by('-created_at')[:limit]
    
    @staticmethod
    def mark_notifications_as_read(user, notification_ids=None):
        """Mark notifications as read for a user"""
        queryset = Notification.objects.filter(user=user, is_read=False)
        
        if notification_ids:
            queryset = queryset.filter(id__in=notification_ids)
        
        return queryset.update(is_read=True)
    
    @staticmethod
    def notify_raw_material_acceptance_test_created(test, created_by=None):
        """Create notification for raw material acceptance test creation"""
        try:
            # Get users who have permission to view acceptance tests
            users = NotificationService.get_users_with_permission('acceptance_test', 'view')
            
            # Also add the creator to the notification list for immediate feedback
            if created_by and created_by not in users:
                users.append(created_by)
            
            # Create descriptive title and message
            title = f"New Acceptance Test Created"
            message = f"Acceptance test for Raw Material Batch #{test.batch_id.batch_id if hasattr(test.batch_id, 'batch_id') else test.batch_id} has been created"
            
            if created_by:
                message += f" by {created_by.get_full_name() or created_by.username}"
            
            # Add test details to message
            if hasattr(test, 'test_value') and test.test_value:
                message += f" with test value: {test.test_value}"
            
            if hasattr(test, 'status') and test.status:
                message += f" (Status: {test.status})"
            
            # Create notifications for all users with permission
            notifications = Notification.create_notification(
                users=users,
                title=title,
                message=message,
                notification_type='create',
                entity_type='acceptance_test',
                entity_id=test.id,
                entity_name=f"Acceptance Test for Batch #{test.batch_id.batch_id if hasattr(test.batch_id, 'batch_id') else test.batch_id}",
                created_by=created_by
            )
            
            return notifications
            
        except Exception as e:
            # Log the error but don't break the main functionality
            print(f"Error creating acceptance test notification: {e}")
            return []
