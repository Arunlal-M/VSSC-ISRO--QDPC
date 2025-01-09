from django.db import models
from django.utils import timezone
from datetime import timedelta
from qdpc_core_models.models.consumable import Consumable
from qdpc_core_models.models.unit import Unit
from qdpc_core_models.models.user import User

class ConsumableBatch(models.Model):
    consumable = models.ForeignKey(Consumable, on_delete=models.CASCADE)
    batch_id = models.CharField(max_length=100, unique=True)
    procurement_date = models.DateField()
    batch_size_value = models.FloatField()
    batch_size_unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='consumable_batch_sizes')
    packing_details = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)  # Automatically set to now when created
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # User who created the record


    def __str__(self):
        return self.batch_id