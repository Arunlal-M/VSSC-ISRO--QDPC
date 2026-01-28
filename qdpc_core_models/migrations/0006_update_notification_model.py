# Generated migration for notification model updates

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('qdpc_core_models', '0005_productbatchs_submitted_by_role_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='title',
            field=models.CharField(default='Notification', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('create', 'Created'), ('update', 'Updated'), ('delete', 'Deleted'), ('approve', 'Approved'), ('reject', 'Rejected')], default='create', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notification',
            name='entity_type',
            field=models.CharField(choices=[('product_batch', 'Product Batch'), ('raw_material', 'Raw Material'), ('component', 'Component'), ('consumable', 'Consumable'), ('equipment', 'Equipment'), ('acceptance_test', 'Acceptance Test'), ('process', 'Process'), ('user', 'User')], default='product_batch', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notification',
            name='entity_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='entity_name',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='notification',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_notifications', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='notification',
            name='message',
            field=models.TextField(),
        ),
    ]
