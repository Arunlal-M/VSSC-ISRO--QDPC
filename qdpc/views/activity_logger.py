# utils/activity_logger.py
from django.contrib.contenttypes.models import ContentType
from  qdpc_core_models.models.activity import  Activity

from qdpc_core_models.models.division import Division

def log_activity(user, instance, action, details=None):
    Activity.objects.create(
        user=user,
        action=action,
        content_type=ContentType.objects.get_for_model(instance),
        object_id=instance.pk,
        details=details or '',
    )
