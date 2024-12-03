from threading import Thread
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.authtoken.models import Token



def send_forgot_username_email(email,username):

    print("sedning mail")
    subject = 'Password Reset Request'
    message = f'Hi ,Your username is :\n{username}'
    from_email = settings.EMAIL_HOST_USER  
    # Use the email address from the settings
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)


def token_creation(user_data):
    """
    :param user_data: database object of login-user.
    This function will get an existing token or create a new token for user login.
    """
    token, created = Token.objects.get_or_create(user=user_data)
    
    return token