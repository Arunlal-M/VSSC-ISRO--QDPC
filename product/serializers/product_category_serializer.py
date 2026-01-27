from rest_framework import serializers
from qdpc_core_models.models.product_category import ProductCategory

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'
