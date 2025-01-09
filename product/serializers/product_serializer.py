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
            'shelf_life_type',  # New field for the shelf life type
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
    def validate_shelf_life_value(self, value):
        """Ensure shelf_life_value is numeric (float or integer)."""
        if value is not None and not isinstance(value, (float, int)):
            raise serializers.ValidationError("Shelf life value must be a numeric type.")
        return value
    def validate(self, data):
        # Ensure shelf_life_value and shelf_life_unit are None when shelf_life_type is 'not_applicable' or 'tbd'
        shelf_life_type = data.get('shelf_life_type')
        if shelf_life_type in ['not_applicable', 'tbd']:
            data['shelf_life_value'] = None
            data['shelf_life_unit'] = None
        return data