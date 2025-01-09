from django.db import models
from django.utils import timezone
from datetime import timedelta
from qdpc_core_models.models.raw_material import RawMaterial
from qdpc_core_models.models.unit import Unit
from qdpc_core_models.models.user import User

class RawMaterialBatch(models.Model):
    raw_material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE)
    batch_id = models.CharField(max_length=100, unique=True)
    procurement_date = models.DateField()
    batch_size_value = models.FloatField()
    batch_size_unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='batch_sizes')
    packing_details = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)  # Automatically set to now when created
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # User who created the record


    def _str_(self):
        return self.batch_id