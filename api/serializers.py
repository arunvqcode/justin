from django.contrib.auth.models import User
from rest_framework import serializers
from .models import CustomUser
from rest_framework.response import Response




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
    
    def save(self):
        name = self.validated_data['name']
        email = self.validated_data['email']
        
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'error': 'P1 and P2 should be same!'})
        
        if CustomUser.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'error': 'Email already exists!'})
        
        account = CustomUser(name=name, email=email)
        account.set_password(password)
        account.save()

        return account
    


    # def validate_email(self, value):
    #     try:
    #         user = CustomUser.objects.get(email=value)
    #     except CustomUser.DoesNotExist:
    #         raise serializers.ValidationError('User with this email does not exist.')
    #     return value