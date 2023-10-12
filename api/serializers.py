# from django.contrib.auth.models import User
from rest_framework import serializers
from .models import CustomUser
from rest_framework.response import Response
import re
# from django.contrib.auth.models import User

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def authenticate_user(self, email, password):
        try:
            user = CustomUser.objects.get(email=email)
            if user.check_password(password):
                return user
            else:
                raise serializers.ValidationError('Incorrect password.')
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError('User with this email does not exist.')


    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = self.authenticate_user(email, password)

        if user:
            data['user'] = user
        else:
            raise serializers.ValidationError('Invalid email or password')

        return data



class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'password', 'password2']
        extra_kwargs = {
            'password' : {'write_only': True}
        }
        
    
    def validate_password(self, password):
        # Minimum length of 8 characters
        if len(password) < 8:
            raise serializers.ValidationError('Password must be at least 8 characters long.')
        
        # At least one alphabet
        if not re.search(r'[a-zA-Z]', password):
            raise serializers.ValidationError('Password must contain at least one alphabet.')
        
        # At least one digit
        if not re.search(r'\d', password):
            raise serializers.ValidationError('Password must contain at least one digit.')
        
        # At least one special character
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise serializers.ValidationError('Password must contain at least one special character.')
        
        return password
    
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        password2 = validated_data.pop('password2')

        if password != password2:
            raise serializers.ValidationError({'error': 'Passwords do not match.'})

        user = CustomUser.objects.create(
            email=validated_data['email'],
            username=validated_data['email'],  # Set the username to be the same as the email
            name=validated_data['name']
        )
        user.set_password(password)
        user.save()
        return user



    # def save(self):
    #     name = self.validated_data['name']
    #     email = self.validated_data['email']
    #     password = self.validated_data['password']
    #     password2 = self.validated_data['password2']

    #     if password != password2:
    #         raise serializers.ValidationError({'error': 'P1 and P2 should be same!'})

    #     if CustomUser.objects.filter(email=email).exists():
    #         raise serializers.ValidationError({'error': 'Email already exists!'})

    #     self.validated_data['username'] = email  # Set email as the username

    #     account = CustomUser(name=name, email=email)
    #     account.set_password(password)
    #     account.save()

    #     return account

    # def validate_email(self, value):
    #     try:
    #         user = CustomUser.objects.get(email=value)
    #     except CustomUser.DoesNotExist:
    #         raise serializers.ValidationError('User with this email does not exist.')
    #     return value
    
    
    # def validate_password(self, value):
    #     """
    #     Validate password against Django password validators and custom complexity requirements.
    #     """
    #     validate_password(value)  # Django's password validators

    #     # Custom complexity requirements
    #     if not re.search(r'[A-Za-z]', value):
    #         raise serializers.ValidationError("Password must contain at least one letter.")

    #     if not re.search(r'[0-9]', value):
    #         raise serializers.ValidationError("Password must contain at least one digit.")

    #     if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
    #         raise serializers.ValidationError("Password must contain at least one special character.")

    #     return value    