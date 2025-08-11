from django.db import models
from django.utils import timezone
from qdpc_core_models.models import Product, RawMaterial, Component, Consumable, Unit,AcceptanceTest,Process,Equipment
from qdpc_core_models.models.product import Drawing
from qdpc_core_models.models.raw_material_acceptence_test import RawMaterialAcceptanceTest


class ProductBatchs(models.Model):
    batch_id = models.CharField(max_length=100, blank=True,null=True)
    unit = models.CharField(max_length=100, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_batches_product')
    manufacturing_start = models.DateField()
    manufacturing_end = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.batch_id
    
class ProductBatchRawMaterial(models.Model):
    product_batch = models.ForeignKey(ProductBatchs, on_delete=models.CASCADE)
    raw_material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE)
    batch = models.ForeignKey('RawMaterialBatch', on_delete=models.CASCADE)  

    date_added = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.product_batch} - {self.raw_material}"


class ProductBatchComponent(models.Model):
    product_batch = models.ForeignKey(ProductBatchs, on_delete=models.CASCADE)
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    batch = models.CharField(max_length=100)
    date_added = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.product_batch} - {self.component}"


class ProductBatchConsumable(models.Model):
    product_batch = models.ForeignKey(ProductBatchs, on_delete=models.CASCADE)
    consumable = models.ForeignKey(Consumable, on_delete=models.CASCADE)
    batch = models.CharField(max_length=100)
    date_added = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.product_batch} - {self.consumable}"
class ProductBatchProcess(models.Model):
    product_batch = models.ForeignKey(ProductBatchs, on_delete=models.CASCADE)
    process = models.ForeignKey(Process, on_delete=models.CASCADE)
    date_added = models.DateField(default=timezone.now)


class ProductBatchDrawing(models.Model):
    product_batch = models.ForeignKey(ProductBatchs, on_delete=models.CASCADE)
    drawing = models.ForeignKey(Drawing, on_delete=models.CASCADE)
    date_added = models.DateField(default=timezone.now)

class ProductBatchEquipment(models.Model):
    product_batch = models.ForeignKey(ProductBatchs, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    date_added = models.DateField(default=timezone.now)


class ProductBatchAcceptanceTest(models.Model):
    product_batch = models.ForeignKey(ProductBatchs, on_delete=models.CASCADE)
    acceptance_test = models.ForeignKey(AcceptanceTest, on_delete=models.CASCADE)
    result = models.CharField(max_length=100, blank=True, null=True)
    date_of_test = models.DateField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    report = models.FileField(upload_to='acceptance_reports/', null=True, blank=True)


class RawmaterialAcceptenceTest(models.Model):
    product_batch = models.ForeignKey(ProductBatchs, on_delete=models.CASCADE)
    raw_material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE)
    acceptance_test = models.ForeignKey(RawMaterialAcceptanceTest, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.raw_material.name} - {self.acceptance_test.acceptance_test_name}'

