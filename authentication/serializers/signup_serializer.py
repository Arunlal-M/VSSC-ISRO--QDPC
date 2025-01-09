from rest_framework import serializers
from qdpc_core_models.models.user import User,Center,Division,Role
from django.core.exceptions import ValidationError
import re

def validate_password(value):
    # Minimum 8 characters
    if len(value) < 8:
        raise ValidationError("Password must be at least 8 characters long.")

    # At least 1 digit
    if not any(char.isdigit() for char in value):
        raise ValidationError("Password must contain at least 1 digit.")

    # At least 1 alphabet
    if not any(char.isalpha() for char in value):
        raise ValidationError("Password must contain at least 1 alphabet.")

    # At least 1 special character
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
        raise ValidationError("Password must contain at least 1 special character.")


def validate_phone_number(value):
    """
    Validate phone numbers to follow a specific format.
    For example: it should be 10 digits and can start with country code.
    """
    if not re.match(r'^\+?\d{10,15}$', value):
        raise ValidationError("Enter a valid phone number.")



def validate_username(value):
    #have check wether the user is alrady eixt 
    pass

def validate_email(value):
    #mail validate logic
    pass

class UserSignupSerializer(serializers.ModelSerializer):
    centre = serializers.ListField(child=serializers.IntegerField(), write_only=True)
    divisions = serializers.ListField(child=serializers.IntegerField(), write_only=True)
    password = serializers.CharField(write_only=True, validators=[validate_password])
    phone_number = serializers.CharField(validators=[validate_phone_number])
    # username=
 

    class Meta:
        model = User
        fields = [
            'username', 'desired_salutation', 'user_id', 'first_name', 
            'last_name', 'email', 'centre', 'divisions', 'phone_number', 
            'usertype', 'password'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        centres = validated_data.pop('centre')
        divisions = validated_data.pop('divisions')

        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password:
            instance.set_password(password)
       
        instance.is_staff = False
        instance.is_approved = False 
        instance.is_active=False
        instance.save()

        instance.centre.set(Center.objects.filter(id__in=centres))
        instance.divisions.set(Division.objects.filter(id__in=divisions))
      

        return instance
    





