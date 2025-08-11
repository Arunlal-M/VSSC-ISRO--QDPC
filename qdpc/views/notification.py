from django.shortcuts import render
from qdpc_core_models.models.notificaiton import Notification
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def view_all_notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'notifications': notifications,
    }
    return render(request, 'index.html', context)


@csrf_exempt
def mark_notification_as_read(request, notification_id):
    print("Enterd mark_notification_as_read")
    if request.method == 'POST':
        notification = Notification.objects.get(id=notification_id, user=request.user)
        notification.is_read = True
        notification.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)
