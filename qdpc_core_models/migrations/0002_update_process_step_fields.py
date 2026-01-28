# Generated manually to fix field length issues

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qdpc_core_models', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='processstep',
            name='test_result',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='processstep',
            name='specification_result',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
