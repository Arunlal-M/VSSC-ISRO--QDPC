from rest_framework import serializers


class ForgotUsernameSerializer(serializers.Serializer):
    email = serializers.CharField()
  