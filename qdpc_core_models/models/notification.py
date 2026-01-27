from django.db import models
from django.conf import settings
from django.utils import timezone


class Notification(models.Model):
    """Model to store system notifications for users"""
    
    NOTIFICATION_TYPES = [
        ('create', 'Created'),
        ('update', 'Updated'),
        ('delete', 'Deleted'),
        ('approve', 'Approved'),
        ('reject', 'Rejected'),
    ]
    
    ENTITY_TYPES = [
        ('product_batch', 'Product Batch'),
        ('raw_material', 'Raw Material'),
        ('component', 'Component'),
        ('consumable', 'Consumable'),
        ('equipment', 'Equipment'),
        ('acceptance_test', 'Acceptance Test'),
        ('process', 'Process'),
        ('user', 'User'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    entity_type = models.CharField(max_length=50, choices=ENTITY_TYPES)
    entity_id = models.IntegerField(null=True, blank=True)
    entity_name = models.CharField(max_length=200, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='created_notifications'
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"
    
    @property
    def time_since(self):
        """Get human readable time since notification was created"""
        now = timezone.now()
        diff = now - self.created_at
        
        if diff.days > 0:
            return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        else:
            return "Just now"
    
    @property
    def icon_class(self):
        """Get CSS icon class based on notification type"""
        icons = {
            'create': 'fas fa-plus-circle text-success',
            'update': 'fas fa-edit text-warning',
            'delete': 'fas fa-trash text-danger',
            'approve': 'fas fa-check-circle text-success',
            'reject': 'fas fa-times-circle text-danger',
        }
        return icons.get(self.notification_type, 'fas fa-bell text-info')
    
    def mark_as_read(self):
        """Mark notification as read"""
        self.is_read = True
        self.save()
    
    @classmethod
    def create_notification(cls, users, title, message, notification_type, entity_type, 
                          entity_id=None, entity_name='', created_by=None):
        """Create notifications for multiple users"""
        notifications = []
        for user in users:
            notification = cls.objects.create(
                user=user,
                title=title,
                message=message,
                notification_type=notification_type,
                entity_type=entity_type,
                entity_id=entity_id,
                entity_name=entity_name,
                created_by=created_by
            )
            notifications.append(notification)
        return notifications
    
    @classmethod
    def get_unread_count(cls, user):
        """Get count of unread notifications for a user"""
        return cls.objects.filter(user=user, is_read=False).count()
    
    @classmethod
    def get_recent_notifications(cls, user, limit=10):
        """Get recent notifications for a user"""
        return cls.objects.filter(user=user).order_by('-created_at')[:limit]
