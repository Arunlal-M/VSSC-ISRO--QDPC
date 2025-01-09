from django.db import models
from .grade import Grade
# from qdpc_core_models.models.user import User
from .source import Sources
from .supplier import Suppliers
from .acceptance_test import AcceptanceTest
from datetime import timedelta

class Component(models.Model):
    name = models.CharField(max_length=255,unique=True)
    sources = models.ManyToManyField(Sources, related_name='components')
    is_active = models.BooleanField(default=True)  # Active Status
    suppliers = models.ManyToManyField(Suppliers, related_name='components')
    # grade = models.CharField(max_length=50)
    grade = models.ManyToManyField(Grade, related_name='components')
    shelf_life_value = models.FloatField()  # The numeric value for shelf life
    shelf_life_unit = models.CharField(max_length=10, choices=[('days', 'Days'), ('months', 'Months')])
    user_defined_date = models.DateField()
    acceptance_test = models.ManyToManyField(AcceptanceTest, related_name='components')

    @property
    def calculate_expiry_date(self):
        procurement_date = self.user_defined_date  # Use user_defined_date as the default procurement_date
        if self.shelf_life_unit == 'days':
            return procurement_date + timedelta(days=self.shelf_life_value)
        elif self.shelf_life_unit == 'months':
            return procurement_date + timedelta(days=self.shelf_life_value * 30)  # Approximation for months

    def __str__(self):
        return self.name
