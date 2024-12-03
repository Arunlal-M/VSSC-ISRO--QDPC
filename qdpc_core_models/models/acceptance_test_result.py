from django.db import models
from qdpc_core_models.models.acceptance_test import AcceptanceTest
from qdpc_core_models.models.raw_materialbach import RawMaterialBatch
from django.utils import timezone
from qdpc_core_models.models.unit import Unit




class AcceptanceTestResult(models.Model):
    raw_material_batch = models.ForeignKey(RawMaterialBatch, on_delete=models.CASCADE, related_name='test_results')
    acceptance_test = models.ForeignKey(AcceptanceTest, on_delete=models.CASCADE)
    test_value = models.FloatField()
    unit=models.ForeignKey(Unit,on_delete=models.CASCADE)  # To store PDF or image files
    test_date = models.DateField(default=timezone.now)
    validity_date = models.DateField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    label = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.validity_date:
            self.validity_date = self.test_date + self.acceptance_test.reevaluation_frequency
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.raw_material_batch} - {self.acceptance_test.name} Test"