from rest_framework import serializers
from qdpc_core_models.models.product import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',                      # Include the ID field if needed
            'name',
            'category',
            'product_owner',
            'is_active',
            'end_uses',
            'specific_use',
            'shelf_life_value',
            'shelf_life_unit',
            'processing_agencies',
            'testing_agencies',
            'components',
            'rawmaterial',
            'consumable',
            'drawing_applicable',
            'drawing_number',
            'drawing_status',
            'drawing_document',
            'product_document',
            'drawing_title',
            'identification_method',
            'batch_size',
            'prefix',
            'suffix',
                         
        ]
