from rest_framework import serializers
from qdpc_core_models.models.role_page_access import RolePageAccess, RolePermission


class RolePermissionSerializer(serializers.ModelSerializer):
    """Serializer for RolePermission model"""
    
    permission_type_display = serializers.CharField(source='get_permission_type_display', read_only=True)
    
    class Meta:
        model = RolePermission
        fields = [
            'id', 'page_code', 'permission_type', 'permission_type_display',
            'is_granted', 'created_at'
        ]


class RolePageAccessSerializer(serializers.ModelSerializer):
    """Serializer for RolePageAccess model"""
    
    permissions = RolePermissionSerializer(many=True, read_only=True)
    allowed_pages_display = serializers.ListField(source='get_allowed_pages_display', read_only=True)
    pages_count = serializers.IntegerField(source='get_pages_count', read_only=True)
    role_name_display = serializers.CharField(source='get_role_name_display', read_only=True)
    
    class Meta:
        model = RolePageAccess
        fields = [
            'id', 'role_name', 'role_name_display', 'allowed_pages', 
            'allowed_pages_display', 'description', 'is_active', 
            'created_at', 'updated_at', 'permissions', 'pages_count'
        ]


class RolePageAccessCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating RolePageAccess"""
    
    class Meta:
        model = RolePageAccess
        fields = ['role_name', 'allowed_pages', 'description', 'is_active']


class RolePageAccessUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating RolePageAccess"""
    
    class Meta:
        model = RolePageAccess
        fields = ['allowed_pages', 'description', 'is_active']


class BulkPermissionUpdateSerializer(serializers.Serializer):
    """Serializer for bulk updating permissions"""
    
    role_id = serializers.IntegerField()
    page_code = serializers.CharField()
    permissions = serializers.DictField(
        child=serializers.BooleanField(),
        help_text="Dictionary of permission types and their granted status"
    )


class RoleCloneSerializer(serializers.Serializer):
    """Serializer for cloning a role"""
    
    source_role_id = serializers.IntegerField()
    new_role_name = serializers.CharField(max_length=100)
    description = serializers.CharField(required=False, allow_blank=True)


class PageAccessSummarySerializer(serializers.Serializer):
    """Serializer for page access summary"""
    
    page_code = serializers.CharField()
    page_name = serializers.CharField()
    roles_with_access = serializers.ListField(child=serializers.CharField())
    total_roles = serializers.IntegerField()
