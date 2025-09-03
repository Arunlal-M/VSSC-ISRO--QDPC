
from django.db import models
from qdpc_core_models.models.acceptance_test import AcceptanceTest
from qdpc_core_models.models.product import Product
from qdpc_core_models.models.unit import Unit

class ProductAcceptanceTest(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    acceptance_test = models.ForeignKey(AcceptanceTest, on_delete=models.CASCADE)
    min_value = models.IntegerField(blank=True, null=True)  
    max_value = models.IntegerField(blank=True, null=True) 
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'acceptance_test') 
    def __str__(self):
        return f"{self.product.name} - {self.acceptance_test.name}"











