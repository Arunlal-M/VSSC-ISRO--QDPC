
from qdpc_core_models.models.user import User
from authentication.serializers.login_serializer import LogininfoSerializer
from rest_framework import status
from qdpc.core import constants
from authentication.serializers.signup_serializer import UserSignupSerializer
from django.contrib.auth.models import  Group
from qdpc_core_models.models.role import Role
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.contrib.auth import login, authenticate
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
    def user_login(self, username, password,request):
        print("enterd userlogin")
        """
        This function will process login function and
        return login status_code, message and is_success
        """
        response_data = {}
        user_data = User.objects.filter(username__iexact=username).first()
        user_exist, user_status = self.check_user_exist(user_data, password)
        usertest = authenticate(request, username=username, password=password)
        print(usertest)
        if user_exist and user_status:
            login(request, usertest)
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
        # from app.models import Role  # adjust import
        print("Entered signup")
        response_data = {}
        success = False
        status_code = status.HTTP_400_BAD_REQUEST
        message = constants.SIGNUP_FAILED

        try:
            print(data)
            user_serializer = UserSignupSerializer(data=data)
            if user_serializer.is_valid():
                validated_data = user_serializer.validated_data

                # Get default GUEST role
                guest_role = Role.objects.get(pk=1)

                # Manually create user
                # from app.models import User  # replace with actual model path
                user = User.objects.create_user(
                    username=validated_data['username'],
                    password=validated_data['password'],
                    email=validated_data.get('email'),
                    first_name=validated_data.get('first_name', ''),
                    last_name=validated_data.get('last_name', ''),
                    phone_number=validated_data.get('phone_number', ''),
                    usertype=validated_data.get('usertype'),
                    desired_salutation=validated_data.get('desired_salutation'),
                    user_id=validated_data.get('user_id'),
                    role=guest_role,
                    is_active=True
                )

                # Many-to-many fields (center, divisions)
                if 'centre' in data:
                    user.centre.set(data.getlist('centre'))
                if 'divisions' in data:
                    user.divisions.set(data.getlist('divisions'))

                # Assign to GUEST group
                group, _ = Group.objects.get_or_create(name='GUEST')
                user.groups.add(group)

                # Send mail
                send_mail = signup_email(user.email, user.username)

                response_data = UserSignupSerializer(user).data
                success = True
                status_code = status.HTTP_201_CREATED
                message = constants.SIGNUP_SUCCESS
            else:
                response_data = user_serializer.errors

        except Exception as e:
            print("Exception:", e)
            response_data = {"error": str(e)}

        return success, status_code, response_data, message

