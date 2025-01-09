
from qdpc.core.helpers import UserAuthenticator
from qdpc.core import constants
from django.conf import settings
from django.core.mail import send_mail
from rest_framework import status
from qdpc_core_models.models.user import User
from qdpc.core.utils import send_forgot_username_email
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from qdpc_core_models.models.reset_password import ResetPassword
import random
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password

import string

def send_forgot_username_email(email,username):

    subject = 'Password Reset Request'
    html_message = render_to_string('forgot_username_email.html', {'username': username})
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER  
    recipient_list = [email]

    send_mail(subject, plain_message, from_email,recipient_list, html_message=html_message)





def send_reset_password_email(email, reset_url,username):
    subject = 'Password Reset Request'
    message = f'Hi {username},\nYour reset password link is:\n{reset_url}'
   

    from_email = settings.EMAIL_HOST_USER  # Use the email address from the settings
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)





class LoginService:
    @classmethod
    def login_username(cls,username, password):
        if username and password:
            user_authenticator = UserAuthenticator()
            success, status_code, data, message = user_authenticator.user_login(username, password)
        else:
            print("enered else")
            message = constants.USERNAME_PASSWORD_REQUIRED
            success = False
            status_code = status.HTTP_400_BAD_REQUEST
  

        return success, status_code, data, message
    

    @classmethod
    def forgot_username_request(cls, email):

        user = User.objects.filter(email__iexact=email).first()    
        username = user.username if user else None
      
        if user :
            send_forgot_username_email(email, username)
              # Assuming this function is defined elsewhere
            message = constants.USERNAME_SENT_SUCCESS
            success = True
            status_code = status.HTTP_201_CREATED
        else:
            message = constants.RESET_EMAIL_FAILED
            success = False
            status_code = status.HTTP_400_BAD_REQUEST
        return message, success, status_code


    @classmethod
    def signup_user(cls, data, *args, **kwargs):

            # Assuming data is already validated at this point
        if data:
            user_authenticator = UserAuthenticator()
            success, status_code, data, message = user_authenticator.user_signup(data=data, *args, **kwargs)
        else:
            message = constants.SIGNUP_FAILED
            success = False
            status_code = status.HTTP_400_BAD_REQUEST
            data = {"error": "Invalid data"}

        return success, status_code, data, message
    
    @classmethod
    def reset_password_request(cls, email):
        print("entred reset")
        user = User.objects.filter(email__iexact=email).first()
     
        if user :
            print("user exists")
            username = user.username
            reset_key = cls.generate_reset_key() 
            print(reset_key,"rest key")
            reset_pass = ResetPassword.objects.create(user=user, reset_key=reset_key)
            print(reset_pass)
            reset_url = f"http://127.0.0.1:8000/reset-password/?reset_key={reset_key}"
            send_reset_password_email(email, reset_url, username)
            message = constants.RESET_KEY_GENERATED_SUCCESS
            success = True
            status_code = status.HTTP_201_CREATED
        return message, success, status_code
    
    @classmethod
    def update_password_request(cls, reset_key, password):
        print("entred reset")
        print(reset_key,"rest key")
        reset_password_obj = ResetPassword.objects.get(reset_key=reset_key)
        print(reset_password_obj,"Testing")
        user_obj = User.objects.filter(id=reset_password_obj.user.id).first()
        print(user_obj,"chekcing one")

        if user_obj and reset_password_obj:
            print("checked all")
            if check_password(password, user_obj.password):
                message = constants.CURRENT_PASSWORD
            else:
                print("entred else")
                user_obj.password = make_password(password)
                user_obj.save()
                reset_password_obj.delete()
                message = constants.PASSWORD_RESET_SUCCESS
                success = True
                status_code = status.HTTP_200_OK
        return message, success, status_code

    
    @staticmethod
    def generate_reset_key():
        # Generate a random reset key
        return ''.join(random.choices(string.ascii_letters + string.digits, k=20))