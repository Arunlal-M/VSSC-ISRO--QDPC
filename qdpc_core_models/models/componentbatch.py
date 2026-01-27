from django.db import models
from django.utils import timezone
from datetime import timedelta
from qdpc_core_models.models.component import Component
from qdpc_core_models.models.unit import Unit
from qdpc_core_models.models.user import User

class ComponentBatch(models.Model):
        
    STAT_CHOICES = [
        ('available', 'Available'),
        ('exhausted', 'Exhausted'),
    ]

    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    batch_id = models.CharField(max_length=100, unique=True)
    # component_unit = models.CharField(max_length=255)  # New field
    procurement_date = models.DateField()
    batch_size_value = models.FloatField()
    batch_size_unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='component_batch_sizes')
    packing_details = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)  # Automatically set to now when created
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # User who created the record
    status = models.CharField(max_length=100, default='available', choices=STAT_CHOICES)
    expiry_date = models.DateField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.expiry_date and self.component.shelf_life_value and self.component.shelf_life_unit:
            if self.component.shelf_life_unit == 'days':
                self.expiry_date = self.procurement_date + timedelta(days=self.component.shelf_life_value)
            elif self.component.shelf_life_unit == 'months':
                self.expiry_date = self.procurement_date + timedelta(days=self.component.shelf_life_value * 30)
            elif self.component.shelf_life_unit == 'years':
                self.expiry_date = self.procurement_date + timedelta(days=self.component.shelf_life_value * 365)
        super().save(*args, **kwargs)
        
    def __str__(self): 
        return f"{self.batch_id}"
        # return f"{self.batch_id} - {self.component_unit}"