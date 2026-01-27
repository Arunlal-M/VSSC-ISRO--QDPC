
from qdpc_core_models.models.user import User
from authentication.serializers.login_serializer import LogininfoSerializer
from rest_framework import status
from qdpc.core import constants
from authentication.serializers.signup_serializer import UserSignupSerializer
from django.contrib.auth.models import Group
from qdpc_core_models.models.role import Role
from qdpc_core_models.models.rolemeta import RoleMeta
from django.db import IntegrityError
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.contrib.auth import login, authenticate
from django.conf import settings
from django.template.loader import render_to_string
import traceback


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

            # Ensure proper role assignment and permissions
            try:
                # Check if user is superuser or admin
                if user_data.is_superuser or user_data.is_staff:
                    # Assign SUPER ADMIN role with full permissions
                    admin_role_name = 'SUPER ADMIN'
                    role_group, _ = Group.objects.get_or_create(name=admin_role_name)
                    role_proxy, _ = Role.objects.get_or_create(name=admin_role_name)
                    
                    # Ensure user has the admin role
                    if not getattr(user_data, 'role', None) or user_data.role.name != admin_role_name:
                        user_data.role = role_proxy
                        user_data.save(update_fields=['role'])
                    
                    # Ensure Django permissions via group membership
                    if not user_data.groups.filter(id=role_group.id).exists():
                        user_data.groups.add(role_group)
                    
                    # Admin users get ALL permissions
                    codes = ['ALL']
                    
                else:
                    # Regular user role assignment
                    if hasattr(user_data, 'role') and user_data.role:
                        # User already has a role, use that
                        role_group = Group.objects.filter(name=user_data.role.name).first()
                        if role_group:
                            if not user_data.groups.filter(id=role_group.id).exists():
                                user_data.groups.add(role_group)
                    else:
                        # Assign default role for regular users
                        default_role_name = 'Division Head SDA'
                        role_group, _ = Group.objects.get_or_create(name=default_role_name)
                        
                        # Check if Role object already exists, if not create it
                        try:
                            role_proxy = Role.objects.get(name=default_role_name)
                        except Role.DoesNotExist:
                            # Only create Role if Group exists and Role doesn't
                            role_proxy = Role.objects.create(name=default_role_name)
                        
                        user_data.role = role_proxy
                        user_data.save(update_fields=['role'])
                        
                        if not user_data.groups.filter(id=role_group.id).exists():
                            user_data.groups.add(role_group)
                    
                    # Get page codes from role
                    try:
                        meta = RoleMeta.objects.filter(group=role_group).first()
                        if meta and meta.page_codes:
                            if meta.page_codes == 'ALL':
                                codes = ['ALL']
                            else:
                                codes = [c.strip() for c in str(meta.page_codes).split(',') if c.strip()]
                        else:
                            # Fallback to required codes for Division Head SDA
                            codes = ['1','5','7','9','12','22']
                    except Exception:
                        codes = ['1','5','7','9','12','22']
                    
                    # Special handling for Division Head SDA - only show products
                    if user_data.role and user_data.role.name == 'Division Head SDA':
                        codes = ['1', '23']  # Only Dashboard and Products

                # Store page codes in session for UI use
                request.session['page_codes'] = codes
                request.session.modified = True
                
            except Exception as _e:
                # Non-fatal: continue login without defaulting role
                print(f"Role assignment error: {_e}")
                pass
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
            print(f"DEBUG: Signup data received: {data}")
            user_serializer = UserSignupSerializer(data=data)
            if user_serializer.is_valid():
                validated_data = user_serializer.validated_data

                # Resolve default Guest group from auth_group (case-insensitive)
                guest_group = Group.objects.filter(name__iexact='Guest').first()
                if not guest_group:
                    return False, status.HTTP_400_BAD_REQUEST, {"error": "Default 'Guest' group is missing. Please seed groups."}, "System configuration error. Please contact administrator."

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
                    role=None,  # role optional; use auth_group membership for permissions
                    is_active=True
                )

                # Many-to-many fields (center, divisions)
                if 'centre' in data:
                    user.centre.set(data.getlist('centre'))
                if 'divisions' in data:
                    user.divisions.set(data.getlist('divisions'))

                # Add to Guest group
                user.groups.add(guest_group)

                # Send mail
                send_mail = signup_email(user.email, user.username)

                response_data = UserSignupSerializer(user).data
                success = True
                status_code = status.HTTP_201_CREATED
                message = constants.SIGNUP_SUCCESS
            else:
                # Handle validation errors with specific messages
                print(f"DEBUG: Validation errors: {user_serializer.errors}")
                response_data = user_serializer.errors
                
                # Create a more user-friendly error message
                error_messages = []
                for field, errors in user_serializer.errors.items():
                    field_name = field.replace('_', ' ').title()
                    if isinstance(errors, list):
                        error_messages.append(f"{field_name}: {', '.join(errors)}")
                    else:
                        error_messages.append(f"{field_name}: {errors}")
                
                if error_messages:
                    message = "Please correct the following errors: " + "; ".join(error_messages[:3])  # Limit to first 3 errors
                else:
                    message = "Please check your input and try again."

        except IntegrityError as ie:
            print(f"DEBUG: Integrity error during signup: {ie}")
            if "username" in str(ie).lower():
                message = "Username already exists. Please choose a different username."
            elif "email" in str(ie).lower():
                message = "Email already exists. Please use a different email address."
            elif "user_id" in str(ie).lower():
                message = "Employee ID already exists. Please use a different ID."
            else:
                message = "A user with this information already exists."
            response_data = {"error": str(ie)}
            
        except Exception as e:
            print(f"DEBUG: Exception during signup: {e}")
            print(f"DEBUG: Traceback: {traceback.format_exc()}")
            message = f"An error occurred: {str(e)}"
            response_data = {"error": str(e)}

        print(f"DEBUG: Final signup response - success={success}, message={message}, status_code={status_code}")
        return success, status_code, response_data, message

