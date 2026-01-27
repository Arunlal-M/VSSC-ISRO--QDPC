from django.db import models
from django.utils import timezone
from datetime import timedelta
from qdpc_core_models.models.raw_material import RawMaterial
from qdpc_core_models.models.unit import Unit
from qdpc_core_models.models.user import User

class RawMaterialBatch(models.Model):
    
    STAT_CHOICES = [
        ('available', 'Available'),
        ('exhausted', 'Exhausted'),
    ]

    raw_material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE)
    batch_id = models.CharField(max_length=100, unique=True)
    procurement_date = models.DateField()
    batch_size_value = models.FloatField()
    batch_size_unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='batch_sizes')
    packing_details = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)  # Automatically set to now when created
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # User who created the record
    status = models.CharField(max_length=100, default='available', choices=STAT_CHOICES)
    expiry_date = models.DateField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Only calculate expiry date if it's not already set AND the raw material has shelf life data
        if not self.expiry_date and self.raw_material.shelf_life_value and self.raw_material.shelf_life_unit:
            try:
                if self.raw_material.shelf_life_unit == 'days':
                    self.expiry_date = self.procurement_date + timedelta(days=self.raw_material.shelf_life_value)
                elif self.raw_material.shelf_life_unit == 'months':
                    self.expiry_date = self.procurement_date + timedelta(days=self.raw_material.shelf_life_value * 30)
                elif self.raw_material.shelf_life_unit == 'years':
                    self.expiry_date = self.procurement_date + timedelta(days=self.raw_material.shelf_life_value * 365)
            except Exception as e:
                # Don't fail the save operation, just log the error silently
                pass
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.batch_id