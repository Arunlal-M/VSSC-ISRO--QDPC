from rest_framework import serializers
from qdpc_core_models.models.user import User
from qdpc.core.utils import token_creation


class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password =serializers.CharField()
    class Meta:
        model = User



class LogininfoSerializer(serializers.Serializer):
    username=serializers.CharField()
    token = serializers.SerializerMethodField()

    @staticmethod
    def get_token(user_data):
        """
        params: user_data - database object of login-user.
        This function return new token for user.
        """
        token = token_creation(user_data)
        return token.key

    class Meta:
        model = User

        fields = ('id', 'first_name', 'last_name','token')
