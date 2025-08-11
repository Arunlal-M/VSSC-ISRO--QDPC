from django.db import models
from qdpc_core_models.models.acceptance_test import AcceptanceTest
from qdpc_core_models.models.raw_material import RawMaterial
from qdpc_core_models.models.source import Sources
from qdpc_core_models.models.supplier import Suppliers
from qdpc_core_models.models.grade import Grade
from qdpc_core_models.models.user import User



class RawMaterialGradeAcceptanceTest(models.Model):
    raw_material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE, related_name='test_data')
    acceptance_test = models.ForeignKey(AcceptanceTest, on_delete=models.CASCADE)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    min_value = models.FloatField()
    max_value = models.FloatField()
    unit_name = models.CharField(max_length=20)
    reevaluation_frequency = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.raw_material.name}"
