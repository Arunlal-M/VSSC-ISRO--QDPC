from django.conf import settings
from django.contrib.auth import get_user_model
from qdpc_core_models.models.notificaiton import Notification
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

def create_notification(message, user=None):
    User = get_user_model()  # Get the actual user model class
    if user:
        Notification.objects.create(user=user, message=message)
    else:
        users = User.objects.all()
        for user in users:
            Notification.objects.create(user=user, message=message)

