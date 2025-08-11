from django.db import models

class DimensionalInspection(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    min_value = models.IntegerField(blank=True, null=True)  # Optional field
    max_value = models.IntegerField(blank=True, null=True) 
    unit = models.ForeignKey('Unit', on_delete=models.CASCADE,null=True,blank=True)