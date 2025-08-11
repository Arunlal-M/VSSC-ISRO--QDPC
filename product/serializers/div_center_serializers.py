from rest_framework import serializers
from  qdpc_core_models.models.center import Center
from  qdpc_core_models.models.division import  Division

class CenterSerializer(serializers.ModelSerializer):
    usertype_name=serializers.SerializerMethodField()
    
    class Meta:
        model = Center
        fields = ['id','name','user_type','usertype_name']
    
    def get_usertype_name(self,obj):
        
        return obj.user_type.name
        
        
        
        
        
        

class DivisionSerializer(serializers.ModelSerializer):
    center_name=serializers.SerializerMethodField()
    
    class Meta:
        model = Division
        fields = ['id','name','center_id' ]
        
    def get_center_name(self,obj):
        
        return obj.center.name
