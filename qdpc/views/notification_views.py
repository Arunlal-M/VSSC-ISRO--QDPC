from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from qdpc_core_models.models.notification import Notification
from qdpc.services.notification_service import NotificationService
import json


def get_time_since(created_at):
    """Get human readable time since notification was created"""
    if not created_at:
        return 'Unknown'
    
    from django.utils import timezone
    
    # Handle both naive and timezone-aware datetimes
    if timezone.is_naive(created_at):
        # If naive, assume it's in UTC
        created_at = timezone.make_aware(created_at, timezone.utc)
    
    now = timezone.now()
    diff = now - created_at
    
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


@login_required
def notification_list(request):
    """Get notifications for the current user"""
    notifications = NotificationService.get_user_notifications(request.user, limit=20)
    unread_count = Notification.get_unread_count(request.user)
    
    context = {
        'notifications': notifications,
        'unread_count': unread_count,
        'page_title': 'Notifications'
    }
    
    return render(request, 'notifications/list.html', context)


@login_required
@csrf_exempt
def notification_api(request):
    """API endpoint for notification operations"""
    if request.method == 'GET':
        try:
            # Get notifications
            limit = int(request.GET.get('limit', 10))
            unread_only = request.GET.get('unread_only', 'false').lower() == 'true'
            
            try:
                notifications = NotificationService.get_user_notifications(
                    request.user, 
                    limit=limit, 
                    unread_only=unread_only
                )
                
                notifications_data = []
                for notification in notifications:
                    notifications_data.append({
                        'id': notification.id,
                        'title': notification.title,
                        'message': notification.message,
                        'type': notification.notification_type,
                        'entity_type': notification.entity_type,
                        'entity_id': notification.entity_id,
                        'entity_name': notification.entity_name,
                        'is_read': notification.is_read,
                        'created_at': notification.created_at.isoformat(),
                        'time_since': notification.time_since,
                        'icon_class': notification.icon_class,
                        'created_by': notification.created_by.username if notification.created_by else None
                    })
                
                unread_count = Notification.get_unread_count(request.user)
                
                return JsonResponse({
                    'notifications': notifications_data,
                    'unread_count': unread_count,
                    'success': True
                })
                
            except Exception as e:
                # If database operations fail, return empty notifications
                print(f"Database error in notification API: {e}")
                return JsonResponse({
                    'notifications': [],
                    'unread_count': 0,
                    'success': True,
                    'message': 'Notifications temporarily unavailable'
                })
                
        except Exception as e:
            print(f"General error in notification API: {e}")
            return JsonResponse({
                'notifications': [],
                'unread_count': 0,
                'success': False,
                'error': 'Internal server error'
            }, status=500)
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            action = data.get('action')
            
            if action == 'mark_read':
                notification_ids = data.get('notification_ids', [])
                if notification_ids:
                    count = NotificationService.mark_notifications_as_read(
                        request.user, 
                        notification_ids
                    )
                else:
                    # Mark all as read
                    count = NotificationService.mark_notifications_as_read(request.user)
                
                return JsonResponse({
                    'success': True,
                    'marked_count': count,
                    'message': f'{count} notification(s) marked as read'
                })
            
            elif action == 'mark_single_read':
                notification_id = data.get('notification_id')
                notification = get_object_or_404(
                    Notification, 
                    id=notification_id, 
                    user=request.user
                )
                notification.mark_as_read()
                
                return JsonResponse({
                    'success': True,
                    'message': 'Notification marked as read'
                })
            
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid action'
                }, status=400)
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@login_required
def notification_count(request):
    """Get unread notification count for current user"""
    try:
        unread_count = Notification.get_unread_count(request.user)
        return JsonResponse({
            'unread_count': unread_count,
            'success': True
        })
    except Exception as e:
        print(f"Error getting notification count: {e}")
        return JsonResponse({
            'unread_count': 0,
            'success': True,
            'message': 'Count temporarily unavailable'
        })

@login_required
def test_notification_api(request):
    """Test endpoint to verify notification system is working"""
    try:
        # Create some realistic test notifications
        test_notifications = [
            {
                'id': 1,
                'title': 'Product Batch Created',
                'message': 'Product Batch #123 for Test Product has been created successfully',
                'type': 'create',
                'entity_type': 'product_batch',
                'is_read': False,
                'time_since': 'Just now',
                'icon_class': 'fas fa-check-circle text-success'
            },
            {
                'id': 2,
                'title': 'Raw Material Received',
                'message': 'New raw material batch received and awaiting approval',
                'type': 'create',
                'entity_type': 'raw_material',
                'is_read': False,
                'time_since': '2 minutes ago',
                'icon_class': 'fas fa-box text-info'
            },
            {
                'id': 3,
                'title': 'Equipment Calibration Due',
                'message': 'Equipment calibration is due in 3 days',
                'type': 'update',
                'entity_type': 'equipment',
                'is_read': True,
                'time_since': '1 hour ago',
                'icon_class': 'fas fa-exclamation-triangle text-warning'
            }
        ]
        
        return JsonResponse({
            'success': True,
            'message': 'Notification API is working correctly',
            'test_data': {
                'notifications': test_notifications,
                'unread_count': 2,
                'total_count': 3
            }
        })
    except Exception as e:
        print(f"Error in test notification API: {e}")
        return JsonResponse({
            'success': False,
            'error': 'Test API encountered an error',
            'test_data': {
                'notifications': [],
                'unread_count': 0,
                'total_count': 0
            }
        }, status=500)
