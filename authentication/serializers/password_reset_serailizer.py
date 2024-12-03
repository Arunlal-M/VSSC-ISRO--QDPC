from rest_framework import serializers



class UpdatePasswordSerializer(serializers.Serializer):
    reset_key = serializers.CharField()
    password = serializers.CharField()


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
