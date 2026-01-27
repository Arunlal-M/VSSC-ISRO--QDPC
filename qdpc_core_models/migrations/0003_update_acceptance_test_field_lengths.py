# Generated manually to increase field lengths for acceptance test fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qdpc_core_models', '0002_update_process_step_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acceptancetest',
            name='test_result',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='acceptancetest',
            name='specification_result',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
