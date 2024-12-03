
from qdpc.core import constants
from rest_framework import status
from qdpc.services.login_service import LoginService
from authentication.serializers.forgot_username_serializer import ForgotUsernameSerializer
from qdpc.core.modelviewset import BaseModelViewSet
from django.shortcuts import render, redirect


class ForgotUsername(BaseModelViewSet):
    "API to get forgot username"

    def get(self,request):

        return render(request,'forgot_username_two.html')

    def post(self, request, format=None):
        serializer = ForgotUsernameSerializer(data=request.data)
        data = request.data
        success=False
        message = constants.RESET_EMAIL_FAILED
        status_code=status.HTTP_400_BAD_REQUEST 
        try:
            if serializer.is_valid():
                email = serializer.validated_data['email']
                message, success, status_code =  LoginService.forgot_username_request(email)     
            exception_message = None
        except Exception as ex:
            success = False
            message = constants.RESET_EMAIL_FAILED
            status_code = status.HTTP_400_BAD_REQUEST
            exception_message = str(ex)
        return self.render_response(data, success, message,
                                status_code)