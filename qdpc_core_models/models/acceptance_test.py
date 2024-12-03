from django.db import models
from datetime import timedelta

class AcceptanceTest(models.Model):
    TIME_UNIT_CHOICES = [
        ('months', 'Months'),
        ('days', 'Days'),
    ]

    TEST_TYPE_CHOICES = [
        ('quantitative', 'Quantitative'),
        ('qualitative', 'Qualitative'),
    ]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    min_value = models.IntegerField(blank=True, null=True)  # Optional field
    max_value = models.IntegerField(blank=True, null=True) 
    unit = models.ForeignKey('Unit', on_delete=models.CASCADE)
    sampling_plan = models.FileField(
        upload_to='acceptance_test_results/',
        blank=True,
        null=True
    )
    reevaluation_frequency_value = models.PositiveIntegerField(default=12)
    reevaluation_frequency_unit = models.CharField(max_length=10, choices=TIME_UNIT_CHOICES, default='months')
    
    # New fields
    test_type = models.CharField(max_length=15, choices=TEST_TYPE_CHOICES, default='quantitative')
    test_result = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def reevaluation_frequency(self):
        if self.reevaluation_frequency_unit == 'days':
            return timedelta(days=self.reevaluation_frequency_value)
        elif self.reevaluation_frequency_unit == 'months':
            return timedelta(days=self.reevaluation_frequency_value * 30)  # Approximation for months
        return None

    @property
    def sampling_plan_filename(self):
        if self.sampling_plan:
            return self.sampling_plan.name.split('/')[-1]
        return 'No file'
