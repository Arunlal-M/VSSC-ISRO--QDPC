from qdpc_core_models.models.notificaiton import Notification

# def notifications(request):
#     if request.user.is_authenticated:
#         notifications = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')[:5]
#         return {'notifications': notifications}
#     return {}



def notifications(request):
    if request.user.is_authenticated:
        # Fetch unread notifications for the current user
        unread_notifications = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')[:5]
        unread_count = unread_notifications.count()
        return {
            'notifications': unread_notifications,
            'unread_count': unread_count,  # Add unread count to the context
        }
    return {}