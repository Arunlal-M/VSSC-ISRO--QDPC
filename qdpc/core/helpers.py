
from qdpc_core_models.models.user import User
from authentication.serializers.login_serializer import LogininfoSerializer
from rest_framework import status
from qdpc.core import constants
from authentication.serializers.signup_serializer import UserSignupSerializer
from django.contrib.auth.models import  Group
from qdpc_core_models.models.role import Role
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string


def signup_email(email,username):

    subject = 'Signup Request'
    html_message = render_to_string('signup_mail.html', {'username': username})
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER  
    recipient_list = [email]

    send_mail(subject, plain_message, from_email,recipient_list, html_message=html_message)
    

class ResponseInfo(object):
    def __init__(self, **args):
        self.response = {
            "message": args.get('message', ""),
            "status": args.get('status', ""),
            "isSuccess": args.get('success', ""),
        }

class UserAuthenticator:
    """ Login for user"""
    def user_login(self, username, password):
        print("enterd userlogin")
        """
        This function will process login function and
        return login status_code, message and is_success
        """
        response_data = {}
        user_data = User.objects.filter(username__iexact=username).first()
        user_exist, user_status = self.check_user_exist(user_data, password)

        if user_exist and user_status:
            response_data =  LogininfoSerializer(user_data).data
            print(response_data,"response data")
            success = True
            message = constants.LOGIN_SUCCESS
            status_code = 200
        elif user_exist and not user_status:
            status_code = 403
            success = False
            message = constants.LOGIN_NOT_APPROVED_OR_INACTIVE
        else:
            status_code = 403
            success = False
            message = constants.LOGIN_FAILED

        return success, status_code, response_data, message

    @staticmethod
    def check_user_exist(user_data, password):
        """
        params: user_data - database object of login-user, password - password of user login.
        This function will return a tuple:
        - boolean indicating if the user exists and the password is correct,
        - boolean indicating if the user is active and approved.
        """
        if user_data and user_data.check_password(password):
            is_user_exist = True
            is_user_status_valid = user_data.is_active and user_data.is_approved
        else:
            is_user_exist = False
            is_user_status_valid = False

        return is_user_exist, is_user_status_valid


    @classmethod
    def user_signup(cls, data, *args, **kwargs):
        """ Handles user signup process """
        print("Ented singn up")
        response_data = {}
        success = False
        status_code = status.HTTP_400_BAD_REQUEST
        message = constants.SIGNUP_FAILED
          
        try:
            # Assuming SignupSerializer is the serializer for user data
            print(data)
            user_serializer = UserSignupSerializer(data=data)
            if user_serializer.is_valid():
                print("it is valid data")
                user = user_serializer.save()

                if user:
                    print("enterd if user")
                    group_name = 'GUEST'  # Replace with your actual group name
                    group, created = Group.objects.get_or_create(name=group_name)
                    role, created = Role.objects.get_or_create(name=group_name)
                
                    user.groups.add(group)
                    user.role.add(role)
                    username = user.username
                    email=user.email
                    send_mail=signup_email(email,username)
                    print("enterd if user tw")
                    # Serialize user data for response
                    response_data = UserSignupSerializer(user).data
                    print(response_data,"testSS")
                    success = True
                    status_code = status.HTTP_201_CREATED
                    message = constants.SIGNUP_SUCCESS
                else:
                    print("Serilzer not valid")
                    response_data = {"error": "User creation failed"}
                    message = constants.SIGNUP_FAILED
            else:
                print("Serilazer not vlaid")
               
                response_data = user_serializer.errors
                message = constants.SIGNUP_FAILED
                status_code = status.HTTP_400_BAD_REQUEST
        
        except Exception as e:
            response_data = {"error": str(e)}
            message = constants.SIGNUP_FAILED
            status_code = status.HTTP_400_BAD_REQUEST

        return success, status_code, response_data, message