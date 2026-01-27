from rest_framework import serializers
from qdpc_core_models.models.product import *


class DrawingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drawing
        fields = ['drawing_number', 'drawing_title', 'drawing_status', 'drawing_document']
        
        def get_drawing_document(self, obj):
            return obj.drawing_document.url if obj.drawing_document else None
        




class ProductSerializer(serializers.ModelSerializer):
    drawings = DrawingSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'category',
            'product_owner',
            'is_active',
            'end_uses',
            'specific_use',
            'shelf_life_type',
            'shelf_life_value',
            'shelf_life_unit',
            'processing_agencies',
            'testing_agencies',
            'components',
            'rawmaterial',
            'consumable',
            'process',
            # 'acceptancetest',
            'drawing_applicable',
            # 'identification_method',
            'batch_size',
            # 'prefix',
            # 'suffix',
            'drawings',
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
    
    def create(self, validated_data):
        drawings_data = validated_data.pop('drawings', [])
        product = Product.objects.create(**validated_data)
        for drawing_data in drawings_data:
            Drawing.objects.create(product=product, **drawing_data)
        return product

    def update(self, instance, validated_data):
        drawings_data = validated_data.pop('drawings')
        instance = super().update(instance, validated_data)
        instance.drawings.all().delete()
        for drawing_data in drawings_data:
            Drawing.objects.create(product=instance, **drawing_data)
        return instance
    
    